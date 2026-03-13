---
topic: disjoint_set_linked_list
pages: 545-548
---

**Figure 19.2 (a)** Linked-list representations of two sets. Set S₁ contains members d, f, and g, with representative f, and set S₂ contains members b, c, e, and h, with representative c. Each object in the list contains a set member, a pointer to the next object in the list, and a pointer back to the set object. Each set object has pointers *head* and *tail* to the first and last objects, respectively. **(b)** The result of UNION(g, e), which appends the linked list containing e to the linked list containing g. The representative of the resulting set is f. The set object for e's list, S₂, is destroyed.

#### **A simple implementation of union**

The simplest implementation of the UNION operation using the linked-list set representation takes significantly more time than MAKE-SET or FIND-SET. As Figure 19.2(b) shows, the operation UNION(x, y) appends y's list onto the end of x's list. The representative of x's list becomes the representative of the resulting set. To quickly find where to append y's list, use the *tail* pointer for x's list. Because all members of y's list join x's list, the UNION operation destroys the set object for y's list. The UNION operation is where this implementation pays the price for FIND-SET taking constant time: UNION must also update the pointer to the set object for each object originally on y's list, which takes time linear in the length of y's list. In Figure 19.2, for example, the operation UNION(g, e) causes pointers to be updated in the objects for b, c, e, and h.

In fact, we can construct a sequence of m operations on n objects that requires Θ(n²) time. Starting with objects x₁, x₂, ..., xₙ, execute the sequence of n MAKE-SET operations followed by n − 1 UNION operations shown in Figure 19.3, so that m = 2n − 1. The n MAKE-SET operations take Θ(n) time. Because the ith UNION operation updates i objects, the total number of objects updated by all n − 1 UNION operations forms an arithmetic series:

| Operation       | Number of objects updated |
|-----------------|---------------------------|
| MAKE-SET(x₁)    | 1                         |
| MAKE-SET(x₂)    | 1                         |
| .               | .                         |
| .               | .                         |
| .               | .                         |
| MAKE-SET(xₙ)    | 1                         |
| UNION(x₂, x₁)   | 1                         |
| UNION(x₃, x₂)   | 2                         |
| UNION(x₄, x₃)   | 3                         |
| .               | .                         |
| .               | .                         |
| .               | .                         |
| UNION(xₙ, xₙ₋₁) | n − 1                   |

**Figure 19.3** A sequence of 2n − 1 operations on n objects that takes Θ(n²) time, or Θ(n) time per operation on average, using the linked-list set representation and the simple implementation of UNION.

$$\sum_{i=1}^{n-1} i = \Theta(n^2) .$$

The total number of operations is 2n − 1, and so each operation on average requires Θ(n) time. That is, the amortized time of an operation is Θ(n).

### **A weighted-union heuristic**

In the worst case, the above implementation of UNION requires an average of Θ(n) time per call, because it might be appending a longer list onto a shorter list, and the procedure must update the pointer to the set object for each member of the longer list. Suppose instead that each list also includes the length of the list (which can be maintained straightforwardly with constant overhead) and that the UNION procedure always appends the shorter list onto the longer, breaking ties arbitrarily. With this simple *weighted-union heuristic*, a single UNION operation can still take Ω(n) time if both sets have Ω(n) members. As the following theorem shows, however, a sequence of m MAKE-SET, UNION, and FIND-SET operations, n of which are MAKE-SET operations, takes O(m + n lg n) time.

#### *Theorem 19.1*

Using the linked-list representation of disjoint sets and the weighted-union heuristic, a sequence of m MAKE-SET, UNION, and FIND-SET operations, n of which are MAKE-SET operations, takes O(m + n lg n) time.

*Proof* Because each UNION operation unites two disjoint sets, at most n − 1 UNION operations occur over all. We now bound the total time taken by these

UNION operations. We start by determining, for each object, an upper bound on the number of times the object's pointer back to its set object is updated. Consider a particular object x. Each time x's pointer is updated, x must have started in the smaller set. The first time x's pointer is updated, therefore, the resulting set must have at least 2 members. Similarly, the next time x's pointer is updated, the resulting set must have had at least 4 members. Continuing on, for any k ≤ n, after x's pointer has been updated ⌈lg k⌉ times, the resulting set must have at least k members. Since the largest set has at most n members, each object's pointer is updated at most ceil(lg n) times over all the UNION operations. Thus the total time spent updating object pointers over all UNION operations is O(n lg n). We must also account for updating the *tail* pointers and the list lengths, which take only Θ(1) time per UNION operation. The total time spent in all UNION operations is thus O(n lg n).

The time for the entire sequence of m operations follows. Each MAKE-SET and FIND-SET operation takes O(1) time, and there are O(m) of them. The total time for the entire sequence is thus O(m + n lg n).

#### **Exercises**

# *19.2-1*

Write pseudocode for MAKE-SET, FIND-SET, and UNION using the linked-list representation and the weighted-union heuristic. Make sure to specify the attributes that you assume for set objects and list objects.

# *19.2-2*

Show the data structure that results and the answers returned by the FIND-SET operations in the following program. Use the linked-list representation with the weighted-union heuristic. Assume that if the sets containing xᵢ and xⱼ have the same size, then the operation UNION(xᵢ, xⱼ) appends xⱼ's list onto xᵢ's list.

```
1 for i = 1 to 16
2     MAKE-SET(xᵢ)
3 for i = 1 to 15 by 2
4     UNION(xᵢ, xᵢ₊₁)
5 for i = 1 to 13 by 4
6     UNION(xᵢ, xᵢ₊₂)
7 UNION(x₁, x₅)
8 UNION(x₁₁, x₁₃)
9 UNION(x₁, x₁₀)
10 FIND-SET(x₂)
11 FIND-SET(x₉)
```

# *19.2-3*

Adapt the aggregate proof of Theorem 19.1 to obtain amortized time bounds of O(1) for MAKE-SET and FIND-SET and O(lg n) for UNION using the linked-list representation and the weighted-union heuristic.

# *19.2-4*

Give a tight asymptotic bound on the running time of the sequence of operations in Figure 19.3 assuming the linked-list representation and the weighted-union heuristic.

# *19.2-5*

Professor Gompers suspects that it might be possible to keep just one pointer in each set object, rather than two (*head* and *tail*), while keeping the number of pointers in each list element at two. Show that the professor's suspicion is well founded by describing how to represent each set by a linked list such that each operation has the same running time as the operations described in this section. Describe also how the operations work. Your scheme should allow for the weighted-union heuristic, with the same effect as described in this section. (*Hint:* Use the tail of a linked list as its set's representative.)

### *19.2-6*

Suggest a simple change to the UNION procedure for the linked-list representation that removes the need to keep the *tail* pointer to the last object in each list. Regardless of whether the weighted-union heuristic is used, your change should not change the asymptotic running time of the UNION procedure. (*Hint:* Rather than appending one list to another, splice them together.)

# **19.3 Disjoint-set forests**

A faster implementation of disjoint sets represents sets by rooted trees, with each node containing one member and each tree representing one set. In a *disjoint-set forest*, illustrated in Figure 19.4(a), each member points only to its parent. The root of each tree contains the representative and is its own parent. As we'll see, although the straightforward algorithms that use this representation are no faster than ones that use the linked-list representation, two heuristics—"union by rank" and "path compression"—yield an asymptotically optimal disjoint-set data structure.

The three disjoint-set operations have simple implementations. A MAKE-SET operation simply creates a tree with just one node. A FIND-SET operation follows parent pointers until it reaches the root of the tree. The nodes visited on this sim-