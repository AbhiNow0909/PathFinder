---
topic: quicksort_analysis
pages: 215-226
---

$$T(n) \le c(n-1)^2 + \Theta(n)$$
  

$$\le cn^2 - c(2n-1) + \Theta(n)$$
  

$$\le cn^2,$$

by picking the constant c large enough that the c(2n - 1) term dominates the Θ(n) term. Thus T(n) = O(n²). Section 7.2 showed a specific case where quicksort takes Ω(n²) time: when partitioning is maximally unbalanced. Thus, the worstcase running time of quicksort is Θ(n²).

## **7.4.2 Expected running time**

We have already seen the intuition behind why the expected running time of RANDOMIZED-QUICKSORT is O(n lg n): if, in each level of recursion, the split induced by RANDOMIZED-PARTITION puts any constant fraction of the elements on one side of the partition, then the recursion tree has depth Θ(lg n) and O(n) work is performed at each level. Even if we add a few new levels with the most unbalanced split possible between these levels, the total time remains O(n lg n). We can analyze the expected running time of RANDOMIZED-QUICKSORT precisely by first understanding how the partitioning procedure operates and then using this understanding to derive an O(n lg n) bound on the expected running time. This upper bound on the expected running time, combined with the Θ(n lg n) best-case bound we saw in Section 7.2, yields a Θ(n lg n) expected running time. We assume throughout that the values of the elements being sorted are distinct.

### **Running time and comparisons**

The QUICKSORT and RANDOMIZED-QUICKSORT procedures differ only in how they select pivot elements. They are the same in all other respects. We can therefore analyze RANDOMIZED-QUICKSORT by considering the QUICKSORT and PARTITION procedures, but with the assumption that pivot elements are selected randomly from the subarray passed to RANDOMIZED-PARTITION. Let's start by relating the asymptotic running time of QUICKSORT to the number of times elements are compared (all in line 4 of PARTITION), understanding that this analysis also applies to RANDOMIZED-QUICKSORT. Note that we are counting the number of times that *array elements* are compared, not comparisons of indices.

### *Lemma 7.1*

The running time of QUICKSORT on an n-element array is O(n + X), where X is the number of element comparisons performed.

*Proof* The running time of QUICKSORT is dominated by the time spent in the PARTITION procedure. Each time PARTITION is called, it selects a pivot element, which is never included in any future recursive calls to QUICKSORT and PARTITION. Thus, there can be at most n calls to PARTITION over the entire execution of the quicksort algorithm. Each time QUICKSORT calls PARTITION, it also recursively calls itself twice, so there are at most 2n calls to the QUICKSORT procedure itself.

One call to PARTITION takes O(1) time plus an amount of time that is proportional to the number of iterations of the **for** loop in lines 3–6. Each iteration of this **for** loop performs one comparison in line 4, comparing the pivot element to another element of the array A. Therefore, the total time spent in the **for** loop across all executions is proportional to X. Since there are at most n calls to PARTITION and the time spent outside the **for** loop is O(1) for each call, the total time spent in PARTITION outside of the **for** loop is O(n). Thus the total time for quicksort is O(n + X).

Our goal for analyzing RANDOMIZED-QUICKSORT, therefore, is to compute the expected value E[X] of the random variable X denoting the total number of comparisons performed in all calls to PARTITION. To do so, we must understand when the quicksort algorithm compares two elements of the array and when it does not. For ease of analysis, let's index the elements of the array A by their position in the sorted output, rather than their position in the input. That is, although the elements in A may start out in any order, we'll refer to them by z₁, z₂, ..., zₙ, where z₁ < z₂ < ⋯ < zₙ, with strict inequality because we assume that all elements are distinct. We denote the set {zᵢ, zᵢ₊₁, ..., zⱼ} by Zᵢⱼ.

The next lemma characterizes when two elements are compared.

### *Lemma 7.2*

During the execution of RANDOMIZED-QUICKSORT on an array of n distinct elements z₁ < z₂ < ⋯ < zₙ, an element zᵢ is compared with an element zⱼ, where i < j, if and only if one of them is chosen as a pivot before any other element in the set Zᵢⱼ. Moreover, no two elements are ever compared twice.

*Proof* Let's look at the first time that an element x ∈ Zᵢⱼ is chosen as a pivot during the execution of the algorithm. There are three cases to consider. If x is neither zᵢ nor zⱼ—that is, zᵢ < x < zⱼ—then zᵢ and zⱼ are not compared at any subsequent time, because they fall into different sides of the partition around x. If x = zᵢ, then PARTITION compares zᵢ with every other item in Zᵢⱼ. Similarly, if x = zⱼ, then PARTITION compares zⱼ with every other item in Zᵢⱼ. Thus, zᵢ and zⱼ are compared if and only if the first element to be chosen as a pivot from Zᵢⱼ is either zᵢ or zⱼ. In the latter two cases, where one of zᵢ and zⱼ is chosen 

as a pivot, since the pivot is removed from future comparisons, it is never compared again with the other element.

As an example of this lemma, consider an input to quicksort of the numbers 1 through 10 in some arbitrary order. Suppose that the first pivot element is 7. Then the first call to PARTITION separates the numbers into two sets: {1, 2, 3, 4, 5, 6} and {8, 9, 10}. In the process, the pivot element 7 is compared with all other elements, but no number from the first set (e.g., 2) is or ever will be compared with any number from the second set (e.g., 9). The values 7 and 9 are compared because 7 is the first item from Z₇,₉ to be chosen as a pivot. In contrast, 2 and 9 are never compared because the first pivot element chosen from Z₂,₉ is 7.

The next lemma gives the probability that two elements are compared.

## *Lemma 7.3*

Consider an execution of the procedure RANDOMIZED-QUICKSORT on an array of n distinct elements z₁ < z₂ < ⋯ < zₙ. Given two arbitrary elements zᵢ and zⱼ where i < j, the probability that they are compared is 2/(j - i + 1).

*Proof* Let's look at the tree of recursive calls that RANDOMIZED-QUICKSORT makes, and consider the sets of elements provided as input to each call. Initially, the root set contains all the elements of Zᵢⱼ, since the root set contains every element in A. The elements belonging to Zᵢⱼ all stay together for each recursive call of RANDOMIZED-QUICKSORT until PARTITION chooses some element x ∈ Zᵢⱼ as a pivot. From that point on, the pivot x appears in no subsequent input set. The first time that RANDOMIZED-SELECT chooses a pivot x ∈ Zᵢⱼ from a set containing all the elements of Zᵢⱼ, each element in Zᵢⱼ is equally likely to be x because the pivot is chosen uniformly at random. Since |Zᵢⱼ| = j - i + 1, the probability is 1/(j - i + 1) that any given element in Zᵢⱼ is the first pivot chosen from Zᵢⱼ. Thus, by Lemma 7.2, we have

$$\Pr\{z_i \text{ is compared with } z_j\} = \Pr\{z_i \text{ or } z_j \text{ is the first pivot chosen from } Z_{ij}\}$$

$$= \Pr\{z_i \text{ is the first pivot chosen from } Z_{ij}\}$$

$$+ \Pr\{z_j \text{ is the first pivot chosen from } Z_{ij}\}$$

$$= \frac{2}{j-i+1},$$

where the second line follows from the first because the two events are mutually exclusive.

We can now complete the analysis of randomized quicksort.

## *Theorem 7.4*

The expected running time of RANDOMIZED-QUICKSORT on an input of n distinct elements is O(n lg n).

*Proof* The analysis uses indicator random variables (see Section 5.2). Let the n distinct elements be z₁ < z₂ < ⋯ < zₙ, and for 1 ≤ i < j ≤ n, define the indicator random variable Xᵢⱼ = I{zᵢ is compared with zⱼ}. From Lemma 7.2, each pair is compared at most once, and so we can express X as follows:

$$X = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij} .$$

By taking expectations of both sides and using linearity of expectation (equation (C.24) on page 1192) and Lemma 5.1 on page 130, we obtain

$$E[X] = E\left[\sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij}\right]$$

$$= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} E[X_{ij}] \qquad \text{(by linearity of expectation)}$$

$$= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \Pr\{z_i \text{ is compared with } z_j\} \qquad \text{(by Lemma 5.1)}$$

$$= \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j-i+1} \qquad \text{(by Lemma 7.3)}.$$

We can evaluate this sum using a change of variables (k = j - i) and the bound on the harmonic series in equation (A.9) on page 1142:

$$E[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j-i+1}$$

$$= \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1}$$

$$< \sum_{i=1}^{n-1} \sum_{k=1}^{n} \frac{2}{k}$$

$$= \sum_{i=1}^{n-1} O(\lg n)$$

$$= O(n \lg n).$$

This bound and Lemma 7.1 allow us to conclude that the expected running time of RANDOMIZED-QUICKSORT is O(n lg n) (assuming that the element values are distinct).

### **Exercises**

## *7.4-1*

Show that the recurrence

$$T(n) = \max \{ T(q) + T(n - q - 1) : 0 \le q \le n - 1 \} + \Theta(n)$$

has a lower bound of T(n) = Ω(n²).

## *7.4-2*

Show that quicksort's best-case running time is Ω(n lg n).

## *7.4-3*

Show that the expression q² + (n - q - 1)² achieves its maximum value over q = 0, 1, ..., n - 1 when q = 0 or q = n - 1.

## *7.4-4*

Show that RANDOMIZED-QUICKSORT's expected running time is Ω(n lg n).

### *7.4-5*

Coarsening the recursion, as we did in Problem 2-1 for merge sort, is a common way to improve the running time of quicksort in practice. We modify the base case of the recursion so that if the array has fewer than k elements, the subarray is sorted by insertion sort, rather than by continued recursive calls to quicksort. Argue that the randomized version of this sorting algorithm runs in O(nk + n lg(n/k)) expected time. How should you pick k, both in theory and in practice?

# ⋆ *7.4-6*

Consider modifying the PARTITION procedure by randomly picking three elements from subarray A[p:r] and partitioning about their median (the middle value of the three elements). Approximate the probability of getting worse than an α-to-(1 - α) split, as a function of α in the range 0 < α < 1/2.

## **Problems**

### *7-1 Hoare partition correctness*

The version of PARTITION given in this chapter is not the original partitioning algorithm. Here is the original partitioning algorithm, which is due to C. A. R. Hoare.

```
HOARE-PARTITION(A, p, r)
1 x = A[p]
2 i = p - 1
3 j = r + 1
4 while TRUE 
5     repeat
6         j = j - 1
7     until A[j] ≤ x
8     repeat
9         i = i + 1
10     until A[i] ≥ x
11     if i < j
12         exchange A[i] with A[j]
13     else return j
```

- *a.* Demonstrate the operation of HOARE-PARTITION on the array A = ⟨13, 19, 9, 5, 12, 8, 7, 4, 11, 2, 6, 21⟩, showing the values of the array and the indices i and j after each iteration of the **while** loop in lines 4–13.
- *b.* Describe how the PARTITION procedure in Section 7.1 differs from HOARE-PARTITION when all elements in A[p:r] are equal. Describe a practical advantage of HOARE-PARTITION over PARTITION for use in quicksort.

The next three questions ask you to give a careful argument that the procedure HOARE-PARTITION is correct. Assuming that the subarray A[p:r] contains at least two elements, prove the following:

- *c.* The indices i and j are such that the procedure never accesses an element of A outside the subarray A[p:r].
- *d.* When HOARE-PARTITION terminates, it returns a value j such that p ≤ j < r.
- *e.* Every element of A[p:j] is less than or equal to every element of A[j + 1:r] when HOARE-PARTITION terminates.

The PARTITION procedure in Section 7.1 separates the pivot value (originally in A[r]) from the two partitions it forms. The HOARE-PARTITION procedure, on the other hand, always places the pivot value (originally in A[p]) into one of the two partitions A[p:j] and A[j + 1:r]. Since p ≤ j < r, neither partition is empty.

*f.* Rewrite the QUICKSORT procedure to use HOARE-PARTITION.

## *7-2 Quicksort with equal element values*

The analysis of the expected running time of randomized quicksort in Section 7.4.2 assumes that all element values are distinct. This problem examines what happens when they are not.

- *a.* Suppose that all element values are equal. What is randomized quicksort's running time in this case?
- *b.* The PARTITION procedure returns an index q such that each element of A[p:q - 1] is less than or equal to A[q] and each element of A[q + 1:r] is greater than A[q]. Modify the PARTITION procedure to produce a procedure PARTITION′(A, p, r), which permutes the elements of A[p:r] and returns two indices q and t, where p ≤ q ≤ t ≤ r, such that
  - all elements of A[q:t] are equal,
  - each element of A[p:q - 1] is less than A[q], and
  - each element of A[t + 1:r] is greater than A[q].

Like PARTITION, your PARTITION′ procedure should take Θ(r - p) time.

- *c.* Modify the RANDOMIZED-PARTITION procedure to call PARTITION′, and name the new procedure RANDOMIZED-PARTITION′. Then modify the QUICKSORT procedure to produce a procedure QUICKSORT′(A, p, r) that calls RANDOMIZED-PARTITION′ and recurses only on partitions where elements are not known to be equal to each other.
- *d.* Using QUICKSORT′, adjust the analysis in Section 7.4.2 to avoid the assumption that all elements are distinct.

### *7-3 Alternative quicksort analysis*

An alternative analysis of the running time of randomized quicksort focuses on the expected running time of each individual recursive call to RANDOMIZED-QUICKSORT, rather than on the number of comparisons performed. As in the analysis of Section 7.4.2, assume that the values of the elements are distinct.

- *a.* Argue that, given an array of size n, the probability that any particular element is chosen as the pivot is 1/n. Use this probability to define indicator random variables Xᵢ = I{ith smallest element is chosen as the pivot}. What is E[Xᵢ]?
- *b.* Let T(n) be a random variable denoting the running time of quicksort on an array of size n. Argue that

$$E[T(n)] = E\left[\sum_{q=1}^{n} X_q \left(T(q-1) + T(n-q) + \Theta(n)\right)\right].$$
 (7.2)

*c.* Show how to rewrite equation (7.2) as

$$E[T(n)] = \frac{2}{n} \sum_{q=1}^{n-1} E[T(q)] + \Theta(n).$$
 (7.3)

*d.* Show that

$$\sum_{q=1}^{n-1} q \lg q \le \frac{n^2}{2} \lg n - \frac{n^2}{8} \tag{7.4}$$

for n ≥ 2. (*Hint:* Split the summation into two parts, one summation for q = 1, 2, ..., ⌈n/2⌉ - 1 and one summation for q = ⌈n/2⌉, ..., n - 1.)

*e.* Using the bound from equation (7.4), show that the recurrence in equation (7.3) has the solution E[T(n)] = O(n lg n). (*Hint:* Show, by substitution, that E[T(n)] ≤ an lg n for sufficiently large n and for some positive constant a.)

### *7-4 Stooge sort*

Professors Howard, Fine, and Howard have proposed a deceptively simple sorting algorithm, named stooge sort in their honor, appearing on the following page.

- *a.* Argue that the call STOOGE-SORT(A, 1, n) correctly sorts the array A[1:n].
- *b.* Give a recurrence for the worst-case running time of STOOGE-SORT and a tight asymptotic (Θ-notation) bound on the worst-case running time.
- *c.* Compare the worst-case running time of STOOGE-SORT with that of insertion sort, merge sort, heapsort, and quicksort. Do the professors deserve tenure?

```
STOOGE-SORT(A, p, r)
1 if A[p] > A[r]
2     exchange A[p] with A[r]
3 if p + 1 < r
4     k = ⌊(r - p + 1)/3⌋ // round down 
5     STOOGE-SORT(A, p, r - k) // first two-thirds
6     STOOGE-SORT(A, p + k, r) // last two-thirds
7     STOOGE-SORT(A, p, r - k) // first two-thirds again
```

## *7-5 Stack depth for quicksort*

The QUICKSORT procedure of Section 7.1 makes two recursive calls to itself. After QUICKSORT calls PARTITION, it recursively sorts the low side of the partition and then it recursively sorts the high side of the partition. The second recursive call in QUICKSORT is not really necessary, because the procedure can instead use an iterative control structure. This transformation technique, called *tail-recursion elimination*, is provided automatically by good compilers. Applying tail-recursion elimination transforms QUICKSORT into the TRE-QUICKSORT procedure.

```
TRE-QUICKSORT(A, p, r)
1 while p < r
2     // Partition and then sort the low side. 
3     q = PARTITION(A, p, r)
4     TRE-QUICKSORT(A, p, q - 1)
5     p = q + 1
```

*a.* Argue that TRE-QUICKSORT(A, 1, n) correctly sorts the array A[1:n].

Compilers usually execute recursive procedures by using a *stack* that contains pertinent information, including the parameter values, for each recursive call. The information for the most recent call is at the top of the stack, and the information for the initial call is at the bottom. When a procedure is called, its information is *pushed* onto the stack, and when it terminates, its information is *popped*. Since we assume that array parameters are represented by pointers, the information for each procedure call on the stack requires O(1) stack space. The *stack depth* is the maximum amount of stack space used at any time during a computation.

*b.* Describe a scenario in which TRE-QUICKSORT's stack depth is Θ(n) on an n-element input array.

*c.* Modify TRE-QUICKSORT so that the worst-case stack depth is Θ(lg n). Maintain the O(n lg n) expected running time of the algorithm.

### *7-6 Median-of-3 partition*

One way to improve the RANDOMIZED-QUICKSORT procedure is to partition around a pivot that is chosen more carefully than by picking a random element from the subarray. A common approach is the *median-of-3* method: choose the pivot as the median (middle element) of a set of 3 elements randomly selected from the subarray. (See Exercise 7.4-6.) For this problem, assume that the n elements in the input subarray A[p:r] are distinct and that n ≥ 3. Denote the sorted version of A[p:r] by z₁, z₂, ..., zₙ. Using the median-of-3 method to choose the pivot element x, define pᵢ = Pr{x = zᵢ}.

- *a.* Give an exact formula for pᵢ as a function of n and i for i = 2, 3, ..., n - 1. (Observe that p₁ = pₙ = 0.)
- *b.* By what amount does the median-of-3 method increase the likelihood of choosing the pivot to be x = z⌊(n+1)/2⌋, the median of A[p:r], compared with the ordinary implementation? Assume that n → ∞, and give the limiting ratio of these probabilities.
- *c.* Suppose that we define a "good" split to mean choosing the pivot as x = zᵢ, where n/3 ≤ i ≤ 2n/3. By what amount does the median-of-3 method increase the likelihood of getting a good split compared with the ordinary implementation? (*Hint:* Approximate the sum by an integral.)
- *d.* Argue that in the Θ(n lg n) running time of quicksort, the median-of-3 method affects only the constant factor.

### *7-7 Fuzzy sorting of intervals*

Consider a sorting problem in which you do not know the numbers exactly. Instead, for each number, you know an interval on the real line to which it belongs. That is, you are given n closed intervals of the form [aᵢ, bᵢ], where aᵢ ≤ bᵢ. The goal is to *fuzzy-sort* these intervals: to produce a permutation ⟨i₁, i₂, ..., iₙ⟩ of the intervals such that for j = 1, 2, ..., n, there exist cⱼ ∈ [aᵢⱼ, bᵢⱼ] satisfying c₁ ≤ c₂ ≤ ⋯ ≤ cₙ.

*a.* Design a randomized algorithm for fuzzy-sorting n intervals. Your algorithm should have the general structure of an algorithm that quicksorts the left endpoints (the aᵢ values), but it should take advantage of overlapping intervals to improve the running time. (As the intervals overlap more and more, the prob-

- lem of fuzzy-sorting the intervals becomes progressively easier. Your algorithm should take advantage of such overlapping, to the extent that it exists.)
- *b.* Argue that your algorithm runs in Θ(n lg n) expected time in general, but runs in Θ(n) expected time when all of the intervals overlap (i.e., when there exists a value x such that x ∈ [aᵢ, bᵢ] for all i). Your algorithm should not be checking for this case explicitly, but rather, its performance should naturally improve as the amount of overlap increases.

## **Chapter notes**

Quicksort was invented by Hoare [219], and his version of PARTITION appears in Problem 7-1. Bentley [51, p. 117] attributes the PARTITION procedure given in Section 7.1 to N. Lomuto. The analysis in Section 7.4 based on an analysis due to Motwani and Raghavan [336]. Sedgewick [401] and Bentley [51] provide good references on the details of implementation and how they matter.

McIlroy [323] shows how to engineer a "killer adversary" that produces an array on which virtually any implementation of quicksort takes Θ(n²) time.

# **8 Sorting in Linear Time**

We have now seen a handful of algorithms that can sort n numbers in O(n lg n) time. Whereas merge sort and heapsort achieve this upper bound in the worst case, quicksort achieves it on average. Moreover, for each of these algorithms, we can produce a sequence of n input numbers that causes the algorithm to run in Ω(n lg n) time.

These algorithms share an interesting property: *the sorted order they determine is based only on comparisons between the input elements*. We call such sorting algorithms *comparison sorts*. All the sorting algorithms introduced thus far are comparison sorts.

In Section 8.1, we'll prove that any comparison sort must make Ω(n lg n) comparisons in the worst case to sort n elements. Thus, merge sort and heapsort are asymptotically optimal, and no comparison sort exists that is faster by more than a constant factor.

Sections 8.2, 8.3, and 8.4 examine three sorting algorithms—counting sort, radix sort, and bucket sort—that run in linear time on certain types of inputs. Of course, these algorithms use operations other than comparisons to determine the sorted order. Consequently, the Ω(n lg n) lower bound does not apply to them.

## **8.1 Lower bounds for sorting**

A comparison sort uses only comparisons between elements to gain order information about an input sequence ⟨a₁, a₂, ..., aₙ⟩. That is, given two elements aᵢ and aⱼ, it performs one of the tests aᵢ < aⱼ, aᵢ ≤ aⱼ, aᵢ = aⱼ, aᵢ ≥ aⱼ, or aᵢ > aⱼ to determine their relative order. It may not inspect the values of the elements or gain order information about them in any other way.

Since we are proving a lower bound, we assume without loss of generality in this section that all the input elements are distinct. After all, a lower bound for distinct elements applies when elements may or may not be distinct. Consequently,