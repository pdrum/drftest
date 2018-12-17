from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse, path
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drftest import BaseViewTest, doc_generator
from drftest.tests.doc_schema import doc_schema


class DummyView(ViewSet):
    def handle_put(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK, data={'a': 'b'})

    def handle_delete(self, request: Request, pk) -> Response:
        return Response(status=status.HTTP_200_OK, data={'c': 'd'})

    def handle_post(self, request: Request) -> Response:
        return Response(status=status.HTTP_200_OK, data={'e': 'f'})


urlpatterns = [
    path(
        'dummy/<int:pk>/',
        DummyView.as_view({'delete': 'handle_delete'}),
        name='dummy-with-pk',
    ),
    path(
        'dummy/',
        DummyView.as_view({'put': 'handle_put', 'post': 'handle_post'}),
        name='dummy',
    ),
]


@override_settings(ROOT_URLCONF=__name__)
class DummyViewPostTest(BaseViewTest):
    """
    Class docstring
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='u1')
        doc_generator.class_docs = {}
        doc_generator.store = []

    def _make_url(self, kwargs=None):
        return reverse('dummy')

    def _get_view_class(self):
        return DummyView

    def test_requests_can_be_made(self, *_):
        response = self._post_for_response()
        self.assertSuccess(response)

    def test_schema_of_docs(self):
        response = self._post_for_response(user=self.user, data={'foo': 'bar'})
        self.assertSuccess(response)
        self.assertEqual(1, len(doc_generator.store))
        self.assertTrue(
            doc_schema.is_valid(doc_generator.store[0]), 'generated docs should match docs schema')

    def test_values_of_doc_dict(self):
        """
        Method docstring
        """
        response = self._post_for_response(user=self.user, data={'foo': 'bar'})
        self.assertSuccess(response)
        self.assertEqual(1, len(doc_generator.store))
        doc = doc_generator.store[0]
        self.assertEqual(doc['method'], 'post')
        self.assertDictEqual(doc['data'], {'foo': 'bar'})
        self.assertEqual(doc['url'], '/dummy/')
        self.assertIsNone(doc['url_kwargs'])
        self.assertEqual(doc['format'], 'json')
        self.assertIn('Authorization', doc['headers'])
        self.assertTrue(doc['success'])
        self.assertEqual(doc['meta']['docs'].strip(), 'Method docstring')
        self.assertEqual(doc['meta']['method_name'].strip(), 'test_values_of_doc_dict')
        self.assertEqual(doc['meta']['class_name'].strip(), 'DummyViewPostTest')
        self.assertEqual(doc['meta']['app_name'].strip(), 'drftest')
        self.assertEqual(doc['response']['status'], status.HTTP_200_OK)
        self.assertEqual(doc['response']['data'], {'e': 'f'})

    def test_class_docstring(self):
        response = self._post_for_response(user=self.user, data={'foo': 'bar'})
        self.assertSuccess(response)
        self.assertEqual(
            doc_generator.class_docs.get('DummyViewPostTest', '').strip(),
            'Class docstring'
        )


@override_settings(ROOT_URLCONF=__name__)
class DummyViewDeleteTest(BaseViewTest):
    """
    Class docstring
    """

    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='u1')
        doc_generator.class_docs = {}
        doc_generator.store = []

    def _make_url(self, kwargs=None):
        return reverse('dummy-with-pk', kwargs=kwargs)

    def _get_view_class(self):
        return DummyView

    def _get_default_url_kwargs(self):
        return {'pk': 1}

    def test_url_kwargs(self, *_):
        response = self._delete_for_response(url_kwargs={'pk': 3})
        self.assertSuccess(response)
        self.assertEqual(len(doc_generator.store), 1)
        doc = doc_generator.store[0]
        self.assertDictEqual(doc['url_kwargs'], {'pk': 3})
