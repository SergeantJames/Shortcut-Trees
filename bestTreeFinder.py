# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:41:17 2022

@author: nasmy
"""
from iterableShortcutTrees import IShortcutTree
from permutableShortcutTrees import PShortcutTree
import binaryTrees
import graphs
import twinWidthSATSolver as tww
from copy import deepcopy



def find_minimal_shortcut_tree(graph):
    """Takes a graph as input and returns the shortcut tree encoding graph with
    the fewest shortcuts"""
    size = len(graph)
    min_stree = [None, None, size**2]
    trees = binaryTrees.binTrees(size-1)
    
    for tree in trees:
        psct = PShortcutTree(tree)
        candidate = psct.minimize_shortcuts(graph)
        if candidate < min_stree[2]:
            min_stree = [psct.tree, psct.perm, candidate]
    
    psct = PShortcutTree(min_stree[0])
    psct.perm = min_stree[1]
    #psct.minimize_shortcuts(graph)
    psct.write_graph_on_tree(graph)
    return psct


def minimal_tree_plot(size):
    """Takes all graphs of size and computes the minimal shortcut tree. Plots
    this information against twin width."""
    plot = []
    for i in range(size):
        appendage = []
        for j in range(size):
            appendage.append(0)
        plot.append(appendage)
    
    graph = graphs.generateEmptyGraph(size)
    width = tww.twin_width(graph)
    psct = find_minimal_shortcut_tree(graph)
    plot[width][psct.min_shortcuts()] += 1
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*size]*size:
        width = tww.twin_width(graph)
        psct = find_minimal_shortcut_tree(graph)
        plot[width][psct.min_shortcuts()] += 1
        graphs.increment_matrix(graph)
    return plot
 

def find_graph_with_k_shortcuts(size, twin_width, k):
    """Returns a graph of the specified size and twin width which cannot be
    represented with fewer than k shortcuts"""
    graph = graphs.generateEmptyGraph(size)
    
    width =  tww.twin_width(graph)
    psct = find_minimal_shortcut_tree(graph)
    if width == twin_width and psct.min_shortcuts() == k:
        return graph
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*size]*size:
        #if graphs.num_edges(graph) != 10: #tailored for graphs with |V| = 7
        #    graphs.increment_matrix(graph)
        #    continue
        width =  tww.twin_width(graph)
        if width != twin_width:
            graphs.increment_matrix(graph)
            continue
        psct = find_minimal_shortcut_tree(graph)
        if psct.min_shortcuts() == k:
            return graph
        graphs.increment_matrix(graph)
    return


def is_smaller_than(graph, k):
    """returns True if graph can be represented on a shortcut tree with k or
    fewer shortcuts, False otherwise"""
    import itertools
    size = len(graph)
    trees = binaryTrees.binTrees(size - 1)
    
    for tree in trees:
        psct = PShortcutTree(tree)
        for perm in itertools.permutations(range(size)):
            psct.perm = perm
            psct.write_graph_on_tree(graph)
            if psct.min_shortcuts() <= k:
                return True
    return False


def all_smaller_than(size, k, randomise_graphs = False):
    """returns True if all graphs of size 'size' can be represented with k or fewer
    shortcut edges. If this is not the case, returns a counter-example"""
    graph = graphs.generateEmptyGraph(size)
    if randomise_graphs:
        graph = graphs.generateRandomGraph(size, (size*(size-1))//4 - 1)
    if not is_smaller_than(graph, k):
        return graph
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*size]*size:
        if not is_smaller_than(graph, k):
            return graph
        graphs.increment_matrix(graph)
    return True


def find_max_shortcut_number(size):
    k = 0
    while type(all_smaller_than(size, k)) == list:
        k+=1
    return k


def max_shortcuts_dictionary(dictionary={}, start_size = 1, start_k = 0):
    """"""
    size = start_size
    ineq = {"="}
    if start_k == -1:
        ineq = ("<=")
    while True:
        k = 0
        if size == start_size:
            k = start_k
        if start_k == -1:
            k = size - 1
        while type(all_smaller_than(size, k)) == list:
            dictionary[0] = k
            print(".........checked k={k}".format(k=k))
            k += 1
        dictionary[size] = k
        print("Done graphs of size", size)
        print("n={size}, k{ineq}{k}".format(size = size, k = k, ineq=ineq))
        size += 1
        print("Now looking at graphs of size", size)


# def min_necessary_shortcuts(size):
#    """Does same as find_max_shortcut_number but slower
#    (I do not understand how it is slower)"""
#     import itertools
#     graph = graphs.generateEmptyGraph(size)
#     trees = binaryTrees.binTrees(size-1)
#     global_min = 0
    
#     graph_min = size**2
#     for tree in trees:
#         psct = PShortcutTree(tree)
#         for perm in itertools.permutations(range(size)):
#             psct.perm = perm
#             psct.write_graph_on_tree(graph)
#             if psct.min_shortcuts() < graph_min:
#                 graph_min = psct.min_shortcuts()
#     if graph_min > global_min:
#         global_min = graph_min
#     graphs.increment_matrix(graph)
    
#     while graph != [[0,]*size]*size:
#         graph_min = size**2
#         for tree in trees:
#             psct = PShortcutTree(tree)
#             for perm in itertools.permutations(range(size)):
#                 psct.perm = perm
#                 psct.write_graph_on_tree(graph)
#                 if psct.min_shortcuts() < graph_min:
#                     graph_min = psct.min_shortcuts()
#                 if psct.min_shortcuts() < global_min:
#                     break
#             if psct.min_shortcuts() < global_min:
#                 break
#         if graph_min > global_min:
#             global_min = graph_min
#         graphs.increment_matrix(graph)
#     return global_min


# def find_best_tree(graph):
#     n = len(graph)
#     init_tree = [0,]*(2*n-1)
#     best = [None, n*(n-1)/2, ""]
#     #width = tww.twin_width(graph)
#     isct = IShortcutTree(init_tree)
    
#     for c in range(catalan(n-1)):
#         isct.increment_tree()
#         isct.write_graph_on_tree(graph)
#         if len(isct.black_edges) < best[1]:
#             best = [deepcopy(isct.tree), len(isct.black_edges), "black", deepcopy(isct.black_edges)]
#         if len(isct.white_edges) < best[1]:
#             best = [deepcopy(isct.tree), len(isct.white_edges), "white", deepcopy(isct.white_edges)]
#     return best


def catalan(k):
    def fact(l):
        if l <= 0:
            return 1
        else:
            return l*fact(l-1)
    return fact(2*k)//(fact(k+1)*fact(k))