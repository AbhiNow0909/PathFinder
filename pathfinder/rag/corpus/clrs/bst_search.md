---
topic: bst_search
pages: 338-342
---

**Figure 12.2** Queries on a binary search tree. Nodes and paths followed in each query are colored blue. **(a)** A search for the key 13 in the tree follows the path 15 → 6 → 7 → 13 from the root. **(b)** The minimum key in the tree is 2, which is found by following *left* pointers from the root. The maximum key 20 is found by following *right* pointers from the root. **(c)** The successor of the node with key 15 is the node with key 17, since it is the minimum key in the right subtree of 15. **(d)** The node with key 13 has no right subtree, and thus its successor is its lowest ancestor whose left child is also an ancestor. In this case, the node with key 15 is its successor.

Since the TREE-SEARCH procedure recurses on either the left subtree or the right subtree, but not both, we can rewrite the algorithm to "unroll" the recursion into a **while** loop. On most computers, the ITERATIVE-TREE-SEARCH procedure on the facing page is more efficient.

#### **Minimum and maximum**

To find an element in a binary search tree whose key is a minimum, just follow *left*  child pointers from the root until you encounter a NIL, as shown in Figure 12.2(b).

The TREE-MINIMUM procedure returns a pointer to the minimum element in the subtree rooted at a given node x, which we assume to be non-NIL.

```
TREE-MINIMUM(x)
1 while x.left ≠ NIL
2     x = x.left
3 return x
TREE-MAXIMUM(x)
1 while x.right ≠ NIL
2     x = x.right
3 return x
```

The binary-search-tree property guarantees that TREE-MINIMUM is correct. If node x has no left subtree, then since every key in the right subtree of x is at least as large as x.key, the minimum key in the subtree rooted at x is x.key. If node x has a left subtree, then since no key in the right subtree is smaller than x.key and every key in the left subtree is not larger than x.key, the minimum key in the subtree rooted at x resides in the subtree rooted at x.left.

The pseudocode for TREE-MAXIMUM is symmetric. Both TREE-MINIMUM and TREE-MAXIMUM run in O(h) time on a tree of height h since, as in TREE-SEARCH, the sequence of nodes encountered forms a simple path downward from the root.

#### **Successor and predecessor**

Given a node in a binary search tree, how can you find its successor in the sorted order determined by an inorder tree walk? If all keys are distinct, the successor of a node x is the node with the smallest key greater than x.key. Regardless of whether the keys are distinct, we define the *successor* of a node as the next node visited in an inorder tree walk. The structure of a binary search tree allows you to determine the successor of a node without comparing keys. The TREE-SUCCESSOR procedure on the facing page returns the successor of a node x in a binary search tree if it exists, or NIL if x is the last node that would be visited during an inorder walk.

The code for TREE-SUCCESSOR has two cases. If the right subtree of node x is nonempty, then the successor of x is just the leftmost node in x's right subtree, which line 2 finds by calling TREE-MINIMUM(x.right). For example, the successor of the node with key 15 in Figure 12.2(c) is the node with key 17.

On the other hand, as Exercise 12.2-6 asks you to show, if the right subtree of node x is empty and x has a successor y, then y is the lowest ancestor of x whose

```
TREE-SUCCESSOR(x)
1 if x.right ≠ NIL
2     return TREE-MINIMUM(x.right) // leftmost node in right subtree
3 else // find the lowest ancestor of x whose left child is an ancestor of x
4     y = x.p
5     while y ≠ NIL and x == y.right
6         x = y
7         y = y.p
8     return y
```

left child is also an ancestor of x. In Figure 12.2(d), the successor of the node with key 13 is the node with key 15. To find y, go up the tree from x until you encounter either the root or a node that is the left child of its parent. Lines 4–8 of TREE-SUCCESSOR handle this case.

The running time of TREE-SUCCESSOR on a tree of height h is O(h), since it either follows a simple path up the tree or follows a simple path down the tree. The procedure TREE-PREDECESSOR, which is symmetric to TREE-SUCCESSOR, also runs in O(h) time.

In summary, we have proved the following theorem.

#### *Theorem 12.2*

The dynamic-set operations SEARCH, MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR can be implemented so that each one runs in O(h) time on a binary search tree of height h.

#### **Exercises**

#### *12.2-1*

You are searching for the number 363 in a binary search tree containing numbers between 1 and 1000. Which of the following sequences *cannot* be the sequence of nodes examined?

```
a. 2, 252, 401, 398, 330, 344, 397, 363.
```

*b.* 924, 220, 911, 244, 898, 258, 362, 363.

```
c. 925, 202, 911, 240, 912, 245, 363.
```

*d.* 2, 399, 387, 219, 266, 382, 381, 278, 363.

*e.* 935, 278, 347, 621, 299, 392, 358, 363.

### *12.2-2*

Write recursive versions of TREE-MINIMUM and TREE-MAXIMUM.

### *12.2-3*

Write the TREE-PREDECESSOR procedure.

### *12.2-4*

Professor Kilmer claims to have discovered a remarkable property of binary search trees. Suppose that the search for key k in a binary search tree ends up at a leaf. Consider three sets: A, the keys to the left of the search path; B, the keys on the search path; and C, the keys to the right of the search path. Professor Kilmer claims that any three keys a ∈ A, b ∈ B, and c ∈ C must satisfy a ≤ b ≤ c. Give a smallest possible counterexample to the professor's claim.

#### *12.2-5*

Show that if a node in a binary search tree has two children, then its successor has no left child and its predecessor has no right child.

### *12.2-6*

Consider a binary search tree T whose keys are distinct. Show that if the right subtree of a node x in T is empty and x has a successor y, then y is the lowest ancestor of x whose left child is also an ancestor of x. (Recall that every node is its own ancestor.)

### *12.2-7*

An alternative method of performing an inorder tree walk of an n-node binary search tree finds the minimum element in the tree by calling TREE-MINIMUM and then making n - 1 calls to TREE-SUCCESSOR. Prove that this algorithm runs in Θ(n) time.

### *12.2-8*

Prove that no matter what node you start at in a height-h binary search tree, k successive calls to TREE-SUCCESSOR take O(k + h) time.

#### *12.2-9*

Let T be a binary search tree whose keys are distinct, let x be a leaf node, and let y be its parent. Show that y:*key* is either the smallest key in T larger than x:*key* or the largest key in T smaller than x:*key*.

### **12.3 Insertion and deletion**

The operations of insertion and deletion cause the dynamic set represented by a binary search tree to change. The data structure must be modified to reflect this change, but in such a way that the binary-search-tree property continues to hold. We'll see that modifying the tree to insert a new element is relatively straightforward, but deleting a node from a binary search tree is more complicated.

### **Insertion**

The TREE-INSERT procedure inserts a new node into a binary search tree. The procedure takes a binary search tree T and a node z for which z.key has already been filled in, z.left = NIL, and z.right = NIL. It modifies T and some of the attributes of z so as to insert z into an appropriate position in the tree.

```
TREE-INSERT(T, z)
1 x = T.root // node being compared with z
2 y = NIL // y will be parent of z
3 while x ≠ NIL // descend until reaching a leaf
4     y = x
5     if z.key < x.key
6         x = x.left
7     else x = x.right
8 z.p = y // found the location—insert z with parent y
9 if y == NIL
10     T.root = z // tree T was empty
11 elseif z.key < y.key
12     y.left = z
13 else y.right = z
```

Figure 12.3 shows how TREE-INSERT works. Just like the procedures TREE-SEARCH and ITERATIVE-TREE-SEARCH, TREE-INSERT begins at the root of the tree and the pointer x traces a simple path downward looking for a NIL to replace with the input node z. The procedure maintains the *trailing pointer* y as the parent of x. After initialization, the **while** loop in lines 3–7 causes these two pointers to move down the tree, going left or right depending on the comparison of z.key with x.key, until x becomes NIL. This NIL occupies the position where node z will go. More precisely, this NIL is a *left* or *right* attribute of the node that will become z's parent, or it is T.root if tree T is currently empty. The procedure needs the