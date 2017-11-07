import subprocess


class CheckZone(object):

    def __init__(self, zonefile, zone, cmd="named-checkzone"):
        self.cmd = cmd
        self.zone= zone
        self.zonefile = zonefile

    def run(self):
        cmd = [
            self.cmd,
            self.zone,
            self.zonefile,
        ]
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, errors = p.communicate()
        return p.returncode, output
