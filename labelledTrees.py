# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 10:09:16 2022

@author: nasmy
"""

def increment_tree(tree):
    while tree != [1,]*len(tree):
        increment_string(tree)
        if is_valid(tree):
            return


def is_valid(tree):
    treeSum = 0
    for i in range(len(tree)):
        treeSum += tree[i]
        if 2*treeSum - i < 0:
            return False
        if 2*treeSum - i == 0:
            return i == len(tree) - 1
    return False


def increment_string(string):
    for i in range(len(string)-1, -1, -1):
        string[i] = 1 - string[i]
        if string[i] == 1:
            return


def count_trees(n):
    n = 2*n + 1
    tree = [0,]*n
    count = 0
    while tree != [1,]*n:
        increment_tree(tree)
        count += 1
    return count - 1