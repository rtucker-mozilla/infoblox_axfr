import context #  NOQA
from infoblox_axfr.common import Common


def test_is_reverse_zone_name():
    assert Common.is_reverse_zone_name('10.0.0.0/16') == True
    assert Common.is_reverse_zone_name('asdf/20') == True
    assert Common.is_reverse_zone_name('asdf') == False


def test_reverse_name():
    assert Common.reverse_name('10.0.0.0/16') == "0.0.10.in-addr.arpa"
    assert Common.reverse_name('foo.bar.domain.com') == "foo.bar.domain.com"
