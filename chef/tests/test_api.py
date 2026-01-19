import os
import pytest

from chef.api import ChefAPI


class TestAPI:
    def load(self, path):
        path = os.path.join(os.path.dirname(__file__), 'configs', path)
        return ChefAPI.from_config_file(path)

    def test_config_with_interpolated_settings(self, mocker):
        mock_subproc_popen = mocker.patch('chef.api.subprocess.Popen')
        process_mock = mocker.Mock()
        output = b'{"chef_server_url": "http:///chef:4000", "client_key": "../client.pem",' \
                 b'"node_name": "test_1"}'
        attrs = {
            'communicate.return_value': (output, 'error'),
            'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_subproc_popen.return_value = process_mock

        api = self.load('basic_with_interpolated_values.rb')
        assert api.client == 'test_1'

    def test_basic(self):
        api = self.load('basic.rb')
        assert api.url == 'http://chef:4000'
        assert api.client == 'test_1'

    def test_current_dir(self):
        api = self.load('current_dir.rb')
        path = os.path.join(os.path.dirname(__file__), 'configs', 'test_1')
        assert os.path.normpath(api.client) == path

    def test_env_variables(self):
        try:
            os.environ['_PYCHEF_TEST_'] = 'foobar'
            api = self.load('env_values.rb')
            assert api.client == 'foobar'
        finally:
            del os.environ['_PYCHEF_TEST_']

    def test_bad_key_raises(self):
        invalids = [None, '']
        for item in invalids:
            with pytest.raises(ValueError):
                ChefAPI('foobar', item, 'user')
