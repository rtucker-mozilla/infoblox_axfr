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
from checkzone import CheckZone
from reloadnamed import ReloadNamed
import dns
import os



def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-d', action="store", type=str, dest="view")
    parser.add_argument('-s', action="store", type=str, dest="server")
    parser.add_argument('-l', action="store", type=int, dest="zone_limit")
    parser.add_argument('-o', action="store", type=str, dest="origin")
    parser.add_argument('-p', action="store", type=str, dest="zone_path")
    parser.add_argument('-w', action="store", type=str, dest="override_path")
    parser.add_argument('-x', action="store_true", dest="delete_unknown_zone")
    parser.add_argument('-e', action="store", dest="named_restart_command")
    args = parser.parse_args()

    config_obj = Config()
    o_config = config_obj.get_config()
    stop_update_file_path = o_config.get('Global', 'StopUpdate')
    statefile_path = o_config.get('Global', 'StateFile')

    try:
        is_config_valid, config_message = config_obj.config_valid(o_config)
    except AttributeError:
        is_config_valid = False
        config_message = "No Configuration File Found"

    if os.path.exists(stop_update_file_path):
        print "Stop Update file Exists"
        sys.exit(2)

    if is_config_valid is False:
        print config_message
        sys.exit(2)

    if not args.view:
        msg = "DNS View command line argument required"
        Common.write_stop_update(stop_update_file_path, msg)
        print msg
        sys.exit(2)

    if not args.server:
        msg = "server command line argument required"
        Common.write_stop_update(stop_update_file_path, msg)
        print msg
        sys.exit(2)

    if not args.zone_path:
        msg = "zone_path command line argument required"
        Common.write_stop_update(stop_update_file_path, msg)
        print msg
        sys.exit(2)

    named_restart_command = "service named restart"
    if args.named_restart_command:
        named_restart_command = args.named_restart_command

    override_path = None
    if args.override_path:
        override_path = args.override_path


    named_reload = False
    named_failures = None
    reload_zones = []


    api = API(o_config, args.view, origin=args.origin)

    all_records = []
    all_zones = api.build_all_zones()
    # Track all of the zone names to compare via os.listdir
    all_zone_names = []


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
        all_zone_names.append(local_zone.zone_name)

        try:
            axfr_zone = dnszone.from_xfr(query.xfr(args.server, zone))
        except dns.exception.FormError:
            axfr_zone = None
        except dns.name.EmptyLabel:
            axfr_zone = None
        except Exception, e:
            axfr_zone = None
        if axfr_zone is None or local_zone is None:
            continue

        if axfr_zone is not None:
            axfr_zone_object = ZoneObject(zone, zone_obj=axfr_zone)
            axfr_serial = axfr_zone_object.get_serial()

        if axfr_serial != local_serial:
            named_reload = True
            write_path = os.path.join(args.zone_path, zone)
            try:
                axfr_zone.to_file(write_path)
            except Exception, e:
                print "Exception: {0}".format(exception)
            reload_zones.append({
                'zone': zone,
                'path': write_path
            })
    all_local_zonefiles = Common.get_local_zones(args.zone_path)
    zones_to_remove = Common.get_zones_to_remove(
        all_local_zonefiles,
        all_zone_names
    )

    if args.delete_unknown_zone:
        for zone_file in zones_to_remove:
            zone_file_full_path = os.path.join(args.zone_path, zone_file)
            os.unlink(zone_file_full_path)

    if override_path is not None:
        for zone in os.listdir(override_path):
            zone_file_full_path = os.path.join(args.zone_path, zone)
            override_full_path = os.path.join(override_path, zone)
            fh = open(zone_file_full_path, 'r')
            current_content = fh.readlines()
            fh.close()
            fh = open(zone_file_full_path, 'a')
            for line in open(override_full_path, 'r').readlines():
                if not line in current_content:
                    fh.write(line)
            fh.close()

    for zone in all_local_zonefiles:
        zone_file_full_path = os.path.join(args.zone_path, zone)
        cz = CheckZone(zone_file_full_path, zone)
        returncode, msg = cz.run()
        if returncode != 0:
            print msg
            Common.write_stop_update(stop_update_file_path, msg)
            print msg
            sys.exit(2)

    if named_reload:
        r = ReloadNamed(named_restart_command)
        r.run()

    Common.touch(statefile_path)

if __name__ == '__main__':
    main()
