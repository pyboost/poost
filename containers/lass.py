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

"""
__all__ = ['LengthAscendingStrings']

from collections import OrderedDict

from turbolist import TurboList


class LengthAscendingStrings (TurboList):
    """ A container for non-repeating length-ascending strings,
        subclassed from poost.TurboList.

        Properties
        ----------
        'lenbounds': [OrderedDict]
            Mapping length to a [lo,hi) index tuple, where the length of string
            of the i-th position can be obtained via len(self).
    """

    def __init__ (self, strings):
        """ Constructor.
        """
        assert all(isinstance(s, str) for s in strings)
        strlist = list(set(strings))  # To ensure no repeating strings
        strlist.sort(key=len)  # enforce ascending lengths
        TurboList.__init__(self, strlist)

        # Build lenbounds
        self.lenbounds = OrderedDict()
        len2lo = OrderedDict()  # mapping length to lower bound
        for lo, s in enumerate(self):
            k = len(s)
            if k not in len2lo:
                len2lo[k] = lo
        # Fill the upper bound also
        for len_lo, hi in zip(len2lo.items(), len2lo.values()[1:]+[len(self)]):
            length, lo = len_lo
            self.lenbounds[length] = (lo, hi)

