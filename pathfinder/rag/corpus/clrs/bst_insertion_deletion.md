---
topic: bst_insertion_deletion
pages: 343-352
---

**Figure 12.3** Inserting a node with key 13 into a binary search tree. The simple path from the root down to the position where the node is inserted is shown in blue. The new node and the link to its parent are highlighted in orange.

trailing pointer y, because by the time it finds the NIL where z belongs, the search has proceeded one step beyond the node that needs to be changed. Lines 8–13 set the pointers that cause z to be inserted.

Like the other primitive operations on search trees, the procedure TREE-INSERT runs in O(h) time on a tree of height h.

#### **Deletion**

The overall strategy for deleting a node z from a binary search tree T has three basic cases and, as we'll see, one of the cases is a bit tricky.

- If z has no children, then simply remove it by modifying its parent to replace z with NIL as its child.
- If z has just one child, then elevate that child to take z's position in the tree by modifying z's parent to replace z by z's child.
- If z has two children, find z's successor y—which must belong to z's right subtree—and move y to take z's position in the tree. The rest of z's original right subtree becomes y's new right subtree, and z's left subtree becomes y's new left subtree. Because y is z's successor, it cannot have a left child, and y's original right child moves into y's original position, with the rest of y's original right subtree following automatically. This case is the tricky one because, as we'll see, it matters whether y is z's right child.

The procedure for deleting a given node z from a binary search tree T takes as arguments pointers to T and z. It organizes its cases a bit differently from the three cases outlined previously by considering the four cases shown in Figure 12.4.

If z has no left child, then as in part (a) of the figure, replace z by its right child, which may or may not be NIL. When z's right child is NIL, this case deals with

**Figure 12.4** Deleting a node z, in blue, from a binary search tree. Node z may be the root, a left child of node q, or a right child of q. The node that will replace node z in its position in the tree is colored orange. **(a)** Node z has no left child. Replace z by its right child r, which may or may not be NIL. **(b)** Node z has a left child l but no right child. Replace z by l. **(c)** Node z has two children. Its left child is node l, its right child is its successor y (which has no left child), and y's right child is node x. Replace z by y, updating y's left child to become l, but leaving x as y's right child. **(d)** Node z has two children (left child l and right child r), and its successor y ≠ r lies within the subtree rooted at r. First replace y by its own right child x, and set y to be r's parent. Then set y to be q's child and the parent of l.

the situation in which z has no children. When z's right child is non-NIL, this case handles the situation in which z has just one child, which is its right child.

- Otherwise, if z has just one child, then that child is a left child. As in part (b) of the figure, replace z by its left child.
- Otherwise, z has both a left and a right child. Find z's successor y, which lies in z's right subtree and has no left child (see Exercise 12.2-5). Splice node y out of its current location and replace z by y in the tree. How to do so depends on whether y is z's right child:
  - • If y is z's right child, then as in part (c) of the figure, replace z by y, leaving y's right child alone.
  - • Otherwise, y lies within z's right subtree but is not z's right child. In this case, as in part (d) of the figure, first replace y by its own right child, and then replace z by y.

As part of the process of deleting a node, subtrees need to move around within the binary search tree. The subroutine TRANSPLANT replaces one subtree as a child of its parent with another subtree. When TRANSPLANT replaces the subtree rooted at node u with the subtree rooted at node v, node u's parent becomes node v's parent, and u's parent ends up having v as its appropriate child. TRANSPLANT allows v to be NIL instead of a pointer to a node.

```
TRANSPLANT(T, u, v)
1 if u.p == NIL
2     T.root = v
3 elseif u == u.p.left
4     u.p.left = v
5 else u.p.right = v
6 if v ≠ NIL
7     v.p = u.p
```

Here is how TRANSPLANT works. Lines 1–2 handle the case in which u is the root of T. Otherwise, u is either a left child or a right child of its parent. Lines 3–4 take care of updating u.p.left if u is a left child, and line 5 updates u.p.right if u is a right child. Because v may be NIL, lines 6–7 update v.p only if v is non-NIL. The procedure TRANSPLANT does not attempt to update v.left and v.right. Doing so, or not doing so, is the responsibility of TRANSPLANT's caller.

The procedure TREE-DELETE on the facing page uses TRANSPLANT to delete node z from binary search tree T. It executes the four cases as follows. Lines 1–2 handle the case in which node z has no left child (Figure 12.4(a)), and lines 3–4

handle the case in which z has a left child but no right child (Figure 12.4(b)). Lines 5–12 deal with the remaining two cases, in which z has two children. Line 5 finds node y, which is the successor of z. Because z has a nonempty right subtree, its successor must be the node in that subtree with the smallest key; hence the call to TREE-MINIMUM(z.right). As we noted before, y has no left child. The procedure needs to splice y out of its current location and replace z by y in the tree. If y is z's right child (Figure 12.4(c)), then lines 10–12 replace z as a child of its parent by y and replace y's left child by z's left child. Node y retains its right child (x in Figure 12.4(c)), and so no change to y.right needs to occur. If y is not z's right child (Figure 12.4(d)), then two nodes have to move. Lines 7–9 replace y as a child of its parent by y's right child (x in Figure 12.4(c)) and make z's right child (r in the figure) become y's right child instead. Finally, lines 10–12 replace z as a child of its parent by y and replace y's left child by z's left child.

```
TREE-DELETE(T, z)
1 if z.left == NIL
2     TRANSPLANT(T, z, z.right) // replace z by its right child
3 elseif z.right == NIL
4     TRANSPLANT(T, z, z.left) // replace z by its left child
5 else y = TREE-MINIMUM(z.right) // y is z's successor
6     if y ≠ z.right // is y farther down the tree?
7         TRANSPLANT(T, y, y.right) // replace y by its right child
8         y.right = z.right // z's right child becomes
9         y.right.p = y // y's right child
10     TRANSPLANT(T, z, y) // replace z by its successor y
11     y.left = z.left // and give z's left child to y,
12     y.left.p = y // which had no left child
```

Each line of TREE-DELETE, including the calls to TRANSPLANT, takes constant time, except for the call to TREE-MINIMUM in line 5. Thus, TREE-DELETE runs in O(h) time on a tree of height h.

In summary, we have proved the following theorem.

#### *Theorem 12.3*

The dynamic-set operations INSERT and DELETE can be implemented so that each one runs in O(h) time on a binary search tree of height h.

### **Exercises**

### *12.3-1*

Give a recursive version of the TREE-INSERT procedure.

### *12.3-2*

Suppose that you construct a binary search tree by repeatedly inserting distinct values into the tree. Argue that the number of nodes examined in searching for a value in the tree is 1 plus the number of nodes examined when the value was first inserted into the tree.

### *12.3-3*

You can sort a given set of n numbers by first building a binary search tree containing these numbers (using TREE-INSERT repeatedly to insert the numbers one by one) and then printing the numbers by an inorder tree walk. What are the worstcase and best-case running times for this sorting algorithm?

### *12.3-4*

When TREE-DELETE calls TRANSPLANT, under what circumstances can the parameter v of TRANSPLANT be NIL?

### *12.3-5*

Is the operation of deletion "commutative" in the sense that deleting x and then y from a binary search tree leaves the same tree as deleting y and then x? Argue why it is or give a counterexample.

#### *12.3-6*

Suppose that instead of each node x keeping the attribute x.p, pointing to x's parent, it keeps x.succ, pointing to x's successor. Give pseudocode for TREE-SEARCH, TREE-INSERT, and TREE-DELETE on a binary search tree T using this representation. These procedures should operate in O(h) time, where h is the height of the tree T. You may assume that all keys in the binary search tree are distinct. (*Hint:* You might wish to implement a subroutine that returns the parent of a node.)

#### *12.3-7*

When node z in TREE-DELETE has two children, you can choose node y to be its predecessor rather than its successor. What other changes to TREE-DELETE are necessary if you do so? Some have argued that a fair strategy, giving equal priority to predecessor and successor, yields better empirical performance. How might TREE-DELETE be minimally changed to implement such a fair strategy?

### **Problems**

#### *12-1 Binary search trees with equal keys*

Equal keys pose a problem for the implementation of binary search trees.

*a.* What is the asymptotic performance of TREE-INSERT when used to insert n items with identical keys into an initially empty binary search tree?

Consider changing TREE-INSERT to test whether z.key = x.key before line 5 and to test whether z.key = y.key before line 11. If equality holds, implement one of the following strategies. For each strategy, find the asymptotic performance of inserting n items with identical keys into an initially empty binary search tree. (The strategies are described for line 5, which compares the keys of z and x. Substitute y for x to arrive at the strategies for line 11.)

- *b.* Keep a boolean flag x.b at node x, and set x to either x.left or x.right based on the value of x.b, which alternates between FALSE and TRUE each time TREE-INSERT visits x while inserting a node with the same key as x.
- *c.* Keep a list of nodes with equal keys at x, and insert z into the list.
- *d.* Randomly set x to either x.left or x.right. (Give the worst-case performance and informally derive the expected running time.)

#### *12-2 Radix trees*

Given two strings a = a₀a¹...aᵖ and b = b₀b¹...bᵠ, where each aᵢ and each bⱼ belongs to some ordered set of characters, we say that string a is *lexicographically less than* string b if either

- 1. there exists an integer j, where 0 ≤ j ≤ min{p, q}, such that aᵢ = bᵢ for all i = 0, 1, ..., j - 1 and aⱼ < bⱼ, or
- 2. p < q and aᵢ = bᵢ for all i = 0, 1, ..., p.

For example, if a and b are bit strings, then 10100<10110 by rule 1 (letting j = 3) and 10100<101000 by rule 2. This ordering is similar to that used in English-language dictionaries.

The *radix tree* data structure shown in Figure 12.5 (also known as a *trie*) stores the bit strings 1011, 10, 011, 100, and 0. When searching for a key a = a₀a¹...aᵖ, go left at a node of depth i if aᵢ = 0 and right if aᵢ = 1. Let S be a set of distinct bit strings whose lengths sum to n. Show how to use a radix tree to sort S lexicographically in Θ(n) time. For the example in Figure 12.5, the output of the sort should be the sequence 0, 011, 10, 100, 1011.

**Figure 12.5** A radix tree storing the bit strings 1011, 10, 011, 100, and 0. To determine each node's key, traverse the simple path from the root to that node. There is no need, therefore, to store the keys in the nodes. The keys appear here for illustrative purposes only. Keys corresponding to blue nodes are not in the tree. Such nodes are present only to establish a path to other nodes.

### *12-3 Average node depth in a randomly built binary search tree*

A *randomly built binary search tree* on n keys is a binary search tree created by starting with an empty tree and inserting the keys in random order, where each of the n! permutations of the keys is equally likely. In this problem, you will prove that the average depth of a node in a randomly built binary search tree with n nodes is O(lg n). The technique reveals a surprising similarity between the building of a binary search tree and the execution of RANDOMIZED-QUICKSORT from Section 7.3.

Denote the depth of any node x in tree T by d(x, T). Then the *total path length* P(T) of a tree T is the sum, over all nodes x in T, of d(x, T).

*a.* Argue that the average depth of a node in T is

$$\frac{1}{n}\sum_{x\in T}d(x,T)=\frac{1}{n}P(T).$$

Thus, you need to show that the expected value of P(T) is O(n lg n).

*b.* Let T<sup>L</sup> and T<sup>R</sup> denote the left and right subtrees of tree T , respectively. Argue that if T has n nodes, then

$$P(T) = P(T_L) + P(T_R) + n - 1$$
.

*c.* Let P(n) denote the average total path length of a randomly built binary search tree with n nodes. Show that

$$P(n) = \frac{1}{n} \sum_{i=0}^{n-1} (P(i) + P(n-i-1) + n - 1).$$

*d.* Show how to rewrite P(n) as

$$P(n) = \frac{2}{n} \sum_{k=1}^{n-1} P(k) + \Theta(n) .$$

*e.* Recalling the alternative analysis of the randomized version of quicksort given in Problem 7-3, conclude that P(n) = O(n lg n).

Each recursive invocation of randomized quicksort chooses a random pivot element to partition the set of elements being sorted. Each node of a binary search tree partitions the set of elements that fall into the subtree rooted at that node.

*f.* Describe an implementation of quicksort in which the comparisons to sort a set of elements are exactly the same as the comparisons to insert the elements into a binary search tree. (The order in which comparisons are made may differ, but the same comparisons must occur.)

### *12-4 Number of different binary trees*

Let bₙ denote the number of different binary trees with n nodes. In this problem, you will find a formula for bₙ, as well as an asymptotic estimate.

*a.* Show that b₀ = 1 and that, for n ≥ 1,

$$b_n = \sum_{k=0}^{n-1} b_k b_{n-1-k} \ .$$

*b.* Referring to Problem 4-5 on page 121 for the definition of a generating function, let B(x) be the generating function

$$B(x) = \sum_{n=0}^{\infty} b_n x^n .$$

Show that B(x) = xB(x)² + 1, and hence one way to express B(x) in closed form is

$$B(x) = \frac{1}{2x} \left( 1 - \sqrt{1 - 4x} \right) .$$

The *Taylor expansion* of f(x) around the point x = a is given by

$$f(x) = \sum_{k=0}^{\infty} \frac{f^{(k)}(a)}{k!} (x - a)^k ,$$

where fᵏᵏ(x) is the kth derivative of f evaluated at x.

*c.* Show that

$$b_n = \frac{1}{n+1} \binom{2n}{n}$$

(the nth *Catalan number*) by using the Taylor expansion of √(1 - 4x) around x = 0. (If you wish, instead of using the Taylor expansion, you may use the generalization of the binomial theorem, equation (C.4) on page 1181, to noninteger exponents n, where for any real number n and for any integer k, you can interpret (n choose k) to be n(n - 1)...(n - k + 1)/k! if k ≥ 0, and 0 otherwise.)

*d.* Show that

$$b_n = \frac{4^n}{\sqrt{\pi}n^{3/2}} \left(1 + O(1/n)\right).$$

# **13 Red-Black Trees**

Chapter 12 showed that a binary search tree of height h can support any of the basic dynamic-set operations—such as SEARCH, PREDECESSOR, SUCCESSOR, MINIMUM, MAXIMUM, INSERT, and DELETE—in O(h) time. Thus, the set operations are fast if the height of the search tree is small. If its height is large, however, the set operations may run no faster than with a linked list. Red-black trees are one of many search-tree schemes that are "balanced" in order to guarantee that basic dynamic-set operations take O(lg n) time in the worst case.

## **13.1 Properties of red-black trees**

A *red-black tree* is a binary search tree with one extra bit of storage per node: its *color*, which can be either RED or BLACK. By constraining the node colors on any simple path from the root to a leaf, red-black trees ensure that no such path is more than twice as long as any other, so that the tree is approximately *balanced*. Indeed, as we're about to see, the height of a red-black tree with n keys is at most 2 lg(n + 1), which is O(lg n).

Each node of the tree now contains the attributes *color*, *key*, *left*, *right*, and p. If a child or the parent of a node does not exist, the corresponding pointer attribute of the node contains the value NIL. Think of these NILs as pointers to leaves (external nodes) of the binary search tree and the normal, key-bearing nodes as internal nodes of the tree.

A red-black tree is a binary search tree that satisfies the following *red-black properties*:

- 1. Every node is either red or black.
- 2. The root is black.
- 3. Every leaf (NIL) is black.