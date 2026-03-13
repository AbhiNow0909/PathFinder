---
topic: master_method
pages: 123-128
---

A master recurrence describes the running time of a divide-and-conquer algorithm that divides a problem of size n into a subproblems, each of size n/b < n. The algorithm solves the a subproblems recursively, each in T(n/b) time. The driving function f(n) encompasses the cost of dividing the problem before the recursion, as well as the cost of combining the results of the recursive solutions to subproblems. For example, the recurrence arising from Strassen's algorithm is a master recurrence with a = 7, b = 2, and driving function f(n) = Θ(n²).

As we have mentioned, in solving a recurrence that describes the running time of an algorithm, one technicality that we'd often prefer to ignore is the requirement that the input size n be an integer. For example, we saw that the running time of merge sort can be described by recurrence (2.3), T(n) = 2T(n/2) + Θ(n), on page 41. But if n is an odd number, we really don't have two problems of exactly half the size. Rather, to ensure that the problem sizes are integers, we round one subproblem down to size ⌊n/2⌋ and the other up to size ⌈n/2⌉, so the true recurrence is T(n) = T(⌈n/2⌉) + T(⌊n/2⌋) + Θ(n). But this floors-and-ceilings recurrence is longer to write and messier to deal with than recurrence (2.3), which is defined on the reals. We'd rather not worry about floors and ceilings, if we don't have to, especially since the two recurrences have the same Θ(n lg n) solution.

The master method allows you to state a master recurrence without floors and ceilings and implicitly infer them. No matter how the arguments are rounded up or down to the nearest integer, the asymptotic bounds that it provides remain the same. Moreover, as we'll see in Section 4.6, if you define your master recurrence on the reals, without implicit floors and ceilings, the asymptotic bounds still don't change. Thus you can ignore floors and ceilings for master recurrences. Section 4.7 gives sufficient conditions for ignoring floors and ceilings in more general divideand-conquer recurrences.

### **The master theorem**

The master method depends upon the following theorem.

#### *Theorem 4.1 (Master theorem)*

Let a ≥ 1 and b > 1 be constants, and let f(n) be a driving function that is defined and nonnegative on all sufficiently large reals. Define the recurrence T(n) on n ∈ ℕ by

$$T(n) = aT(n/b) + f(n),$$
 (4.17)

where aT(n/b) actually means a'T(⌊n/b⌋) + a''T(⌈n/b⌉) for some constants a' ≥ 0 and a'' ≥ 0 satisfying a = a' + a''. Then the asymptotic behavior of T(n) can be characterized as follows:

- 1. If there exists a constant ε > 0 such that f(n) = O(n^{log_b a − ε}), then T(n) = Θ(n^{log_b a}).
- 2. If there exists a constant k ≥ 0 such that f(n) = Θ(n^{log_b a} lg^k n), then T(n) = Θ(n^{log_b a} lg^{k+1} n).
- 3. If there exists a constant ε > 0 such that f(n) = Ω(n^{log_b a + ε}), and if f(n) additionally satisfies the *regularity condition* af(n/b) ≤ cf(n) for some constant c < 1 and all sufficiently large n, then T(n) = Θ(f(n)).

Before applying the master theorem to some examples, let's spend a few moments to understand broadly what it says. The function n^{log_b a} is called the *watershed function*. In each of the three cases, we compare the driving function f(n) to the watershed function n^{log_b a}. Intuitively, if the watershed function grows asymptotically faster than the driving function, then case 1 applies. Case 2 applies if the two functions grow at nearly the same asymptotic rate. Case 3 is the "opposite" of case 1, where the driving function grows asymptotically faster than the watershed function. But the technical details matter.

In case 1, not only must the watershed function grow asymptotically faster than the driving function, it must grow *polynomially* faster. That is, the watershed function n^{log_b a} must be asymptotically larger than the driving function f(n) by at least a factor of Θ(n^ε) for some constant ε > 0. The master theorem then says that the solution is T(n) = Θ(n^{log_b a}). In this case, if we look at the recursion tree for the recurrence, the cost per level grows at least geometrically from root to leaves, and the total cost of leaves dominates the total cost of the internal nodes.

In case 2, the watershed and driving functions grow at nearly the same asymptotic rate. But more specifically, the driving function grows faster than the watershed function by a factor of Θ(lg^k n), where k ≥ 0. The master theorem says that we tack on an extra lg n factor to f(n), yielding the solution T(n) = Θ(n^{log_b a} lg^{k+1} n). In this case, each level of the recursion tree costs approximately the same—Θ(n^{log_b a} lg^k n)—and there are Θ(lg n) levels. In practice, the most common situation for case 2 occurs when k = 0, in which case the watershed and driving functions have the same asymptotic growth, and the solution is T(n) = Θ(n^{log_b a} lg n).

Case 3 mirrors case 1. Not only must the driving function grow asymptotically faster than the watershed function, it must grow *polynomially* faster. That is, the driving function f(n) must be asymptotically larger than the watershed function n^{log_b a} by at least a factor of Θ(n^ε) for some constant ε > 0. Moreover, the driving function must satisfy the regularity condition that af(n/b) ≤ cf(n). This condition is satisfied by most of the polynomially bounded functions that you're likely to encounter when applying case 3. The regularity condition might not be satisfied

if the driving function grows slowly in local areas, yet relatively quickly overall. (Exercise 4.5-5 gives an example of such a function.) For case 3, the master theorem says that the solution is T(n) = Θ(f(n)). If we look at the recursion tree, the cost per level drops at least geometrically from the root to the leaves, and the root cost dominates the cost of all other nodes.

It's worth looking again at the requirement that there be polynomial separation between the watershed function and the driving function for either case 1 or case 3 to apply. The separation doesn't need to be much, but it must be there, and it must grow polynomially. For example, for the recurrence T(n) = 4T(n/2) + n^{1.99} (admittedly not a recurrence you're likely to see when analyzing an algorithm), the watershed function is n^{log_b a} = n². Hence the driving function f(n) = n^{1.99} is polynomially smaller by a factor of n^{0.01}. Thus case 1 applies with ε = 0.01.

## **Using the master method**

To use the master method, you determine which case (if any) of the master theorem applies and write down the answer.

As a first example, consider the recurrence T(n) = 9T(n/3) + n. For this recurrence, we have a = 9 and b = 3, which implies that n^{log_b a} = n^{log_3 9} = Θ(n²). Since f(n) = n = O(n^{2−ε}) for any constant ε ≤ 1, we can apply case 1 of the master theorem to conclude that the solution is T(n) = Θ(n²).

Now consider the recurrence T(n) = T(2n/3) + 1, which has a = 1 and b = 3/2, which means that the watershed function is n^{log_b a} = n^{log_{3/2} 1} = n⁰ = 1. Case 2 applies since f(n) = 1 = Θ(n^{log_b a} lg⁰ n) = Θ(1). The solution to the recurrence is T(n) = Θ(lg n).

For the recurrence T(n) = 3T(n/4) + n lg n, we have a = 3 and b = 4, which means that n^{log_b a} = n^{log_4 3} = O(n^{0.793}). Since f(n) = n lg n = Ω(n^{log_4 3 + ε}), where ε can be as large as approximately 0.2, case 3 applies as long as the regularity condition holds for f(n). It does, because for sufficiently large n, we have that af(n/b) = 3(n/4)lg(n/4) ≤ (3/4)n lg n = cf(n) for c = 3/4. By case 3, the solution to the recurrence is T(n) = Θ(n lg n).

Next, let's look at the recurrence T(n) = 2T(n/2) + n lg n, where we have a = 2, b = 2, and n^{log_b a} = n^{log_2 2} = n. Case 2 applies since f(n) = n lg n = Θ(n^{log_b a} lg¹ n). We conclude that the solution is T(n) = Θ(n lg² n).

We can use the master method to solve the recurrences we saw in Sections 2.3.2, 4.1, and 4.2.

Recurrence (2.3), T(n) = 2T(n/2) + Θ(n), on page 41, characterizes the running time of merge sort. Since a = 2 and b = 2, the watershed function is n^{log_b a} = n^{log_2 2} = n. Case 2 applies because f(n) = Θ(n), and the solution is T(n) = Θ(n lg n).

Recurrence (4.9), T(n) = 8T(n/2) + Θ(1), on page 84, describes the running time of the simple recursive algorithm for matrix multiplication. We have a = 8 and b = 2, which means that the watershed function is n^{log_b a} = n^{log_2 8} = n³. Since n³ is polynomially larger than the driving function f(n) = Θ(1)—indeed, we have f(n) = O(n^{3−ε}) for any positive ε < 3—case 1 applies. We conclude that T(n) = Θ(n³).

Finally, recurrence (4.10), T(n) = 7T(n/2) + Θ(n²), on page 87, arose from the analysis of Strassen's algorithm for matrix multiplication. For this recurrence, we have a = 7 and b = 2, and the watershed function is n^{log_b a} = n^{lg 7}. Observing that lg 7 = 2.807355..., we can let ε = 0.8 and bound the driving function f(n) = Θ(n²) = O(n^{lg 7 − ε}). Case 1 applies with solution T(n) = Θ(n^{lg 7}).

## **When the master method doesn't apply**

There are situations where you can't use the master theorem. For example, it can be that the watershed function and the driving function cannot be asymptotically compared. We might have that f(n) ≪ n^{log_b a} for an infinite number of values of n but also that f(n) ≫ n^{log_b a} for an infinite number of different values of n. As a practical matter, however, most of the driving functions that arise in the study of algorithms can be meaningfully compared with the watershed function. If you encounter a master recurrence for which that's not the case, you'll have to resort to substitution or other methods.

Even when the relative growths of the driving and watershed functions can be compared, the master theorem does not cover all the possibilities. There is a gap between cases 1 and 2 when f(n) = o(n^{log_b a}), yet the watershed function does not grow polynomially faster than the driving function. Similarly, there is a gap between cases 2 and 3 when f(n) = ω(n^{log_b a}) and the driving function grows more than polylogarithmically faster than the watershed function, but it does not grow polynomially faster. If the driving function falls into one of these gaps, or if the regularity condition in case 3 fails to hold, you'll need to use something other than the master method to solve the recurrence.

As an example of a driving function falling into a gap, consider the recurrence T(n) = 2T(n/2) + n/lg n. Since a = 2 and b = 2, the watershed function is n^{log_b a} = n^{log_2 2} = n¹ = n. The driving function is n/lg n = o(n), which means that it grows asymptotically more slowly than the watershed function n. But n/lg n grows only *logarithmically* slower than n, not *polynomially* slower. More precisely, equation (3.24) on page 67 says that lg n = o(n^ε) for any constant ε > 0, which means that 1/lg n = ω(n^{−ε}) and n/lg n = ω(n^{1−ε}) = ω(n^{log_b a − ε}). Thus no constant ε > 0 exists such that n/lg n = O(n^{log_b a − ε}), which is required for case 1 to apply. Case 2 fails to apply as well, since n/lg n ≠ Θ(n^{log_b a} lg^k n), where k = −1, but k must be nonnegative for case 2 to apply.

To solve this kind of recurrence, you must use another method, such as the substitution method (Section 4.3) or the Akra-Bazzi method (Section 4.7). (Exercise 4.6-3 asks you to show that the answer is Θ(n lg lg n).) Although the master theorem doesn't handle this particular recurrence, it does handle the overwhelming majority of recurrences that tend to arise in practice.

# **Exercises**

# *4.5-1*

Use the master method to give tight asymptotic bounds for the following recurrences.

a. 
$$T(n) = 2T(n/4) + 1$$
.

**b.** 
$$T(n) = 2T(n/4) + \sqrt{n}$$
.

c. 
$$T(n) = 2T(n/4) + \sqrt{n} \lg^2 n$$
.

**d.** 
$$T(n) = 2T(n/4) + n$$
.

e. 
$$T(n) = 2T(n/4) + n^2$$
.

## *4.5-2*

Professor Caesar wants to develop a matrix-multiplication algorithm that is asymptotically faster than Strassen's algorithm. His algorithm will use the divide-and-conquer method, dividing each matrix into n/4 × n/4 submatrices, and the divide and combine steps together will take Θ(n²) time. Suppose that the professor's algorithm creates a recursive subproblems of size n/4. What is the largest integer value of a for which his algorithm could possibly run asymptotically faster than Strassen's?

## *4.5-3*

Use the master method to show that the solution to the binary-search recurrence T(n) = T(n/2) + Θ(1) is T(n) = Θ(lg n). (See Exercise 2.3-6 for a description of binary search.)

## *4.5-4*

Consider the function f(n) = lg n. Argue that although f(n/2) < f(n), the regularity condition af(n/b) ≤ cf(n) with a = 1 and b = 2 does not hold for any constant c < 1. Argue further that for any ε > 0, the condition in case 3 that f(n) = Ω(n^{log_b a + ε}) does not hold.

## *4.5-5*

Show that for suitable constants a, b, and ε, the function f(n) = 2^{⌈lg n⌉} satisfies all the conditions in case 3 of the master theorem except the regularity condition.

# ⋆ **4.6 Proof of the continuous master theorem**

Proving the master theorem (Theorem 4.1) in its full generality, especially dealing with the knotty technical issue of floors and ceilings, is beyond the scope of this book. This section, however, states and proves a variant of the master theorem, called the *continuous master theorem*¹ in which the master recurrence (4.17) is defined over sufficiently large positive real numbers. The proof of this version, uncomplicated by floors and ceilings, contains the main ideas needed to understand how master recurrences behave. Section 4.7 discusses floors and ceilings in divide-and-conquer recurrences at greater length, presenting sufficient conditions for them not to affect the asymptotic solutions.

Of course, since you need not understand the proof of the master theorem in order to apply the master method, you may choose to skip this section. But if you wish to study more-advanced algorithms beyond the scope of this textbook, you may appreciate a better understanding of the underlying mathematics, which the proof of the continuous master theorem provides.

Although we usually assume that recurrences are algorithmic and don't require an explicit statement of a base case, we must be much more careful for proofs that justify the practice. The lemmas and theorem in this section explicitly state the base cases, because the inductive proofs require mathematical grounding. It is common in the world of mathematics to be extraordinarily careful proving theorems that justify acting more casually in practice.

The proof of the continuous master theorem involves two lemmas. Lemma 4.2 uses a slightly simplified master recurrence with a threshold constant of n₀ = 1, rather than the more general n₀ > 0 threshold constant implied by the unstated base case. The lemma employs a recursion tree to reduce the solution of the simplified master recurrence to that of evaluating a summation. Lemma 4.3 then provides asymptotic bounds for the summation, mirroring the three cases of the master theorem. Finally, the continuous master theorem itself (Theorem 4.4) gives asymptotic bounds for master recurrences, while generalizing to an arbitrary threshold constant n₀ > 0 as implied by the unstated base case.

¹ This terminology does not mean that either T(n) or f(n) need be continuous, only that the domain of T(n) is the real numbers, as opposed to integers.