# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:44:06 2022

@author: nasmy
"""


class ShortcutTree():
    """
    
    Key
    -vertices are labelled between [-n,n-2].
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
    
    
    def __str__(self):
        current_line = [0,]
        output = ""
        
        while current_line != []:
            next_line = []
            for vertex in current_line:
                next_line.extend(self.get_children(vertex))
                if vertex >= 0:
                    output = output + "  " + str(vertex)
                else:
                    output = output + " " + str(vertex)
            current_line = next_line
            del next_line
            output = output + "\n"
        output = output + "Black Edges: " + str(self.black_edges)
        output = output + "\nWhite Edges: " + str(self.white_edges)
        return output
    
    
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
                children.append(-(child_start_index + i))
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


    def shortcut_number(self):
        """Returns the total number (int) of shortcut edges."""
        return len(self.black_edges) + len(self.white_edges)
    
    
    def get_leaves(self):
        return list(range(-self.size, 0))
    
    def get_internal_vertices(self):
        return list(range(0,self.size-1))
    
    def get_vertices(self):
        return list(range(-self.size, self.size-1))