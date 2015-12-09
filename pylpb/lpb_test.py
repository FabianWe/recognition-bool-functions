#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lpb_test.py

# Copyright (C) 2015 Fabian Wenzelmann
#
# This file is part of recognition-bool-functions.
#
# recognition-bool-functions is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# recognition-bool-functions is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with recognition-bool-functions.
# If not, see <http://www.gnu.org/licenses/>.
#

from lpb import *

def test_eq_one():
    l1 = LPB(1, 5, 4, 3, 2)
    l2 = LPB(1, 5, 4, 3, 2)
    assert l1 == l2


def test_eq_two():
    l1 = LPB(1, 3, 2, 1)
    l2 = LPB(1, 3, 2)
    assert not l1 == l2


def test_ne_one():
    l1 = LPB(1, 5, 4, 3, 2)
    l2 = LPB(1, 5, 4, 3, 2)
    assert not l1 != l2


def test_ne_two():
    l1 = LPB(1, 3, 2, 1)
    l2 = LPB(1, 3, 2)
    assert l1 != l2


def test_parse_lpb_one():
    l = parse_lpb('3 2 5')
    assert l == LPB(5, 3, 2)


def test_parse_lpb_two():
    l = parse_lpb('6 10 2 4 1 2 55 2')
    assert l == LPB(2, 6, 10, 2, 4, 1, 2, 55)


def test_len_one():
    l = LPB(1, 2, 3, 4)
    assert len(l) == 3


def test_len_two():
    l = LPB(1, 2, 3, 4, 5, 6, 7)
    assert len(l) == 6


def test_dnf_to_set_one():
    assert dnf_to_set([]) == set()


def test_dnf_to_set_two():
    assert dnf_to_set([[]]) == set([frozenset()])


def test_dnf_to_set_three():
    dnf = [[0, 1], [1, 2, 3], [4, 5]]
    assert dnf_to_set(dnf) == set([frozenset([0, 1]), frozenset([1, 2, 3]),
                                frozenset([4, 5])])


def test_lpb_to_dnf_one():
    l = LPB(0, 3, 2, 1)
    assert l.toDNF() == [[]]


def test_lpb_to_dnf_two():
    l = LPB(3, 3, 2, 1)
    assert l.toDNF() == [[0], [1, 2]]


def test_lpb_to_dnf_three():
    l = LPB(8, 5, 3, 3, 2, 1)
    result = dnf_to_set(l.toDNF())
    expected = { frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 3, 4}), frozenset({1, 2, 3}) }
    assert result == expected


def test_lpb_to_dnf_four():
    l = LPB(15, 9, 7, 6, 4, 4, 1)
    expected = { frozenset({0, 1}), frozenset({0, 2}), frozenset({0, 3, 4}), frozenset({1, 2, 3}),
                frozenset({1, 2, 4}), frozenset({1, 3, 4}), frozenset({2, 3, 4, 5})}
    result = dnf_to_set(l.toDNF())
    assert result == expected
