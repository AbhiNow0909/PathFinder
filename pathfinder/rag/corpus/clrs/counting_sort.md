---
topic: counting_sort
pages: 230-232
---

*8.2 Counting sort 209* 

```
COUNTING-SORT(A, n, k)
1 let B[1:n] and C[0:k] be new arrays 
2 for i = 0 to k
3   C[i] = 0
4 for j = 1 to n
5   C[A[j]] = C[A[j]] + 1
6 // C[i] now contains the number of elements equal to i. 
7 for i = 1 to k
8   C[i] = C[i] + C[i - 1]
9 // C[i] now contains the number of elements less than or equal to i. 
10 // Copy A to B, starting from the end of A. 
11 for j = n downto 1
12   B[C[A[j]]] = A[j]
13   C[A[j]] = C[A[j]] - 1 // to handle duplicate values 
14 return B
```

Figure 8.2 illustrates counting sort. After the **for** loop of lines 2-3 initializes the array C to all zeros, the **for** loop of lines 4-5 makes a pass over the array A to inspect each input element. Each time it finds an input element whose value is i, it increments C[i]. Thus, after line 5, C[i] holds the number of input elements equal to i for each integer i = 0, 1, ..., k. Lines 7-8 determine for each i = 0, 1, ..., k how many input elements are less than or equal to i by keeping a running sum of the array C.

Finally, the **for** loop of lines 11-13 makes another pass over A, but in reverse, to place each element A[j] into its correct sorted position in the output array B. If all n elements are distinct, then when line 11 is first entered, for each A[j], the value C[A[j]] is the correct final position of A[j] in the output array, since there are C[A[j]] elements less than or equal to A[j]. Because the elements might not be distinct, the loop decrements C[A[j]] each time it places a value A[j] into B. Decrementing C[A[j]] causes the previous element in A with a value equal to A[j], if one exists, to go to the position immediately before A[j] in the output array B.

How much time does counting sort require? The **for** loop of lines 2-3 takes Θ(k) time, the **for** loop of lines 4-5 takes Θ(n) time, the **for** loop of lines 7-8 takes Θ(k) time, and the **for** loop of lines 11-13 takes Θ(n) time. Thus, the overall time is Θ(k + n). In practice, we usually use counting sort when we have k = O(n), in which case the running time is Θ(n).

Counting sort can beat the lower bound of Ω(n lg n) proved in Section 8.1 because it is not a comparison sort. In fact, no comparisons between input elements occur anywhere in the code. Instead, counting sort uses the actual values of the

**Figure 8.2** The operation of COUNTING-SORT on an input array A[1:8], where each element of A is a nonnegative integer no larger than k = 5. **(a)** The array A and the auxiliary array C after line 5. **(b)** The array C after line 8. **(c)–(e)** The output array B and the auxiliary array C after one, two, and three iterations of the loop in lines 11-13, respectively. Only the tan elements of array B have been filled in. **(f)** The final sorted output array B.

elements to index into an array. The Ω(n lg n) lower bound for sorting does not apply when we depart from the comparison sort model.

An important property of counting sort is that it is *stable*: elements with the same value appear in the output array in the same order as they do in the input array. That is, it breaks ties between two elements by the rule that whichever element appears first in the input array appears first in the output array. Normally, the property of stability is important only when satellite data are carried around with the element being sorted. Counting sort's stability is important for another reason: counting sort is often used as a subroutine in radix sort. As we shall see in the next section, in order for radix sort to work correctly, counting sort must be stable.

### **Exercises**

### *8.2-1*

Using Figure 8.2 as a model, illustrate the operation of COUNTING-SORT on the array A = ⟨6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2⟩.

### *8.2-2*

Prove that COUNTING-SORT is stable.

*8.3 Radix sort 211* 

### *8.2-3*

Suppose that we were to rewrite the **for** loop header in line 11 of the COUNTING-SORT as

# ¹¹ **for** j = 1 **to** n

Show that the algorithm still works properly, but that it is not stable. Then rewrite the pseudocode for counting sort so that elements with the same value are written into the output array in order of increasing index and the algorithm is stable.

### *8.2-4*

Prove the following loop invariant for COUNTING-SORT:

At the start of each iteration of the **for** loop of lines 11-13, the last element in A with value i that has not yet been copied into B belongs in B[C[i]].

### *8.2-5*

Suppose that the array being sorted contains only integers in the range 0 to k and that there are no satellite data to move with those keys. Modify counting sort to use just the arrays A and C, putting the sorted result back into array A instead of into a new array B.

### *8.2-6*

Describe an algorithm that, given n integers in the range 0 to k, preprocesses its input and then answers any query about how many of the n integers fall into a range [a:b] in O(1) time. Your algorithm should use Θ(n + k) preprocessing time.

### *8.2-7*

Counting sort can also work efficiently if the input values have fractional parts, but the number of digits in the fractional part is small. Suppose that you are given n numbers in the range 0 to k, each with at most d decimal (base 10) digits to the right of the decimal point. Modify counting sort to run in Θ(n + 10ᵈk) time.

## **8.3 Radix sort**

*Radix sort* is the algorithm used by the card-sorting machines you now find only in computer museums. The cards have 80 columns, and in each column a machine can punch a hole in one of 12 places. The sorter can be mechanically "programmed" to examine a given column of each card in a deck and distribute the card into one