---
topic: rooted_tree_representation
pages: 287-293
---

**Figure 10.6** The representation of a binary tree T . Each node x has the attributes x:*p* (top), x:*left*  (lower left), and x:*right* (lower right). The *key* attributes are not shown.

**Figure 10.7** The left-child, right-sibling representation of a tree T . Each node x has attributes x:*p*  (top), x:*left*-*child* (lower left), and x:*right*-*sibling* (lower right). The *key* attributes are not shown.

### **Other tree representations**

We sometimes represent rooted trees in other ways. In Chapter 6, for example, we represented a heap, which is based on a complete binary tree, by a single array along with an attribute giving the index of the last node in the heap. The trees that appear in Chapter 19 are traversed only toward the root, and so only the parent pointers are present: there are no pointers to children. Many other schemes are possible. Which scheme is best depends on the application.

## **Exercises**

*10.3-1* Draw the binary tree rooted at index 6 that is represented by the following attributes:

| index | key | left | right |
|-------|-----|------|-------|
| 1     | 17  | 8    | 9     |
| 2     | 14  | NIL  | NIL   |
| 3     | 12  | NIL  | NIL   |
| 4     | 20  | 10   | NIL   |
| 5     | 33  | 2    | NIL   |
| 6     | 15  | 1    | 4     |
| 7     | 28  | NIL  | NIL   |
| 8     | 22  | NIL  | NIL   |
| 9     | 13  | 3    | 7     |
| 10    | 25  | NIL  | 5     |
|       |     |      |       |

## *10.3-2*

Write an O(n)-time recursive procedure that, given an n-node binary tree, prints out the key of each node in the tree.

## *10.3-3*

Write an O(n)-time nonrecursive procedure that, given an n-node binary tree, prints out the key of each node in the tree. Use a stack as an auxiliary data structure.

### *10.3-4*

Write an O(n)-time procedure that prints out all the keys of an arbitrary rooted tree with n nodes, where the tree is stored using the left-child, right-sibling representation.

# ⋆ *10.3-5*

Write an O(n)-time nonrecursive procedure that, given an n-node binary tree, prints out the key of each node. Use no more than constant extra space outside 

of the tree itself and do not modify the tree, even temporarily, during the procedure.

# ⋆ *10.3-6*

The left-child, right-sibling representation of an arbitrary rooted tree uses three pointers in each node: *left*-*child*, *right*-*sibling*, and *parent*. From any node, its parent can be accessed in constant time and all its children can be accessed in time linear in the number of children. Show how to use only two pointers and one boolean value in each node x so that x's parent or all of x's children can be accessed in time linear in the number of x's children.

## **Problems**

## *10-1 Comparisons among lists*

For each of the four types of lists in the following table, what is the asymptotic worst-case running time for each dynamic-set operation listed?

|             | unsorted,<br>singly | sorted,<br>singly | unsorted,<br>doubly | sorted,<br>doubly |
||||||
|             | linked              | linked            | linked              | linked            |
| SEARCH      |                     |                   |                     |                   |
| I NSERT     |                     |                   |                     |                   |
| DELETE      |                     |                   |                     |                   |
| SUCCESSOR   |                     |                   |                     |                   |
| PREDECESSOR |                     |                   |                     |                   |
| MINIMUM     |                     |                   |                     |                   |
| MAXIMUM     |                     |                   |                     |                   |

## *10-2 Mergeable heaps using linked lists*

A *mergeable heap* supports the following operations: MAKE-HEAP (which creates an empty mergeable heap), INSERT, MINIMUM, EXTRACT-MIN, and UNION.¹

¹ Because we have defined a mergeable heap to support MINIMUM and EXTRACT-MIN, we can also refer to it as a *mergeable min-heap*. Alternatively, if it supports MAXIMUM and EXTRACT-MAX, it is a *mergeable max-heap*.

Show how to implement mergeable heaps using linked lists in each of the following cases. Try to make each operation as efficient as possible. Analyze the running time of each operation in terms of the size of the dynamic set(s) being operated on.

- *a.* Lists are sorted.
- *b.* Lists are unsorted.
- *c.* Lists are unsorted, and dynamic sets to be merged are disjoint.

### *10-3 Searching a sorted compact list*

We can represent a singly linked list with two arrays, *key* and *next*. Given the index i of an element, its value is stored in *key*[i], and the index of its successor is given by *next*[i], where *next*[i] = NIL for the last element. We also need the index *head* of the first element in the list. An n-element list stored in this way is *compact* if it is stored only in positions 1 through n of the *key* and *next* arrays.

Let's assume that all keys are distinct and that the compact list is also sorted, that is, *key*[i] < *key*[*next*[i]] for all i = 1, 2, ..., n such that *next*[i] ≠ NIL. Under these assumptions, you will show that the randomized algorithm COMPACT-LIST-SEARCH searches the list for key k in O(√n) expected time.

```
COMPACT-LIST-SEARCH(key, next, head, n, k)
1 i = head 
2 while i ≠ NIL and key[i] < k
3    j = RANDOM(1, n)
4    if key[i] < key[j] and key[j] ≤ k
5       i = j
6    if key[i] == k
7       return i
8    i = next[i]
9 if i == NIL or key[i] > k
10    return NIL 
11 else return i
```

If you ignore lines 3–7 of the procedure, you can see that it's an ordinary algorithm for searching a sorted linked list, in which index i points to each position of the list in turn. The search terminates once the index i "falls off" the end of the list or once *key*[i] ≥ k. In the latter case, if *key*[i] = k, the procedure has found a key with the value k. If, however, *key*[i] > k, then the search will never find a key with the value k, so that terminating the search was the correct action.

Lines 3–7 attempt to skip ahead to a randomly chosen position j. Such a skip helps if *key*[j] is larger than *key*[i] and no larger than k. In such a case, j marks a position in the list that i would reach during an ordinary list search. Because the list is compact, we know that any choice of j between 1 and n indexes some element in the list.

Instead of analyzing the performance of COMPACT-LIST-SEARCH directly, you will analyze a related algorithm, COMPACT-LIST-SEARCH′, which executes two separate loops. This algorithm takes an additional parameter t, which specifies an upper bound on the number of iterations of the first loop.

```
COMPACT-LIST-SEARCH'(key, next, head, n, k, t)
1 i = head 
2 for q = 1 to t
3    j = RANDOM(1, n)
4    if key[i] < key[j] and key[j] ≤ k
5       i = j
6    if key[i] == k
7       return i
8 while i ≠ NIL and key[i] < k
9    i = next[i]
10 if i == NIL or key[i] > k
11    return NIL 
12 else return i
```

To compare the execution of the two algorithms, assume that the sequence of calls of RANDOM(1, n) yields the same sequence of integers for both algorithms.

*a.* Argue that for any value of t, COMPACT-LIST-SEARCH(*key*, *next*, *head*, n, k) and COMPACT-LIST-SEARCH′(*key*, *next*, *head*, n, k, t) return the same result and that the number of iterations of the **while** loop of lines 2–8 in COMPACT-LIST-SEARCH is at most the total number of iterations of both the **for** and **while** loops in COMPACT-LIST-SEARCH′.

In the call COMPACT-LIST-SEARCH′(*key*, *next*, *head*, n, k, t), let Xₜ be the random variable that describes the distance in the linked list (that is, through the chain of *next* pointers) from position i to the desired key k after t iterations of the **for** loop of lines 2–7 have occurred.

- *b.* Argue that COMPACT-LIST-SEARCH′(*key*, *next*, *head*, n, k, t) has an expected running time of O(t + E[Xₜ]).
- *c.* Show that E[Xₜ] = Σᵣ₌₁ⁿ (1 - r/n)ᵗ. (*Hint:* Use equation (C.28) on page 1193.)

- *d.* Show that Σᵣ₌₀ⁿ⁻¹ rᵗ ≤ nᵗ⁺¹/(t + 1). (*Hint:* Use inequality (A.18) on page 1150.)
- *e.* Prove that E[Xₜ] ≤ n/(t + 1).
- *f.* Show that COMPACT-LIST-SEARCH′(*key*, *next*, *head*, n, k, t) has an expected running time of O(t + n/t).
- *g.* Conclude that COMPACT-LIST-SEARCH runs in O(√n) expected time.
- *h.* Why do we assume that all keys are distinct in COMPACT-LIST-SEARCH? Argue that random skips do not necessarily help asymptotically when the list contains repeated key values.

## **Chapter notes**

Aho, Hopcroft, and Ullman [6] and Knuth [259] are excellent references for elementary data structures. Many other texts cover both basic data structures and their implementation in a particular programming language. Examples of these types of textbooks include Goodrich and Tamassia [196], Main [311], Shaffer [406], and Weiss [452, 453, 454]. The book by Gonnet and Baeza-Yates [193] provides experimental data on the performance of many data-structure operations.

The origin of stacks and queues as data structures in computer science is unclear, since corresponding notions already existed in mathematics and paper-based business practices before the introduction of digital computers. Knuth [259] cites A. M. Turing for the development of stacks for subroutine linkage in 1947.

Pointer-based data structures also seem to be a folk invention. According to Knuth, pointers were apparently used in early computers with drum memories. The A-1 language developed by G. M. Hopper in 1951 represented algebraic formulas as binary trees. Knuth credits the IPL-II language, developed in 1956 by A. Newell, J. C. Shaw, and H. A. Simon, for recognizing the importance and promoting the use of pointers. Their IPL-III language, developed in 1957, included explicit stack operations.

# **11 Hash Tables**

Many applications require a dynamic set that supports only the dictionary operations INSERT, SEARCH, and DELETE. For example, a compiler that translates a programming language maintains a symbol table, in which the keys of elements are arbitrary character strings corresponding to identifiers in the language. A hash table is an effective data structure for implementing dictionaries. Although searching for an element in a hash table can take as long as searching for an element in a linked list—Θ(n) time in the worst case—in practice, hashing performs extremely well. Under reasonable assumptions, the average time to search for an element in a hash table is O(1). Indeed, the built-in dictionaries of Python are implemented with hash tables.

A hash table generalizes the simpler notion of an ordinary array. Directly addressing into an ordinary array takes advantage of the O(1) access time for any array element. Section 11.1 discusses direct addressing in more detail. To use direct addressing, you must be able to allocate an array that contains a position for every possible key.

When the number of keys actually stored is small relative to the total number of possible keys, hash tables become an effective alternative to directly addressing an array, since a hash table typically uses an array of size proportional to the number of keys actually stored. Instead of using the key as an array index directly, we *compute* the array index from the key. Section 11.2 presents the main ideas, focusing on "chaining" as a way to handle "collisions," in which more than one key maps to the same array index. Section 11.3 describes how to compute array indices from keys using hash functions. We present and analyze several variations on the basic theme. Section 11.4 looks at "open addressing," which is another way to deal with collisions. The bottom line is that hashing is an extremely effective and practical technique: the basic dictionary operations require only O(1) time on the average. Section 11.5 discusses the hierarchical memory systems of modern computer systems have and illustrates how to design hash tables that work well in such systems.