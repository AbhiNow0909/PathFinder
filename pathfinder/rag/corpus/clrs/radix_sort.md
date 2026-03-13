---
topic: radix_sort
pages: 233-236
---

**Figure 8.3** The operation of radix sort on seven 3-digit numbers. The leftmost column is the input. The remaining columns show the numbers after successive sorts on increasingly significant digit positions. Tan shading indicates the digit position sorted on to produce each list from the previous one.

of 12 bins depending on which place has been punched. An operator can then gather the cards bin by bin, so that cards with the first place punched are on top of cards with the second place punched, and so on.

For decimal digits, each column uses only 10 places. (The other two places are reserved for encoding nonnumeric characters.) A d-digit number occupies a field of d columns. Since the card sorter can look at only one column at a time, the problem of sorting n cards on a d-digit number requires a sorting algorithm.

Intuitively, you might sort numbers on their *most significant* (leftmost) digit, sort each of the resulting bins recursively, and then combine the decks in order. Unfortunately, since the cards in 9 of the 10 bins must be put aside to sort each of the bins, this procedure generates many intermediate piles of cards that you would have to keep track of. (See Exercise 8.3-6.)

Radix sort solves the problem of card sorting—counterintuitively—by sorting on the *least significant* digit first. The algorithm then combines the cards into a single deck, with the cards in the 0 bin preceding the cards in the 1 bin preceding the cards in the 2 bin, and so on. Then it sorts the entire deck again on the second-least significant digit and recombines the deck in a like manner. The process continues until the cards have been sorted on all d digits. Remarkably, at that point the cards are fully sorted on the d-digit number. Thus, only d passes through the deck are required to sort. Figure 8.3 shows how radix sort operates on a "deck" of seven 3-digit numbers.

In order for radix sort to work correctly, the digit sorts must be stable. The sort performed by a card sorter is stable, but the operator must be careful not to change the order of the cards as they come out of a bin, even though all the cards in a bin have the same digit in the chosen column.

In a typical computer, which is a sequential random-access machine, we sometimes use radix sort to sort records of information that are keyed by multiple fields. For example, we might wish to sort dates by three keys: year, month, and day. We could run a sorting algorithm with a comparison function that, given two dates, 

*8.3 Radix sort 213* 

compares years, and if there is a tie, compares months, and if another tie occurs, compares days. Alternatively, we could sort the information three times with a stable sort: first on day (the "least significant" part), next on month, and finally on year.

The code for radix sort is straightforward. The RADIX-SORT procedure assumes that each element in array A[1:n] has d digits, where digit 1 is the lowest-order digit and digit d is the highest-order digit.

```
RADIX-SORT(A, n, d)
1 for i = 1 to d
2     use a stable sort to sort array A[1:n] on digit i
```

Although the pseudocode for RADIX-SORT does not specify which stable sort to use, COUNTING-SORT is commonly used. If you use COUNTING-SORT as the stable sort, you can make RADIX-SORT a little more efficient by revising COUNTING-SORT to take a pointer to the output array as a parameter, having RADIX-SORT preallocate this array, and alternating input and output between the two arrays in successive iterations of the **for** loop in RADIX-SORT.

### *Lemma 8.3*

Given n d-digit numbers in which each digit can take on up to k possible values, RADIX-SORT correctly sorts these numbers in Θ(d(n + k)) time if the stable sort it uses takes Θ(n + k) time.

*Proof* The correctness of radix sort follows by induction on the column being sorted (see Exercise 8.3-3). The analysis of the running time depends on the stable sort used as the intermediate sorting algorithm. When each digit lies in the range 0 to k - 1 (so that it can take on k possible values), and k is not too large, counting sort is the obvious choice. Each pass over n d-digit numbers then takes Θ(n + k) time. There are d passes, and so the total time for radix sort is Θ(d(n + k)).

When d is constant and k = O(n), we can make radix sort run in linear time. More generally, we have some flexibility in how to break each key into digits.

### *Lemma 8.4*

Given n b-bit numbers and any positive integer r ≤ b, RADIX-SORT correctly sorts these numbers in Θ((b/r)(n + 2ʳ)) time if the stable sort it uses takes Θ(n + k) time for inputs in the range 0 to k.

*Proof* For a value r ≤ b, view each key as having d = ⌈b/r⌉ digits of r bits each. Each digit is an integer in the range 0 to 2ʳ - 1, so that we can use counting sort with k = 2ʳ - 1. (For example, we can view a 32-bit word as having four 8-bit digits, so that b = 32, r = 8, k = 2ʳ - 1 = 255, and d = b/r = 4.) Each pass of counting sort takes Θ(n + k) = Θ(n + 2ʳ) time and there are d passes, for a total running time of Θ(d(n + 2ʳ)) = Θ((b/r)(n + 2ʳ)).

Given n and b, what value of r ≤ b minimizes the expression (b/r)(n + 2ʳ)? As r decreases, the factor b/r increases, but as r increases so does 2ʳ. The answer depends on whether b < ⌊lg n⌋. If b < ⌊lg n⌋, then r ≤ b implies (n + 2ʳ) = Θ(n). Thus, choosing r = b yields a running time of (b/b)(n + 2ᵇ) = Θ(n), which is asymptotically optimal. If b ≥ ⌊lg n⌋, then choosing r = ⌊lg n⌋ gives the best running time to within a constant factor, which we can see as follows.¹ Choosing r = ⌊lg n⌋ yields a running time of Θ(bn/lg n). As r increases above ⌊lg n⌋, the 2ʳ term in the numerator increases faster than the r term in the denominator, and so increasing r above ⌊lg n⌋ yields a running time of Ω(bn/lg n). If instead r were to decrease below ⌊lg n⌋, then the b/r term increases and the n + 2ʳ term remains at Θ(n).

Is radix sort preferable to a comparison-based sorting algorithm, such as quicksort? If b = O(lg n), as is often the case, and r ≈ lg n, then radix sort's running time is Θ(n), which appears to be better than quicksort's expected running time of Θ(n lg n). The constant factors hidden in the Θ-notation differ, however. Although radix sort may make fewer passes than quicksort over the n keys, each pass of radix sort may take significantly longer. Which sorting algorithm to prefer depends on the characteristics of the implementations, of the underlying machine (e.g., quicksort often uses hardware caches more effectively than radix sort), and of the input data. Moreover, the version of radix sort that uses counting sort as the intermediate stable sort does not sort in place, which many of the Θ(n lg n)-time comparison sorts do. Thus, when primary memory storage is at a premium, an in-place algorithm such as quicksort could be the better choice.

### **Exercises**

## *8.3-1*

Using Figure 8.3 as a model, illustrate the operation of RADIX-SORT on the following list of English words: COW, DOG, SEA, RUG, ROW, MOB, BOX, TAB, BAR, EAR, TAR, DIG, BIG, TEA, NOW, FOX.

¹ The choice of r = ⌊lg n⌋ assumes that n > 1. If n ≤ 1, there is nothing to sort.

*8.4 Bucket sort 215* 

## *8.3-2*

Which of the following sorting algorithms are stable: insertion sort, merge sort, heapsort, and quicksort? Give a simple scheme that makes any comparison sort stable. How much additional time and space does your scheme entail?

### *8.3-3*

Use induction to prove that radix sort works. Where does your proof need the assumption that the intermediate sort is stable?

### *8.3-4*

Suppose that COUNTING-SORT is used as the stable sort within RADIX-SORT. If RADIX-SORT calls COUNTING-SORT d times, then since each call of COUNTING-SORT makes two passes over the data (lines 4–5 and 11–13), altogether 2d passes over the data occur. Describe how to reduce the total number of passes to d + 1.

### *8.3-5*

Show how to sort n integers in the range 0 to n³ - 1 in O(n) time.

# ⋆ *8.3-6*

In the first card-sorting algorithm in this section, which sorts on the most significant digit first, exactly how many sorting passes are needed to sort d-digit decimal numbers in the worst case? How many piles of cards does an operator need to keep track of in the worst case?

## **8.4 Bucket sort**

*Bucket sort* assumes that the input is drawn from a uniform distribution and has an average-case running time of O(n). Like counting sort, bucket sort is fast because it assumes something about the input. Whereas counting sort assumes that the input consists of integers in a small range, bucket sort assumes that the input is generated by a random process that distributes elements uniformly and independently over the interval [0, 1). (See Section C.2 for a definition of a uniform distribution.)

Bucket sort divides the interval [0, 1) into n equal-sized subintervals, or *buckets*, and then distributes the n input numbers into the buckets. Since the inputs are uniformly and independently distributed over [0, 1), we do not expect many numbers to fall into each bucket. To produce the output, we simply sort the numbers in each bucket and then go through the buckets in order, listing the elements in each.

The BUCKET-SORT procedure on the next page assumes that the input is an array A[1:n] and that each element A[i] in the array satisfies 0 ≤ A[i] < 1. The code requires an auxiliary array B[0:n - 1] of linked lists (buckets) and assumes