import ConfigParser
import os


def get_config(config_path=None):
    config = ConfigParser.RawConfigParser()
    if config_path is None:
        config_path = 'infoblox_axfr.cfg'
    paths = [
        os.path.join(os.path.dirname(__file__), config_path),
        os.path.join('/usr/local/bin', config_path),
        os.path.join(os.path.dirname(__file__), '../' + config_path),
    ]
    print paths
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

def config_valid(config):
    try:
        config.get('InfoBlox', 'HostName')
        config.get('InfoBlox', 'UserName')
        config.get('InfoBlox', 'Password')
        config.get('InfoBlox', 'Zone')
    except ConfigParser.NoOptionError, e:
        return False, str(e)
    return config, ''
    # config.get('InfoBlox', 'Hostname')
