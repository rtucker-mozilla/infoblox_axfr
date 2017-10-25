import os
import datetime
import dns.zone
all_record_item_types = [
    1, #  A
    2, #  NS
    5, #  CNAME
    15, #  MX
    16, #  TXT
]
bad_record_item_types = [
    6 #seems to be SOA
]


class ZoneWriter(object):


    def __init__(self, zone_name, lines, path):
        self.zone_name = zone_name
        self.lines = lines
        self.serial = None
        self.path = path
        if not path.startswith('/'):
            path = '/' + path
        self.full_path = os.path.join(path, zone_name)
        self.file_exists = os.path.exists(self.full_path)

    def _get_serial_by_date(self, date_obj):
        return datetime.datetime.strftime(date_obj, "%Y%m%d00")

    def _read_zonefile(self, path, zone_name):
        zone = dns.zone.from_file(path, zone_name)
        return zone

    def _get_all_records_from_zone(self, zone):
        return_items = []
        for name, node in zone.nodes.items():
            for rdata in node.rdatasets:
                for item in rdata.items:

                    if item.rdtype not in bad_record_item_types:
                        return_items.append(item)
        return return_items

    def _serial_from_zonefile(self, zone):
        serial = None
        for name, node in zone.nodes.items():
            for rdata in node.rdatasets:
                for item in rdata.items:
                    if item.rdtype == 6:
                        try:
                            serial = int(item.serial)
                            return serial
                        except:
                            continue
        return serial

    def get_serial(self, date_obj=None):
        if self.file_exists is False:
            if date_obj is None:
                date_obj = datetime.datetime.now()
            self.serial = self._get_serial_by_date(date_obj)
        elif self.file_exists is True:
            zone = self._read_zonefile(self.full_path, self.zone_name)
            self.serial = self._serial_from_zonefile
        return self.serial


    def increment_serial(self, serial):
        today_first8 = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
        serial = str(serial)
        first8 = serial[0:8]
        if int(today_first8) > int(first8):
            return "{0}{1}".format(today_first8, '00')
        else:
            last2 = serial[-2:]
            last2 = int(last2) + 1
            if int(last2) < 10:
                last2 = "0{0}".format(last2)
            return "{0}{1}".format(first8, last2)
