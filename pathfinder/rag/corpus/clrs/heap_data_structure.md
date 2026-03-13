---
topic: heap_data_structure
pages: 183-185
---

**Figure 6.1** A max-heap viewed as **(a)** a binary tree and **(b)** an array. The number within the circle at each node in the tree is the value stored at that node. The number above a node is the corresponding index in the array. Above and below the array are lines showing parent-child relationships, with parents always to the left of their children. The tree has height 3, and the node at index 4 (with value 8) has height 1.

there's a simple way to compute the indices of its parent, left child, and right child with the one-line procedures PARENT, LEFT, and RIGHT.

```
PARENT(i)
1 return ⌊i/2⌋
LEFT(i)
1 return 2i
RIGHT(i)
1 return 2i + 1
```

On most computers, the LEFT procedure can compute 2i in one instruction by simply shifting the binary representation of i left by one bit position. Similarly, the RIGHT procedure can quickly compute 2i+1 by shifting the binary representation of i left by one bit position and then adding 1. The PARENT procedure can compute ⌊i/2⌋ by shifting i right one bit position. Good implementations of heapsort often implement these procedures as macros or inline procedures.

There are two kinds of binary heaps: max-heaps and min-heaps. In both kinds, the values in the nodes satisfy a *heap property*, the specifics of which depend on the kind of heap. In a *max-heap*, the *max-heap property* is that for every node i other than the root,

```
A[PARENT(i)] ≥ A[i] ;
```

*6.1 Heaps 163* 

that is, the value of a node is at most the value of its parent. Thus, the largest element in a max-heap is stored at the root, and the subtree rooted at a node contains values no larger than that contained at the node itself. A *min-heap* is organized in the opposite way: the *min-heap property* is that for every node i other than the root,

A[PARENT(i)] ≤ A[i] .

The smallest element in a min-heap is at the root.

The heapsort algorithm uses max-heaps. Min-heaps commonly implement priority queues, which we discuss in Section 6.5. We'll be precise in specifying whether we need a max-heap or a min-heap for any particular application, and when properties apply to either max-heaps or min-heaps, we just use the term "heap."

Viewing a heap as a tree, we define the *height* of a node in a heap to be the number of edges on the longest simple downward path from the node to a leaf, and we define the height of the heap to be the height of its root. Since a heap of n elements is based on a complete binary tree, its height is Θ(lg n) (see Exercise 6.1-2). As we'll see, the basic operations on heaps run in time at most proportional to the height of the tree and thus take O(lg n) time. The remainder of this chapter presents some basic procedures and shows how they are used in a sorting algorithm and a priority-queue data structure.

- The MAX-HEAPIFY procedure, which runs in O(lg n) time, is the key to maintaining the max-heap property.
- The BUILD-MAX-HEAP procedure, which runs in linear time, produces a maxheap from an unordered input array.
- The HEAPSORT procedure, which runs in O(n lg n) time, sorts an array in place.
- The procedures MAX-HEAP-INSERT, MAX-HEAP-EXTRACT-MAX, MAX-HEAP-INCREASE-KEY, and MAX-HEAP-MAXIMUM allow the heap data structure to implement a priority queue. They run in O(lg n) time plus the time for mapping between objects being inserted into the priority queue and indices in the heap.

### **Exercises**

### *6.1-1*

What are the minimum and maximum numbers of elements in a heap of height h?

## *6.1-2*

Show that an n-element heap has height floor(lg n).

## *6.1-3*

Show that in any subtree of a max-heap, the root of the subtree contains the largest value occurring anywhere in that subtree.

## *6.1-4*

Where in a max-heap might the smallest element reside, assuming that all elements are distinct?

## *6.1-5*

At which levels in a max-heap might the kth largest element reside, for 2 ≤ k ≤ ⌊n/2⌋, assuming that all elements are distinct?

## *6.1-6*

Is an array that is in sorted order a min-heap?

## *6.1-7*

Is the array with values ⟨33, 19, 20, 15, 13, 10, 2, 13, 16, 12⟩ a max-heap?

### *6.1-8*

Show that, with the array representation for storing an n-element heap, the leaves are the nodes indexed by ⌊n/2⌋+1, ⌊n/2⌋+2, ..., n.

## **6.2 Maintaining the heap property**

The procedure MAX-HEAPIFY on the facing page maintains the max-heap property. Its inputs are an array A with the *heap-size* attribute and an index i into the array. When it is called, MAX-HEAPIFY assumes that the binary trees rooted at LEFT(i) and RIGHT(i) are max-heaps, but that A[i] might be smaller than its children, thus violating the max-heap property. MAX-HEAPIFY lets the value at A[i] "float down" in the max-heap so that the subtree rooted at index i obeys the maxheap property.

Figure 6.2 illustrates the action of MAX-HEAPIFY. Each step determines the largest of the elements A[i], A[LEFT(i)], and A[RIGHT(i)] and stores the index of the largest element in *largest*. If A[i] is largest, then the subtree rooted at node i is already a max-heap and nothing else needs to be done. Otherwise, one of the two children contains the largest element. Positions i and *largest* swap their contents, which causes node i and its children to satisfy the max-heap property. The node indexed by *largest*, however, just had its value decreased, and thus the subtree rooted at *largest* might violate the max-heap property. Consequently, MAX-HEAPIFY calls itself recursively on that subtree.