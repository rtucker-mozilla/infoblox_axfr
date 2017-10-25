#!/usr/bin/python
import sys
import argparse
from common import Common
from config import Config
from api import API
from dns_cmd import CMD
from build import Build
from zonewriter import ZoneWriter


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', action="store", type=str, dest="view")
    parser.add_argument('-s', action="store", type=str, dest="server")
    parser.add_argument('-l', action="store", type=int, dest="zone_limit")
    args = parser.parse_args()

    if not args.view:
        print "DNS View required"
        sys.exit(2)

    if not args.server:
        print "server required"
        sys.exit(2)
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

    all_records = []
    all_zones = api.build_all_zones()

    api = API(o_config, args.view)
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

    all_records = sorted(all_records)
    for r in all_records:
        print r


if __name__ == '__main__':
    main()
