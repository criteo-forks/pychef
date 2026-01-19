import os
import pytest

from chef.rsa import Key, SSLError
from chef.tests import TEST_ROOT

class TestRSA:
    def test_load_private(self):
        key = Key(os.path.join(TEST_ROOT, 'client.pem'))
        assert not key.public

    def test_load_public(self):
        key = Key(os.path.join(TEST_ROOT, 'client_pub.pem'))
        assert key.public

    def test_private_export(self):
        key = Key(os.path.join(TEST_ROOT, 'client.pem'))
        raw = open(os.path.join(TEST_ROOT, 'client.pem'), 'rb').read()
        assert key.private_export().strip() == raw.strip()

    def test_public_export(self):
        key = Key(os.path.join(TEST_ROOT, 'client.pem'))
        raw = open(os.path.join(TEST_ROOT, 'client_pub.pem'), 'rb').read()
        assert key.public_export().strip() == raw.strip()

    def test_private_export_pubkey(self):
        key = Key(os.path.join(TEST_ROOT, 'client_pub.pem'))
        with pytest.raises(SSLError):
            key.private_export()

    def test_public_export_pubkey(self):
        key = Key(os.path.join(TEST_ROOT, 'client_pub.pem'))
        raw = open(os.path.join(TEST_ROOT, 'client_pub.pem'), 'rb').read()
        assert key.public_export().strip() == raw.strip()

    def test_encrypt_decrypt(self):
        key = Key(os.path.join(TEST_ROOT, 'client.pem'))
        msg = 'Test string!'
        assert key.public_decrypt(key.private_encrypt(msg)) == msg

    def test_encrypt_decrypt_pubkey(self):
        key = Key(os.path.join(TEST_ROOT, 'client.pem'))
        pubkey = Key(os.path.join(TEST_ROOT, 'client_pub.pem'))
        msg = 'Test string!'
        assert pubkey.public_decrypt(key.private_encrypt(msg)) == msg

    def test_generate(self):
        key = Key.generate()
        msg = 'Test string!'
        assert key.public_decrypt(key.private_encrypt(msg)) == msg

    def test_generate_load(self):
        key = Key.generate()
        key2 = Key(key.private_export())
        assert not key2.public
        key3 = Key(key.public_export())
        assert key3.public

    def test_load_pem_string(self):
        key = Key(open(os.path.join(TEST_ROOT, 'client.pem'), 'rb').read())
        assert not key.public

    def test_load_public_pem_string(self):
        key = Key(open(os.path.join(TEST_ROOT, 'client_pub.pem'), 'rb').read())
        assert key.public
