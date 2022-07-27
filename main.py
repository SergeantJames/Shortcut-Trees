# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:09:25 2022

@author: nasmy
"""

import graphs
import binaryTrees
import shortcutTrees


def generateAllShortcutTrees(n):
    shortcut_numbers = []
    
    trees = binaryTrees.binTrees(n-1)
    
    for tree in trees:
        graph = graphs.generateEmptyGraph(n)
        empty_graph = graphs.generateEmptyGraph(n)
        
        graphs.increment_matrix(graph)
        while graph != empty_graph:
            sct = shortcutTrees.ShortcutTree(graph, tree)
            shortcut_numbers.append(sct.shortcut_number())
    return shortcut_numbers            