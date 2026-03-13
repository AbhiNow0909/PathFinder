---
topic: algorithm_design_strategies
pages: 56-70
---

**Divide** the subarray A[p : r] to be sorted into two adjacent subarrays, each of half the size. To do so, compute the midpoint q of A[p : r] (taking the average of p and r), and divide A[p : r] into subarrays A[p : q] and A[q + 1 : r].

**Conquer** by sorting each of the two subarrays A[p : q] and A[q + 1 : r] recursively using merge sort.

**Combine** by merging the two sorted subarrays A[p : q] and A[q + 1 : r] back into A[p : r], producing the sorted answer.

The recursion "bottoms out"—it reaches the base case—when the subarray A[p : r] to be sorted has just 1 element, that is, when p equals r. As we noted in the initialization argument for INSERTION-SORT's loop invariant, a subarray comprising just a single element is always sorted.

The key operation of the merge sort algorithm occurs in the "combine" step, which merges two adjacent, sorted subarrays. The merge operation is performed by the auxiliary procedure MERGE(A; p; q; r) on the following page, where A is an array and p, q, and r are indices into the array such that p ≤ q < r. The procedure assumes that the adjacent subarrays A[p : q] and A[q + 1 : r] were already recursively sorted. It *merges* the two sorted subarrays to form a single sorted subarray that replaces the current subarray A[p : r].

To understand how the MERGE procedure works, let's return to our card-playing motif. Suppose that you have two piles of cards face up on a table. Each pile is sorted, with the smallest-value cards on top. You wish to merge the two piles into a single sorted output pile, which is to be face down on the table. The basic step consists of choosing the smaller of the two cards on top of the face-up piles, removing it from its pile—which exposes a new top card—and placing this card face down onto the output pile. Repeat this step until one input pile is empty, at which time you can just take the remaining input pile and flip over the entire pile, placing it face down onto the output pile.

Let's think about how long it takes to merge two sorted piles of cards. Each basic step takes constant time, since you are comparing just the two top cards. If the two sorted piles that you start with each have n/2 cards, then the number of basic steps is at least n/2 (since in whichever pile was emptied, every card was found to be smaller than some card from the other pile) and at most n (actually, at most n - 1, since after n - 1 basic steps, one of the piles must be empty). With each basic step taking constant time and the total number of basic steps being between n/2 and n, we can say that merging takes time roughly proportional to n. That is, merging takes Θ(n) time.

In detail, the MERGE procedure works as follows. It copies the two subarrays A[p : q] and A[q + 1 : r] into temporary arrays L and R ("left" and "right"), and then it merges the values in L and R back into A[p : r]. Lines 1 and 2 compute the lengths n<sup>L</sup> and n<sup>R</sup> of the subarrays A[p : q] and A[q + 1 : r], respectively. Then

```
MERGE(A; p; q; r)
1 nL = q - p + 1 // length of A[p : q]
2 nR = r - q // length of A[q + 1 : r]
3 let L[0 : nL - 1] and R[0 : nR - 1] be new arrays 
4 for i = 0 to nL - 1 // copy A[p : q] into L[0 : nL - 1]
5 L[i] = A[p + i]
6 for j = 0 to nR - 1 // copy A[q + 1 : r] into R[0 : nR - 1]
7 R[j] = A[q + j + 1]
8 i = 0 // i indexes the smallest remaining element in L
9 j = 0 // j indexes the smallest remaining element in R
10 k = p // k indexes the location in A to fill
11 // As long as each of the arrays L and R contains an unmerged element, 
   // copy the smallest unmerged element back into A[p : r]. 
12 while i < nL and j < nR
13 if L[i] ≤ R[j]
14 A[k] = L[i]
15 i = i + 1
16 else A[k] = R[j]
17 j = j + 1
18 k = k + 1
19 // Having gone through one of L and R entirely, copy the 
   // remainder of the other to the end of A[p : r]. 
20 while i < nL
21 A[k] = L[i]
22 i = i + 1
23 k = k + 1
24 while j < nR
25 A[k] = R[j]
26 j = j + 1
27 k = k + 1
```

line 3 creates arrays L[0 : n<sup>L</sup> - 1] and R[0 : n<sup>R</sup> - 1] with respective lengths n<sup>L</sup> and nR. The **for** loop of lines 4–5 copies the subarray A[p : q] into L, and the **for** loop of lines 6–7 copies the subarray A[q + 1 : r] into R.

Lines 8–18, illustrated in Figure 2.3, perform the basic steps. The **while** loop of lines 12–18 repeatedly identifies the smallest value in L and R that has yet to

 This procedure is the rare case that uses both 1-origin indexing (for array A) and 0-origin indexing (for arrays L and R). Using 0-origin indexing for L and R makes for a simpler loop invariant in Exercise 2.3-3.

**Figure 2.3** The operation of the **while** loop in lines 8–18 in the call MERGE(A; 9; 12; 16), when the subarray A[9 : 16] contains the values h2; 4; 6; 7; 1; 2; 3; 5i. After allocating and copying into the arrays L and R, the array L contains h2; 4; 6; 7i, and the array R contains h1; 2; 3; 5i. Tan positions in A contain their final values, and tan positions in L and R contain values that have yet to be copied back into A. Taken together, the tan positions always comprise the values originally in A[9 : 16]. Blue positions in A contain values that will be copied over, and dark positions in L and R contain values that have already been copied back into A. **(a)–(g)** The arrays A, L, and R, and their respective indices k, i, and j prior to each iteration of the loop of lines 12–18. At the point in part (g), all values in R have been copied back into A (indicated by j equaling the length of R), and so the **while** loop in lines 12–18 terminates. **(h)** The arrays and indices at termination. The **while** loops of lines 20–23 and 24–27 copied back into A the remaining values in L and R, which are the largest values originally in A[9 : 16]. Here, lines 20–23 copied L[2 : 3] into A[15 : 16], and because all values in R had already been copied back into A, the **while** loop of lines 24–27 iterated 0 times. At this point, the subarray in A[9 : 16] is sorted.

be copied back into A[p : r] and copies it back in. As the comments indicate, the index k gives the position of A that is being filled in, and the indices i and j give the positions in L and R, respectively, of the smallest remaining values. Eventually, either all of L or all of R is copied back into A[p : r], and this loop terminates. If the loop terminates because all of R has been copied back, that is, because j equals nR, then i is still less than nL, so that some of L has yet to be copied back, and these values are the greatest in both L and R. In this case, the **while** loop of lines 20–23 copies these remaining values of L into the last few positions of A[p : r]. Because j equals nR, the **while** loop of lines 24–27 iterates 0 times. If instead the **while** loop of lines 12–18 terminates because i equals nL, then all of L has already been copied back into A[p : r], and the **while** loop of lines 24–27 copies the remaining values of R back into the end of A[p : r].

To see that the MERGE procedure runs in Θ(n) time, where n = r - p + 1, 13 observe that each of lines 1–3 and 8–10 takes constant time, and the **for** loops of lines 4–7 take Θ(n<sup>L</sup> + nR) = Θ(n) time. <sup>14</sup> To account for the three **while** loops of lines 12–18, 20–23, and 24–27, observe that each iteration of these loops copies exactly one value from L or R back into A and that every value is copied back into A exactly once. Therefore, these three loops together make a total of n iterations. Since each iteration of each of the three loops takes constant time, the total time spent in these three loops is Θ(n).

We can now use the MERGE procedure as a subroutine in the merge sort algorithm. The procedure MERGE-SORT(A; p; r) on the facing page sorts the elements in the subarray A[p : r]. If p equals r, the subarray has just 1 element and is therefore already sorted. Otherwise, we must have p < r, and MERGE-SORT runs the divide, conquer, and combine steps. The divide step simply computes an index q that partitions A[p : r] into two adjacent subarrays: A[p : q], containing ⌈n/2⌉ elements, and A[q + 1 : r], containing ⌊n/2⌋ elements. <sup>15</sup> The initial call MERGE-SORT(A; 1; n) sorts the entire array A[1 : n].

Figure 2.4 illustrates the operation of the procedure for n = 8, showing also the sequence of divide and merge steps. The algorithm recursively divides the array down to 1-element subarrays. The combine steps merge pairs of 1-element subar-

<sup>13</sup> If you're wondering where the "+1" comes from, imagine that r = p + 1. Then the subarray A[p : r] consists of two elements, and r - p + 1 = 2.

<sup>14</sup> Chapter 3 shows how to formally interpret equations containing Θ-notation.

<sup>15</sup> The expression ⌈x⌉ denotes the least integer greater than or equal to x, and ⌊x⌋ denotes the greatest integer less than or equal to x. These notations are defined in Section 3.3. The easiest way to verify that setting q to ⌊(p + r)/2⌋ yields subarrays A[p : q] and A[q + 1 : r] of sizes ⌈n/2⌉ and ⌊n/2⌋, respectively, is to examine the four cases that arise depending on whether each of p and r is odd or even.

```
MERGE-SORT(A; p; r)
1 if p ≥ r // zero or one element?
2 return
3 q = ⌊(p + r)/2⌋ // midpoint of A[p : r]
4 MERGE-SORT(A; p; q) // recursively sort A[p : q]
5 MERGE-SORT(A; q + 1; r) // recursively sort A[q + 1 : r]
6 // Merge A[p : q] and A[q + 1 : r] into A[p : r]. 
7 MERGE(A; p; q; r)
```

rays to form sorted subarrays of length 2, merges those to form sorted subarrays of length 4, and merges those to form the final sorted subarray of length 8. If n is not an exact power of 2, then some divide steps create subarrays whose lengths differ by 1. (For example, when dividing a subarray of length 7, one subarray has length 4 and the other has length 3.) Regardless of the lengths of the two subarrays being merged, the time to merge a total of n items is Θ(n).

## **2.3.2 Analyzing divide-and-conquer algorithms**

When an algorithm contains a recursive call, you can often describe its running time by a *recurrence equation* or *recurrence*, which describes the overall running time on a problem of size n in terms of the running time of the same algorithm on smaller inputs. You can then use mathematical tools to solve the recurrence and provide bounds on the performance of the algorithm.

A recurrence for the running time of a divide-and-conquer algorithm falls out from the three steps of the basic method. As we did for insertion sort, let T(n) be the worst-case running time on a problem of size n. If the problem size is small enough, say n < n<sup>0</sup> for some constant n<sup>0</sup> > 0, the straightforward solution takes constant time, which we write as Θ(1). <sup>16</sup> Suppose that the division of the problem yields a subproblems, each with size n/b, that is, 1/b the size of the original. For merge sort, both a and b are 2, but we'll see other divide-and-conquer algorithms in which a ≠ b. It takes T(n/b) time to solve one subproblem of size n/b, and so it takes aT(n/b) time to solve all a of them. If it takes D(n) time to divide the problem into subproblems and C(n) time to combine the solutions to the subproblems into the solution to the original problem, we get the recurrence

<sup>16</sup> If you're wondering where Θ(1) comes from, think of it this way. When we say that n <sup>2</sup>/100 is Θ(n<sup>2</sup> ), we are ignoring the coefficient 1/100 of the factor n 2 . Likewise, when we say that a constant c is Θ(1), we are ignoring the coefficient c of the factor 1 (which you can also think of as n 0 ).

**Figure 2.4** The operation of merge sort on the array A with length 8 that initially contains the sequence h12; 3; 7; 9; 14; 6; 11; 2i. The indices p, q, and r into each subarray appear above their values. Numbers in italics indicate the order in which the MERGE-SORT and MERGE procedures are called following the initial call of MERGE-SORT(A; 1; 8).

$$T(n) = \begin{cases} \Theta(1) & \text{if } n < n_0 ,\\ D(n) + aT(n/b) + C(n) & \text{otherwise} . \end{cases}$$

Chapter 4 shows how to solve common recurrences of this form.

Sometimes, the n/b size of the divide step isn't an integer. For example, the MERGE-SORT procedure divides a problem of size n into subproblems of sizes ⌈n/2⌉ and ⌊n/2⌋. Since the difference between ⌈n/2⌉ and ⌊n/2⌋ is at most 1, 

which for large n is much smaller than the effect of dividing n by 2, we'll squint a little and just call them both size n/2. As Chapter 4 will discuss, this simplification of ignoring floors and ceilings does not generally affect the order of growth of a solution to a divide-and-conquer recurrence.

Another convention we'll adopt is to omit a statement of the base cases of the recurrence, which we'll also discuss in more detail in Chapter 4. The reason is that the base cases are pretty much always T(n) = Θ(1) if n < n<sup>0</sup> for some constant n<sup>0</sup> > 0. That's because the running time of an algorithm on an input of constant size is constant. We save ourselves a lot of extra writing by adopting this convention.

## **Analysis of merge sort**

Here's how to set up the recurrence for T(n), the worst-case running time of merge sort on n numbers.

**Divide:** The divide step just computes the middle of the subarray, which takes constant time. Thus, D(n) = Θ(1).

**Conquer:** Recursively solving two subproblems, each of size n/2, contributes 2T(n/2) to the running time (ignoring the floors and ceilings, as we discussed).

**Combine:** Since the MERGE procedure on an n-element subarray takes Θ(n) time, we have C(n) = Θ(n).

When we add the functions D(n) and C(n) for the merge sort analysis, we are adding a function that is Θ(n) and a function that is Θ(1). This sum is a linear function of n. That is, it is roughly proportional to n when n is large, and so merge sort's dividing and combining times together are Θ(n). Adding Θ(n) to the 2T(n/2) term from the conquer step gives the recurrence for the worst-case running time T(n) of merge sort:

$$T(n) = 2T(n/2) + \Theta(n)$$
. (2.3)

Chapter 4 presents the "master theorem," which shows that T(n) = Θ(n lg n). 17 Compared with insertion sort, whose worst-case running time is Θ(n<sup>2</sup> ), merge sort trades away a factor of n for a factor of lg n. Because the logarithm function grows more slowly than any linear function, that's a good trade. For large enough inputs, merge sort, with its Θ(n lg n) worst-case running time, outperforms insertion sort, whose worst-case running time is Θ(n<sup>2</sup> ).

<sup>17</sup> The notation lg n stands for log <sup>2</sup> n, although the base of the logarithm doesn't matter here, but as computer scientists, we like logarithms base 2. Section 3.3 discusses other standard notation.

We do not need the master theorem, however, to understand intuitively why the solution to recurrence (2.3) is T(n) = Θ(n lg n). For simplicity, assume that n is an exact power of 2 and that the implicit base case is n = 1. Then recurrence (2.3) is essentially

$$T(n) = \begin{cases} c_1 & \text{if } n = 1, \\ 2T(n/2) + c_2 n & \text{if } n > 1, \end{cases}$$
 (2.4)

where the constant c<sup>1</sup> > 0 represents the time required to solve a problem of size 1, and c<sup>2</sup> > 0 is the time per array element of the divide and combine steps. <sup>18</sup>

Figure 2.5 illustrates one way of figuring out the solution to recurrence (2.4). Part (a) of the figure shows T(n), which part (b) expands into an equivalent tree representing the recurrence. The c2n term denotes the cost of dividing and combining at the top level of recursion, and the two subtrees of the root are the two smaller recurrences T(n/2). Part (c) shows this process carried one step further by expanding T(n/2). The cost for dividing and combining at each of the two nodes at the second level of recursion is c2n/2. Continue to expand each node in the tree by breaking it into its constituent parts as determined by the recurrence, until the problem sizes get down to 1, each with a cost of c1. Part (d) shows the resulting *recursion tree*.

Next, add the costs across each level of the tree. The top level has total cost c2n, the next level down has total cost c2(n/2) + c2(n/2) = c2n, the level after that has total cost c2(n/4) + c2(n/4) + c2(n/4) + c2(n/4) = c2n, and so on. Each level has twice as many nodes as the level above, but each node contributes only half the cost of a node from the level above. From one level to the next, doubling and halving cancel each other out, so that the cost across each level is the same: c2n. In general, the level that is i levels below the top has 2 <sup>i</sup> nodes, each contributing a cost of c2(n/2<sup>i</sup> ), so that the ith level below the top has total cost 2 i c2(n/2<sup>i</sup> ) = c2n. The bottom level has n nodes, each contributing a cost of c1, for a total cost of c1n.

The total number of levels of the recursion tree in Figure 2.5 is lg n + 1, where n is the number of leaves, corresponding to the input size. An informal inductive argument justifies this claim. The base case occurs when n = 1, in which case the tree has only 1 level. Since lg 1 = 0, we have that lg n + 1 gives the correct number of levels. Now assume as an inductive hypothesis that the number of levels of a recursion tree with 2 i leaves is lg 2 <sup>i</sup> + 1 = i + 1 (since for any value of i, we have that lg 2 <sup>i</sup> = i). Because we assume that the input size is an exact power of 2, the next input size to consider is 2 i+1 . A tree with n = 2 i+1 leaves has 1 more

<sup>18</sup> It is unlikely that c<sup>1</sup> is exactly the time to solve problems of size 1 and that c2n is exactly the time of the divide and combine steps. We'll look more closely at bounding recurrences in Chapter 4, where we'll be more careful about this kind of detail.

**Figure 2.5** How to construct a recursion tree for the recurrence (2.4). Part **(a)** shows T(n), which progressively expands in **(b)–(d)** to form the recursion tree. The fully expanded tree in part (d) has lg n + 1 levels. Each level above the leaves contributes a total cost of c2n, and the leaf level contributes c1n. The total cost, therefore, is c2n lg n + c1n = Θ(n lg n).

level than a tree with 2 i leaves, and so the total number of levels is (i + 1) + 1 = lg 2 i+1 + 1.

To compute the total cost represented by the recurrence (2.4), simply add up the costs of all the levels. The recursion tree has lg n + 1 levels. The levels above the leaves each cost c2n, and the leaf level costs c1n, for a total cost of c2n lg n+c1n = Θ(n lg n).

## **Exercises**

# *2.3-1*

Using Figure 2.4 as a model, illustrate the operation of merge sort on an array initially containing the sequence h3; 41; 52; 26; 38; 57; 9; 49i.

# *2.3-2*

The test in line 1 of the MERGE-SORT procedure reads "**if** p ≥ r" rather than "**if** p ≠ r." If MERGE-SORT is called with p > r, then the subarray A[p : r] is empty. Argue that as long as the initial call of MERGE-SORT(A; 1; n) has n ≥ 1, the test "**if** p ≠ r" suffices to ensure that no recursive call has p > r.

# *2.3-3*

State a loop invariant for the **while** loop of lines 12–18 of the MERGE procedure. Show how to use it, along with the **while** loops of lines 20–23 and 24–27, to prove that the MERGE procedure is correct.

## *2.3-4*

Use mathematical induction to show that when n ≥ 2 is an exact power of 2, the solution of the recurrence

$$T(n) = \begin{cases} 2 & \text{if } n = 2, \\ 2T(n/2) + n & \text{if } n > 2 \end{cases}$$

is 
$$T(n) = n \lg n$$
.

## *2.3-5*

You can also think of insertion sort as a recursive algorithm. In order to sort A[1 : n], recursively sort the subarray A[1 : n - 1] and then insert A[n] into the sorted subarray A[1 : n - 1]. Write pseudocode for this recursive version of insertion sort. Give a recurrence for its worst-case running time.

## *2.3-6*

Referring back to the searching problem (see Exercise 2.1-4), observe that if the subarray being searched is already sorted, the searching algorithm can check the midpoint of the subarray against v and eliminate half of the subarray from further 

consideration. The *binary search* algorithm repeats this procedure, halving the size of the remaining portion of the subarray each time. Write pseudocode, either iterative or recursive, for binary search. Argue that the worst-case running time of binary search is Θ(lg n).

## *2.3-7*

The **while** loop of lines 5–7 of the INSERTION-SORT procedure in Section 2.1 uses a linear search to scan (backward) through the sorted subarray A[1 : j - 1]. What if insertion sort used a binary search (see Exercise 2.3-6) instead of a linear search? Would that improve the overall worst-case running time of insertion sort to Θ(n lg n)?

# *2.3-8*

Describe an algorithm that, given a set S of n integers and another integer x, determines whether S contains two elements that sum to exactly x. Your algorithm should take Θ(n lg n) time in the worst case.

# **Problems**

## *2-1 Insertion sort on small arrays in merge sort*

Although merge sort runs in Θ(n lg n) worst-case time and insertion sort runs in Θ(n<sup>2</sup> ) worst-case time, the constant factors in insertion sort can make it faster in practice for small problem sizes on many machines. Thus it makes sense to *coarsen* the leaves of the recursion by using insertion sort within merge sort when subproblems become sufficiently small. Consider a modification to merge sort in which n/k sublists of length k are sorted using insertion sort and then merged using the standard merging mechanism, where k is a value to be determined.

- *a.* Show that insertion sort can sort the n/k sublists, each of length k, in Θ(nk) worst-case time.
- *b.* Show how to merge the sublists in Θ(n lg(n/k)) worst-case time.
- *c.* Given that the modified algorithm runs in Θ(nk + n lg(n/k)) worst-case time, what is the largest value of k as a function of n for which the modified algorithm has the same running time as standard merge sort, in terms of Θ-notation?
- *d.* How should you choose k in practice?

# *2-2 Correctness of bubblesort*

Bubblesort is a popular, but inefficient, sorting algorithm. It works by repeatedly swapping adjacent elements that are out of order. The procedure BUBBLESORT sorts array A[1 : n].

```
BUBBLESORT(A; n)
1 for i = 1 to n - 1
2 for j = n downto i + 1
3 if A[j] < A[j - 1]
4 exchange A[j] with A[j - 1]
```

*a.* Let A <sup>0</sup> denote the array A after BUBBLESORT(A; n) is executed. To prove that BUBBLESORT is correct, you need to prove that it terminates and that

$$A'[1] \le A'[2] \le \dots \le A'[n]$$
 (2.5)

In order to show that BUBBLESORT actually sorts, what else do you need to prove?

The next two parts prove inequality (2.5).

- *b.* State precisely a loop invariant for the **for** loop in lines 2–4, and prove that this loop invariant holds. Your proof should use the structure of the loop-invariant proof presented in this chapter.
- *c.* Using the termination condition of the loop invariant proved in part (b), state a loop invariant for the **for** loop in lines 1–4 that allows you to prove inequality (2.5). Your proof should use the structure of the loop-invariant proof presented in this chapter.
- *d.* What is the worst-case running time of BUBBLESORT? How does it compare with the running time of INSERTION-SORT?

#### *2-3 Correctness of Horner's rule*

You are given the coefficients a0; a1; a2; : : : ; a<sup>n</sup> of a polynomial

$$P(x) = \sum_{k=0}^{n} a_k x^k$$
  
=  $a_0 + a_1 x + a_2 x^2 + \dots + a_{n-1} x^{n-1} + a_n x^n$ ,

and you want to evaluate this polynomial for a given value of x. *Horner's rule* says to evaluate the polynomial according to this parenthesization:

$$P(x) = a_0 + x \Big( a_1 + x \Big( a_2 + \dots + x (a_{n-1} + x a_n) \dots \Big) \Big)$$

The procedure HORNER implements Horner's rule to evaluate P(x), given the coefficients a0; a1; a2; : : : ; a<sup>n</sup> in an array A[0 : n] and the value of x.

```
HORNER(A; n; x)
1 p = 0
2 for i = n downto 0
3 p = A[i] + x · p
4 return p
```

- *a.* In terms of Θ-notation, what is the running time of this procedure?
- *b.* Write pseudocode to implement the naive polynomial-evaluation algorithm that computes each term of the polynomial from scratch. What is the running time of this algorithm? How does it compare with HORNER?
- *c.* Consider the following loop invariant for the procedure HORNER:

At the start of each iteration of the **for** loop of lines 2–3,

$$p = \sum_{k=0}^{n-(i+1)} A[k+i+1] \cdot x^k.$$

Interpret a summation with no terms as equaling 0. Following the structure of the loop-invariant proof presented in this chapter, use this loop invariant to show that, at termination, p = $$\sum_{k=0}^{n} A[k] \cdot x^k.$$

## *2-4 Inversions*

Let A[1 : n] be an array of n distinct numbers. If i < j and A[i] > A[j], then the pair (i; j) is called an *inversion* of A.

- *a.* List the five inversions of the array h2; 3; 8; 6; 1i.
- *b.* What array with elements from the set {1; 2; : : : ; ng has the most inversions? How many does it have?
- *c.* What is the relationship between the running time of insertion sort and the number of inversions in the input array? Justify your answer.
- *d.* Give an algorithm that determines the number of inversions in any permutation on n elements in Θ(n lg n) worst-case time. (*Hint:* Modify merge sort.)

# **Chapter notes**

In 1968, Knuth published the first of three volumes with the general title *The Art of Computer Programming* [259, 260, 261]. The first volume ushered in the modern study of computer algorithms with a focus on the analysis of running time. The full series remains an engaging and worthwhile reference for many of the topics presented here. According to Knuth, the word "algorithm" is derived from the name "al-Khowârizmî," a ninth-century Persian mathematician.

Aho, Hopcroft, and Ullman [5] advocated the asymptotic analysis of algorithms—using notations that Chapter 3 introduces, including Θ-notation—as a means of comparing relative performance. They also popularized the use of recurrence relations to describe the running times of recursive algorithms.

Knuth [261] provides an encyclopedic treatment of many sorting algorithms. His comparison of sorting algorithms (page 381) includes exact step-counting analyses, like the one we performed here for insertion sort. Knuth's discussion of insertion sort encompasses several variations of the algorithm. The most important of these is Shell's sort, introduced by D. L. Shell, which uses insertion sort on periodic subarrays of the input to produce a faster sorting algorithm.

Merge sort is also described by Knuth. He mentions that a mechanical collator capable of merging two decks of punched cards in a single pass was invented in 1938. J. von Neumann, one of the pioneers of computer science, apparently wrote a program for merge sort on the EDVAC computer in 1945.

The early history of proving programs correct is described by Gries [200], who credits P. Naur with the first article in this field. Gries attributes loop invariants to R. W. Floyd. The textbook by Mitchell [329] is a good reference on how to prove programs correct.

# **3 Characterizing Running Times**

The order of growth of the running time of an algorithm, defined in Chapter 2, gives a simple way to characterize the algorithm's efficiency and also allows us to compare it with alternative algorithms. Once the input size n becomes large enough, merge sort, with its Θ(n lg n) worst-case running time, beats insertion sort, whose worst-case running time is Θ(n<sup>2</sup>). Although we can sometimes determine the exact running time of an algorithm, as we did for insertion sort in Chapter 2, the extra precision is rarely worth the effort of computing it. For large enough inputs, the multiplicative constants and lower-order terms of an exact running time are dominated by the effects of the input size itself.

When we look at input sizes large enough to make relevant only the order of growth of the running time, we are studying the *asymptotic* efficiency of algorithms. That is, we are concerned with how the running time of an algorithm increases with the size of the input *in the limit*, as the size of the input increases without bound. Usually, an algorithm that is asymptotically more efficient is the best choice for all but very small inputs.

This chapter gives several standard methods for simplifying the asymptotic analysis of algorithms. The next section presents informally the three most commonly used types of "asymptotic notation," of which we have already seen an example in Θ-notation. It also shows one way to use these asymptotic notations to reason about the worst-case running time of insertion sort. Then we look at asymptotic notations more formally and present several notational conventions used throughout this book. The last section reviews the behavior of functions that commonly arise when analyzing algorithms.