---
topic: heap_operations
pages: 186-191
---

**Figure 6.2** The action of MAX-HEAPIFY(A, 2), where A.*heap-size* = 10. The node that potentially violates the max-heap property is shown in blue. **(a)** The initial configuration, with A[2] at node i = 2 violating the max-heap property since it is not larger than both children. The max-heap property is restored for node 2 in **(b)** by exchanging A[2] with A[4], which destroys the max-heap property for node 4. The recursive call MAX-HEAPIFY(A, 4) now has i = 4. After A[4] and A[9] are swapped, as shown in **(c)**, node 4 is fixed up, and the recursive call MAX-HEAPIFY(A, 9) yields no further change to the data structure.

```
MAX-HEAPIFY(A, i)
1 l = LEFT(i)
2 r = RIGHT(i)
3 if l ≤ A.heap-size and A[l] > A[i]
4    largest = l
5 else largest = i
6 if r ≤ A.heap-size and A[r] > A[largest]
7    largest = r
8 if largest ≠ i
9    exchange A[i] with A[largest]
10   MAX-HEAPIFY(A, largest)
```

To analyze MAX-HEAPIFY, let T(n) be the worst-case running time that the procedure takes on a subtree of size at most n. For a tree rooted at a given node i, the running time is the Θ(1) time to fix up the relationships among the elements A[i], A[LEFT(i)], and A[RIGHT(i)], plus the time to run MAX-HEAPIFY on a subtree rooted at one of the children of node i (assuming that the recursive call occurs). The children's subtrees each have size at most 2n/3 (see Exercise 6.2-2), and therefore we can describe the running time of MAX-HEAPIFY by the recurrence

$$T(n) \le T(2n/3) + \Theta(1)$$
 (6.1)

The solution to this recurrence, by case 2 of the master theorem (Theorem 4.1 on page 102), is T(n) = O(lg n). Alternatively, we can characterize the running time of MAX-HEAPIFY on a node of height h as O(h).

### **Exercises**

### *6.2-1*

Using Figure 6.2 as a model, illustrate the operation of MAX-HEAPIFY(A, 3) on the array A = ⟨27, 17, 3, 16, 13, 10, 1, 5, 7, 12, 4, 8, 9, 0⟩.

## *6.2-2*

Show that each child of the root of an n-node heap is the root of a subtree containing at most 2n/3 nodes. What is the smallest constant α such that each subtree has at most αn nodes? How does that affect the recurrence (6.1) and its solution?

### *6.2-3*

Starting with the procedure MAX-HEAPIFY, write pseudocode for the procedure MIN-HEAPIFY(A, i), which performs the corresponding manipulation on a minheap. How does the running time of MIN-HEAPIFY compare with that of MAX-HEAPIFY?

### *6.2-4*

What is the effect of calling MAX-HEAPIFY(A, i) when the element A[i] is larger than its children?

### *6.2-5*

What is the effect of calling MAX-HEAPIFY(A, i) for i > A.*heap-size*/2?

### *6.2-6*

The code for MAX-HEAPIFY is quite efficient in terms of constant factors, except possibly for the recursive call in line 10, for which some compilers might produce inefficient code. Write an efficient MAX-HEAPIFY that uses an iterative control construct (a loop) instead of recursion.

## *6.2-7*

Show that the worst-case running time of MAX-HEAPIFY on a heap of size n is Ω(lg n). (*Hint:* For a heap with n nodes, give node values that cause MAX-HEAPIFY to be called recursively at every node on a simple path from the root down to a leaf.)

## **6.3 Building a heap**

The procedure BUILD-MAX-HEAP converts an array A[1:n] into a max-heap by calling MAX-HEAPIFY in a bottom-up manner. Exercise 6.1-8 says that the elements in the subarray A[⌊n/2⌋+1:n] are all leaves of the tree, and so each is a 1-element heap to begin with. BUILD-MAX-HEAP goes through the remaining nodes of the tree and runs MAX-HEAPIFY on each one. Figure 6.3 shows an example of the action of BUILD-MAX-HEAP.

```
BUILD-MAX-HEAP(A, n)
1 A.heap-size = n
2 for i = ⌊n/2⌋ downto 1
3    MAX-HEAPIFY(A, i)
```

To show why BUILD-MAX-HEAP works correctly, we use the following loop invariant:

At the start of each iteration of the **for** loop of lines 2–3, each node i+1, i+2, ..., n is the root of a max-heap.

We need to show that this invariant is true prior to the first loop iteration, that each iteration of the loop maintains the invariant, that the loop terminates, and that the invariant provides a useful property to show correctness when the loop terminates.

**Initialization:** Prior to the first iteration of the loop, i = ⌊n/2⌋. Each node ⌊n/2⌋+1, ⌊n/2⌋+2, ..., n is a leaf and is thus the root of a trivial max-heap.

**Maintenance:** To see that each iteration maintains the loop invariant, observe that the children of node i are numbered higher than i. By the loop invariant, therefore, they are both roots of max-heaps. This is precisely the condition required for the call MAX-HEAPIFY(A, i) to make node i a max-heap root. Moreover, the MAX-HEAPIFY call preserves the property that nodes i+1, i+2, ..., n are all roots of max-heaps. Decrementing i in the **for** loop update reestablishes the loop invariant for the next iteration.

**Figure 6.3** The operation of BUILD-MAX-HEAP, showing the data structure before the call to MAX-HEAPIFY in line 3 of BUILD-MAX-HEAP. The node indexed by i in each iteration is shown in blue. **(a)** A 10-element input array A and the binary tree it represents. The loop index i refers to node 5 before the call MAX-HEAPIFY(A, i). **(b)** The data structure that results. The loop index i for the next iteration refers to node 4. **(c)–(e)** Subsequent iterations of the **for** loop in BUILD-MAX-HEAP. Observe that whenever MAX-HEAPIFY is called on a node, the two subtrees of that node are both max-heaps. **(f)** The max-heap after BUILD-MAX-HEAP finishes.

**Termination:** The loop makes exactly ⌊n/2⌋ iterations, and so it terminates. At termination, i = 0. By the loop invariant, each node 1, 2, ..., n is the root of a max-heap. In particular, node 1 is.

We can compute a simple upper bound on the running time of BUILD-MAX-HEAP as follows. Each call to MAX-HEAPIFY costs O(lg n) time, and BUILD-MAX-HEAP makes O(n) such calls. Thus, the running time is O(n lg n). This upper bound, though correct, is not as tight as it can be.

We can derive a tighter asymptotic bound by observing that the time for MAX-HEAPIFY to run at a node varies with the height of the node in the tree, and that the heights of most nodes are small. Our tighter analysis relies on the properties that an n-element heap has height ⌊lg n⌋ (see Exercise 6.1-2) and at most ⌈n/2^(h+1)⌉ nodes of any height h (see Exercise 6.3-4).

The time required by MAX-HEAPIFY when called on a node of height h is O(h). Letting c be the constant implicit in the asymptotic notation, we can express the total cost of BUILD-MAX-HEAP as being bounded from above by Σ^⌊lg n⌋_{h=0} ⌈n/2^(h+1)⌉ ch. As Exercise 6.3-2 shows, we have ⌈n/2^(h+1)⌉ ≥ 1/2 for 0 ≤ h ≤ ⌊lg n⌋. Since ⌈x⌉ ≤ 2x for any x ≥ 1/2, we have ⌈n/2^(h+1)⌉ ≤ n/2^h. We thus obtain

$$\sum_{h=0}^{\lfloor \lg n \rfloor} \left\lceil \frac{n}{2^{h+1}} \right\rceil ch$$

$$\leq \sum_{h=0}^{\lfloor \lg n \rfloor} \frac{n}{2^h} ch$$

$$= cn \sum_{h=0}^{\lfloor \lg n \rfloor} \frac{h}{2^h}$$

$$\leq cn \sum_{h=0}^{\infty} \frac{h}{2^h}$$

$$\leq cn \cdot \frac{1/2}{(1-1/2)^2} \quad \text{(by equation (A.11) on page 1142 with } x = 1/2)$$

$$= O(n) .$$

Hence, we can build a max-heap from an unordered array in linear time.

To build a min-heap, use the procedure BUILD-MIN-HEAP, which is the same as BUILD-MAX-HEAP but with the call to MAX-HEAPIFY in line 3 replaced by a call to MIN-HEAPIFY (see Exercise 6.2-3). BUILD-MIN-HEAP produces a min-heap from an unordered linear array in linear time.

## **Exercises**

## *6.3-1*

Using Figure 6.3 as a model, illustrate the operation of BUILD-MAX-HEAP on the array A = ⟨5, 3, 17, 10, 84, 19, 6, 22, 9⟩.

## *6.3-2*

Show that ⌈n/2^(h+1)⌉ ≥ 1/2 for 0 ≤ h ≤ ⌊lg n⌋.

## *6.3-3*

Why does the loop index i in line 2 of BUILD-MAX-HEAP decrease from ⌊n/2⌋ to 1 rather than increase from 1 to ⌊n/2⌋?

## *6.3-4*

Show that there are at most ⌈n/2^(h+1)⌉ nodes of height h in any n-element heap.

## **6.4 The heapsort algorithm**

The heapsort algorithm, given by the procedure HEAPSORT, starts by calling the BUILD-MAX-HEAP procedure to build a max-heap on the input array A[1:n]. Since the maximum element of the array is stored at the root A[1], HEAPSORT can place it into its correct final position by exchanging it with A[n]. If the procedure then discards node n from the heap—and it can do so by simply decrementing A.*heap-size*—the children of the root remain max-heaps, but the new root element might violate the max-heap property. To restore the max-heap property, the procedure just calls MAX-HEAPIFY(A, 1), which leaves a max-heap in A[1:n−1]. The HEAPSORT procedure then repeats this process for the max-heap of size n−1 down to a heap of size 2. (See Exercise 6.4-2 for a precise loop invariant.)

```
HEAPSORT(A, n)
1 BUILD-MAX-HEAP(A, n)
2 for i = n downto 2 
3    exchange A[1] with A[i]
4    A.heap-size = A.heap-size − 1
5    MAX-HEAPIFY(A, 1)
```

Figure 6.4 shows an example of the operation of HEAPSORT after line 1 has built the initial max-heap. The figure shows the max-heap before the first iteration of the **for** loop of lines 2–5 and after each iteration.