import os
import shutil
import traceback

from django.conf import settings
from django.template import loader
from django_nose.runner import NoseTestSuiteRunner
from typing import List, Dict

from drftest.base_view_test import BaseViewTest


def categorize_store(store: List) -> Dict:
    categorized = {}
    for test_result in store:
        app_name = test_result['meta']['app_name']
        class_name = test_result['meta']['class_name']
        if app_name not in categorized:
            categorized[app_name] = {}
        if class_name not in categorized[app_name]:
            categorized[app_name][class_name] = [test_result]
        else:
            categorized[app_name][class_name].append(test_result)
    return categorized


def clear_docs_path(docs_path: str):
    if os.path.exists(docs_path):
        if os.path.isdir(docs_path):
            shutil.rmtree(docs_path)
        else:
            os.remove(docs_path)
    os.mkdir(docs_path)


def rewrite_yml(root_dir: str):
    yml_path = os.path.join(root_dir, 'mkdocs.yml')
    with open(yml_path, 'w+') as yml_file:
        yml_file.write('site_name: DRF Tests')


def write_docs(store: List):
    if not hasattr(settings, 'DRF_TEST_DOCS_DIR') or not settings.DRF_TEST_DOCS_DIR:
        return
    root = os.path.expanduser(settings.DRF_TEST_DOCS_DIR)
    if not os.path.exists(root):
        os.mkdir(root)
    docs_path = os.path.join(root, 'docs')
    clear_docs_path(docs_path)
    rewrite_yml(root)
    categorized_store = categorize_store(store)
    is_first = True
    for app_name, app_docs in categorized_store.items():
        file_name = '{}.md'.format(app_name)
        if is_first:
            file_name = 'index.md'
            is_first = False
        md_path = os.path.join(docs_path, file_name)
        t = loader.get_template('doc_of_app.md')
        rendered = t.render({
            'app_name': app_name,
            'app_docs': app_docs,
        })
        with open(md_path, 'w+') as md_file:
            md_file.write(rendered)


class TestRunner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        result = None
        try:
            result = super().run_tests(test_labels, extra_tests)
            write_docs(BaseViewTest.docs_store)
        except Exception:
            traceback.print_exc()
        finally:
            return result
