---
topic: b_tree_definition
pages: 523-525
---

- 1. Every node x has the following attributes:
  - a. x.n, the number of keys currently stored in node x,
  - b. the x.n keys themselves, x.key₁, x.key₂, ..., x.key_{x.n}, stored in monotonically increasing order, so that x.key₁ ≤ x.key₂ ≤ ... ≤ x.key_{x.n},
  - c. x.leaf, a boolean value that is TRUE if x is a leaf and FALSE if x is an internal node.
- 2. Each internal node x also contains x.n + 1 pointers x.c₁, x.c₂, ..., x.c_{x.n+1} to its children. Leaf nodes have no children, and so their c_i attributes are undefined.
- 3. The keys x.key_i separate the ranges of keys stored in each subtree: if k_i is any key stored in the subtree with root x.c_i, then

$$k_1 \le x.key_1 \le k_2 \le x.key_2 \le \dots \le x.key_{x.n} \le k_{x.n+1}$$
.

- 4. All leaves have the same depth, which is the tree's height h.
- 5. Nodes have lower and upper bounds on the number of keys they can contain, expressed in terms of a fixed integer t ≥ 2 called the *minimum degree* of the B-tree:
  - a. Every node other than the root must have at least t - 1 keys. Every internal node other than the root thus has at least t children. If the tree is nonempty, the root must have at least one key.
  - b. Every node may contain at most 2t - 1 keys. Therefore, an internal node may have at most 2t children. We say that a node is *full* if it contains exactly 2t - 1 keys. ³

The simplest B-tree occurs when t = 2. Every internal node then has either 2, 3, or 4 children, and it is a *2-3-4 tree*. In practice, however, much larger values of t yield B-trees with smaller height.

#### **The height of a B-tree**

The number of disk accesses required for most operations on a B-tree is proportional to the height of the B-tree. The following theorem bounds the worst-case height of a B-tree.

³ Another common variant on a B-tree, known as a *B*-tree*, requires each internal node to be at least 2/3 full, rather than at least half full, as a B-tree requires.

**Figure 18.4** A B-tree of height 3 containing a minimum possible number of keys. Shown inside each node x is x.n.

#### *Theorem 18.1*

If n ≥ 1, then for any n-key B-tree T of height h and minimum degree t ≥ 2,

$$h \le \log_t \frac{n+1}{2} .$$

*Proof* By definition, the root of a nonempty B-tree T contains at least one key, and all other nodes contain at least t - 1 keys. Let h be the height of T. Then T contains at least 2 nodes at depth 1, at least 2t nodes at depth 2, at least 2t² nodes at depth 3, and so on, until at depth h, it has at least 2t^{h-1} nodes. Figure 18.4 illustrates such a tree for h = 3. The number n of keys therefore satisfies the inequality

$$n \ge 1 + (t - 1) \sum_{i=1}^{h} 2t^{i-1}$$
  
=  $1 + 2(t - 1) \left(\frac{t^h - 1}{t - 1}\right)$  (by equation (A.6) on page 1142)  
=  $2t^h - 1$ ,

so that t^h ≤ (n + 1)/2. Taking base-t logarithms of both sides proves the theorem.

You can see the power of B-trees as compared with red-black trees. Although the height of the tree grows as O(log n) in both cases (recall that t is a constant), for B-trees the base of the logarithm can be many times larger. Thus, B-trees save a factor of about lg t over red-black trees in the number of nodes examined for most tree operations. Because examining an arbitrary node in a tree usually entails accessing the disk, B-trees avoid a substantial number of disk accesses.

#### **Exercises**

# *18.1-1*

Why isn't a minimum degree of t = 1 allowed?

# *18.1-2*

For what values of t is the tree of Figure 18.1 a legal B-tree?

# *18.1-3*

Show all legal B-trees of minimum degree 2 that store the keys 1; 2; 3; 4; 5.

### *18.1-4*

As a function of the minimum degree t, what is the maximum number of keys that can be stored in a B-tree of height h?

### *18.1-5*

Describe the data structure that results if each black node in a red-black tree absorbs its red children, incorporating their children with its own.

# **18.2 Basic operations on B-trees**

This section presents the details of the operations B-TREE-SEARCH, B-TREE-CREATE, and B-TREE-INSERT. These procedures observe two conventions:

- The root of the B-tree is always in main memory, so that no procedure ever needs to perform a DISK-READ on the root. If any changes to the root node occur, however, then DISK-WRITE must be called on the root.
- Any nodes that are passed as parameters must already have had a DISK-READ operation performed on them.

The procedures are all <one-pass= algorithms that proceed downward from the root of the tree, without having to back up.

#### **Searching a B-tree**

Searching a B-tree is much like searching a binary search tree, except that instead of making a binary, or <two-way,= branching decision at each node, the search