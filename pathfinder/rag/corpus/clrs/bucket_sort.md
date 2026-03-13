---
topic: bucket_sort
pages: 237-248
---

**Figure 8.4** The operation of BUCKET-SORT for n = 10. **(a)** The input array A[1:10]. **(b)** The array B[0:9] of sorted lists (buckets) after line 7 of the algorithm, with slashes indicating the end of each bucket. Bucket i holds values in the half-open interval [i/10, (i + 1)/10). The sorted output consists of a concatenation of the lists B[0], B[1], ..., B[9] in order.

that there is a mechanism for maintaining such lists. (Section 10.2 describes how to implement basic operations on linked lists.) Figure 8.4 shows the operation of bucket sort on an input array of 10 numbers.

```
BUCKET-SORT(A, n)
1 let B[0:n - 1] be a new array
2 for i = 0 to n - 1
3     make B[i] an empty list
4 for i = 1 to n
5     insert A[i] into list B[⌊n · A[i]⌋]
6 for i = 0 to n - 1
7     sort list B[i] with insertion sort
8 concatenate the lists B[0], B[1], ..., B[n - 1] together in order
9 return the concatenated lists
```

To see that this algorithm works, consider two elements A[i] and A[j]. Assume without loss of generality that A[i] ≤ A[j]. Since ⌊n · A[i]⌋ ≤ ⌊n · A[j]⌋, either element A[i] goes into the same bucket as A[j] or it goes into a bucket with a lower index. If A[i] and A[j] go into the same bucket, then the **for** loop of lines 6–7 puts them into the proper order. If A[i] and A[j] go into different buckets, then line 8 puts them into the proper order. Therefore, bucket sort works correctly.

*8.4 Bucket sort 217*

To analyze the running time, observe that, together, all lines except line 7 take O(n) time in the worst case. We need to analyze the total time taken by the n calls to insertion sort in line 7.

To analyze the cost of the calls to insertion sort, let nᵢ be the random variable denoting the number of elements placed in bucket B[i]. Since insertion sort runs in quadratic time (see Section 2.2), the running time of bucket sort is

$$T(n) = \Theta(n) + \sum_{i=0}^{n-1} O(n_i^2).$$
(8.1)

We now analyze the average-case running time of bucket sort, by computing the expected value of the running time, where we take the expectation over the input distribution. Taking expectations of both sides and using linearity of expectation (equation (C.24) on page 1192), we have

$$E[T(n)] = E\left[\Theta(n) + \sum_{i=0}^{n-1} O(n_i^2)\right]$$

$$= \Theta(n) + \sum_{i=0}^{n-1} E\left[O(n_i^2)\right] \quad \text{(by linearity of expectation)}$$

$$= \Theta(n) + \sum_{i=0}^{n-1} O\left(E\left[n_i^2\right]\right) \quad \text{(by equation (C.25) on page 1193)}. \quad (8.2)$$

We claim that

$$\mathrm{E}\left[n_i^2\right] = 2 - 1/n\tag{8.3}$$

for i = 0, 1, ..., n - 1. It is no surprise that each bucket i has the same value of E[n²ᵢ], since each value in the input array A is equally likely to fall in any bucket.

To prove equation (8.3), view each random variable nᵢ as the number of successes in n Bernoulli trials (see Section C.4). Success in a trial occurs when an element goes into bucket B[i], with a probability p = 1/n of success and q = 1 - 1/n of failure. A binomial distribution counts nᵢ, the number of successes, in the n trials. By equations (C.41) and (C.44) on pages 1199–1200, we have E[nᵢ] = np = n(1/n) = 1 and Var[nᵢ] = npq = 1 - 1/n. Equation (C.31) on page 1194 gives

$$E[n_i^2] = Var[n_i] + E^2[n_i]$$
  
=  $(1 - 1/n) + 1^2$   
=  $2 - 1/n$ ,

which proves equation (8.3). Using this expected value in equation (8.2), we get that the average-case running time for bucket sort is Θ(n) + nO(2 - 1/n) = Θ(n).

Even if the input is not drawn from a uniform distribution, bucket sort may still run in linear time. As long as the input has the property that the sum of the squares of the bucket sizes is linear in the total number of elements, equation (8.1) tells us that bucket sort runs in linear time.

## **Exercises**

## *8.4-1*

Using Figure 8.4 as a model, illustrate the operation of BUCKET-SORT on the array A = ⟨.79, .13, .16, .64, .39, .20, .89, .53, .71, .42⟩.

## *8.4-2*

Explain why the worst-case running time for bucket sort is Θ(n²). What simple change to the algorithm preserves its linear average-case running time and makes its worst-case running time O(n lg n)?

## *8.4-3*

Let X be a random variable that is equal to the number of heads in two flips of a fair coin. What is E[X²]? What is E²[X]?

## *8.4-4*

An array A of size n > 10 is filled in the following way. For each element A[i], choose two random variables xᵢ and yᵢ uniformly and independently from [0, 1). Then set

$$A[i] = \frac{\lfloor 10x_i \rfloor}{10} + \frac{y_i}{n} .$$

Modify bucket sort so that it sorts the array A in O.n/ expected time.

## *8.4-5*

You are given n points in the unit disk, pᵢ = (xᵢ, yᵢ), such that 0 < x²ᵢ + y²ᵢ ≤ 1 for i = 1, 2, ..., n. Suppose that the points are uniformly distributed, that is, the probability of finding a point in any region of the disk is proportional to the area of that region. Design an algorithm with an average-case running time of Θ(n) to sort the n points by their distances dᵢ = √(x²ᵢ + y²ᵢ) from the origin. (*Hint:* Design the bucket sizes in BUCKET-SORT to reflect the uniform distribution of the points in the unit disk.)

## *8.4-6*

A *probability distribution function* P(x) for a random variable X is defined by P(x) = Pr{X ≤ x}. Suppose that you draw a list of n random variables X₁, X₂, ..., Xₙ from a continuous probability distribution function P that is computable in O(1) time (given y you can find x such that P(x) = y in O(1) time). Give an algorithm that sorts these numbers in linear average-case time.

## **Problems**

### *8-1 Probabilistic lower bounds on comparison sorting*

In this problem, you will prove a probabilistic Ω(n lg n) lower bound on the running time of any deterministic or randomized comparison sort on n distinct input elements. You'll begin by examining a deterministic comparison sort A with decision tree Tₐ. Assume that every permutation of A's inputs is equally likely.

- *a.* Suppose that each leaf of Tₐ is labeled with the probability that it is reached given a random input. Prove that exactly n! leaves are labeled 1/n! and that the rest are labeled 0.
- *b.* Let D(T) denote the external path length of a decision tree T—the sum of the depths of all the leaves of T. Let T be a decision tree with k > 1 leaves, and let *LT* and *RT* be the left and right subtrees of T. Show that D(T) = D(*LT*) + D(*RT*) + k.
- *c.* Let d(k) be the minimum value of D(T) over all decision trees T with k > 1 leaves. Show that d(k) = min {d(i) + d(k - i) + k : 1 ≤ i ≤ k - 1}. (*Hint:* Consider a decision tree T with k leaves that achieves the minimum. Let i₀ be the number of leaves in *LT* and k - i₀ the number of leaves in *RT*.)
- *d.* Prove that for a given value of k > 1 and i in the range 1 ≤ i ≤ k - 1, the function i lg i + (k - i) lg(k - i) is minimized at i = k/2. Conclude that d(k) = Ω(k lg k).
- *e.* Prove that D(T_A) = Ω(n! lg(n!)), and conclude that the average-case time to sort n elements is Ω(n lg n).

Now consider a *randomized* comparison sort B. We can extend the decision-tree model to handle randomization by incorporating two kinds of nodes: ordinary comparison nodes and "randomization" nodes. A randomization node models a random choice of the form RANDOM(1, r) made by algorithm B. The node has r children, each of which is equally likely to be chosen during an execution of the algorithm.

*f.* Show that for any randomized comparison sort B, there exists a deterministic comparison sort A whose expected number of comparisons is no more than those made by B.

## *8-2 Sorting in place in linear time*

You have an array of n data records to sort, each with a key of 0 or 1. An algorithm for sorting such a set of records might possess some subset of the following three desirable characteristics:

- 1. The algorithm runs in O(n) time.
- 2. The algorithm is stable.
- 3. The algorithm sorts in place, using no more than a constant amount of storage space in addition to the original array.
- *a.* Give an algorithm that satisfies criteria 1 and 2 above.
- *b.* Give an algorithm that satisfies criteria 1 and 3 above.
- *c.* Give an algorithm that satisfies criteria 2 and 3 above.
- *d.* Can you use any of your sorting algorithms from parts (a)–(c) as the sorting method used in line 2 of RADIX-SORT, so that RADIX-SORT sorts n records with b-bit keys in O(bn) time? Explain how or why not.
- *e.* Suppose that the n records have keys in the range from 1 to k. Show how to modify counting sort so that it sorts the records in place in O(n + k) time. You may use O(k) storage outside the input array. Is your algorithm stable?

### *8-3 Sorting variable-length items*

- *a.* You are given an array of integers, where different integers may have different numbers of digits, but the total number of digits over *all* the integers in the array is n. Show how to sort the array in O(n) time.
- *b.* You are given an array of strings, where different strings may have different numbers of characters, but the total number of characters over all the strings is n. Show how to sort the strings in O(n) time. (The desired order is the standard alphabetical order: for example, a < ab < b.)

### *8-4 Water jugs*

You are given n red and n blue water jugs, all of different shapes and sizes. All the red jugs hold different amounts of water, as do all the blue jugs, and you cannot tell from the size of a jug how much water it holds. Moreover, for every jug of one color, there is a jug of the other color that holds the same amount of water.

Your task is to group the jugs into pairs of red and blue jugs that hold the same amount of water. To do so, you may perform the following operation: pick a pair of jugs in which one is red and one is blue, fill the red jug with water, and then pour the water into the blue jug. This operation tells you whether the red jug or the blue jug can hold more water, or that they have the same volume. Assume that such a comparison takes one time unit. Your goal is to find an algorithm that makes a minimum number of comparisons to determine the grouping. Remember that you may not directly compare two red jugs or two blue jugs.

- *a.* Describe a deterministic algorithm that uses Θ(n²) comparisons to group the jugs into pairs.
- *b.* Prove a lower bound of Ω(n lg n) for the number of comparisons that an algorithm solving this problem must make.
- *c.* Give a randomized algorithm whose expected number of comparisons is O(n lg n), and prove that this bound is correct. What is the worst-case number of comparisons for your algorithm?

### *8-5 Average sorting*

Suppose that, instead of sorting an array, we just require that the elements increase on average. More precisely, we call an n-element array A k*-sorted* if, for all i = 1, 2, ..., n - k, the following holds:

$$\frac{\sum_{j=i}^{i+k-1} A[j]}{k} \le \frac{\sum_{j=i+1}^{i+k} A[j]}{k} .$$

- *a.* What does it mean for an array to be 1-sorted?
- *b.* Give a permutation of the numbers 1, 2, ..., 10 that is 2-sorted, but not sorted.
- *c.* Prove that an n-element array is k-sorted if and only if A[i] ≤ A[i + k] for all i = 1, 2, ..., n - k.
- *d.* Give an algorithm that k-sorts an n-element array in O(n lg(n/k)) time.

We can also show a lower bound on the time to produce a k-sorted array, when k is a constant.

- *e.* Show how to sort a k-sorted array of length n in O(n lg k) time. (*Hint:* Use the solution to Exercise 6.5-11.)
- *f.* Show that when k is a constant, k-sorting an n-element array requires Ω(n lg n) time. (*Hint:* Use the solution to part (e) along with the lower bound on comparison sorts.)

### *8-6 Lower bound on merging sorted lists*

The problem of merging two sorted lists arises frequently. We have seen a procedure for it as the subroutine MERGE in Section 2.3.1. In this problem, you will prove a lower bound of 2n - 1 on the worst-case number of comparisons required to merge two sorted lists, each containing n items. First, you will show a lower bound of 2n - o(n) comparisons by using a decision tree.

- *a.* Given 2n numbers, compute the number of possible ways to divide them into two sorted lists, each with n numbers.
- *b.* Using a decision tree and your answer to part (a), show that any algorithm that correctly merges two sorted lists must perform at least 2n o.n/ comparisons.

Now you will show a slightly tighter 2n 1 bound.

- *c.* Show that if two elements are consecutive in the sorted order and from different lists, then they must be compared.
- *d.* Use your answer to part (c) to show a lower bound of 2n - 1 comparisons for merging two sorted lists.

### *8-7 The 0-1 sorting lemma and columnsort*

A *compare-exchange* operation on two array elements A[i] and A[j], where i < j, has the form

```
COMPARE-EXCHANGE(A, i, j)
1 if A[i] > A[j]
2     exchange A[i] with A[j]
```

After the compare-exchange operation, we know that A[i] ≤ A[j].

An *oblivious compare-exchange algorithm* operates solely by a sequence of prespecified compare-exchange operations. The indices of the positions compared in the sequence must be determined in advance, and although they can depend on the number of elements being sorted, they cannot depend on the values being sorted, nor can they depend on the result of any prior compare-exchange operation. For example, the COMPARE-EXCHANGE-INSERTION-SORT procedure on the facing page shows a variation of insertion sort as an oblivious compare-exchange algorithm. (Unlike the INSERTION-SORT procedure on page 19, the oblivious version runs in Θ(n²) time in all cases.)

The *0-1 sorting lemma* provides a powerful way to prove that an oblivious compare-exchange algorithm produces a sorted result. It states that if an oblivious compare-exchange algorithm correctly sorts all input sequences consisting of only 0s and 1s, then it correctly sorts all inputs containing arbitrary values.

```
COMPARE-EXCHANGE-INSERTION-SORT(A, n)
1 for i = 2 to n
2     for j = i - 1 downto 1
3         COMPARE-EXCHANGE(A, j, j + 1)
```

You will prove the 0-1 sorting lemma by proving its contrapositive: if an oblivious compare-exchange algorithm fails to sort an input containing arbitrary values, then it fails to sort some 0-1 input. Assume that an oblivious compare-exchange algorithm X fails to correctly sort the array A[1:n]. Let A[p] be the smallest value in A that algorithm X puts into the wrong location, and let A[q] be the value that algorithm X moves to the location into which A[p] should have gone. Define an array B[1:n] of 0s and 1s as follows:

$$B[i] = \begin{cases} 0 & \text{if } A[i] \le A[p], \\ 1 & \text{if } A[i] > A[p]. \end{cases}$$

- *a.* Argue that A[q] > A[p], so that B[p] = 0 and B[q] = 1.
- *b.* To complete the proof of the 0-1 sorting lemma, prove that algorithm X fails to sort array B correctly.

Now you will use the 0-1 sorting lemma to prove that a particular sorting algorithm works correctly. The algorithm, *columnsort*, works on a rectangular array of n elements. The array has r rows and s columns (so that n = rs), subject to three restrictions:

- r must be even,
- s must be a divisor of r, and
- r ≥ 2s².

When columnsort completes, the array is sorted in *column-major order*: reading down each column in turn, from left to right, the elements monotonically increase.

Columnsort operates in eight steps, regardless of the value of n. The odd steps are all the same: sort each column individually. Each even step is a fixed permutation. Here are the steps:

- 1. Sort each column.
- 2. Transpose the array, but reshape it back to r rows and s columns. In other words, turn the leftmost column into the top r/s rows, in order; turn the next column into the next r/s rows, in order; and so on.

| 10  | 4   | 4   | 1   | 1   |
|-----|-----|-----|-----|-----|
| 14  | 1   | 8   | 3   | 4   |
| 5   | 2   | 10  | 6   | 11  |
| 8   | 8   | 12  | 2   | 3   |
| 7   | 3   | 16  | 5   | 8   |
| 17  | 5   | 18  | 7   | 14  |
| 12  | 10  | 1   | 4   | 6   |
| 1   | 7   | 3   | 8   | 10  |
| 6   | 6   | 7   | 10  | 17  |
| 16  | 12  | 9   | 9   | 2   |
| 9   | 9   | 14  | 13  | 9   |
| 11  | 11  | 15  | 15  | 12  |
| 4   | 16  | 2   | 11  | 5   |
| 15  | 14  | 5   | 14  | 13  |
| 2   | 13  | 6   | 17  | 16  |
| 18  | 18  | 11  | 12  | 7   |
| 3   | 15  | 13  | 16  | 15  |
| 13  | 17  | 17  | 18  | 18  |
| (a) | (b) | (c) | (d) | (e) |
| 1   | 5   | 4   | 1   |     |
| 4   | 10  | 10  | 7   |     |
| 11  | 16  | 16  | 13  |     |
| 2   | 6   | 5   | 2   |     |
| 8   | 13  | 11  | 8   |     |
| 12  | 17  | 17  | 14  |     |
| 3   | 7   | 6   | 3   |     |
| 9   | 15  | 12  | 9   |     |
| 14  | 18  | 18  | 15  |     |
| 5   | 1   | 1   | 4   |     |
| 10  | 4   | 7   | 10  |     |
| 16  | 11  | 13  | 16  |     |
| 6   | 2   | 2   | 5   |     |
| 13  | 8   | 8   | 11  |     |
| 17  | 12  | 14  | 17  |     |
| 7   | 3   | 3   | 6   |     |
| 15  | 9   | 9   | 12  |     |
| 18  | 14  | 15  | 18  |     |
| (f) | (g) | (h) | (i) |     |

**Figure 8.5** The steps of columnsort. **(a)** The input array with 6 rows and 3 columns. (This example does not obey the r ≥ 2s² requirement, but it works.) **(b)** After sorting each column in step 1. **(c)** After transposing and reshaping in step 2. **(d)** After sorting each column in step 3. **(e)** After performing step 4, which inverts the permutation from step 2. **(f)** After sorting each column in step 5. **(g)** After shifting by half a column in step 6. **(h)** After sorting each column in step 7. **(i)** After performing step 8, which inverts the permutation from step 6. Steps 6-8 sort the bottom half of each column with the top half of the next column. After step 8, the array is sorted in column-major order.

- 3. Sort each column.
- 4. Perform the inverse of the permutation performed in step 2.
- 5. Sort each column.
- 6. Shift the top half of each column into the bottom half of the same column, and shift the bottom half of each column into the top half of the next column to the right. Leave the top half of the leftmost column empty. Shift the bottom half of the last column into the top half of a new rightmost column, and leave the bottom half of this new column empty.
- 7. Sort each column.
- 8. Perform the inverse of the permutation performed in step 6.

You can think of steps 638 as a single step that sorts the bottom half of each column and the top half of the next column. Figure 8.5 shows an example of the steps of columnsort with r = 6 and s = 3. (Even though this example violates the requirement that <sup>r</sup> 2s<sup>2</sup> , it happens to work.)

*c.* Argue that we can treat columnsort as an oblivious compare-exchange algorithm, even if we do not know what sorting method the odd steps use.

Although it might seem hard to believe that columnsort actually sorts, you will use the 0-1 sorting lemma to prove that it does. The 0-1 sorting lemma applies because we can treat columnsort as an oblivious compare-exchange algorithm. A couple of definitions will help you apply the 0-1 sorting lemma. We say that an area of an array is *clean* if we know that it contains either all 0s or all 1s or if it is empty. Otherwise, the area might contain mixed 0s and 1s, and it is *dirty*. From here on, assume that the input array contains only 0s and 1s, and that we can treat it as an array with r rows and s columns.

- *d.* Prove that after steps 1-3, the array consists of clean rows of 0s at the top, clean rows of 1s at the bottom, and at most s dirty rows between them. (One of the clean rows could be empty.)
- *e.* Prove that after step 4, the array, read in column-major order, starts with a clean area of 0s, ends with a clean area of 1s, and has a dirty area of at most s² elements in the middle. (Again, one of the clean areas could be empty.)
- *f.* Prove that steps 5-8 produce a fully sorted 0-1 output. Conclude that columnsort correctly sorts all inputs containing arbitrary values.
- *g.* Now suppose that s does not divide r. Prove that after steps 1-3, the array consists of clean rows of 0s at the top, clean rows of 1s at the bottom, and at most 2s - 1 dirty rows between them. (Once again, one of the clean areas could be empty.) How large must r be, compared with s, for columnsort to correctly sort when s does not divide r?
- *h.* Suggest a simple change to step 1 that allows us to maintain the requirement that r ≥ 2s² even when s does not divide r, and prove that with your change, columnsort correctly sorts.

## **Chapter notes**

The decision-tree model for studying comparison sorts was introduced by Ford and Johnson [150]. Knuth's comprehensive treatise on sorting [261] covers many variations on the sorting problem, including the information-theoretic lower bound on the complexity of sorting given here. Ben-Or [46] studied lower bounds for sorting using generalizations of the decision-tree model.

Knuth credits H. H. Seward with inventing counting sort in 1954, as well as with the idea of combining counting sort with radix sort. Radix sorting starting with the least significant digit appears to be a folk algorithm widely used by operators of mechanical card-sorting machines. According to Knuth, the first published reference to the method is a 1929 document by L. J. Comrie describing punched-card equipment. Bucket sorting has been in use since 1956, when the basic idea was proposed by Isaac and Singleton [235].

Munro and Raman [338] give a stable sorting algorithm that performs O(n^(1+ε)) comparisons in the worst case, where 0 < ε ≤ 1 is any fixed constant. Although any of the O(n lg n)-time algorithms make fewer comparisons, the algorithm by Munro and Raman moves data only O(n) times and operates in place.

The case of sorting n b-bit integers in o(n lg n) time has been considered by many researchers. Several positive results have been obtained, each under slightly different assumptions about the model of computation and the restrictions placed on the algorithm. All the results assume that the computer memory is divided into addressable b-bit words. Fredman and Willard [157] introduced the fusion tree data structure and used it to sort n integers in O(n lg n / lg lg n) time. This bound was later improved to O(n√(lg n)) time by Andersson [17]. These algorithms require the use of multiplication and several precomputed constants. Andersson, Hagerup, Nilsson, and Raman [18] have shown how to sort n integers in O(n lg lg n) time without using multiplication, but their method requires storage that can be unbounded in terms of n. Using multiplicative hashing, we can reduce the storage needed to O(n), but then the O(n lg lg n) worst-case bound on the running time becomes an expected-time bound. Generalizing the exponential search trees of Andersson [17], Thorup [434] gave an O(n(lg lg n)²)-time sorting algorithm that does not use multiplication or randomization, and it uses linear space. Combining these techniques with some new ideas, Han [207] improved the bound for sorting to O(n lg lg n lg lg lg n) time. Although these algorithms are important theoretical breakthroughs, they are all fairly complicated and at the present time seem unlikely to compete with existing sorting algorithms in practice.

The columnsort algorithm in Problem 8-7 is by Leighton [286].

# **9 Medians and Order Statistics**

The ith *order statistic* of a set of n elements is the ith smallest element. For example, the *minimum* of a set of elements is the first order statistic (i = 1), and the *maximum* is the nth order statistic (i = n). A *median*, informally, is the "halfway point" of the set. When n is odd, the median is unique, occurring at i = (n+1)/2. When n is even, there are two medians, the *lower median* occurring at i = n/2 and the *upper median* occurring at i = n/2 + 1. Thus, regardless of the parity of n, medians occur at i = ⌊(n + 1)/2⌋ and i = ⌈(n + 1)/2⌉. For simplicity in this text, however, we consistently use the phrase "the median" to refer to the lower median.

This chapter addresses the problem of selecting the ith order statistic from a set of n distinct numbers. We assume for convenience that the set contains distinct numbers, although virtually everything that we do extends to the situation in which a set contains repeated values. We formally specify the *selection problem* as follows:

**Input:** A set A of n distinct numbers¹ and an integer i, with 1 ≤ i ≤ n.

**Output:** The element x ∈ A that is larger than exactly i - 1 other elements of A.

We can solve the selection problem in O(n lg n) time simply by sorting the numbers using heapsort or merge sort and then outputting the ith element in the sorted array. This chapter presents asymptotically faster algorithms.

Section 9.1 examines the problem of selecting the minimum and maximum of a set of elements. More interesting is the general selection problem, which we investigate in the subsequent two sections. Section 9.2 analyzes a practical randomized algorithm that achieves an O(n) expected running time, assuming dis-

¹ As in the footnote on page 182, you can enforce the assumption that the numbers are distinct by converting each input value A[i] to an ordered pair (A[i], i) with (A[i], i) < (A[j], j) if either A[i] < A[j] or A[i] = A[j] and i < j.