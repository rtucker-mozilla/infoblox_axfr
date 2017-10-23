import context #  NOQA
import hashlib
import time
import os
import pytest
import ConfigParser
from infoblox_axfr.config import Config

@pytest.yield_fixture(scope='function')
def config():
    c = Config
    yield c
    c = None

def test_get_config_not_exists():
    config = Config('/tmp/asdfkjasdfkjasdfasdfasdfasdfsadf')
    ret = config.get_config()
    assert ret is None
    config = None


def remove_config(filepath):
    if os.path.exists(filepath):
        os.unlink(filepath)


def write_test_config_file(filename):
    content = "[InfoBlox]\n"
    content += "HostName = test.domain.com\n"
    fh = open(filename, 'w')
    fh.write(content)
    fh.close()


def test_get_config():
    millis = str(int(round(time.time() * 1000)))
    filename_hash = hashlib.sha1(millis).hexdigest()
    filename = "{0}.cfg".format(filename_hash)
    remove_config(filename)
    c = Config(filename)
    assert c.get_config() is None
    write_test_config_file(filename)
    config = c.get_config()
    assert config.get("InfoBlox", "HostName") == "test.domain.com"
    remove_config(filename)


def test_get_config_missing_infoblox_hostname():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    c = Config('/tmp/blah')
    config, error = c.config_valid(config)
    assert config is False
    assert error == "No option 'HostName' in section: 'InfoBlox'"


def test_get_config_missing_infoblox_username():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    config.set('InfoBlox', 'HostName', 'test.domain.com')
    config.set('InfoBlox', 'Password', 'testpassword')
    c = Config('/tmp/blah')
    config, error = c.config_valid(config)
    assert config is False
    assert error == "No option 'UserName' in section: 'InfoBlox'"


def test_get_config_missing_infoblox_password():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    config.set('InfoBlox', 'HostName', 'test.domain.com')
    config.set('InfoBlox', 'UserName', 'username')
    c = Config('/tmp/blah')
    config, error = c.config_valid(config)
    assert config is False
    assert error == "No option 'Password' in section: 'InfoBlox'"
