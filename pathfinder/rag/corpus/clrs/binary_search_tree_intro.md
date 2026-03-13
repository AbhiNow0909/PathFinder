---
topic: binary_search_tree_intro
pages: 334-337
---

**Figure 12.1** Binary search trees. For any node x, the keys in the left subtree of x are at most x.key, and the keys in the right subtree of x are at least x.key. Different binary search trees can represent the same set of values. The worst-case running time for most search-tree operations is proportional to the height of the tree. **(a)** A binary search tree on 6 nodes with height 2. The top figure shows how to view the tree conceptually, and the bottom figure shows the *left*, *right*, and p attributes in each node, in the style of Figure 10.6 on page 266. **(b)** A less efficient binary search tree, with height 4, that contains the same keys.

that points to the root node, or NIL if the tree is empty. The root node T.root is the only node in a tree T whose parent is NIL.

The keys in a binary search tree are always stored in such a way as to satisfy the *binary-search-tree property*:

Let x be a node in a binary search tree. If y is a node in the left subtree of x, then y.key ≤ x.key. If y is a node in the right subtree of x, then y.key ≥ x.key.

Thus, in Figure 12.1(a), the key of the root is 6, the keys 2, 5, and 5 in its left subtree are no larger than 6, and the keys 7 and 8 in its right subtree are no smaller than 6. The same property holds for every node in the tree. For example, looking at the root's left child as the root of a subtree, this subtree root has the key 5, the key 2 in its left subtree is no larger than 5, and the key 5 in its right subtree is no smaller than 5.

Because of the binary-search-tree property, you can print out all the keys in a binary search tree in sorted order by a simple recursive algorithm, called an *inorder tree walk*, given by the procedure INORDER-TREE-WALK. This algorithm is so named because it prints the key of the root of a subtree between printing the values in its left subtree and printing those in its right subtree. (Similarly, a *preorder tree walk* prints the root before the values in either subtree, and a *postorder tree walk* prints the root after the values in its subtrees.) To print all the elements in a binary search tree T, call INORDER-TREE-WALK(T.root). For example, the inorder tree walk prints the keys in each of the two binary search trees from Figure 12.1 in the order 2; 5; 5; 6; 7; 8. The correctness of the algorithm follows by induction directly from the binary-search-tree property.

```
INORDER-TREE-WALK(x)
1 if x ≠ NIL
2 INORDER-TREE-WALK(x.left)
3 print x.key
4 INORDER-TREE-WALK(x.right)
```

It takes Θ(n) time to walk an n-node binary search tree, since after the initial call, the procedure calls itself recursively exactly twice for each node in the tree—once for its left child and once for its right child. The following theorem gives a formal proof that it takes linear time to perform an inorder tree walk.

#### *Theorem 12.1*

If x is the root of an n-node subtree, then the call INORDER-TREE-WALK(x) takes Θ(n) time.

*Proof* Let T(n) denote the time taken by INORDER-TREE-WALK when it is called on the root of an n-node subtree. Since INORDER-TREE-WALK visits all n nodes of the subtree, we have T(n) = Ω(n). It remains to show that T(n) = O(n).

Since INORDER-TREE-WALK takes a small, constant amount of time on an empty subtree (for the test x ≠ NIL), we have T(0) = c for some constant c > 0.

For n > 0, suppose that INORDER-TREE-WALK is called on a node x whose left subtree has k nodes and whose right subtree has n - k - 1 nodes. The time to perform INORDER-TREE-WALK(x) is bounded by T(n) ≤ T(k) + T(n - k - 1) + d for some constant d > 0 that reflects an upper bound on the time to execute the body of INORDER-TREE-WALK(x), exclusive of the time spent in recursive calls.

We use the substitution method to show that T(n) = O(n) by proving that T(n) ≤ (c + d)n + c. For n = 0, we have (c + d)·0 + c = c = T(0). For n > 0, we have

$$T(n) \leq T(k) + T(n - k - 1) + d$$

$$\leq ((c + d)k + c) + ((c + d)(n - k - 1) + c) + d$$

$$= (c + d)n + c - (c + d) + c + d$$

$$= (c + d)n + c,$$

which completes the proof.

#### **Exercises**

### *12.1-1*

For the set {1; 4; 5; 10; 16; 17; 21} of keys, draw binary search trees of heights 2, 3, 4, 5, and 6.

#### *12.1-2*

What is the difference between the binary-search-tree property and the min-heap property on page 163? Can the min-heap property be used to print out the keys of an n-node tree in sorted order in O(n) time? Show how, or explain why not.

#### *12.1-3*

Give a nonrecursive algorithm that performs an inorder tree walk. (*Hint:* An easy solution uses a stack as an auxiliary data structure. A more complicated, but elegant, solution uses no stack but assumes that you can test two pointers for equality.)

#### *12.1-4*

Give recursive algorithms that perform preorder and postorder tree walks in Θ(n) time on a tree of n nodes.

### *12.1-5*

Argue that since sorting n elements takes Ω(n lg n) time in the worst case in the comparison model, any comparison-based algorithm for constructing a binary search tree from an arbitrary list of n elements takes Ω(n lg n) time in the worst case.

### **12.2 Querying a binary search tree**

Binary search trees can support the queries MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR, as well as SEARCH. This section examines these operations and shows how to support each one in O(h) time on any binary search tree of height h.

### **Searching**

To search for a node with a given key in a binary search tree, call the TREE-SEARCH procedure. Given a pointer x to the root of a subtree and a key k, TREE-SEARCH(x, k) returns a pointer to a node with key k if one exists in the subtree; otherwise, it returns NIL. To search for key k in the entire binary search tree T, call TREE-SEARCH(T.root, k).

```
TREE-SEARCH(x, k)
1 if x == NIL or k == x.key
2 return x
3 if k < x.key
4 return TREE-SEARCH(x.left, k)
5 else return TREE-SEARCH(x.right, k)
ITERATIVE-TREE-SEARCH(x, k)
1 while x ≠ NIL and k ≠ x.key
2 if k < x.key
3 x = x.left
4 else x = x.right
5 return x
```

The TREE-SEARCH procedure begins its search at the root and traces a simple path downward in the tree, as shown in Figure 12.2(a). For each node x it encounters, it compares the key k with x.key. If the two keys are equal, the search terminates. If k is smaller than x.key, the search continues in the left subtree of x, since the binary-search-tree property implies that k cannot reside in the right subtree. Symmetrically, if k is larger than x.key, the search continues in the right subtree. The nodes encountered during the recursion form a simple path downward from the root of the tree, and thus the running time of TREE-SEARCH is O(h), where h is the height of the tree.