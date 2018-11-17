import traceback

from django_nose.runner import NoseTestSuiteRunner

from drftest.doc_generator import write_docs


class TestRunner(NoseTestSuiteRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        result = None
        try:
            result = super().run_tests(test_labels, extra_tests)
            write_docs()
        except Exception:
            traceback.print_exc()
        finally:
            return result
