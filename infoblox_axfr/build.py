default_allowed_types = [
    "A",
    "SRV",
    "CNAME",
    "TXT",
    "PTR",
]
class Build(object):
    def __init__(self, cmd_output, allowed_types = None):
        if allowed_types is None:
            self.allowed_types = default_allowed_types
        self.lines = cmd_output.split('\n')

    def run(self):
        matched_records = []
        for line in self.lines:
            r_split = line.strip().split()
            try:
                r_type = r_split[3]
            except IndexError:
                continue
            if r_type in self.allowed_types:
                matched_records.append('\t'.join(r_split))
        return matched_records
