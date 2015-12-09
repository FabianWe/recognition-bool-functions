#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# lpb.py

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

class LPB(object):
    """
    Class representing an LPB a1 * l1 + ... + an * ln >= d.

    Note that we start the variable numeration with 0.

    Attributes:
        d (number): The threshold of the LPB
        coefficients (list or tuple of number): The coefficients of the LPB
    """
    def __init__(self, d, *args, _type=None):
        """
        Creates a new LPB given the threshold and the coefficients
        in args.

        Args:
            d (number): The threshold of the LPB
            args (tuple of number): The coefficients of the LPB
            _type (type): The container type for the coefficients, should
                be list or tuple, default is tuple
        """
        if _type is None:
            _type = tuple
        self.d = d
        self.coefficients = _type(args)


    def __repr__(self):
        l = ['%d * x%d' % (a, i) for (i, a) in enumerate(self.coefficients)]
        s = ' + '.join(l)
        s += ' >= %d' % self.d
        return s


    def toDNF(self):
        # TODO doc and test me... why do I even work?
        n = len(self)
        if not n and self.d > 0:
            # never true
            return []
        if self.d <= 0:
            # always false because coefficients must be >= 0
            return [[]]
        dnf = []
        clause_sets = []
        for _ in self.coefficients:
            t = ([], 0)
            ci = [t]
            clause_sets.append(ci)
        for i, a in enumerate(self.coefficients):
            for t in clause_sets[i]:
                if a + t[1] >= self.d:
                    t[0].append(i)
                    dnf.append(t[0])
                else:
                    for j in range(i + 1, len(self)):
                        cPrime = t[0].copy()
                        cPrime.append(i)
                        newT = (cPrime, t[1] + a)
                        clause_sets[j].append(newT)
        return dnf



    def __eq__(self, other):
        return self.d == other.d and self.coefficients == other.coefficients


    def __ne__(self, other):
        return not self == other


    def __len__(self):
        return len(self.coefficients)


def parse_lpb(s, _type=None, number_type=None):
    """
    Parse an LPB given a string.

    Args:
        s (string): The single line presentation of an LPB
        _type (type): The container type for the coefficients, should
            be list or tuple, default is tuple
        number_type (type): The number type, should be int or float, default is
            int
    Raises:
        ValueError: If the string does not contain a single number or one of
            the elements is not a number.
    The input format for the LPB a1 * l1 + ... + an * ln >= d is
    a1 a2 ... an d
    For example the input for the LPB 3x1 + 2x2 >= 5 is
    3 2 5
    """
    if number_type is None:
        number_type = int
    s = s.strip()
    l = []
    for c in s.split(' '):
        if not c:
            continue
        l.append(number_type(c))
    if not l:
        raise ValueError('Input for LPB is empty.')
    return LPB(l[-1], *l[:-1], _type=_type)


def dnf_to_set(dnf):
    return set(frozenset(clause) for clause in dnf)
