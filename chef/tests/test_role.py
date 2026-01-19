from chef import Role
from chef.tests import ChefTestCase

class TestRole(ChefTestCase):
    def test_get(self):
        r = Role('test_1')
        assert r.exists
        assert r.description == 'Static test role 1'
        assert r.run_list == []
        assert r.default_attributes['test_attr'] == 'default'
        assert r.default_attributes['nested']['nested_attr'] == 1
        assert r.override_attributes['test_attr'] == 'override'

    def test_create(self):
        name = self.random()
        r = Role.create(name, description='A test role', run_list=['recipe[foo]'],
                        default_attributes={'attr': 'foo'}, override_attributes={'attr': 'bar'})
        self.register(r)
        assert r.description == 'A test role'
        assert r.run_list == ['recipe[foo]']
        assert r.default_attributes['attr'] == 'foo'
        assert r.override_attributes['attr'] == 'bar'

        r2 = Role(name)
        assert r2.exists
        assert r2.description == 'A test role'
        assert r2.run_list == ['recipe[foo]']
        assert r2.default_attributes['attr'] == 'foo'
        assert r2.override_attributes['attr'] == 'bar'

    def test_delete(self):
        name = self.random()
        r = Role.create(name)
        r.delete()
        for n in Role.list():
            assert n != name
        assert not Role(name).exists
