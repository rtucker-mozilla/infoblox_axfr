import context #  NOQA
import datetime
import pytest
import os
import time
from shutil import copyfile
from infoblox_axfr.zonewriter import ZoneWriter

t_date = datetime.datetime.strptime("2017-12-31", "%Y-%m-%d")
origin = 'domain.com'
zone_name = origin
lines = ['a','b','c']
path = '/tmp'
origin_path = os.path.join(path, origin)

@pytest.yield_fixture
def z():
    z = ZoneWriter(zone_name, lines, path)
    yield z
    z = None


def write_zonefile():
    ret = copyfile('tests/' + origin, origin_path)
    return ret

def remove_zonefile():
    try:
        os.unlink(origin_path)
    except Exception, e:
        print e

def test_zone_writer_constructor(z):
    assert z is not None
    assert len(z.lines) is 3

def test_get_serial_by_date_obj(z):
    assert z.get_serial(date_obj=t_date) == '2017123100'

def test_increment_serial(z):
    serial = z.get_serial(date_obj=t_date)
    assert z.increment_serial(serial) == '2017123101'

def test_increment_serial_proper_date(z):
    serial = z.get_serial(date_obj=t_date)
    today_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    today_serial ='{}00'.format(str(today_str))
    today_serial_incremented ='{}01'.format(str(today_str))
    assert z.increment_serial(today_serial) == today_serial_incremented

def test_read_zonefile():
    write_zonefile()
    z = ZoneWriter(zone_name, lines, path)
    assert z.file_exists is True
    zone = z._read_zonefile(origin_path, origin)
    assert zone is not None
    remove_zonefile()

def test_read_serial_zonefile():
    write_zonefile()
    z = ZoneWriter(zone_name, lines, path)
    zone = z._read_zonefile(origin_path, origin)
    serial = z._serial_from_zonefile(zone)
    assert serial == 2017072400
    remove_zonefile()

def test_increment_serial_from_zonefile():
    write_zonefile()
    z = ZoneWriter(zone_name, lines, path)
    zone = z._read_zonefile(origin_path, origin)
    serial = z._serial_from_zonefile(zone)
    date_obj = datetime.datetime.now()
    today_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    # 2017102500
    today_serial ='{}00'.format(str(today_str))
    assert z.increment_serial(serial) == today_serial
    remove_zonefile()
