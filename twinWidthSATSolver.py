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
            