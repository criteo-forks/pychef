import os
import random
from functools import wraps

import pytest

from chef.api import ChefAPI
from chef.exceptions import ChefError
from chef.search import Search

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))

def skipSlowTest():
    return pytest.mark.skipif(not os.environ.get('PYCHEF_SLOW_TESTS'), reason='slow tests skipped, set $PYCHEF_SLOW_TESTS=1 to enable')

def mock_search(mocker, search_data):
    def _search_inst(index, q='*:*', *args, **kwargs):
        data = search_data[index, q]
        if not isinstance(data, dict):
            data = {'total': len(data), 'rows': data}
        search = Search(index, q, *args, **kwargs)
        search._data = data
        return search
    return mocker.patch('chef.search.Search', side_effect=_search_inst)


def test_chef_api(**kwargs):
    return ChefAPI('https://api.opscode.com/organizations/pycheftest', os.path.join(TEST_ROOT, 'client.pem'), 'unittests', **kwargs)


class ChefTestCase(object):
    """Base class for Chef unittests."""

    @pytest.fixture(autouse=True)
    def setup_chef(self):
        self.api = test_chef_api()
        self.api.set_default()
        self.objects = []
        yield
        for obj in self.objects:
            try:
                obj.delete()
            except ChefError as e:
                print(e)
                # Continue running

    def register(self, obj):
        self.objects.append(obj)

    def random(self, length=8, alphabet='0123456789abcdef'):
        return ''.join(random.choice(alphabet) for _ in range(length))
