# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 11:07:07 2022

@author: nasmy
"""

def generateEmptyGraph(n):
    """
    Input: a positive integer n
    Output: an empty graph on n vertices.
    """
    incidence_matrix = []
    for i in range(n):
        incidence_matrix.append([0]*n)
    return incidence_matrix
    #return [[0]*n]*n


def increment_matrix(matrix):
    n = len(matrix)
    max_edges = (n*(n-1)/2)
    for row in range(n-1, -1 , -1):
        for col in range(row-1, -1, -1):
            matrix[row][col] = 1 - matrix[row][col]
            if row != col:
                matrix[col][row] = 1 - matrix[col][row]
            if matrix[row][col] == 1:
                if num_edges(matrix) > max_edges/2:
                    return increment_matrix(matrix)
                    #continue
                return matrix
    return matrix


def num_graphs(n):
    count = 1
    graph = generateEmptyGraph(n)
    empty_graph = generateEmptyGraph(n)
    increment_matrix(graph)
    while graph != empty_graph:
        count+=1
        increment_matrix(graph)
    return count


def num_edges(graph):
    num_edges = 0
    for row in graph:
        num_edges += sum(row)
    return num_edges/2


    