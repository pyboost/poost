#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CONTRIBUTORS (sorted by surname)
# LUO, Pengkui <pengkui.luo@gmail.com>
#
#
# UPDATED ON
# 2013: 04/20, 04/21,
#
"""
Unit tests for containers.py

"""
import unittest

import poost


class Test_TurboList (unittest.TestCase):

    def setUp (self):
        self.sequence = [3, 1, -2, 'abc', tuple()]
        self.turbolist = poost.TurboList(self.sequence)

    def test_islist (self):
        self.assertIsInstance(self.turbolist, list)

    def test__contains__ (self):
        turbolist = self.turbolist
        self.assertTrue(-2 in turbolist)
        self.assertTrue('abc' in turbolist)

    def test__len__ (self):
        self.assertTrue(len(self.turbolist)==5)

    def test__getitem__ (self):
        turbolist = self.turbolist
        self.assertEqual(turbolist[1], 1)
        self.assertListEqual(turbolist[2:4], [-2, 'abc'])
        self.assertListEqual(turbolist[:], self.sequence)
        self.assertListEqual(turbolist, self.sequence)

    def test_index (self):
        turbolist = self.turbolist
        self.assertEqual(turbolist.index(3), 0)
        self.assertEqual(turbolist.index('abc'), 3)
        self.assertEqual(turbolist.index(tuple()), 4)

    def test_append (self):
        turbolist = self.turbolist
        turbolist.append(None)
        self.assertListEqual(turbolist, self.sequence+[None])
        self.assertListEqual(turbolist[:], self.sequence+[None])

    def test_remove_1 (self):
        turbolist = self.turbolist
        turbolist.remove('abc')
        self.assertListEqual(turbolist, [3, 1, -2, tuple()])
        indices = sorted(turbolist._indices.values())
        self.assertListEqual(indices, range(4))

    def test_remove_2 (self):
        turbolist = self.turbolist
        turbolist.remove(3)
        turbolist.remove(tuple())
        self.assertListEqual(turbolist, [1, -2, 'abc'])
        indices = sorted(turbolist._indices.values())
        self.assertListEqual(indices, range(3))


class Test_Clusters (unittest.TestCase):

    def setUp (self):
        objects = poost.TurboList ([-9, 'a', (1,2), 222])
        self.clusters = poost.Clusters (objects)

    def test__init__ (self):
        clusters = self.clusters
        self.assertEqual(len(clusters), 0)
        self.assertEqual(len(clusters.cids), 4)

    def test_merge_1 (self):

        #objects = poost.TurboList ([-9, 'a', (1,2), 222])
        clusters = self.clusters
        clusters.merge(-9, (1,2))
        self.assertListEqual(clusters.cids, [0, None, 0, None])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, (1,2)]))
        self.assertListEqual(clusters.unclustered_objs, ['a', 222])

        clusters.merge('a', (1,2))
        self.assertListEqual(clusters.cids, [0, 0, 0, None])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, 'a', (1,2)]))
        self.assertListEqual(clusters.unclustered_objs, [222])

        clusters.merge('a', 222)
        self.assertListEqual(clusters.cids, [0, 0, 0, 0])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[0], set([-9, 'a', (1,2), 222]))
        self.assertListEqual(clusters.unclustered_objs, [])

    def test_merge_2 (self):

        #objects = poost.TurboList ([-9, 'a', (1,2), 222])
        clusters = self.clusters
        clusters.merge(-9, (1,2))
        self.assertListEqual(clusters.cids, [0, None, 0, None])
        self.assertListEqual(clusters.unclustered_objs, ['a', 222])

        clusters.merge('a', 222)
        self.assertListEqual(clusters.cids, [0, 1, 0, 1])
        self.assertEqual(len(clusters), 2)
        self.assertSetEqual(clusters[0], set([-9, (1,2)]))
        self.assertSetEqual(clusters[1], set(['a', 222]))
        self.assertListEqual(clusters.unclustered_objs, [])

        clusters.merge('a', (1,2))
        self.assertListEqual(clusters.cids, [1, 1, 1, 1])
        self.assertEqual(len(clusters), 1)
        self.assertSetEqual(clusters[1], set([-9, 'a', (1,2), 222]))
        self.assertListEqual(clusters.unclustered_objs, [])


class Test_LengthAscendingStrings (unittest.TestCase):

    def setUp (self):
        self.lass = poost.LengthAscendingStrings(['abc', 'bcd', 'a', 'abcd'])
        self.reordered = ['a', 'bcd', 'abc', 'abcd']

    def test__init__ (self):
        self.assertListEqual(self.lass, self.reordered)
        # Note: assertDictEqual does not differentiate dict and OrderedDict
        self.assertDictEqual(self.lass.lenbounds, {1:(0,1), 3:(1,3), 4:(3,4)})
        self.assertDictEqual(self.lass.lenbounds, {3:(1,3), 1:(0,1), 4:(3,4)})

    def test_isinstance (self):
        self.assertIsInstance(self.lass, poost.LengthAscendingStrings)
        self.assertIsInstance(self.lass, poost.TurboList)
        self.assertIsInstance(self.lass, list)

    def test__contains__ (self):
        self.assertTrue('abc' in self.lass)
        self.assertTrue('a' in self.lass)

    def test__len__ (self):
        self.assertTrue(len(self.lass)==4)

    def test__getitem__ (self):
        self.assertTrue(self.lass[3]=='abcd')
        self.assertListEqual(self.lass[:], self.reordered)
        self.assertListEqual(self.lass, self.reordered)
        self.assertListEqual(self.lass[1:2], ['bcd'])


if __name__ == '__main__':
    unittest.main()
