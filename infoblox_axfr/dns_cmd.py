import subprocess


class CMD(object):

    def __init__(self, zone, server):
        self.zone = zone
        self.server = server

    def run(self):
        dig_list = [
            "dig",
            "AXFR",
            self.zone,
            "@" + self.server
        ]
        p = subprocess.Popen(
            dig_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return p.communicate()
