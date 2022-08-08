# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 10:24:35 2022

@author: nasmy
"""
from shortcutTrees import ShortcutTree

class TreeIterator():
    
    
    def __init__(self, tree):
        self.stree = ShortcutTree(tree)
        self.possible_shortcuts = self.get_possible_shortcut_edges(self.stree)
    
    
    def get_possible_shortcut_edges(stree):
        descendents = {}
        possible_edges = {}
        for vert in stree.get_vertices():
            descendents[vert] = stree.get_leaf_descendents(vert)
        for vert in stree.get_vertices():
            edges = []
            for vert2 in stree.get_vertices():
                if set(descendents[vert]).isdisjoint(set(descendents[vert2])):
                    edges.append([vert,vert2])
            possible_edges[vert] = edges
        return possible_edges
        