---
topic: order_statistics_basics
pages: 249-251
---

tinct elements. Section 9.3 contains an algorithm of more theoretical interest that achieves the O.n/ running time in the worst case.

## **9.1 Minimum and maximum**

How many comparisons are necessary to determine the minimum of a set of n elements? To obtain an upper bound of n - 1 comparisons, just examine each element of the set in turn and keep track of the smallest element seen so far. The MINIMUM procedure assumes that the set resides in array A[1:n].

```
MINIMUM(A, n)
1 min = A[1]
2 for i = 2 to n
3     if min > A[i]
4         min = A[i]
5 return min
```

It's no more difficult to find the maximum with n - 1 comparisons.

Is this algorithm for minimum the best we can do? Yes, because it turns out that there's a lower bound of n - 1 comparisons for the problem of determining the minimum. Think of any algorithm that determines the minimum as a tournament among the elements. Each comparison is a match in the tournament in which the smaller of the two elements wins. Since every element except the winner must lose at least one match, we can conclude that n - 1 comparisons are necessary to determine the minimum. Hence the algorithm MINIMUM is optimal with respect to the number of comparisons performed.

### **Simultaneous minimum and maximum**

Some applications need to find both the minimum and the maximum of a set of n elements. For example, a graphics program may need to scale a set of (x, y) data to fit onto a rectangular display screen or other graphical output device. To do so, the program must first determine the minimum and maximum value of each coordinate.

Of course, we can determine both the minimum and the maximum of n elements using Θ(n) comparisons. We simply find the minimum and maximum independently, using n - 1 comparisons for each, for a total of 2n - 2 = Θ(n) comparisons.

Although 2n - 2 comparisons is asymptotically optimal, it is possible to improve the leading constant. We can find both the minimum and the maximum using at most 3⌊n/2⌋ comparisons. The trick is to maintain both the minimum and maximum elements seen thus far. Rather than processing each element of the input by comparing it against the current minimum and maximum, at a cost of 2 comparisons per element, process elements in pairs. Compare pairs of elements from the input first *with each other*, and then compare the smaller with the current minimum and the larger to the current maximum, at a cost of 3 comparisons for every 2 elements.

How you set up initial values for the current minimum and maximum depends on whether n is odd or even. If n is odd, set both the minimum and maximum to the value of the first element, and then process the rest of the elements in pairs. If n is even, perform 1 comparison on the first 2 elements to determine the initial values of the minimum and maximum, and then process the rest of the elements in pairs as in the case for odd n.

Let's count the total number of comparisons. If n is odd, then 3⌊n/2⌋ comparisons occur. If n is even, 1 initial comparison occurs, followed by another 3(n - 2)/2 comparisons, for a total of 3n/2 - 2. Thus, in either case, the total number of comparisons is at most 3⌊n/2⌋.

### **Exercises**

### *9.1-1*

Show that the second smallest of n elements can be found with n + ⌈lg n⌉ - 2 comparisons in the worst case. (*Hint:* Also find the smallest element.)

### *9.1-2*

Given n > 2 distinct numbers, you want to find a number that is neither the minimum nor the maximum. What is the smallest number of comparisons that you need to perform?

### *9.1-3*

A racetrack can run races with five horses at a time to determine their relative speeds. For 25 horses, it takes six races to determine the fastest horse, assuming transitivity (see page 1159). What's the minimum number of races it takes to determine the fastest three horses out of 25?

# ⋆ *9.1-4*

Prove the lower bound of ⌈3n/2⌉ - 2 comparisons in the worst case to find both the maximum and minimum of n numbers. (*Hint:* Consider how many numbers are potentially either the maximum or minimum, and investigate how a comparison affects these counts.)

## **9.2 Selection in expected linear time**

The general selection problem—finding the ith order statistic for any value of i—appears more difficult than the simple problem of finding a minimum. Yet, surprisingly, the asymptotic running time for both problems is the same: Θ(n). This section presents a divide-and-conquer algorithm for the selection problem. The algorithm RANDOMIZED-SELECT is modeled after the quicksort algorithm of Chapter 7. Like quicksort it partitions the input array recursively. But unlike quicksort, which recursively processes both sides of the partition, RANDOMIZED-SELECT works on only one side of the partition. This difference shows up in the analysis: whereas quicksort has an expected running time of Θ(n lg n), the expected running time of RANDOMIZED-SELECT is Θ(n), assuming that the elements are distinct.

RANDOMIZED-SELECT uses the procedure RANDOMIZED-PARTITION introduced in Section 7.3. Like RANDOMIZED-QUICKSORT, it is a randomized algorithm, since its behavior is determined in part by the output of a random-number generator. The RANDOMIZED-SELECT procedure returns the ith smallest element of the array A[p:r], where 1 ≤ i ≤ r - p + 1.

```
RANDOMIZED-SELECT(A, p, r, i)
1 if p == r
2     return A[p] // 1 ≤ i ≤ r - p + 1 when p == r means that i = 1
3 q = RANDOMIZED-PARTITION(A, p, r)
4 k = q - p + 1
5 if i == k
6     return A[q] // the pivot value is the answer 
7 elseif i < k
8     return RANDOMIZED-SELECT(A, p, q - 1, i)
9 else return RANDOMIZED-SELECT(A, q + 1, r, i - k)
```

Figure 9.1 illustrates how the RANDOMIZED-SELECT procedure works. Line 1 checks for the base case of the recursion, in which the subarray A[p:r] consists of just one element. In this case, i must equal 1, and line 2 simply returns A[p] as the ith smallest element. Otherwise, the call to RANDOMIZED-PARTITION in line 3 partitions the array A[p:r] into two (possibly empty) subarrays A[p:q - 1] and A[q + 1:r] such that each element of A[p:q - 1] is less than or equal to A[q], which in turn is less than each element of A[q + 1:r]. (Although our analysis assumes that the elements are distinct, the procedure still yields the correct result even if equal elements are present.) As in quicksort, we'll refer to A[q] as the *pivot* element. Line 4 computes the number k of elements in the subarray A[p:q], that is,