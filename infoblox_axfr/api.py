import requests
class API(object):
    def __init__(self, o_config, zone):
        self.hostname = o_config.get('InfoBlox', 'HostName')
        self.username = o_config.get('InfoBlox', 'UserName')
        self.password = o_config.get('InfoBlox', 'Password')
        self.zone = zone
        self.verify = False

    def get_url(self):
        final = "{0}/wapi/v2.7/zone_auth?view={1}".format(
            self.hostname,
            self.zone,
        )
        return final

    def build_all_zones(self):
        all_zones = []
        final = self.get_url()
        resp = requests.get(final, auth=(self.username, self.password), verify=self.verify)
        if resp.status_code == 200:
            for data in resp.json():
                name = data[u"fqdn"]
                all_zones.append(name)
        return all_zones
