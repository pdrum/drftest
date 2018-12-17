DRF Test
----------

[![Build Status](https://travis-ci.com/pdrum/drftest.svg?branch=master)](https://travis-ci.com/pdrum/drftest)

**DRF Test** is a minimal testing library that aims to facilitate writing **DRY** tests for 
django rest framework views. It also [optionally] generates good looking API documentations based
on tests it runs. 

One thing that usually becomes bothering about documentations is that
they need to be kept up to date and keeping them up to date takes a lot of effort from development
teams and more often than not we tend to not keep them up to date and they eventually lose their
value. With **DRF Test** API docs will be generated based on your tests. So as long as your
tests pass and your code is working, you can be sure that your docs are also up to date!

# Installation
Run `pip install drftest`. Also Make sure you use `python >= 3.4.0`.

# Preparation
In order to use `DRF Test` initially you need to take the following four steps:

* Add `drftest` to your list of `INSTALLED_APPS` like:
```python
INSTALLED_APPS = [
    ...,
    'drftest',
]
```

* Add `TEST_RUNNER = 'drftest.TestRunner'` to your `settings.py` file.

*  **DRF Test** has an interface called `AuthProvider` which can be imported with
`from drftest import AuthProvider` and looks like
```python
class AuthProvider:
    @abstractmethod
    def set_auth(self, api_client: APIClient, user):
        """
        Authenticates user using the given `api_client`
        """
        raise NotImplementedError()

    def get_auth_headers(self, user):
        """
        Returns a dictionary indicating what headers need to be set for authentication
        purpose of given user.
        It is only used in docs.
        """
        return {}
```

In order to use **DRF Test** you need to make a class that inherits from `AuthProvider`
and implements its two abstract methods. Then you need to tell **DRFTest** where your 
auth provider lives. For example if the class is called `MyAuthProvider` and resides
in a module called `my_auth_provider` at the root of your project, you should add the following
line to your `settings.py` file:
```python
DRF_TEST_AUTH_PROVIDER_CLASS = 'my_auth_provider.MyAuthProvider'
```

* Optionally you can set value of a special variable called `DRF_TEST_DOCS_DIR` in your
settings if you do so, then **DRF Test** will create a nice documentation in the directory
specified by `DRF_TEST_DOCS_DIR`. In this documentation will provide a view of what each
endpoint you have tested gets as an input and what it produces as an output. If this 
variable is not set **DRF Test** will avoid creating docs after tests are run. It's also 
a good idea to let `DRF_TEST_DOCS_DIR` be a directory under root of your django project so 
that it is kept track of using VCS under the same repository as the rest of your code.

# Writing your first test
**DRF Test** is not just about generating docs but it also helps you not repeat yourself while
writing tests for your django views. Writing tests usinng **DRF Test** is not much different
with writing simple django tests except for a few simple things.

Your test classes should extend either `BaseViewTest` or `BaseAuthenticatedViewTest` and implement
their abstract methods. Each test class tests only a single url which is handled by methods
of a view class.

For `BaseViewTest` (`from drftest import BaseViewTest`) you override the following two methods:
```python
@abstractmethod
def _make_url(self, kwargs=None):
    """
    :param kwargs: path parameters in a form which can get passed to django's 
    reverse function 
    :return: url which is being tested. (Most probably generated using django's reverse 
    function)
    """
    raise NotImplementedError()
 
 
@abstractmethod
def _get_view_class(self):
    """
    :return: The view class which is being tested. For example if MyAwsomeView is being
    tested, this method should look like `return MyAwsomeView` 
    """
    raise NotImplementedError
```

Also for tests where the url being tested has some path parameters you should override the
following method as well. (It defaults to returning `None`.)
```python
def _get_default_url_kwargs(self):
    """
    :return: A dictionary where the keys are name of path parameters and the values
    are their default values. It doesn't matter if the values are not meaningful
    defaults. The output is just used by tests generated by drftest which check
    whether or not things like url mapping, etc are working and your view is working.
    """
    return None
```

In case the view class being tested has some `permission_classes` your tests can inherit
`BaseAuthenticatedViewTest` (`from drftest import BaseAuthenticatedViewTest`) instead of 
`BaseViewTest`. This way you should also override a fourth method which looks like:
```python
@abstractmethod
def _get_permission_classes(self):
    """
    Should return a list of permission classes. drftest generates a testcase to check if
    result of calling this method matches those specified by `permission_classes` attribute
    of your class. This way you can test your permission classes separately and in other
    tests just use drftest's auto-generated testcases to check if correct permissions are set.  
    """
    raise NotImplementedError()
```

Finally whenever you need to make a request use `self._get_for_response`, `self._post_for_response`,
`self._put_for_response`, `self._head_for_response` and `self._patch_for_response`. Here's what each 
of their parameters does (None of them are required. They all have default values.):
* **User** is user of the request. User will be authenticated using `AuthProvider` you wrote earlier.
If user is not given, request will be sent using an anonymous user.
* **data** is body of requests (in case of things like POST) or query parameters (in case of
things like GET or DELETE that do not have a body.)
* **url_kwargs** is a dictionary specifying path parameters to use.
* **format** defaults to `json`. Can also be set to `multipart`. Docs will not get generated
for multipart requests.
* **docs** is a boolean whether or not the request should appear in docs and defaults to `True` 
* **extra [as kwargs]** Headers can be passed as kwargs.

# Using generated docs
Docs are generated to be used with [mkdocs](https://www.mkdocs.org/). Installing it takes onnly
a single command. After installing it you can use `mkdocs serve` to run the docs and then
visit them at `http://localhost:8000`. You can 
also generate a static website out of it very easily. For more information visit [mkdocs](https://www.mkdocs.org/).

Here's how you can install mkdocs onn mac and ubuntu respectively.

```
brew install mkdocs
sudo apt-get install mkdocs-doc
``` 

# Advantages
* You will not repeat things like writing url of test, name of class being tested, 
authentication mechanism for user sending requests in your tests, etc in each and every test.
* Tests of your view will all look quite similar even if multiple people are working on them 
simultaneously.
* Docs will get generated from your tests.
