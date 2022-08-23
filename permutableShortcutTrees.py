# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:21:18 2022

@author: nasmy
"""


class PShortcutTree():
    """
    
    Key
    -vertices are labelled between [-n,n-1).
    -The negative labels refer to the leaves -- specifically, the vertex
    labelled -k is the k-th vertex of the graph.
    -the non-negative labels refer to the internal nodes with that index 
    (according to self.tree).
    
    """
    
    def __init__(self, tree, black_edges = [], white_edges=[], graph = [[],]):
        """
        Input:
            -graph should be in the format of an incidence matrix
            -tree should be a list of length n-1. The i-th entry refers to
            the number of *internal* nodes which are children of the i-th
            node.
            e.g [2,2,0,0,0] is
                 *                             2
                / \                           / \   
               *   *                         2   0   
              / \  /\                       / \  /\   
             *   * l l                     0   0 l l    
            / \  /\                       / \  /\            
           l  l  l l                      l  l l l
        """
        self.graph = graph
        self.tree = tree
        self.size = len(tree) + 1
        self.black_edges = black_edges
        self.white_edges = white_edges
        self.perm = []
        #self.inv_perm = {}
        for i in range(self.size):
            self.perm.append(i)
            #self.inv_perm[i] = i
    
    
    def write_graph_on_tree(self, graph):
        
        def write_graph_on_leaves():
            """"""
            for row in list(range(self.size)):
                for col in range(row+1,self.size):
                    if self.graph[self.perm[row]][self.perm[col]] == 1:
                        self.black_edges.append({-self.perm[row]-1, -self.perm[col]-1})
                    else:
                        self.white_edges.append({-self.perm[row]-1, -self.perm[col]-1})
            return
        
        self.black_edges = []
        self.white_edges = []
        self.graph = graph
        write_graph_on_leaves()
        self.pull_up_shortcuts()
    
    
    def pull_up_shortcuts(self):
        still_going = True
        while(still_going):
            still_going = False
            for edge_set in [self.black_edges, self.white_edges]:
                for vertex in range(self.size-1):
                    for target in range(-self.size, self.size-1):
                        if vertex == target:
                            continue
                        if vertex < 0:
                            vertex = -self.perm[-1-vertex]-1
                        if target < 0:
                            target = -self.perm[-1-target]-1
                        children = self.get_children(vertex)
                        if children == []:
                            continue
                        if ({children[0], target}) in edge_set and ({children[1], target}) in edge_set:
                            edge_set.remove({children[0], target})
                            edge_set.remove({children[1], target})
                            edge_set.append({vertex, target})
                            still_going = True
        return

    
    
    def get_children(self, vertex):
        """Input: a vertex (int in [-n, n-1)
        Output: a list containing 0 or 2 integers, which are children of the input."""
    
        def get_internal_children(self, vertex):
            child_pos = sum(self.tree[0:vertex+1])
            children = []
            for i in range(self.tree[vertex]):
                children.append(child_pos-i)
            return children
        
        def get_leaf_children(self, vertex):
            children = []
            inverted_tree = []
            for entry in self.tree:
                inverted_tree.append(2-entry)
            child_start_index = sum(inverted_tree[0:vertex])
            for i in range(1, inverted_tree[vertex]+1):
                children.append(-self.perm[child_start_index + i-1]-1)
            return children
        
        if vertex < 0:
            return []
        return get_internal_children(self, vertex) + get_leaf_children(self, vertex)
    
    
    def get_leaf_descendents(self, vertex):
        """"""
        if vertex < 0:
            return [vertex,]
        leaf_descendents = []
        children = self.get_children(vertex)
        for child in children:
            if child < 0:
                leaf_descendents.append(child)
            else:
                leaf_descendents.extend(self.get_leaf_descendents(child))
        return leaf_descendents
    
    
    def find_minimal_perm(self):
        """Finds a permutation for the graph and tree which produces the
        shortcut tree with the fewest shortcut edges"""
        import itertools
        best_perm = self.perm
        best_edges = (self.size)**2
        
        for p in itertools.permutations(range(self.size)):
            self.perm = p
            self.write_graph_on_tree(self.graph)
            if len(self.black_edges) < best_edges:
                best_edges = len(self.black_edges)
                best_perm = p    
            if len(self.white_edges) < best_edges:
                best_edges = len(self.white_edges)
                best_perm = p
        return best_perm
    
    
    def minimize_shortcuts(self, graph):
        """Finds the permutation which minimises the shortcut edges.
        Returns the minimal number of shortcuts needed to encode graph
        onto self.tree"""
        self.graph = graph
        self.perm = self.find_minimal_perm()
        self.write_graph_on_tree(graph)
        return min(len(self.black_edges), len(self.white_edges))
        


    def shortcut_number(self):
        """Returns the total number (int) of shortcut edges."""
        return len(self.black_edges) + len(self.white_edges)
    
    def min_shortcuts(self):
        return min(len(self.black_edges), len(self.white_edges))
    
    
    def get_leaves(self):
        return list(range(-self.size, 0))
    
    def get_internal_vertices(self):
        return list(range(0,self.size-1))
    
    def get_vertices(self):
        return list(range(-self.size, self.size-1))