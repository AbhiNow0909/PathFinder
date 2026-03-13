---
topic: randomized_quicksort
pages: 213-214
---

Exercise 7.2-4. Section 5.3 showed that judicious randomization can sometimes be added to an algorithm to obtain good expected performance over all inputs. For quicksort, randomization yields a fast and practical algorithm. Many software libraries provide a randomized version of quicksort as their algorithm of choice for sorting large data sets.

In Section 5.3, the RANDOMIZED-HIRE-ASSISTANT procedure explicitly permutes its input and then runs the deterministic HIRE-ASSISTANT procedure. We could do the same for quicksort as well, but a different randomization technique yields a simpler analysis. Instead of always using A[r] as the pivot, a randomized version randomly chooses the pivot from the subarray A[p:r], where each element in A[p:r] has an equal probability of being chosen. It then exchanges that element with A[r] before partitioning. Because the pivot is chosen randomly, we expect the split of the input array to be reasonably well balanced on average.

The changes to PARTITION and QUICKSORT are small. The new partitioning procedure, RANDOMIZED-PARTITION, simply swaps before performing the partitioning. The new quicksort procedure, RANDOMIZED-QUICKSORT, calls RANDOMIZED-PARTITION instead of PARTITION. We'll analyze this algorithm in the next section.

```
RANDOMIZED-PARTITION(A, p, r)
1 i = RANDOM(p, r)
2 exchange A[r] with A[i]
3 return PARTITION(A, p, r)
RANDOMIZED-QUICKSORT(A, p, r)
1 if p < r
2     q = RANDOMIZED-PARTITION(A, p, r)
3     RANDOMIZED-QUICKSORT(A, p, q - 1)
4     RANDOMIZED-QUICKSORT(A, q + 1, r)
```

### **Exercises**

### *7.3-1*

Why do we analyze the expected running time of a randomized algorithm and not its worst-case running time?

## *7.3-2*

When RANDOMIZED-QUICKSORT runs, how many calls are made to the randomnumber generator RANDOM in the worst case? How about in the best case? Give your answer in terms of Θ-notation.

## **7.4 Analysis of quicksort**

Section 7.2 gave some intuition for the worst-case behavior of quicksort and for why we expect the algorithm to run quickly. This section analyzes the behavior of quicksort more rigorously. We begin with a worst-case analysis, which applies to either QUICKSORT or RANDOMIZED-QUICKSORT, and conclude with an analysis of the expected running time of RANDOMIZED-QUICKSORT.

### **7.4.1 Worst-case analysis**

We saw in Section 7.2 that a worst-case split at every level of recursion in quicksort produces a Θ(n²) running time, which, intuitively, is the worst-case running time of the algorithm. We now prove this assertion.

We'll use the substitution method (see Section 4.3) to show that the running time of quicksort is O(n²). Let T(n) be the worst-case time for the procedure QUICKSORT on an input of size n. Because the procedure PARTITION produces two subproblems with total size n - 1, we obtain the recurrence

$$T(n) = \max \{ T(q) + T(n-1-q) : 0 \le q \le n-1 \} + \Theta(n) , \qquad (7.1)$$

We guess that T(n) ≤ cn² for some constant c > 0. Substituting this guess into recurrence (7.1) yields

$$T(n) \le \max \left\{ cq^2 + c(n-1-q)^2 : 0 \le q \le n-1 \right\} + \Theta(n)$$
  
=  $c \cdot \max \left\{ q^2 + (n-1-q)^2 : 0 \le q \le n-1 \right\} + \Theta(n)$ .

Let's focus our attention on the maximization. For q = 0, 1, ..., n - 1, we have

$$q^{2} + (n-1-q)^{2} = q^{2} + (n-1)^{2} - 2q(n-1) + q^{2}$$
$$= (n-1)^{2} + 2q(q-(n-1))$$
$$\leq (n-1)^{2}$$

because q ≤ n - 1 implies that 2q(q - (n - 1)) ≤ 0. Thus every term in the maximization is bounded by (n - 1)².

Continuing with our analysis of T(n), we obtain