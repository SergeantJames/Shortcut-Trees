def btnumber(n):
    """
    Input: a positive integer n
    Output: the number of 'distinct' unlabelled binary trees on n vertices
    """
    output = 0
    if n in [0,1]:
        output = 1
    elif n%2 == 0:
        for i in range(int(n/2)):
            output += btnumber(i)*btnumber(n-1-i)
    elif n%2 != 0:
        for i in range(int((n-1)/2)):
            output += btnumber(i)*btnumber(n-1-i)
        output += choose(btnumber((n-1)/2)+1,2)
    return output


btnumber_dict = {}
def fastbtnumber(n):
    if n in btnumber_dict.keys():
        return btnumber_dict[n]
    output = 0
    if n in [0,1]:
        output = 1
    elif n%2 == 0:
        for i in range(int(n/2)):
            output += fastbtnumber(i)*fastbtnumber(n-1-i)
    elif n%2 != 0:
        for i in range(int((n-1)/2)):
            output += fastbtnumber(i)*fastbtnumber(n-1-i)
        output += choose2(fastbtnumber((n-1)/2)+1)
    btnumber_dict[n] = output
    return output


def factorial(n):
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)


def choose(n,k):
    return int(factorial(n)/(factorial(k)*factorial(n-k)))


def choose2(n):
    return (n*(n-1))//2


def binTrees(n):
    """
    Input: a positive integer n
    Output: an array containing all 'distinct' unabelled full binary trees on
    2n+1 vertices.
    
    Trees are represented by a list of length n-1. The i-th entry refers to
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
    if n == 0:
        return [[],]
    if n == 1:
        return [[0,],]
    out = []
    for i in range(int(n/2)):
        leftTrees = binTrees(i)
        rightTrees = binTrees(n-1-i)
        for left in leftTrees:
            for right in rightTrees:
                out.append(combine(left,right))
    if n%2 == 1:
        half_trees = binTrees((n-1)/2)
        while len(half_trees) > 0:
            left = half_trees[0]
            for right in half_trees:
                out.append(combine(left,right))
            half_trees.remove(left)
    return out


def combine(left, right):
    """
    Input: two arrays defining binary trees.
    Output: the tree resulting from combining the two inputs
    
    A new root node is created. Then the first input becomes the left child,
    and the second input the right child.
    """
    left_count = 1
    right_count = 1
    if len(left) == 0:
        left_count = 0
    if len(right) == 0:
        right_count = 0
    new_tree = [(left_count+right_count),]
    left_pos = 0
    right_pos = 0
    track = 0
    while left_count + right_count > 0:
        while left_count > 0:
            new_tree.append(left[left_pos])
            track += left[left_pos]
            left_pos += 1
            left_count -=1
        left_count += track
        track = 0
        while right_count > 0:
            new_tree.append(right[right_pos])
            track += right[right_pos]
            right_pos += 1
            right_count -= 1
        right_count += track
        track = 0
    return new_tree
    
        
        

