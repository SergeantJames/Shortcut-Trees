# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 17:54:59 2022

@author: Thomas James

A different implementation of the shortcut trees class.
This variation stores (full binary) trees as a string of 1s and 0s. In this
way, we can represent ALL full binary trees, not just all trees up to
isomorphism, which is the case for the implementation in the original
ShortcutTree class.

This class also has the ability to increment its tree. That is, to change its
tree to the next one in some predefined order.
"""



class IShortcutTree():
    """
    
    Key
    -vertices are labelled between [-n,n-1).
    -The negative labels refer to the leaves -- specifically, the vertex
    labelled -k is the k-th vertex of the graph.
    -the non-negative labels refer to the internal nodes with that index 
    (according to self.tree).
    
    """
    
    def __init__(self, tree, graph = [[],]):
        """
        Input:
            -graph should be in the format of an incidence matrix
            -tree should be a list of length 2n-1. The i-th entry indicates
            whether the i-th vertex in the tree has two children (1) or no
            children (0).
            e.g [1,1,1,1,1,0,0,0,0,0,0] is
                 *                             1
                / \                           / \   
               *   *                         1   1   
              / \  /\                       / \  /\   
             *   * * *                     1  1 0 0    
            / \  /\                       / \  /\            
           *  *  * *                     0  0 0 0
        """
        self.graph = graph
        self.tree = tree
        self.size = int((len(tree) + 1)/2)
        self.black_edges = []
        self.white_edges = []
    
    
    def write_graph_on_tree(self, graph):
        
        def write_graph_on_leaves():
            """"""
            size = list(range(self.size))
            for row in size:
                for col in range(row+1,self.size):
                    if self.graph[row][col] == 1:
                        self.black_edges.append({-(row+1), -(col+1)})
                    else:
                        self.white_edges.append({-(row+1), -(col+1)})
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
        index = self.get_index(vertex)
        
        if self.tree[index] == 0:
            return []
        
        child_pos = 2*sum(self.tree[0:index]) + 1
        
        return [self.get_vertex(child_pos), self.get_vertex(child_pos+1)]
    
    
    def get_index(self, vertex):
        count = -1
        if vertex >= 0:
            for i in range(len(self.tree)):
                count += self.tree[i]
                if count >= vertex:
                    return i
        else:
            count = 0
            for i in range(len(self.tree)):
                count += 1-self.tree[i]
                if count == -vertex:
                    return i
        return
    
    
    def get_vertex(self, index):
        treesum = sum(self.tree[0:index])
        if self.tree[index] == 1:
            return treesum
        if self.tree[index] == 0:
            return treesum - index - 1
    
    
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
    
    
    def increment_tree(self):
        
        def is_valid_tree(tree):
            if 2*sum(tree) != len(tree) - 1:
                return False
            for i in range(len(tree)-1):
                if 2*sum(tree[0:i]) < i:
                    return False
                if tree[i] not in {0,1}:
                    return False
            return True
        
        def increment_binary(array):
            for i in range(len(array)-1, -1, -1):
                array[i] = 1-array[i]
                if array[i] == 1:
                    return
        if len(self.tree)%2==0:
            return
        increment_binary(self.tree)
        while not is_valid_tree(self.tree):
            increment_binary(self.tree)
        return

    def shortcut_number(self):
        """Returns the total number (int) of shortcut edges."""
        return len(self.black_edges) + len(self.white_edges)
    
    
    def get_leaves(self):
        return list(range(-self.size, 0))
    
    def get_internal_vertices(self):
        return list(range(0,self.size-1))
    
    def get_vertices(self):
        return list(range(-self.size, self.size-1))