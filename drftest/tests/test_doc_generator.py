import os
import shutil

from django.test import override_settings, TestCase

from drftest import doc_generator


@override_settings(DRF_TEST_DOCS_DIR='drftest/tests/test_docs')
class DocGeneratorTest(TestCase):
    def setUp(self):
        super().setUp()
        doc_generator.store = [{
            'method': 'post',
            'data': {'foo': 'bar'},
            'url': '/api',
            'url_kwargs': {'pk': 2},
            'format': 'json',
            'headers': {'Authorization': 'Token abcde'},
            'success': True,
            'meta': {
                'docs': 'Method docstring',
                'method_name': 'test_sth',
                'class_name': 'SthTest',
                'app_name': 'some_app'
            },
            'response': {
                'data': {'foo': 'barium'},
                'status': 200,
            }
        }]
        doc_generator.class_docs = {'SthTest': 'Class docstring'}

    def to_absolute_path(self, *paths):
        return os.path.join(os.path.dirname(__file__), *paths)

    def tearDown(self):
        super().tearDown()
        dirpath = self.to_absolute_path('test_docs')
        if os.path.exists(dirpath) and os.path.isdir(dirpath):
            shutil.rmtree(dirpath)

    def test_yml_file(self):
        doc_generator.write_docs()
        yml_path = self.to_absolute_path('test_docs', 'mkdocs.yml')
        self.assertTrue(os.path.exists(yml_path))
        with open(yml_path) as f:
            self.assertIn('site_name: DRF Tests', f.readlines()[0])

    def assertStrListContainsSubstring(self, str_list, substring):
        joined = ' '.join(str_list)
        self.assertIn(substring, joined)

    def test_index_page(self):
        doc_generator.write_docs()
        md_path = self.to_absolute_path('test_docs', 'docs', 'index.md')
        self.assertTrue(os.path.exists(md_path))

    def test_app_page(self):
        doc_generator.write_docs()
        md_path = self.to_absolute_path('test_docs', 'docs', 'some_app.md')
        self.assertTrue(os.path.exists(md_path))
        with open(md_path) as f:
            lines = f.readlines()
            self.assertStrListContainsSubstring(lines[:3], '# some_app')
            self.assertStrListContainsSubstring(lines[:15], 'Class docstring')
            self.assertStrListContainsSubstring(lines[:15], '## SthTest')
            self.assertStrListContainsSubstring(lines[:25], '**test_sth**')
            self.assertStrListContainsSubstring(lines[:25], 'Method docstring')
            self.assertStrListContainsSubstring(lines[15:30], '* **URL:** `/api`')
            self.assertStrListContainsSubstring(lines[15:30], '* **Method:** `post`')
            self.assertStrListContainsSubstring(lines[15:30], '* **Format:** `json`')
            self.assertStrListContainsSubstring(lines, '"Authorization": "Token abcde"')
            self.assertStrListContainsSubstring(lines, '* **Response data:** ')
            self.assertStrListContainsSubstring(lines, '* **Response status code**: 200')
            self.assertStrListContainsSubstring(lines, '* **Request data:**')
