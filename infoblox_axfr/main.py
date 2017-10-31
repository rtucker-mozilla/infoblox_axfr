#!/usr/bin/python
import sys
import argparse
from common import Common
from config import Config
from api import API
from dns_cmd import CMD
from build import Build
from zoneobject import ZoneObject
from dns import zone as dnszone, query
from dns.exception import FormError
import dns
import os



def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', action="store", type=str, dest="view")
    parser.add_argument('-s', action="store", type=str, dest="server")
    parser.add_argument('-l', action="store", type=int, dest="zone_limit")
    parser.add_argument('-o', action="store", type=str, dest="origin")
    parser.add_argument('-p', action="store", type=str, dest="zone_path")
    args = parser.parse_args()

    if not args.view:
        print "DNS View required"
        sys.exit(2)

    if not args.server:
        print "server required"
        sys.exit(2)

    if not args.zone_path:
        print "zone_path required"
        sys.exit(2)

    named_reload = False
    config_obj = Config()
    o_config = config_obj.get_config()
    try:
        is_config_valid, message = config_obj.config_valid(o_config)
    except AttributeError:
        is_config_valid = False
        message = "No Configuration File Found"

    if is_config_valid is False:
        print message
        sys.exit(2)

    api = API(o_config, args.view, origin=args.origin)

    all_records = []
    all_zones = api.build_all_zones()

    if args.zone_limit:
        all_zones = all_zones[:args.zone_limit]
    for zone in all_zones:
        is_reverse = Common.is_reverse_zone_name(zone)
        if is_reverse:
            zone = Common.reverse_name(zone)

        d_cmd = CMD(zone, args.server)
        output, errors = d_cmd.run()
        build = Build(output)
        all_records += build.run()

        local_zone = ZoneObject(zone, path=args.zone_path)
        local_serial = local_zone.get_serial()

        try:
            axfr_zone = dnszone.from_xfr(query.xfr(args.server, zone))
        except dns.exception.FormError:
            axfr_zone = None

        if axfr_zone is not None:
            axfr_zone_object = ZoneObject(zone, zone_obj=axfr_zone)
            axfr_serial = axfr_zone_object.get_serial()

        if axfr_serial != local_serial:
            print "Reload"
            should_reload = True
            write_path = os.path.join(args.zone_path, zone)
            axfr_zone.to_file(write_path)

    if should_reload:
        # decide how to handle this
        # should also check using named-checkzone

if __name__ == '__main__':
    main()
