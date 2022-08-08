# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 11:09:25 2022

@author: nasmy
"""

import graphs
import binaryTrees
from shortcutTrees import ShortcutTree
import twinWidthSATSolver as tww
import copy


def run(n, immediate_return = True):
    counter_examples = []
    trees = binaryTrees.binTrees(n-1)
    
    for tree in trees:
        graph = graphs.generateEmptyGraph(n)
        empty_graph = graphs.generateEmptyGraph(n)
        
        sct = ShortcutTree(tree)
        sct.write_graph_on_tree(graph)
        graphs.increment_matrix(graph)
        width = tww.twin_width(graph)
        if (2*width + 1)*(n-1) > sct.shortcut_number():
            if immediate_return:
                return [tree, graph]
            counter_examples.append([tree, copy.deepcopy(graph)])
        
        while graph != empty_graph:
            sct = ShortcutTree(tree)
            sct.write_graph_on_tree(graph)
            graphs.increment_matrix(graph)
            width = tww.twin_width(graph)
            if (2*width + 1)*(n-1) > sct.shortcut_number():
                if immediate_return:
                    return  [tree, graph]
                counter_examples.append([tree, copy.deepcopy(graph)])
    return counter_examples


def find_counter_tree(graph):
    """Given a graph, tries to find a tree which gives a counter-example"""
    n = len(graph)
    width = tww.twin_width(graph)
    trees = binaryTrees.binTrees(n-1)
    for tree in trees:
        sct = ShortcutTree(tree)
        sct.write_graph_on_tree(graph)
        if (2*width + 1)*(n-1) > sct.shortcut_number():
            return tree
    print("No counter-example found")
    return