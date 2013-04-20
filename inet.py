#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
# 
#
# UPDATED ON
# 2012: 11/17, 
# 2013: 
#
"""
Utility functions for manipulating Internet data.


"""

from struct import pack, unpack
from socket import inet_aton, inet_ntoa

HOSTNAME_ALLOWED_CHARS = re.compile("(?!-)[a-zA-Z\d-]{1,63}(?<!-)$")


def inet_atoi (ip):
    """
    Converts a 'xxx.xxx.xxx.xxx' IPv4 string to a 32-bit integer.
    """
    return unpack('!I', inet_aton(ip))[0]

    
def inet_itoa (ipint):
    """
    Converts a 32-bit integer IPv4 address to its 4-quad string form.
    """
    return inet_ntoa(pack('!I', ipint))


def hostname_valid (hostname):
    """
    Determines if a hostname is syntactically valid (without DNS resolution).

    http://stackoverflow.com/questions/2532053/validate-hostname-string-in-python
    'Any domain name is syntactically valid if it's a dot-separated list of
    identifiers, each no longer than 63 characters, and made up of letters,
    digits and dashes (no underscores?).'

    """
    if len(hostname) > 255:
        return False
    if hostname[-1:] == '.':  # strip the trailing dot
        hostname = hostname[:-1]
    return all(HOSTNAME_ALLOWED_CHARS.match(s) for s in hostname.split('.'))


