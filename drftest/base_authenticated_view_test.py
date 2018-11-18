from abc import abstractmethod
from inspect import isclass

from rest_framework.settings import api_settings

from drftest.abc_test_meta import ABCTestMeta
from drftest.base_view_test import BaseViewTest

ABCTestMeta.add_ignored_test_class_name('BaseAuthenticatedViewTest')


class BaseAuthenticatedViewTest(BaseViewTest, metaclass=ABCTestMeta):
    @abstractmethod
    def _get_permission_classes(self):
        """
        Should return a list of permission classes. drftest generates a testcase to check if
        result of calling this method matches those specified by `permission_classes` attribute
        of your class. This way you can test your permission classes separately and in other
        tests just use drftest's auto-generated testcases to check if correct permissions are set.
        """
        raise NotImplementedError()

    def _get_permission_classes_for_docs(self):
        return [str(c) if not isclass(c) else c.__name__
                for c in self._get_permission_classes()]

    @staticmethod
    def __diff(first, second):
        return set(first) - set(second)

    def test_has_permission_classes(self, *_):
        if not self._get_permission_classes():
            self.assertEqual(self._get_view_class().permission_classes,
                             api_settings.DEFAULT_PERMISSION_CLASSES,
                             'Extra permissions are set for the view.')
            return
        xor = set(self._get_permission_classes()) ^ set(self._get_view_class().permission_classes)
        if not xor:
            return
        self.fail('Expected permission classes: {expected} But found: {actual}'.format(
            expected=self._get_permission_classes(),
            actual=self._get_view_class().permission_classes
        ))
