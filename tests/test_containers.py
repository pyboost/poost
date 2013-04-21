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
Unit tests for containers.py

"""
import unittest

import poost


class Test_SetList (unittest.TestCase):

    def setUp (self):
        self.sequence = [3, 1, 2, 'abc', tuple()]
        self.setlist = poost.SetList(self.sequence)

    def test_islist (self):
        self.assertIsInstance(self.setlist, list)

    def test__contains__ (self):
        setlist = self.setlist
        self.assertTrue(2 in setlist)
        self.assertTrue('abc' in setlist)

    def test__len__ (self):
        self.assertTrue(len(self.setlist)==5)

    def test__getitem__ (self):
        setlist = self.setlist
        self.assertEqual(setlist[1], 1)
        self.assertListEqual(setlist[2:4], [2, 'abc'])
        self.assertListEqual(setlist[:], self.sequence)
        self.assertListEqual(setlist, self.sequence)

    def test_append (self):
        setlist = self.setlist
        setlist.append(None, doublecheck=True)
        self.assertListEqual(setlist, self.sequence+[None])
        self.assertListEqual(setlist[:], self.sequence+[None])

    def test_remove_1 (self):
        setlist = self.setlist
        setlist.remove('abc')
        self.assertListEqual(setlist, [3, 1, 2, tuple()])
        self.assertSetEqual(setlist._set, set([3, 1, 2, tuple()]))

    def test_remove_2 (self):
        setlist = self.setlist
        setlist.remove('abc', pos=3)
        self.assertListEqual(setlist, [3, 1, 2, tuple()])
        self.assertSetEqual(setlist._set, set([3, 1, 2, tuple()]))

    def test_remove_3 (self):
        setlist = self.setlist
        setlist.remove('abc', pos=3, doublecheck=True)
        self.assertListEqual(setlist, [3, 1, 2, tuple()])
        self.assertSetEqual(setlist._set, set([3, 1, 2, tuple()]))


if __name__ == '__main__':
    unittest.main()
