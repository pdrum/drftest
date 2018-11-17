from abc import ABCMeta


class ABCTestMeta(ABCMeta):
    ignored_test_class_names = []

    @classmethod
    def add_ignored_test_class_name(mcs, non_test_class):
        mcs.ignored_test_class_names.append(non_test_class)

    def __new__(mcs, name, bases, namespace):
        cls = super(ABCTestMeta, mcs).__new__(mcs, name, bases, namespace)
        cls.__test__ = cls.__name__ not in mcs.ignored_test_class_names
        return cls
