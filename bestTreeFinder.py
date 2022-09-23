# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 16:41:17 2022

@author: nasmy
"""
from iterableShortcutTrees import IShortcutTree
from permutableShortcutTrees import PShortcutTree
import binaryTrees
import graphs
import graphReader
import twinWidthSATSolver as tww
from copy import deepcopy



def find_minimal_shortcut_tree(graph, count_both_edge_sets=False, verbose=False):
    """Takes a graph as input and returns the shortcut tree encoding graph with
    the fewest shortcuts"""
    size = len(graph)
    min_stree = [None, None, size**2]
    trees = binaryTrees.binTrees(size-1)
    
    for tree in trees:
        psct = PShortcutTree(tree)
        candidate = psct.minimize_shortcuts(graph, count_both_edge_sets)
        if candidate < min_stree[2]:
            min_stree = [psct.tree, psct.perm, candidate]
            if verbose:
                print(candidate)
    
    psct = PShortcutTree(min_stree[0])
    psct.perm = min_stree[1]
    #psct.minimize_shortcuts(graph)
    psct.write_graph_on_tree(graph)
    return psct


def minimal_tree_plot(size, connected_only = False, min_twin_width=None):
    """Takes all graphs of size and computes the minimal shortcut tree. Plots
    this information against twin width.
    
    Use reduced_tree_plot instead because it is faster"""
    plot = []
    for i in range(size):
        appendage = []
        for j in range(size):
            appendage.append(0)
        plot.append(appendage)
    
    graph = graphs.generateEmptyGraph(size)
    if not connected_only:
        width = tww.twin_width(graph)
        psct = find_minimal_shortcut_tree(graph)
        plot[width][psct.min_shortcuts()] += 1
        plot[width][psct.shortcut_number()] += 1
    graphs.increment_matrix(graph, False)
    
    while graph != [[0,]*size]*size:
        if (not connected_only or graphs.is_connected(graph)):
            if min_twin_width:
                if tww.bounded_twin_width(graph, min_twin_width-1):
                    graphs.increment_matrix(graph, False)
                    continue
            width = tww.twin_width(graph)
            psct = find_minimal_shortcut_tree(graph)
            plot[width][psct.min_shortcuts()] += 1
        graphs.increment_matrix(graph, False)
    return plot


def reduced_tree_plot(size, x_axis = 0, y_axis = 0, connected_only=False, verbose=False):
    """A better and faster version of minimal_tree_plot
    
    Over all graphs of a certain size, plots an invariant of that graph
    (x axis) against a the size of a minimal shortcut tree of that graph
    (y axis). Options exist for different graph invariants and different ways
    of measuring the sizes of shortcut trees.
    
    By default, the invariant is twin width and shortcut trees are measured by
    the size of their smallest shortcut set.
    
    Inputs:
        Size: 
            The size (number of vertices) of graphs to be plotted over.
            Limited to the interval [1, 10].
    
        x_axis:
            0: size of smallest shortcut set (default)
            1: combined size of both shortcut sets
        
        y_axis:
            0: twin width
            1: number of edges
        
        connected_only:
            False by default
            If True, will skip (not plot) all graphs which are not connected
        
        verbose:
            False by default
            If True, will print the number of graphs plotted at regular
            intervals.
        
        Output:
            The plot is output in the form of a matrix
        """
    def get_y_axis_value(graph, y_axis):
        if y_axis == 0:
            return tww.twin_width(graph)
        if y_axis == 1:
            return graphs.num_edges(graph)
        return
    
    def get_x_axis_value(graph, x_axis):
        if x_axis == 0:
            psct = find_minimal_shortcut_tree(graph, False)
            return psct.min_shortcuts()
        if x_axis == 1:
            psct = find_minimal_shortcut_tree(graph, True)
            return psct.shortcut_number()
        return
    
    if size < 1 or size > 10:
        return
    plot = []
    for i in range((size*(size+1))//2):
    #for i in range(size//2 + 1):
        appendage = []
        for j in range(2*size + 1):
            appendage.append(0)
        plot.append(appendage)
        
    count = 0
    for graph in graphReader.overGraphs(size):
        count += 1
        if connected_only:
            if not graphs.is_connected(graph):
                continue
        #width = tww.twin_width(graph)
        #num_edges = graphs.num_edges(graph)
        y_value = get_y_axis_value(graph, y_axis)
        #psct = find_minimal_shortcut_tree(graph)
        x_value = get_x_axis_value(graph, x_axis)
        #plot[width][psct.min_shortcuts()] += 1
        #plot[num_edges][psct.min_shortcuts()] += 1
        plot[y_value][x_value] += 1
        if verbose:
            if count in [1,2,3,4,5] or count%10==0:
                print("Done up to", count)
    return plot 


def find_graph_with_k_shortcuts(size, twin_width, k, count_both_edge_sets=False):
    """Returns a graph of the specified size and twin width which cannot be
    represented with fewer than k shortcuts"""
    graph = graphs.generateEmptyGraph(size)
    
    width =  tww.twin_width(graph)
    psct = find_minimal_shortcut_tree(graph, count_both_edge_sets)
    if width == twin_width and psct.min_shortcuts() == k:
        return graph
    graphs.increment_matrix(graph)
    
    while graph != [[0,]*size]*size:
        width =  tww.twin_width(graph)
        if width != twin_width:
            graphs.increment_matrix(graph)
            continue
        psct = find_minimal_shortcut_tree(graph, count_both_edge_sets)
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


def all_smaller_than_reduced(size, k):
    """A faster and better version of all_smaller_than"""
    for graph in graphReader.overGraphs(size):
        if not is_smaller_than(graph, k):
            return graph
    return True


def find_max_shortcut_number(size, reduced = True):
    k = 0
    if reduced:
        while type(all_smaller_than_reduced(size,k)) == list:
            k+=1
    else:
        while type(all_smaller_than(size, k)) == list:
            k+=1
    return k


def max_shortcuts_dictionary(dictionary={}, start_size = 2, start_k = 0):
    """
    Produces a dictionary where the keys are integers representing graph sizes
    and the value at each entry is the smallest integer k such that any graph
    of that size can be represented with at most k shortcuts (of one colour).
    
    In other words, any graph on [key] vertices can be represented with [value]
    or fewer shortcuts.
    """
    size = start_size
    ineq = "="
    if start_k < 0:
        ineq = "<="
    while True:
        k = 0
        if size == start_size:
            k = start_k
        if start_k < 0:
            k = size + start_k
        while type(all_smaller_than_reduced(size, k)) == list:
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