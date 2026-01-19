from chef.tests import ChefTestCase, mock_search

class TestFabric(ChefTestCase):
    def test_roledef(self, mocker):
        search_data = {
            ('role', '*:*'): {},
        }
        search_mock_memo = {}
        def search_mock_fn(index, q='*:*', *args, **kwargs):
            data = search_data[index, q]
            search_mock_inst = search_mock_memo.get((index, q))
            if search_mock_inst is None:
                search_mock_inst = search_mock_memo[index, q] = mocker.Mock()
                search_mock_inst.data = data
            return search_mock_inst

        mocker.patch('chef.search.Search', side_effect=search_mock_fn)

    def test_roledef2(self, mocker):
        mock_search(mocker, {('role', '*:*'): {1:2}})
