---
topic: heapsort_algorithm
pages: 192-193
---

**Figure 6.4** The operation of HEAPSORT. **(a)** The max-heap data structure just after BUILD-MAX-HEAP has built it in line 1. **(b)–(j)** The max-heap just after each call of MAX-HEAPIFY in line 5, showing the value of i at that time. Only blue nodes remain in the heap. Tan nodes contain the largest values in the array, in sorted order. **(k)** The resulting sorted array A.

The HEAPSORT procedure takes O(n lg n) time, since the call to BUILD-MAX-HEAP takes O(n) time and each of the n−1 calls to MAX-HEAPIFY takes O(lg n) time.

### **Exercises**

## *6.4-1*

Using Figure 6.4 as a model, illustrate the operation of HEAPSORT on the array A = ⟨5, 13, 2, 25, 7, 17, 20, 8, 4⟩.

## *6.4-2*

Argue the correctness of HEAPSORT using the following loop invariant:

At the start of each iteration of the **for** loop of lines 2–5, the subarray A[1:i] is a max-heap containing the i smallest elements of A[1:n], and the subarray A[i+1:n] contains the n−i largest elements of A[1:n], sorted.

### *6.4-3*

What is the running time of HEAPSORT on an array A of length n that is already sorted in increasing order? How about if the array is already sorted in decreasing order?

### *6.4-4*

Show that the worst-case running time of HEAPSORT is Ω(n lg n).

# ? *6.4-5*

Show that when all the elements of A are distinct, the best-case running time of HEAPSORT is Ω(n lg n).

## **6.5 Priority queues**

In Chapter 8, we will see that any comparison-based sorting algorithm requires Ω(n lg n) comparisons and hence Ω(n lg n) time. Therefore, heapsort is asymptotically optimal among comparison-based sorting algorithms. Yet, a good implementation of quicksort, presented in Chapter 7, usually beats it in practice. Nevertheless, the heap data structure itself has many uses. In this section, we present one of the most popular applications of a heap: as an efficient priority queue. As with heaps, priority queues come in two forms: max-priority queues and min-priority queues. We'll focus here on how to implement max-priority queues, which are in turn based on max-heaps. Exercise 6.5-3 asks you to write the procedures for min-priority queues.