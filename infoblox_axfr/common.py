import os


class Common(object):
    @classmethod
    def is_reverse_zone_name(self, input_name):
        retval = False
        if '/' in input_name:
            retval = True
        return retval

    @classmethod
    def reverse_name(self, input_name):
        if not Common.is_reverse_zone_name(input_name):
            return input_name
        f_name_only = input_name.split("/")[0]
        f_name_split = f_name_only.split(".")
        f_name_split.reverse()
        final_name = ".".join(f_name_split[1:])
        final_name = "{}.in-addr.arpa".format(final_name)
        return final_name

    @classmethod
    def get_local_zones(self, zone_path):
        return os.listdir(zone_path)

    @classmethod
    def get_zones_to_remove(self, l_all_local_zonefiles, l_all_zone_names):
        to_remove = []
        for l_f in l_all_local_zonefiles:
            if l_f not in l_all_zone_names:
                to_remove.append(l_f)
        return to_remove

    @classmethod
    def touch(self, fname):
        if os.path.exists(fname):
            os.utime(fname, None)
        else:
            open(fname, 'a').close()

    @classmethod
    def write_stop_update(self, fname, message):
        fh = open(fname, 'w')
        fh.write(message)
        fh.close()

