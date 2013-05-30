#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
#
#
# UPDATED ON
# 2013: 04/20, 04/21, 5/30
#
"""
Named dict.

"""
__all__ = [
    'NamedDict',
]

from collections import OrderedDict

class NamedDict (OrderedDict):
    """ NamedDict
    """
    def __init__(self, attribute=None, **kwargs):
        indict = kwargs.items()
        self.attribute = attribute
        OrderedDict.__init__(self, indict)
        self.__initialised = True

    def __getattr__(self, item):
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        if not self.__dict__.has_key('_NamedDict__initialised'):
            return OrderedDict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):
            OrderedDict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __delattr__(self, item):
        if self.__dict__.has_key(item):
            OrderedDict.__delattr__(self, item)
        else:
            self.__delitem__(item)
