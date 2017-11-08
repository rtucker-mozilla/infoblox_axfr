import ConfigParser
import os


class Config(object):

    def __init__(self, config_path=None):
        self.config_path = config_path

    def get_config(self):
        config = ConfigParser.RawConfigParser()
        if self.config_path is None:
            config_path = 'infoblox_axfr.cfg'
        else:
            config_path = self.config_path
        paths = [
            os.path.join(os.path.dirname(__file__), config_path),
            os.path.join('/usr/local/bin', config_path),
            os.path.join(os.path.dirname(__file__), '../' + config_path),
        ]
        config_found = False
        for path in paths:
            if os.path.exists(path):
                config_path = path
                config_found = True
                continue

        config_path = os.path.join(os.path.dirname(__file__), config_path)
        if not config_found:
            print "No Config File Found"
            return None

        config.read(config_path)
        return config

    def config_valid(self, config):
        try:
            config.get('InfoBlox', 'HostName')
            config.get('InfoBlox', 'UserName')
            config.get('InfoBlox', 'Password')
            config.get('InfoBlox', 'Zone')
            config.get('Global', 'StopUpdate')
        except ConfigParser.NoOptionError, e:
            return False, str(e)
        return config, ''
