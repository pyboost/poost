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


if __name__ == '__main__':
    unittest.main()
