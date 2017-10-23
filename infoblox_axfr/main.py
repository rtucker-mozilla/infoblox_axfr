#!/usr/bin/python
import subprocess
import sys
from common import Common
from config import Config
from api import API
from cmd import CMD
from build import Build

server = "10.48.75.120"




def main():
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
    view = 'MDC1%20Private'

    api = API(o_config, view)

    all_zones = api.build_all_zones()
    all_zones = all_zones[:2]
    for zone in all_zones:
        is_reverse = Common.is_reverse_zone_name(zone)
        if is_reverse:
            zone = Common.reverse_name(zone)

        cmd = CMD(zone, server)
        output, errors = cmd.run()
        build = Build(output)
        all_records = build.run()

    all_records = sorted(all_records)
    for r in all_records:
        print r


if __name__ == '__main__':
    main()
