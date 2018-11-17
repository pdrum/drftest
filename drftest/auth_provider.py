from abc import abstractmethod

from rest_framework.test import APIClient


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
