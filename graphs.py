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


def generateRandomGraph(n, max_edges = None):
    """generates a random graph on n vertices"""
    import random
    if max_edges == None:
        max_edges = (n*(n-1))//2
    graph = generateEmptyGraph(n)
    for i in range(n-1):
        for j in range(i+1,n):
            rand = 0
            if max_edges > 0:
                rand = random.randint(0, 1)
            graph[i][j] = rand
            graph[j][i] = rand
            if rand >= 1:
                max_edges -= 1
    return graph
    


def increment_matrix(matrix, compliments_r_equal = True):
    """
    Input: -an adjacency matrix of a graph, in the form of an array of arrays
           -a boolean, defaults to True. If True, skips graphs with more
           than (nC2)/2 edges, since their compliment will be given.
    
    Output: -an adjacency matrix, distinct from the input one but of the same
            dimensions
    
    Gives an order to the graphs on n vertices. Outputs the graph next in order
    after the input. If input is the last graph, outputs the empty graph (first
    in order).
    """
    n = len(matrix)
    max_edges = (n*(n-1)/2)
    for row in range(n-1, -1 , -1):
        for col in range(row-1, -1, -1):
            matrix[row][col] = 1 - matrix[row][col]
            if row != col:
                matrix[col][row] = 1 - matrix[col][row]
            if matrix[row][col] == 1:
                if compliments_r_equal and num_edges(matrix) > max_edges/2:
                    return increment_matrix(matrix)
                return matrix
    return matrix


def num_graphs(n, compliments_r_equal = True):
    """
    Input: -an integer n
           -a boolean, default to True. If True, treats complimentary graphs as
           identical, so halves the total number of graphs.
    Output: the number (int) of graphs on n vertices
    """
    count = 1
    graph = generateEmptyGraph(n)
    empty_graph = generateEmptyGraph(n)
    increment_matrix(graph, compliments_r_equal)
    while graph != empty_graph:
        count+=1
        increment_matrix(graph, compliments_r_equal)
    return count


def num_edges(graph):
    num_edges = 0
    for row in graph:
        num_edges += sum(row)
    return num_edges/2


def neighbourhood(graph, v):
    neighbours = []
    row = graph[v-1]
    for vertex in range(len(row)):
        if row[vertex] == 1:
            neighbours.append(vertex+1)
    return neighbours


def is_connected(graph):
    domain = set(neighbourhood(graph, 1))
    size = 0
    while size < len(domain):
        size = len(domain)
        additions = set()
        for v in domain:
            additions.update(neighbourhood(graph, v))
        domain.update(additions)
    return len(domain) == len(graph)
    


    