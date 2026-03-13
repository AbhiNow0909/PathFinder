---
topic: quicksort_performance
pages: 209-212
---

$$T(n) = T(n-1) + T(0) + \Theta(n)$$
  
=  $T(n-1) + \Theta(n)$ .

By summing the costs incurred at each level of the recursion, we obtain an arithmetic series (equation (A.3) on page 1141), which evaluates to Θ(n²). Indeed, the substitution method can be used to prove that the recurrence T(n) = T(n - 1) + Θ(n) has the solution T(n) = Θ(n²). (See Exercise 7.2-1).

Thus, if the partitioning is maximally unbalanced at every recursive level of the algorithm, the running time is Θ(n²). The worst-case running time of quicksort is therefore no better than that of insertion sort. Moreover, the Θ(n²) running time occurs when the input array is already completely sorted—a situation in which insertion sort runs in O(n) time.

### **Best-case partitioning**

In the most even possible split, PARTITION produces two subproblems, each of size no more than n/2, since one is of size ⌊(n - 1)/2⌋ ≤ n/2 and one of size ⌈(n - 1)/2⌉ - 1 ≤ n/2. In this case, quicksort runs much faster. An upper bound on the running time can then be described by the recurrence

$$T(n) = 2T(n/2) + \Theta(n) .$$

By case 2 of the master theorem (Theorem 4.1 on page 102), this recurrence has the solution T(n) = Θ(n lg n). Thus, if the partitioning is equally balanced at every level of the recursion, an asymptotically faster algorithm results.

### **Balanced partitioning**

As the analyses in Section 7.4 will show, the average-case running time of quicksort is much closer to the best case than to the worst case. By appreciating how the balance of the partitioning affects the recurrence describing the running time, we can gain an understanding of why.

Suppose, for example, that the partitioning algorithm always produces a 9-to-1 proportional split, which at first blush seems quite unbalanced. We then obtain the recurrence

$$T(n) = T(9n/10) + T(n/10) + \Theta(n) ,$$

on the running time of quicksort. Figure 7.4 shows the recursion tree for this recurrence, where for simplicity the Θ(n) driving function has been replaced by n, which won't affect the asymptotic solution of the recurrence (as Exercise 4.7-1 on page 118 justifies). Every level of the tree has cost n, until the recursion bottoms out in a base case at depth log₁₀ n = Θ(lg n), and then the levels have cost

**Figure 7.4** A recursion tree for QUICKSORT in which PARTITION always produces a 9-to-1 split, yielding a running time of O(n lg n). Nodes show subproblem sizes, with per-level costs on the right.

at most n. The recursion terminates at depth log₁₀₌g n = Θ(lg n). Thus, with a 9-to-1 proportional split at every level of recursion, which intuitively seems highly unbalanced, quicksort runs in O(n lg n) time—asymptotically the same as if the split were right down the middle. Indeed, even a 99-to-1 split yields an O(n lg n) running time. In fact, any split of *constant* proportionality yields a recursion tree of depth Θ(lg n), where the cost at each level is O(n). The running time is therefore O(n lg n) whenever the split has constant proportionality. The ratio of the split affects only the constant hidden in the O-notation.

### **Intuition for the average case**

To develop a clear notion of the expected behavior of quicksort, we must assume something about how its inputs are distributed. Because quicksort determines the sorted order using only comparisons between input elements, its behavior depends on the relative ordering of the values in the array elements given as the input, not on the particular values in the array. As in the probabilistic analysis of the hiring problem in Section 5.2, assume that all permutations of the input numbers are equally likely and that the elements are distinct.

When quicksort runs on a random input array, the partitioning is highly unlikely to happen in the same way at every level, as our informal analysis has assumed.

**Figure 7.5 (a)** Two levels of a recursion tree for quicksort. The partitioning at the root costs n and produces a "bad" split: two subarrays of sizes 0 and n - 1. The partitioning of the subarray of size n - 1 costs n - 1 and produces a "good" split: subarrays of size (n - 1)/2 - 1 and (n - 1)/2. **(b)** A single level of a recursion tree that is well balanced. In both parts, the partitioning cost for the subproblems shown with blue shading is Θ(n). Yet the subproblems remaining to be solved in (a), shown with tan shading, are no larger than the corresponding subproblems remaining to be solved in (b).

We expect that some of the splits will be reasonably well balanced and that some will be fairly unbalanced. For example, Exercise 7.2-6 asks you to show that about 80% of the time PARTITION produces a split that is at least as balanced as 9 to 1, and about 20% of the time it produces a split that is less balanced than 9 to 1.

In the average case, PARTITION produces a mix of "good" and "bad" splits. In a recursion tree for an average-case execution of PARTITION, the good and bad splits are distributed randomly throughout the tree. Suppose for the sake of intuition that the good and bad splits alternate levels in the tree, and that the good splits are bestcase splits and the bad splits are worst-case splits. Figure 7.5(a) shows the splits at two consecutive levels in the recursion tree. At the root of the tree, the cost is n for partitioning, and the subarrays produced have sizes n - 1 and 0: the worst case. At the next level, the subarray of size n - 1 undergoes best-case partitioning into subarrays of size (n - 1)/2 - 1 and (n - 1)/2. Let's assume that the base-case cost is 1 for the subarray of size 0.

The combination of the bad split followed by the good split produces three subarrays of sizes 0, (n - 1)/2 - 1, and (n - 1)/2 at a combined partitioning cost of Θ(n) + Θ(n - 1) = Θ(n). This situation is at most a constant factor worse than that in Figure 7.5(b), namely, where a single level of partitioning produces two subarrays of size (n - 1)/2, at a cost of Θ(n). Yet this latter situation is balanced! Intuitively, the Θ(n - 1) cost of the bad split in Figure 7.5(a) can be absorbed into the Θ(n) cost of the good split, and the resulting split is good. Thus, the running time of quicksort, when levels alternate between good and bad splits, is like the running time for good splits alone: still O(n lg n), but with a slightly larger constant hidden by the O-notation. We'll analyze the expected running time of a randomized version of quicksort rigorously in Section 7.4.2.

## **Exercises**

## *7.2-1*

Use the substitution method to prove that the recurrence T(n) = T(n - 1) + Θ(n) has the solution T(n) = Θ(n²), as claimed at the beginning of Section 7.2.

### *7.2-2*

What is the running time of QUICKSORT when all elements of array A have the same value?

## *7.2-3*

Show that the running time of QUICKSORT is Θ(n²) when the array A contains distinct elements and is sorted in decreasing order.

## *7.2-4*

Banks often record transactions on an account in order of the times of the transactions, but many people like to receive their bank statements with checks listed in order by check number. People usually write checks in order by check number, and merchants usually cash them with reasonable dispatch. The problem of converting time-of-transaction ordering to check-number ordering is therefore the problem of sorting almost-sorted input. Explain persuasively why the procedure INSERTION-SORT might tend to beat the procedure QUICKSORT on this problem.

### *7.2-5*

Suppose that the splits at every level of quicksort are in the constant proportion α to β, where α + β = 1 and 0 < α ≤ β < 1. Show that the minimum depth of a leaf in the recursion tree is approximately log₁₌ₐ n and that the maximum depth is approximately log₁₌ᵦ n. (Don't worry about integer round-off.)

## *7.2-6*

Consider an array with distinct elements and for which all permutations of the elements are equally likely. Argue that for any constant 0 < α ≤ 1/2, the probability is approximately 1 - 2α that PARTITION produces a split at least as balanced as 1 - α to α.

## **7.3 A randomized version of quicksort**

In exploring the average-case behavior of quicksort, we have assumed that all permutations of the input numbers are equally likely. This assumption does not always hold, however, as, for example, in the situation laid out in the premise for