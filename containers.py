#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
#
#
# UPDATED ON
# 2013: 04/20,
#
"""
More fancy or complex container types.

"""
__all__ = [
    'SetList',
]

from collections import OrderedDict


class SetList (list):
    """ A subclass of type list, but support set-like fast lookup and removals.

        Main usage:
        1. Testing whether 'x in setlist';
        2. Iterating over elements;
        3. Removing an element from setlist.

        Note: only sequences with non-repeating elements are accepted.

    """
    def __init__ (self, sequence=[], **kwargs):
        """ Constructs a SetList instance.

        """
        # Built-in types (e.g. list) are new-style classes, supporting 'super'.
        # http://rhettinger.wordpress.com/2011/05/26/super-considered-super/
        #super(SetList, self).__init__(sequence)
        list.__init__(self, sequence)
        self._set = set(sequence)
        assert len(self._set) == len(self)

    def __contains__ (self, x):
        """ Returns True if x in this setlist
        """
        return x in self._set

    def append (self, x, doublecheck=False):
        """ Appends an element to this setlist.
            Double check consistency if doublecheck==True.
        """
        list.append(self, x)
        self._set.add(x)
        if doublecheck:
            assert len(self._set) == len(self)

    def remove (self, x, pos=None, doublecheck=False):
        """ Removes an element from this setlist.
            Double check consistency if doublecheck==True.
        """
        self._set.remove(x)
        # Find the correct position in the list.
        if pos is None:
            pos = self.index(x)
        # If needed, double-check the provided position is correct.
        elif doublecheck:
            assert pos == self.index(x)
        del self[pos]
        # Double-check non-repeating after removal
        if doublecheck:
            assert len(self._set) == len(self)


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
