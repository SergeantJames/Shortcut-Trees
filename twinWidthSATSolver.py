# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 11:12:09 2022

@author: nasmy

Implementation of the SAT encoding by Schidler and Szeider (A SAT Approach to
Twin Width).
"""

from pysat.solvers import Cadical
from pysat.formula import CNF
from pysat.card import CardEnc


def constructSAT(graph):
    n = len(graph)
    cnf = CNF()
    o_transitivity_clauses(cnf, n)
    at_least_one_parent_clauses(cnf, n)
    at_most_one_parent_clauses(cnf, n)
    parent_child_order_clauses(cnf, n)
    a_semantics_clauses(cnf, n)
    r_semantics_clauses(cnf, graph, n)
    subset_1a_clauses(cnf, n)
    subset_1b_clauses(cnf, n)
    return cnf


def twin_width(graph):
    for d in range(len(graph)):
        if bounded_twin_width(graph, d):
            return d
    return "Error: function does not work"


def twin_width_2(graph):
    for d in range(len(graph), -1, -1):
        if not bounded_twin_width(graph, d):
            return d + 1
    return "Error: function does not work"


def bounded_twin_width(graph, d):
    n = len(graph)
    SAT = constructSAT(graph)
    for i in range(1,n):
        for j in range(1, n+1):
            cardinality_vars = []
            for k in range(1, n+1):
                if k != j:
                    cardinality_vars.append(r_star(i,j,k,n))
            eq_cons = CardEnc.atmost(lits=cardinality_vars, bound=d, encoding=6, top_id=SAT.nv)
            SAT.extend(eq_cons.clauses)
    cadical = Cadical()
    cadical.append_formula(SAT.clauses)
    return cadical.solve()


def o_transitivity_clauses(cnf, n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n+1):
                if i!=j and i!=k and j!=k:
                    cnf.append([-o_star(i,j,n),-o_star(j,k,n),o_star(i,k,n)])
    return

def at_least_one_parent_clauses(cnf, n):
    for i in range(1, n):
        clause = []
        for j in range(i+1,n+1):
            clause.append(p(i,j,n))
        cnf.append(clause)
    return

def at_most_one_parent_clauses(cnf, n):
    for i in range(1, n):
        for j in range(i+1, n+1):
            for k in range(i+1, n+1):
                if j!=k:
                    cnf.append([-p(i,j,n), -p(i,k,n)])
    return

def parent_child_order_clauses(cnf, n):
    for i in range(1, n):
        for j in range(i+1, n+1):
            cnf.append([-p(i,j,n), o_star(i,j,n)])
    return

def a_semantics_clauses(cnf, n):
    for i in range(1, n):
        for j in range(i+1, n+1):
            for k in range(1, n+1):
                if i!=k and j!=k:
                    cnf.append([-o_star(i,j,n), -o_star(i,k,n), -r_star(i,j,k,n), a_star(j,k,n)])
    return

def r_semantics_clauses(cnf, graph, n):
    for i in range(1, n):
        for j in range(i+1, n+1):
            for k in range(1, n+1):
                if graph[i-1][k-1] != graph[j-1][k-1] and k not in [i,j]:
                    cnf.append([-p(i,j,n), -o_star(i,k,n), r_star(i,j,k,n)])
    return

def subset_1b_clauses(cnf, n):
    for i in range(1, n):
        for j in range(i+1, n+1):
            for k in range(1, n+1):
                if i!=k and j!=k:
                    cnf.append([-p(i,j,n), -o_star(i,k,n), -a_star(i,k,n), r_star(i,j,k,n)])
    return

def subset_1a_clauses(cnf, n):
    for i in range(1, n+1):
        for j in range(1, n+1):
            for k in range(1, n):
                for m in range(k+1, n+1):
                    if len({i,j,k,m}) == 4:  # checks they are mutually distinct
                        cnf.append([-o_star(i,j,n), -o_star(j,k,n), -o_star(j,m,n), -r_star(i,k,m,n), r_star(j,k,m,n)])
    return


def o_star(i, j, n):
    I = min(i,j)
    J = max(i,j)
    return (2*(I==i)-1)*int((-I**2)/2 + (n-1/2)*I + J - n)

def p(i,j,n):
    return int((n*(n-1))/2 + ((-i**2)/2 + (n-1/2)*i + j - n))
    
def r_star(i, j, k, n):
    J = min(j,k)
    K = max(j,k)
    #return (2*(J==j)-1)*int(n*(n-1) + (i-1)*(n*(n-1)/2) + (-J**2)/2 + (n-1/2)*J + K - n)
    return int(n*(n-1) + (i-1)*(n*(n-1)/2) + (-J**2)/2 + (n-1/2)*J + K - n)


def a_star(i, j, n):
    I = min(i,j)
    J = max(i,j)
    #return (2*(I==i)-1)*int((2+n)*(n*(n-1)/2) + (-I**2)/2 + (n-1/2)*I + J - n)
    return int((2+n)*(n*(n-1)/2) + (-I**2)/2 + (n-1/2)*I + J - n)



# def totalise(cnf, variables):
#     """"""
#     def num_totaliser_vars(card):
#         if card == 1:
#             return 1
#         else:
#             return num_totaliser_vars(card-1) + 3 + (math.floor(math.log2(card-1)))


#     def num_linking_vars(card):
#         return num_totaliser_vars(card) - 2*card
    
    
#     def get_output_variables(cnf, card):
#         link = num_linking_vars(card)
#         start = cnf.nv + link + 1
#         output = []
#         for i in range(start, start + card):
#             output.append(i)
#         return output

    
#     def totaliser_tree(cnf, input_variables, output_variables):
#         tree = []
#         tree.append(output_variables)
#         num_entries = 2**(math.ceil(math.log2(len(input_variables)))+1)
#         var_num = cnf.nv + 1
#         for i in range(1, num_entries-1):
#             if i%2 == 1:
#                 parent = len(tree[int((i-1)/2)])
#                 val = math.floor(parent/2)
#                 if parent == 1:
#                     tree.append([])
#                 elif val == 1:
#                     tree.append([input_variables.pop(0),])
#                 else:
#                     new_vertex = []
#                     for i in range(var_num, var_num + val):
#                         new_vertex.append(i)
#                     var_num += val
#                     tree.append(new_vertex)
#             else:
#                 parent = len(tree[int(i/2 - 1)])
#                 val = parent - math.floor(parent/2)
#                 if parent == 1:
#                     tree.append([])
#                 elif val == 1:
#                     tree.append([input_variables.pop(0),])
#                 else:
#                     new_vertex = []
#                     for i in range(var_num, var_num + val):
#                         new_vertex.append(i)
#                     var_num += val
#                     tree.append(new_vertex)
#         return tree
    
    
#     cardinality = len(variables)
#     start = cnf.nv + 1
#     output_vars = get_output_variables(cnf, cardinality)
#     tree = totaliser_tree(cnf, variables, output_vars)
    
#     for vertex in tree:
#         if len(vertex)>1:
#             pass
#     return tree
    
    
    



# def cardinality_clauses(cnf, n, d):
    
#     def num_totaliser_vars(card):
#         if card == 1:
#             return 1
#         else:
#             return num_totaliser_vars(card-1) + 3 + (math.floor(math.log2(card-1)))
    
#     def num_linking_vars(card):
#         return num_totaliser_vars(card) - 2*card
    
#     def totaliser_tree(cnf, card, n):
#         tree = []
#         tree.append(get_output_variables(cnf, card, n))
#         num_entries = 2**(math.ceil(math.log2(card))+1)
#         var_num = cnf.nv + 1
#         for i in range(1, num_entries-1):
#             if i%2 == 1:
#                 parent = len(tree[int((i-1)/2)])
#                 val = math.floor(parent/2)
#                 if parent == 1:
#                     tree.append([])
#                 elif val == 1:
#                     tree.append(["c",])
#                 else:
#                     new_vertex = []
#                     for i in range(var_num, var_num + val):
#                         new_vertex.append(i)
#                     var_num += val
#                     tree.append(new_vertex)
#             else:
#                 parent = len(tree[int(i/2 - 1)])
#                 val = parent - math.floor(parent/2)
#                 if parent == 1:
#                     tree.append([])
#                 elif val == 1:
#                     tree.append(["c",])
#                 else:
#                     new_vertex = []
#                     for i in range(var_num, var_num + val):
#                         new_vertex.append(i)
#                     var_num += val
#                     tree.append(new_vertex)
#         return tree
    
    
#     def get_cardinality_vars(n):
#         card_vars = []
#         for i in range(1,n+1):
#             for j in range(1,n):
#                 for k in range(j+1, n+1):
#                     card_vars.append(r_star(i,j,k,n))
#         return card_vars
    
    
#     def get_output_variables(cnf, card, n):
#         link = num_linking_vars(card)
#         start = cnf.nv + link
#         num_vars = math.comb(n, 2)
#         output = []
#         for i in range(start, start + num_vars):
#             output.append(i)
#         return output
    
    
#     card_vars = get_cardinality_vars(n)
#     card = n * math.comb(n, 2)
#     output_vars = get_output_variables(cnf, card, n)
#     tree = totaliser_tree(cnf, card, n)
#     return [tree, card_vars, output_vars]
    
            