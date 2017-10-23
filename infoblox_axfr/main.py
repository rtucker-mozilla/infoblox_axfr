#!/usr/bin/python
import requests
import subprocess
import sys
from common import is_reverse_zone_name, reverse_name
from config import Config
o_config = Config.get_config()

try:
    is_config_valid, message = Config.config_valid(o_config)
except AttributeError:
    is_config_valid = False
    message = "No Configuration File Found"

if is_config_valid is False:
    print message
    sys.exit(2)


final = "{0}/wapi/v2.7/zone_auth?view={1}".format(
    o_config.get('InfoBlox', 'HostName'),
    o_config.get('InfoBlox', 'Zone'),
)
username = o_config.get('InfoBlox', 'UserName')
password = o_config.get('InfoBlox', 'Password')
server = "10.48.75.120"

allowed_types = [
    "A",
    "SRV",
    "CNAME",
    "PTR",
]


def main():
    resp = requests.get(final, auth=(username, password), verify=False)
    all_zones = []
    all_records = []
    if resp.status_code == 200:
        for data in resp.json():
            name = data[u"fqdn"]
            all_zones.append(name)

    all_zones = all_zones[:2]
    print all_zones
    for zone in all_zones:
        is_reverse = is_reverse_zone_name(zone)
        if is_reverse:
            zone = reverse_name(zone)
        dig_list = [
            "dig",
            "AXFR",
            zone,
            "@" + server
        ]
        p = subprocess.Popen(
            dig_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, errors = p.communicate()
        print output
        for line in output.split("\n"):
            r_split = line.strip().split()
            try:
                r_type = r_split[3]
            except IndexError:
                continue
            if r_type in allowed_types:
                all_records.append('\t'.join(r_split))

    all_records = sorted(all_records)
    for r in all_records:
        print r


if __name__ == '__main__':
    main()
