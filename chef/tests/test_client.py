from chef import Client
from chef.tests import ChefTestCase

class TestClient(ChefTestCase):
    def test_list(self):
        assert 'test_1' in Client.list()

    def test_get(self):
        client = Client('test_1')
        assert client.platform
        assert client.orgname == 'pycheftest'
        assert client.public_key
        assert client.certificate
        assert client.private_key is None

    def test_create(self):
        name = self.random()
        client = Client.create(name)
        self.register(client)
        assert client.name == name
        #assert client.orgname == 'pycheftest' # See CHEF-2019
        assert client.private_key
        assert client.public_key
        assert name in Client.list()

        client2 = Client(name)
        client2.rekey()
        assert client.public_key == client2.public_key
        assert client.private_key != client2.private_key

    def test_delete(self):
        name = self.random()
        client = Client.create(name)
        client.delete()
        assert name not in Client.list()
