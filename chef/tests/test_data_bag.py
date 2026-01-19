from chef import DataBag, DataBagItem, Search
from chef.tests import ChefTestCase

class TestDataBag(ChefTestCase):
    def test_list(self):
        bags = DataBag.list()
        assert 'test_1' in bags
        assert isinstance(bags['test_1'], DataBag)

    def test_keys(self):
        bag = DataBag('test_1')
        assert set(bag.keys()) == {'item_1', 'item_2'}
        assert set(bag) == {'item_1', 'item_2'}

    def test_item(self):
        bag = DataBag('test_1')
        item = bag['item_1']
        assert item['test_attr'] == 1
        assert item['other'] == 'foo'

    def test_search_item(self):
        assert 'test_1' in Search.list()
        q = Search('test_1')
        assert 'item_1' in q
        assert 'item_2' in q
        assert q['item_1']['raw_data']['test_attr'] == 1
        item = q['item_1'].object
        assert isinstance(item, DataBagItem)
        assert item['test_attr'] == 1

    def test_direct_item(self):
        item = DataBagItem('test_1', 'item_1')
        assert item['test_attr'] == 1
        assert item['other'] == 'foo'

    def test_direct_item_bag(self):
        bag = DataBag('test_1')
        item = DataBagItem(bag, 'item_1')
        assert item['test_attr'] == 1
        assert item['other'] == 'foo'

    def test_create_bag(self):
        name = self.random()
        bag = DataBag.create(name)
        self.register(bag)
        assert name in DataBag.list()

    def test_create_item(self):
        value = self.random()
        bag_name = self.random()
        bag = DataBag.create(bag_name)
        self.register(bag)
        item_name = self.random()
        item = DataBagItem.create(bag, item_name, foo=value)
        assert 'foo' in item
        assert item['foo'] == value
        assert item_name in bag
        bag2 = DataBag(bag_name)
        assert item_name in bag2
        item2 = bag2[item_name]
        assert 'foo' in item2
        assert item2['foo'] == value

    def test_set_item(self):
        value = self.random()
        value2 = self.random()
        bag_name = self.random()
        bag = DataBag.create(bag_name)
        self.register(bag)
        item_name = self.random()
        item = DataBagItem.create(bag, item_name, foo=value)
        item['foo'] = value2
        item.save()
        assert item['foo'] == value2
        item2 = DataBagItem(bag, item_name)
        assert item2['foo'] == value2
