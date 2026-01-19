import pytest
from chef import Environment
from chef.exceptions import ChefAPIVersionError
from chef.tests import ChefTestCase, test_chef_api

class TestEnvironment(ChefTestCase):
    def test_version_error_list(self):
        with test_chef_api(version='0.9.0'):
            with pytest.raises(ChefAPIVersionError):
                Environment.list()

    def test_version_error_create(self):
        with test_chef_api(version='0.9.0'):
            with pytest.raises(ChefAPIVersionError):
                Environment.create(self.random())

    def test_version_error_init(self):
        with test_chef_api(version='0.9.0'):
            with pytest.raises(ChefAPIVersionError):
                Environment(self.random())
