#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# test_lpb_comb.py

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

from lpb_comb import *


def test_op_cmp():
    # all occurrence patterns tests are taken from from Smaus' first publication
    # http://www.informatik.uni-freiburg.de/~ki/papers/smaus-tr230.pdf
    o1 = OccurrencePattern(0, [2, 2, 2, 2])
    o2 = OccurrencePattern(1, [2, 2, 2])
    o3 = OccurrencePattern(2, [2, 3, 3])
    o4 = OccurrencePattern(3, [2, 3])

    assert o1 > o2
    assert o1 > o3
    assert o1 > o4

    assert o2 < o1
    assert o3 < o1

    assert o2 > o3
    assert o2 > o4

    assert o3 > o4

    assert o1 != o2
    assert o2 != o3
    assert o3 != o4

    assert o1 == o1
    assert o2 == o2
    assert o3 == o3
    assert o4 == o4


def test_variable_setting():
    dnf = [[0], [1, 2], [1, 3, 4]]
    vs = VariableSetting(dnf)
    assert len(vs.occurrences) == 5
    assert vs.variablePos[:3] == [0, 1, 2]

    assert(vs.occurrences[0].variable) == 0
    assert(vs.occurrences[1].variable) == 1
    assert(vs.occurrences[2].variable) == 2
