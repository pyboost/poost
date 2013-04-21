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
    'NamedDict',
    'TurboList',
    'Clusters',
    'LengthAscendingStrings',
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

    def remove (self, x, check_consistency=True, **kwargs):
        """ Removes an element from this setlist (overriding 'list.remove')
        """
        pos = self._indices[x]
        del self[pos]
        del self._indices[x]
        self._rebuild_indices(pos)
        if check_consistency:
            assert self._isconsistent()


class Clusters (dict):
    """ Container for storing clustering info for a TurboList object.

        Main data structor: subclassed from dict,
        mapping a cluster id [int] to an (initially empty) set of objects.

        Usage:
        ------
        len(self): returns the number of formed clusters, initially 0.

        Other properties:
        -----------------
        'objs': [TurboList instance]
        'cids': [list] of cluster ids, initially all None.
        'unclustered_objs': [TurboList instance] not-yet-clustered objects.

    """

    def __init__ (self, objects, **kwargs):
        """ Constructor. Take a TurboList object as input.
        """
        assert isinstance(objects, TurboList)
        dict.__init__(self, {})
        self.objs = objects
        self.cids = [None for _ in xrange(len(self.objs))]
        self.unclustered_objs = TurboList(objects)

    def merge (self, obj1, obj2, *args):
        """  Merges belonging clusters of objects obj1, obj2, ... into one.
        """
        # Turbolist positions
        i1 = self.objs.index(obj1)
        i2 = self.objs.index(obj2)
        # Cluster IDs
        cid1 = self.cids[i1]
        cid2 = self.cids[i2]

        # Case 1: neither obj1 nor obj2 has been clustered yet.
        if (cid1 is None) and (cid2 is None):
            cid0 = 1 + max([-1]+self.keys())  # in case len(self)==0
            self[cid0] = set([obj1, obj2])
            self.cids[i1] = self.cids[i2] = cid0
            self.unclustered_objs.remove(obj1)
            self.unclustered_objs.remove(obj2)

        # Case 2: obj1 was clustered into c1, but obj2 has not been clustered yet.
        elif (cid1 is not None) and (cid2 is None):
            self[cid1].add(obj2)
            self.cids[i2] = cid1
            self.unclustered_objs.remove(obj2)

        # Case 3: s2 was clustered into c2, but s1 has not been clustered yet.
        elif (cid1 is None) and (cid2 is not None):
            self[cid2].add(obj1)
            self.cids[i1] = cid2
            self.unclustered_objs.remove(obj1)

        # Case 4: both obj1 and obj2 have been clustered -> merge 2 clusters
        elif cid1 != cid2:
            cid0 = max(cid1, cid2)
            set0 = self[cid1].union(self[cid2])
            del self[cid1]
            del self[cid2]
            self[cid0] = set0
            for obj in set0:
                i = self.objs.index(obj)
                self.cids[i] = cid0


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

