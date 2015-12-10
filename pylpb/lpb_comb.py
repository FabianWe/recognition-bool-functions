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
This module provides a method for the combinatorial by Jan-Georg Smaus,
which is now proven to be incomplete.
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


class TreeContext(object):

    """
    Stores some global information about a splittint tree.

    Attributes:
        variableCount (int): The number of variables in the original dnf.
        tree (list of list of SplittingTreeNode): For each column in the table
            stores a list of nodes in it.
    """

    def __init__(self, variableCount):
        """
        Creates a new tree context.

        Args:
            variableCount (int): The number of variables in the original dnf.
        """
        self.variableCount = variableCount
        self.tree = [[] for _ in range(variableCount + 1)]

    def addNode(self, node):
        """
        Add a splitting tree node to this tree context.

        The column of the node is determined through the node. The node is
        added to the end of this column.

        Args:
            node (SplittingTreeNode): The node that will be added to the tree.
        Returns:
            The position in the column, i.e. the row (int).
        """
        c = self.tree[node.column]
        c.append(node)
        return len(c) - 1

    def __len__(self):
        return len(self.tree)


class SplittingTreeNode(object):

    """
    Superclass for all nodes in a splitting tree.

    Such a node always consists of a DNF and child / parent nodes in the tree.

    Attributes:
        lowerChild (SplittingTreeNode): The lower child in the tree.
        upperChild (SplittingTreeNode): The upper child in the tree.
        lowerParent (SplittingTreeNode): The lower parent in the tree.
        upperParent (SplittingTreeNode): The upper parent in the tree.
        dnf (DNF): The dnf saved in the node
        column (int): The column in the tree.
        row (int): The row in the tree.
        occurrencePatterns (list of OccurrencePattern): The patterns for the
            dnf
        context (TreeContext): The tree conext that gives us some information
            about the tree this node is used in.
        alreadySplit (bool): If the nodes link method has already been called
            this value is set to True.
    Abstract methods:
        split(vs (VariableSetting), symmetryTest (bool)):
            This abstract method is used to create the successors of this node.

            The variable that is split away is the first variable in the
            occurrence pattern array.

            If this method has been called the two child nodes should not be
            null (the split method must created them).

            This method is only called on nodes if there are still some
            variables to split away (i. e. the occurrence patterns in this
            nodes are not empty).

            If there is no variable to split away the behavior is not
            specified.

            A call of this method sets the value of alreadySplit to True.
        isFinal(): This method should return True if this node is a final node
            and False otherwise
    """

    def __init__(self, dnf, occurrencePatterns, context,
                 lowerParent=None, upperParent=None):
        self.lowerChild = None
        self.upperChild = None
        self.lowerParent = lowerParent
        self.upperParent = upperParent
        self.dnf = dnf
        self.occurrencePatterns = occurrencePatterns
        self.context = context
        self.alreadySplit = False
        if lowerParent is not None:
            self.column = lowerParent.column + 1
        elif upperParent is not None:
            self.column = upperParent.column + 1
        else:
            self.column = 0
        if context is not None:
            # TODO can this happen???
            self.row = context.addNode(self)
        else:
            self.row = None


class MainNode(SplittingTreeNode):

    """
    Subclass for the main nodes as defined by Smaus.

    Attributes:
        maxL (int): The maximal l value such that the first i occurrence
            patterns are equal.
        isFinal (bool): Value is set to True if this is a final main node (i.e.
            True if its DNF is true or false).
    """

    def __init__(self, dnf, occurrencePatterns, context):
        super(MainNode, self).__init__(dnf, occurrencePatterns, context)
        self.isFinal = self._calcIsFinal()
        self.maxL = None

    def _calcIsFinal(self):
        """
        Return True if this node is final, i.e. the DNF is true or false.
        """
        if not len(self.dnf):
            return True
        elif len(self.dnf) == 1:
            clause = dnf[0]
            if not len(clause):
                return True
        return False
