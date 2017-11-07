import subprocess


class ReloadNamed(object):

    def __init__(self, cmd="system anmed restart"):
        self.cmd = cmd

    def run(self):
        cmd = [
            self.cmd,
        ]
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, errors = p.communicate()
        return p.returncode, output
