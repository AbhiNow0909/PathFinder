---
topic: b_tree_deletion
pages: 535-541
---

**Figure 18.8** Deleting keys from a B-tree. The minimum degree for this B-tree is t = 3, so that, other than the root, every node must have at least 2 keys. Blue nodes are those that are modified by the deletion process. **(a)** The B-tree of Figure 18.7(e). **(b)** Deletion of F, which is case 1: simple deletion from a leaf when all nodes visited during the search (other than the root) have at least t = 3 keys. **(c)** Deletion of M, which is case 2a: the predecessor L of M moves up to take M's position.

*Case 1: The search arrives at a leaf node* x*.* If x contains key k, then delete k from x. If x does not contain key k, then k was not in the B-tree and nothing else needs to be done.

*Case 2: The search arrives at an internal node* x *that contains key* k*.* Let k = x.key_i. One of the following three cases applies, depending on the number of keys in x.c_i (the child of x that precedes k) and x.c_{i+1} (the child of x that follows k).

*Case 2a:* x.c_i *has at least* t *keys.* Find the predecessor k' of k in the subtree rooted at x.c_i. Recursively delete k' from x.c_i, and replace k by k' in x. (Key k' can be found and deleted in a single downward pass.)

*Case 2b:* x.c_i *has t - 1 keys and* x.c_{i+1} *has at least* t *keys.* This case is symmetric to case 2a. Find the successor k' of k in the subtree rooted at x.c_{i+1}.

**Figure 18.8, continued (d)** Deletion of G, which is case 2c: push G down to make node DEGJK and then delete G from this leaf (case 1). **(e)** Deletion of D, which is case 3b: since the recursion cannot descend to node CL because it has only 2 keys, push P down and merge it with CL and TX to form CLPTX. Then delete D from a leaf (case 1). **(e'**)** After (e), delete the empty root. The tree shrinks in height by 1. **(f)** Deletion of B, which is case 3a: C moves to fill B's position and E moves to fill C's position.

Recursively delete k' from x.c_{i+1}, and replace k by k' in x. (Again, finding and deleting k' can be done in a single downward pass.)

*Case 2c: Both* x.c_i *and* x.c_{i+1} *have t - 1 keys.* Merge k and all of x.c_{i+1} into x.c_i, so that x loses both k and the pointer to x.c_{i+1}, and x.c_i now contains 2t - 1 keys. Then free x.c_{i+1} and recursively delete k from x.c_i.

*Case 3: The search arrives at an internal node* x *that does not contain key* k*.*  Continue searching down the tree while ensuring that each node visited has at least t keys. To do so, determine the root x.c_i of the appropriate subtree that must contain k, if k is in the tree at all. If x.c_i has only t - 1 keys, execute case 3a or 3b as necessary to guarantee descending to a node containing at least t keys. Then finish by recursing on the appropriate child of x.

*Case 3a:* x.c_i *has only t - 1 keys but has an immediate sibling with at least* t *keys.* Give x.c_i an extra key by moving a key from x down into x.c_i, moving a key from x.c_i's immediate left or right sibling up into x, and moving the appropriate child pointer from the sibling into x.c_i.

*Case 3b:* x.c_i *and each of* x.c_i*'s immediate siblings have t - 1 keys.* (It is possible for x.c_i to have either one or two siblings.) Merge x.c_i with one sibling, which involves moving a key from x down into the new merged node to become the median key for that node.

In cases 2c and 3b, if node x is the root, it could end up having no keys. When this situation occurs, then x is deleted, and x's only child x.c_1 becomes the new root of the tree. This action decreases the height of the tree by one and preserves the property that the root of the tree contains at least one key (unless the tree is empty).

Since most of the keys in a B-tree are in the leaves, deletion operations often end up deleting keys from leaves. The B-TREE-DELETE procedure then acts in one downward pass through the tree, without having to back up. When deleting a key in an internal node x, however, the procedure might make a downward pass through the tree to find the key's predecessor or successor and then return to node x to replace the key with its predecessor or successor (cases 2a and 2b). Returning to node x does not require a traversal through all the levels between x and the node containing the predecessor or successor, however, since the procedure can just keep a pointer to x and the key position within x and put the predecessor or successor key directly there.

Although this procedure seems complicated, it involves only O(h) disk operations for a B-tree of height h, since only O(1) calls to DISK-READ and DISK-WRITE are made between recursive invocations of the procedure. The CPU time required is O(th) = O(t log_t n).

#### **Exercises**

#### *18.3-1*

Show the results of deleting C, P, and V, in order, from the tree of Figure 18.8(f).

# *18.3-2*

Write pseudocode for B-TREE-DELETE.

# **Problems**

#### *18-1 Stacks on secondary storage*

Consider implementing a stack in a computer that has a relatively small amount of fast primary memory and a relatively large amount of slower disk storage. The operations PUSH and POP work on single-word values. The stack can grow to be much larger than can fit in memory, and thus most of it must be stored on disk.

A simple, but inefficient, stack implementation keeps the entire stack on disk. Maintain in memory a stack pointer, which is the disk address of the top element on the stack. Indexing block numbers and word offsets within blocks from 0, if the pointer has value p, the top element is the (p mod m)th word on block ⌊p/m⌋ of the disk, where m is the number of words per block.

To implement the PUSH operation, increment the stack pointer, read the appropriate block into memory from disk, copy the element to be pushed to the appropriate word on the block, and write the block back to disk. A POP operation is similar. Read in the appropriate block from disk, save the top of the stack, decrement the stack pointer, and return the saved value. You need not write back the block, since it was not modified, and the word in the block that contained the popped value is ignored.

As in the analyses of B-tree operations, two costs matter: the total number of disk accesses and the total CPU time. A disk access also incurs a cost in CPU time. In particular, any disk access to a block of m words incurs charges of one disk access and Θ(m) CPU time.

*a.* Asymptotically, what is the worst-case number of disk accesses for n stack operations using this simple implementation? What is the CPU time for n stack operations? Express your answer in terms of m and n for this and subsequent parts.

Now consider a stack implementation in which you keep one block of the stack in memory. (You also maintain a small amount of memory to record which block is currently in memory.) You can perform a stack operation only if the relevant disk block resides in memory. If necessary, you can write the block currently in memory to the disk and read the new block from the disk into memory. If the relevant disk block is already in memory, then no disk accesses are required.

- *b.* What is the worst-case number of disk accesses required for n PUSH operations? What is the CPU time?
- *c.* What is the worst-case number of disk accesses required for n stack operations? What is the CPU time?

Suppose that you now implement the stack by keeping two blocks in memory (in addition to a small number of words for bookkeeping).

*d.* Describe how to manage the stack blocks so that the amortized number of disk accesses for any stack operation is O(1/m) and the amortized CPU time for any stack operation is O(1).

#### *18-2 Joining and splitting 2-3-4 trees*

The *join* operation takes two dynamic sets S' and S'' and an element x such that x'.key < x.key < x''.key for any x' ∈ S' and x'' ∈ S''. It returns a set S = S' ∪ {x} ∪ S''. The *split* operation is like an "inverse" join: given a dynamic set S and an element x ∈ S, it creates a set S' that consists of all elements in S - {x} whose keys are less than x.key and another set S'' that consists of all elements in S - {x} whose keys are greater than x.key. This problem investigates how to implement these operations on 2-3-4 trees (B-trees with t = 2). Assume for convenience that elements consist only of keys and that all key values are distinct.

- *a.* Show how to maintain, for every node x of a 2-3-4 tree, the height of the subtree rooted at x as an attribute x.height. Make sure that your implementation does not affect the asymptotic running times of searching, insertion, and deletion.
- *b.* Show how to implement the join operation. Given two 2-3-4 trees T' and T'' and a key k, the join operation should run in O(1 + |h' - h''|) time, where h' and h'' are the heights of T' and T'', respectively.
- *c.* Consider the simple path p from the root of a 2-3-4 tree T to a given key k, the set S' of keys in T that are less than k, and the set S'' of keys in T that are greater than k. Show that p breaks S' into a set of trees {T'_0, T'_1, ..., T'_m} and a set of keys {k'_1, k'_2, ..., k'_m} such that y < k'_i < z for i = 1, 2, ..., m and any keys y ∈ T'_{i-1} and z ∈ T'_i. What is the relationship between the heights of T'_{i-1} and T'_i? Describe how p breaks S'' into sets of trees and keys.
- *d.* Show how to implement the split operation on T. Use the join operation to assemble the keys in S' into a single 2-3-4 tree T' and the keys in S'' into a single 2-3-4 tree T''. The running time of the split operation should be O(lg n), where n is the number of keys in T. (*Hint:* The costs for joining should telescope.)

# **Chapter notes**

Knuth [261], Aho, Hopcroft, and Ullman [5], and Sedgewick and Wayne [402] give further discussions of balanced-tree schemes and B-trees. Comer [99] provides a comprehensive survey of B-trees. Guibas and Sedgewick [202] discuss the relationships among various kinds of balanced-tree schemes, including red-black trees and 2-3-4 trees.

In 1970, J. E. Hopcroft invented 2-3 trees, a precursor to B-trees and 2-3-4 trees, in which every internal node has either two or three children. Bayer and McCreight [39] introduced B-trees in 1972 with no explanation of their choice of name.

Bender, Demaine, and Farach-Colton [47] studied how to make B-trees perform well in the presence of memory-hierarchy effects. Their *cache-oblivious* algorithms work efficiently without explicitly knowing the data transfer sizes within the memory hierarchy.

# **19 Data Structures for Disjoint Sets**

Some applications involve grouping n distinct elements into a collection of disjoint sets—sets with no elements in common. These applications often need to perform two operations in particular: finding the unique set that contains a given element and uniting two sets. This chapter explores methods for maintaining a data structure that supports these operations.

Section 19.1 describes the operations supported by a disjoint-set data structure and presents a simple application. Section 19.2 looks at a simple linked-list implementation for disjoint sets. Section 19.3 presents a more efficient representation using rooted trees. The running time using the tree representation is theoretically superlinear, but for all practical purposes it is linear. Section 19.4 defines and discusses a very quickly growing function and its very slowly growing inverse, which appears in the running time of operations on the tree-based implementation, and then, by a complex amortized analysis, proves an upper bound on the running time that is just barely superlinear.

# **19.1 Disjoint-set operations**

A *disjoint-set data structure* maintains a collection S = {S_1, S_2, ..., S_k} of disjoint dynamic sets. To identify each set, choose a *representative*, which is some member of the set. In some applications, it doesn't matter which member is used as the representative; it matters only that if you ask for the representative of a dynamic set twice without modifying the set between the requests, you get the same answer both times. Other applications may require a prespecified rule for choosing the representative, such as choosing the smallest member in the set (for a set whose elements can be ordered).