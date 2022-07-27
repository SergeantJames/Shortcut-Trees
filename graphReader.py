# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 15:02:49 2022

@author: nasmy
"""



# code taken from https://or.stackexchange.com/questions/638/is-there-any-way-
# to-generate-all-the-possible-undirected-graphs-with-unlabeled-n
# written by user Ramin Fakhimi.

# graph files from http://users.cecs.anu.edu.au/~bdm/data/graphs.html
# written by Brendan McKay


def getGraphs(n):
    
    file_contents = open("./simple graphs/graph{N}.g6".format(N=n), "r")
    lines = file_contents.readlines()
    
    for line in lines:
        n = ord(line.split()[0][0]) - 63
        h = ''
        
        l = n - 1
        for i in range(1,l):
            temp = bin(ord(line.split()[0][i])-63)[2:]
            if len(temp) < 6:
                for k in range(6 - len(temp)):
                    h = h + '0'
            h = h + temp
        
        
        A = [[0]*n for j in range(n)]
        k = 0;
        for i in range(1,n):
            for j in range(0,i):
                A[i][j] = int(h[k])
                A[j][i] = A[i][j]
                k = k+1
        return A