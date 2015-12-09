#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lpb_comb.py

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

"""
This module provides a method for the combinatorial by Jan-Georg Smaus, which
is now proven to be incomplete.
"""

class OccurrencePattern(object):
    """
    Class for occurrence patterns.


    For the definition of occurrence patterns see
    http://www.informatik.uni-freiburg.de/~ki/papers/smaus-tr230.pdf

    An occurrence pattern in C++ is just an ordered list
    of integers.
    """

    def __init__(self, variable, occurrences=None):
        self.variable = variable
        if occurrences is None:
            occurrences = []
        self.occurrences = occurrences.copy()


    def sort(self):
        self.occurrences.sort()

    def __getitem__(self, key):
        return self.occurrences[key]


    def __iter__(self):
        return iter(self.occurrences)


    def __len__(self):
        return len(self.occurrences)

    def append(self, obj):
        self.occurrences.append(obj)


    def compare(self, other):
        for ((i, v1), (j, v2)) in zip(enumerate(self), enumerate(other)):
            if v2 < v1:
                return -1
            elif v1 < v2:
                return 1
        if i + 1 < len(self):
            return 1
        elif j + 1 < len(other):
            return -1
        else:
            return 0


    def __eq__(self, other):
        if not isinstance(other, OccurrencePattern):
            return False
        return self.occurrences == other.occurrences


    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.compare(other) < 0


    def __le__(self, other):
        return self.compare(other) <= 0


    def __gt__(self, other):
        return self.compare(other) > 0


    def __ge__(self, other):
        return self.compare(other) >= 0


class VariableSetting(object):
    def __init__(self, dnf, variables=None):
        if variables is None:
            variables = variable_count(dnf)
        self.occurrences = []
        self.variablePos = []
        for i in range(variables):
            self.occurrences.append(OccurrencePattern(i))
            self.variablePos.append(-1)
        for c in dnf:
            clauseSize = len(c)
            for x in c:
                self.occurrences[x].append(clauseSize)
        # sort each occurrence pattern
        for op in self.occurrences:
            op.sort()
        # sort the occurrence pattern according the "importance order"
        self.occurrences.sort(reverse=True)
        # save for each variable id the position in the ordering
        for i, op in enumerate(self.occurrences):
            self.variablePos[op.variable] = i
