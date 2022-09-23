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
        width = tww.twin_width(graph)
        if (2*width + 1)*(n-1) > sct.shortcut_number():
            if immediate_return:
                return [tree, graph]
            counter_examples.append([tree, copy.deepcopy(graph)])
        graphs.increment_matrix(graph)
        
        while graph != empty_graph:
            sct = ShortcutTree(tree)
            sct.write_graph_on_tree(graph)
            width = tww.twin_width(graph)
            if (2*width + 1)*(n-1) > sct.shortcut_number():
                if immediate_return:
                    return  [tree, graph]
                counter_examples.append([tree, copy.deepcopy(graph)])
            graphs.increment_matrix(graph)
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
    #print("No counter-example found")
    return


def find_counter_graph(tree, min_edges = 0):
    "Given a tree, tries to find a graph which produces a counter example"
    n = len(tree) + 1
    graph = graphs.generateEmptyGraph(n)
    sct = ShortcutTree(tree)
    sct.write_graph_on_tree(graph)
    if sct.shortcut_number() < n-1:
        return graph
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*n]*n:
        sct.write_graph_on_tree(graph)
        width = tww.twin_width(graph)
        if (2*width + 1)*(n-1) > sct.shortcut_number() and graphs.num_edges(graph) >= min_edges:
            return graph
        graphs.increment_matrix(graph)
    return


# naming functions is hard
def run2(n, leeway=0, immediate_return = True):
    counter_examples = []
    trees = binaryTrees.binTrees(n-1)
    
    for tree in trees:
        graph = graphs.generateEmptyGraph(n)
        empty_graph = graphs.generateEmptyGraph(n)
        
        sct = ShortcutTree(tree)
        sct.write_graph_on_tree(graph)
        graphs.increment_matrix(graph)
        width = tww.twin_width(graph)
        short_number = min(len(sct.black_edges), len(sct.white_edges))
        if (width+1/2)*(n-1) < short_number - leeway:
            if immediate_return:
                return [tree, graph]
            counter_examples.append([tree, copy.deepcopy(graph)])
        
        while graph != empty_graph:
            sct = ShortcutTree(tree)
            sct.write_graph_on_tree(graph)
            graphs.increment_matrix(graph)
            width = tww.twin_width(graph)
            short_number = min(len(sct.black_edges), len(sct.white_edges))
            if (width+1/2)*(n-1) < short_number - leeway:
                if immediate_return:
                    return  [tree, graph]
                counter_examples.append([tree, copy.deepcopy(graph)])
    return counter_examples


def run_on_cubics(n, immediate_return = True):
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
            if not graphs.is_cubic(graph):
                graphs.increment_matrix(graph)
                continue
            sct = ShortcutTree(tree)
            sct.write_graph_on_tree(graph)
            width = tww.twin_width(graph)
            if (2*width + 1)*(n-1) > sct.shortcut_number():
                if immediate_return:
                    return  [tree, graph]
                counter_examples.append([tree, copy.deepcopy(graph)])
            graphs.increment_matrix(graph)
    return counter_examples