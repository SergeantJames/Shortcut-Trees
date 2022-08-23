# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 09:26:07 2022

@author: nasmy
"""

import main
import binaryTrees
import graphs
import copy

def graphs4trees(n, immediate_return = True):
    """Cycles through all trees of size n-1 and tries to find a graph such
    that the pair forms a counter example to the conjecture.
    If it comes across a tree for which it cannot find a corresponding graph, 
    returns that tree if immediate_return is True. If immediate_return is
    False, returns all such pairs at the end of its run."""
    output = []
    trees = binaryTrees.binTrees(n-1)
    for tree in trees:
        if main.find_counter_graph(tree) == None:
            if immediate_return:
                return tree
            output.append(tree)
    return output


def perfect_tree_search(start = 2, stop = -1):
    while start != stop + 1:
        a = graphs4trees(start)
        if a != []:
            return [start, a]
        print("no perfect trees for n={start}".format(start=start))
        start += 1


def trees4graphs(n, immediate_return=True):
    """Cycles through all graphs of size n and for each tries to find a tree
    such that the pair forms a counter-example to the conjecture.
    If it comes accross a graph for which it cannot find such a tree, returns
    that graph if immediate_return is True. If immediate_return is False,
    returns all such graphs at the end of its run."""
    output = []
    graph = graphs.generateEmptyGraph(n)
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*n]*n:
        skip = False
        for vertex in graph:
            if sum(vertex)==0 or sum(vertex) == n-1:
                skip = True
        if skip:
            graphs.increment_matrix(graph)
            continue
        if main.find_counter_tree(graph) == None and graphs.is_connected(graph):
            if immediate_return:
                return graph
            output.append(copy.deepcopy(graph))
        graphs.increment_matrix(graph)
    return output


def find_minimal_shortcut_tree(graph):
    """Takes a graph as input and returns the shortcut tree encoding graph with
    the fewest shortcuts"""
    size = len(graph)
    from permutableShortcutTrees import PShortcutTree
    min_stree = [None, size^2]
    trees = binaryTrees.binTrees(size-1)
    
    for tree in trees:
        psct = PShortcutTree(tree)
        candidate = psct.minimize_shortcuts(graph)
        if candidate < min_stree[1]:
            min_stree = [psct.perm, candidate]
    
    psct = PShortcutTree(tree)
    psct.perm = min_stree[0]
    psct.write_graph_on_tree(graph)
    return psct
    
    