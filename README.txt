Important: The graphReader module reads graphs from the 'simple graphs' folder. The graph files stored in this folder are those found at
http://users.cecs.anu.edu.au/~bdm/data/graphs.html, particularly files graph2.g6 through graph11.g6. For size reasons, I have not included all
of these in my code submission, so some functionality relying on this module may not work.


Modules:

bestTreeFinder
	Contains functionality for finding the minimal shortcut tree encodings of graphs

	Main functions
		find_minimal_shortcut_tree(graph) - returns the shortcut tree representation of graph with the fewest shortcuts
		minimal_tree_plot(size) - Produces the tables given in figures 12 and 15
		reduced_tree_plot(size) - faster and better version of minimal_tree_plot
		max_shortcuts_dictionary() - produces a dictionary where each natural number n is paired with the minimal number of shortcuts necessary to encode any graph with n vertices


binaryTrees
	Contains functionality for generating lists of binary trees and counting the number of structurally distinct binary trees.

	Main functions:
		btnumber(n) (and fastbtnumber(n)) - returns the number of structurally distinct binary trees on n vertices
		binTrees(n) - returns a list of all structurally distinct unlabelled trees on n vertices in a ternary encoding

graphs
	Contains functionality for operating on graphs
	
	Main functions:
		generateEmptyGraph(n) - outputs an empty graph of size n
		increment_matrix(matrix) - 'increments' a graph in matrix form. (assumes an order over all graphs; returns the next graph in that order following the input)
		num_graphs(n) - returns the number of graphs on n vertices
		num_edges(graph) - returns the number of edges of graph
		neighbourhoos(graph, v) - returns the neighbourhood of vertex v in graph
		is_connected(graph) - returns True iff graph is connected, False otw
		is_cubic(graph) - returns True iff graph is cubic, False otw
		permute_graph(graph, perm) - returns the graph with vertices permuted according to perm

shortcutTrees
	Contains an implementation of a ShortcutTree class

permutableShortcutTrees
	Contains an implementation of a PermutableShortcutTree class

twinWidthSATsolver
	Implements Schidler and Szeiders's SAT twin-width finder

	Main functions:
		twin_width(graph) - returns the twin-width of graph
		twin_width_2(graph) - returns the twin-width of graph (slower)
		bounded_twin_width(graph, d) - returns True iff tww(graph) <= d, False otherwise

Main
	Runs the counter-example search

	Main functions:
		run(n) - searches for and returns a counter example to Conjecture 1 on n vertices
		find_counter_tree(graph) - finds a tree such that the resulting graph+tree combo is a counter to Conjecture 1
		find_counter_graph(tree) - finds a graph such that the resulting graph+tree combo is a counter to Conjecture 1

shortcutPerfectObjectFinder
	Contains functionality for finding shortcut perfect graphs and shortcut perfect trees
	
	Main functions:
		perfect_tree_finder(n) - returns a perfect tree on n nodes
		perfect_tree_search() - searches for perfect trees on 4 or more nodes
		perfect_graph_finder(n) - returns a shortcut perfect graph (or list of shortcut perfect graphs) on n vertices
		find_minimal_shortcut_tree(graph) - returns the shortcut tree encoding of graph with the fewesr shortcuts

graphReader
	Reads graph files from the file 'simple graphs'
	The simple graphs come from http://users.cecs.anu.edu.au/~bdm/data/graphs.html, maintained by Brendan McKay
	For size reasons, I've not included this file in my submission

	Main functions
		getGraphs(n) - returns a list of all unlabelled graphs on n vertices
		overGraphs(n) - generates all unlabelled graphs on n vertices

