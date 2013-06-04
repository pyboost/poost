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

__all__ = ['TurboList']


class TurboList (list):
    """ A subclass of type 'list', supporting:
        1. Efficient membership test 'x in setlist';
        2. Efficient index lookup 'setlist.index(x)';
        3. (Arguably) efficient element removal 'setlist.remove(x)'.

        These are achieved by maintaining a '_indices' dict that maps elements
        back to list indices.

        Limitation: repeating elements are not allowed.
    """

    def __init__ (self, sequence=[], **kwargs):
        """ Constructs a TurboList instance.

        """
        # Built-in types (e.g. list) are new-style classes, supporting 'super'.
        # http://rhettinger.wordpress.com/2011/05/26/super-considered-super/
        #super(SetList, self).__init__(sequence)
        list.__init__(self, sequence)
        self._indices = None
        self._rebuild_indices()
        assert self._isconsistent()

    def __contains__ (self, x):
        """ Returns True if x in this setlist
        """
        return x in self._indices

    def _isconsistent (self):
        """ Consistent if no repeating elements.
        """
        return len(self) == len(self._indices)

    def _rebuild_indices (self, pos=None):
        """ Rebuilds self._indices from the pos-th element.
        """
        if pos is None:
            self._indices = dict((x, i) for i, x in enumerate(self))
        else:
            for i, x in enumerate(self[pos:]):
                self._indices[x] = i + pos

    def index (self, x):
        """ Finds the index of element x in self (overriding 'list.index')
        """
        return self._indices[x]

    def append (self, x, check_consistency=True, **kwargs):
        """ Appends an element to this setlist (overriding 'list.append').
        """
        list.append(self, x)
        self._indices[x] = len(self) - 1
        if check_consistency:
            assert self._isconsistent()

    def insert (self, pos, x, check_consistency=True):
        """ Insert element x before index pos.
        """
        list.insert(self, pos, x)
        self._rebuild_indices(pos)
        if check_consistency:
            assert self._isconsistent()

    def remove (self, x, check_consistency=True, **kwargs):
        """ Removes an element from this setlist (overriding 'list.remove')
        """
        pos = self._indices[x]
        del self[pos]
        del self._indices[x]
        self._rebuild_indices(pos)
        if check_consistency:
            assert self._isconsistent()
