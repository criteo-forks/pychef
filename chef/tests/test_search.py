from chef import Search, Node
from chef.tests import ChefTestCase, mock_search

class TestSearch(ChefTestCase):
    def test_search_all(self):
        s = Search('node')
        assert len(s) >= 3
        assert 'test_1' in s
        assert 'test_2' in s
        assert 'test_3' in s

    def test_search_query(self):
        s = Search('node', 'role:test_1')
        assert len(s) >= 2
        assert 'test_1' in s
        assert 'test_2' not in s
        assert 'test_3' in s

    def test_list(self):
        searches = Search.list()
        assert 'node' in searches
        assert 'role' in searches

    def test_search_set_query(self):
        s = Search('node').query('role:test_1')
        assert len(s) >= 2
        assert 'test_1' in s
        assert 'test_2' not in s
        assert 'test_3' in s

    def test_search_call(self):
        s = Search('node')('role:test_1')
        assert len(s) >= 2
        assert 'test_1' in s
        assert 'test_2' not in s
        assert 'test_3' in s

    def test_rows(self):
        s = Search('node', rows=1)
        assert len(s) == 1
        assert s.total >= 3

    def test_start(self):
        s = Search('node', start=1)
        assert len(s) == s.total - 1
        assert s.total >= 3

    def test_slice(self):
        s = Search('node')[1:2]
        assert len(s) == 1
        assert s.total >= 3

        s2 = s[1:2]
        assert len(s2) == 1
        assert s2.total >= 3
        assert s[0]['name'] != s2[0]['name']

        s3 = Search('node')[2:3]
        assert len(s3) == 1
        assert s3.total >= 3
        assert s2[0]['name'] == s3[0]['name']

    def test_object(self):
        s = Search('node', 'name:test_1')
        assert len(s) == 1
        node = s[0].object
        assert node.name == 'test_1'
        assert node.run_list == ['role[test_1]']


class TestMockSearch(ChefTestCase):
    def test_single_node(self, mocker):
        mock_search(mocker, {
            ('node', '*:*'): [Node('fake_1', skip_load=True).to_dict()]
        })
        import chef.search
        s = chef.search.Search('node')
        assert len(s) == 1
        assert 'fake_1' in s
