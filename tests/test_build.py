import context #  NOQA
import hashlib
import time
import os
import pytest
import ConfigParser
from infoblox_axfr.build import Build



def test_type_matching_ptr():
    lines = """1.0.0.127.in-addr.arpa.    60    IN    PTR    host1.domain.com\n
2.0.0.127.in-addr.arpa.    60    IN    PTR    host2.domain.com\n
3.0.0.127.in-addr.arpa.    60    IN    PTR    host2.domain.com\n
"""

    allowed_types = ['PTR']
    b = Build(lines, allowed_types)
    records = b.run()
    assert len(records) == 3

def test_type_matching_forward_default_types():
    lines = """host1.domain.com.    60    IN    A    127.0.0.1\n
host2.domain.com.    60    IN    A    127.0.0.2\n
host2.domain.com.    60    IN    TXT    the content here is open ended\n
host2.domain.com.    60    IN    CNAME    host1.domain.com\n
"""

    b = Build(lines)
    records = b.run()
    assert len(records) == 4
