def is_reverse_zone_name(input_name):
    retval = False
    if '/' in input_name:
        retval = True
    return retval

def reverse_name(input_name):
    if not is_reverse_zone_name(input_name):
        return input_name
    f_name_only = input_name.split("/")[0]
    f_name_split = f_name_only.split(".")
    f_name_split.reverse()
    final_name = ".".join(f_name_split[1:])
    final_name = "{}.in-addr.arpa".format(final_name)
    return final_name