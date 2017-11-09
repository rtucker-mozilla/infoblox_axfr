import context #  NOQA
import random
import string
import os
from infoblox_axfr.common import Common


def test_is_reverse_zone_name():
    assert Common.is_reverse_zone_name('10.0.0.0/16') == True
    assert Common.is_reverse_zone_name('asdf/20') == True
    assert Common.is_reverse_zone_name('asdf') == False


def test_reverse_name():
    assert Common.reverse_name('10.0.0.0/16') == "0.0.10.in-addr.arpa"
    assert Common.reverse_name('foo.bar.domain.com') == "foo.bar.domain.com"

def test_touch_empty_file():
    random_path = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(12)
    )
    t_file = os.path.join('/tmp/', random_path)
    if os.path.exists(t_file):
        os.unlink(t_file)
    Common.touch(t_file)
    assert os.path.exists(t_file)
    os.unlink(t_file)

def test_write_stop_update():
    random_path = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(12)
    )
    t_file = os.path.join('/tmp/', random_path)
    if os.path.exists(t_file):
        os.unlink(t_file)
    message = "Failure Message Here"
    Common.write_stop_update(t_file, message)
    assert os.path.exists(t_file)
    content = open(t_file, 'r').read()
    assert content == message
    os.unlink(t_file)
