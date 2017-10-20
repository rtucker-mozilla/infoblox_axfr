import context #  NOQA
from infoblox_transfer.common import is_reverse_zone_name, reverse_name


def test_is_reverse_zone_name():
    assert is_reverse_zone_name('10.0.0.0/16') == True
    assert is_reverse_zone_name('asdf/20') == True
    assert is_reverse_zone_name('asdf') == False


def test_reverse_name():
    assert reverse_name('10.0.0.0/16') == "0.0.10.in-addr.arpa"
    assert reverse_name('foo.bar.domain.com') == "foo.bar.domain.com"
