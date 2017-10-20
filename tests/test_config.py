import context #  NOQA
import hashlib
import time
import os
import ConfigParser
from infoblox_axfr.config import get_config, config_valid


def test_get_config_not_exists():
    assert get_config('/tmp/asdfasdfasdfasdfsdaf') is None


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
    assert get_config(filename) is None
    write_test_config_file(filename)
    config = get_config(filename)
    assert config.get("InfoBlox", "HostName") == "test.domain.com"
    remove_config(filename)

def test_get_config_missing_infoblox_hostname():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    config, error = config_valid(config)
    assert config is False
    assert error == "No option 'HostName' in section: 'InfoBlox'"

def test_get_config_missing_infoblox_username():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    config.set('InfoBlox', 'HostName', 'test.domain.com')
    config.set('InfoBlox', 'Password', 'testpassword')
    config, error = config_valid(config)
    assert config is False
    assert error == "No option 'UserName' in section: 'InfoBlox'"

def test_get_config_missing_infoblox_password():
    config = ConfigParser.RawConfigParser()
    config.add_section('InfoBlox')
    config.set('InfoBlox', 'HostName', 'test.domain.com')
    config.set('InfoBlox', 'UserName', 'username')
    config, error = config_valid(config)
    assert config is False
    assert error == "No option 'Password' in section: 'InfoBlox'"
