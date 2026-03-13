---
topic: strassens_algorithm
pages: 107-111
---

ing them both "additions" because subtraction is structurally the same computation as addition, except for a change of sign.

To get an inkling how the number of multiplications might be reduced, as well as why reducing the number of multiplications might be desirable for matrix calculations, suppose that you have two numbers x and y, and you want to calculate the quantity x² - y². The straightforward calculation requires two multiplications to square x and y, followed by one subtraction (which you can think of as a "negative addition"). But let's recall the old algebra trick x² - y² = x² - xy + xy - y² = x(x - y) + y(x - y) = (x + y)(x - y). Using this formulation of the desired quantity, you could instead compute the sum x + y and the difference x - y and then multiply them, requiring only a single multiplication and two additions. At the cost of an extra addition, only one multiplication is needed to compute an expression that looks as if it requires two. If x and y are scalars, there's not much difference: both approaches require three scalar operations. If x and y are large matrices, however, the cost of multiplying outweighs the cost of adding, in which case the second method outperforms the first, although not asymptotically.

Strassen's strategy for reducing the number of matrix multiplications at the expense of more matrix additions is not at all obvious—perhaps the biggest understatement in this book! As with MATRIX-MULTIPLY-RECURSIVE, Strassen's algorithm uses the divide-and-conquer method to compute C = A × B, where A, B, and C are all n × n matrices and n is an exact power of 2. Strassen's algorithm computes the four submatrices C₁₁, C₁₂, C₂₁, and C₂₂ of C from equations (4.5)–(4.8) on page 82 in four steps. We'll analyze costs as we go along to develop a recurrence T(n) for the overall running time. Let's see how it works:

- 1. If n = 1, the matrices each contain a single element. Perform a single scalar multiplication and a single scalar addition, as in line 3 of MATRIX-MULTIPLY-RECURSIVE, taking Θ(1) time, and return. Otherwise, partition the input matrices A and B and output matrix C into n/2 × n/2 submatrices, as in equation (4.2). This step takes Θ(1) time by index calculation, just as in MATRIX-MULTIPLY-RECURSIVE.
- 2. Create n/2 × n/2 matrices S₁, S₂, ..., S₁₀, each of which is the sum or difference of two submatrices from step 1. Create and zero the entries of seven n/2 × n/2 matrices P₁, P₂, ..., P₇ to hold seven n/2 × n/2 matrix products. All 17 matrices can be created, and the Pᵢ initialized, in Θ(n²) time.
- 3. Using the submatrices from step 1 and the matrices S₁, S₂, ..., S₁₀ created in step 2, recursively compute each of the seven matrix products P₁, P₂, ..., P₇, taking 7T(n/2) time.
- 4. Update the four submatrices C₁₁, C₁₂, C₂₁, C₂₂ of the result matrix C by adding or subtracting various Pᵢ matrices, which takes Θ(n²) time.

We'll see the details of steps 2–4 in a moment, but we already have enough information to set up a recurrence for the running time of Strassen's method. As is common, the base case in step 1 takes Θ(1) time, which we'll omit when stating the recurrence. When n > 1, steps 1, 2, and 4 take a total of Θ(n²) time, and step 3 requires seven multiplications of n/2 × n/2 matrices. Hence, we obtain the following recurrence for the running time of Strassen's algorithm:

$$T(n) = 7T(n/2) + \Theta(n^2). (4.10)$$

Compared with MATRIX-MULTIPLY-RECURSIVE, we have traded off one recursive submatrix multiplication for a constant number of submatrix additions. Once you understand recurrences and their solutions, you'll be able to see why this tradeoff actually leads to a lower asymptotic running time. By the master method in Section 4.5, recurrence (4.10) has the solution T(n) = Θ(n^(lg 7)) = O(n^2.81), beating the Θ(n³)-time algorithms.

Now, let's delve into the details. Step 2 creates the following 10 matrices:

$$\begin{array}{rcl} S_1 &=& B_{12} - B_{22} \;, \\ S_2 &=& A_{11} + A_{12} \;, \\ S_3 &=& A_{21} + A_{22} \;, \\ S_4 &=& B_{21} - B_{11} \;, \\ S_5 &=& A_{11} + A_{22} \;, \\ S_6 &=& B_{11} + B_{22} \;, \\ S_7 &=& A_{12} - A_{22} \;, \\ S_8 &=& B_{21} + B_{22} \;, \\ S_9 &=& A_{11} - A_{21} \;, \\ S_{10} &=& B_{11} + B_{12} \;. \end{array}$$

This step adds or subtracts n/2 × n/2 matrices 10 times, taking Θ(n²) time.

Step 3 recursively multiplies n/2 × n/2 matrices 7 times to compute the following n/2 × n/2 matrices, each of which is the sum or difference of products of A and B submatrices:

$$\begin{split} P_1 &= A_{11} \cdot S_1 \ (= A_{11} \cdot B_{12} - A_{11} \cdot B_{22}) \ , \\ P_2 &= S_2 \cdot B_{22} \ (= A_{11} \cdot B_{22} + A_{12} \cdot B_{22}) \ , \\ P_3 &= S_3 \cdot B_{11} \ (= A_{21} \cdot B_{11} + A_{22} \cdot B_{11}) \ , \\ P_4 &= A_{22} \cdot S_4 \ (= A_{22} \cdot B_{21} - A_{22} \cdot B_{11}) \ , \\ P_5 &= S_5 \cdot S_6 \ \ (= A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22}) \ , \\ P_6 &= S_7 \cdot S_8 \ \ (= A_{12} \cdot B_{21} + A_{12} \cdot B_{22} - A_{22} \cdot B_{21} - A_{22} \cdot B_{22}) \ , \\ P_7 &= S_9 \cdot S_{10} \ \ (= A_{11} \cdot B_{11} + A_{11} \cdot B_{12} - A_{21} \cdot B_{11} - A_{21} \cdot B_{12}) \ . \end{split}$$

The only multiplications that the algorithm performs are those in the middle column of these equations. The right-hand column just shows what these products equal in terms of the original submatrices created in step 1, but the terms are never explicitly calculated by the algorithm.

Step 4 adds to and subtracts from the four n/2 × n/2 submatrices of the product C the various Pᵢ matrices created in step 3. We start with

$$C_{11} = C_{11} + P_5 + P_4 - P_2 + P_6.$$

Expanding the calculation on the right-hand side, with the expansion of each Pᵢ on its own line and vertically aligning terms that cancel out, we see that the update to C₁₁ equals

$$\begin{array}{c} A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22} \\ - A_{22} \cdot B_{11} & + A_{22} \cdot B_{21} \\ - A_{11} \cdot B_{22} & - A_{12} \cdot B_{22} \\ \hline - A_{22} \cdot B_{22} - A_{22} \cdot B_{21} + A_{12} \cdot B_{22} + A_{12} \cdot B_{21} \\ \hline A_{11} \cdot B_{11} & + A_{12} \cdot B_{21} \end{array}$$

which corresponds to equation (4.5). Similarly, setting

$$C_{12} = C_{12} + P_1 + P_2$$

means that the update to C<sup>12</sup> equals

$$\frac{A_{11} \cdot B_{12} - A_{11} \cdot B_{22}}{+ A_{11} \cdot B_{22} + A_{12} \cdot B_{22}}$$

$$\frac{A_{11} \cdot B_{12}}{+ A_{12} \cdot B_{22}},$$

corresponding to equation (4.6). Setting

$$C_{21} = C_{21} + P_3 + P_4$$

means that the update to C<sup>21</sup> equals

$$\begin{array}{c}
A_{21} \cdot B_{11} + A_{22} \cdot B_{11} \\
- A_{22} \cdot B_{11} + A_{22} \cdot B_{21}
\end{array} \\
A_{21} \cdot B_{11} + A_{22} \cdot B_{21},$$

corresponding to equation (4.7). Finally, setting

$$C_{22} = C_{22} + P_5 + P_1 - P_3 - P_7$$

means that the update to C<sup>22</sup> equals

$$\begin{array}{c} A_{11} \cdot B_{11} + A_{11} \cdot B_{22} + A_{22} \cdot B_{11} + A_{22} \cdot B_{22} \\ - A_{11} \cdot B_{22} & + A_{11} \cdot B_{12} \\ - A_{22} \cdot B_{11} & - A_{21} \cdot B_{11} \\ - A_{11} \cdot B_{11} & - A_{11} \cdot B_{12} + A_{21} \cdot B_{11} + A_{21} \cdot B_{12} \\ \hline A_{22} \cdot B_{22} & + A_{21} \cdot B_{12} , \end{array}$$

which corresponds to equation (4.8). Altogether, since we add or subtract n/2 × n/2 matrices 12 times in step 4, this step indeed takes Θ(n²) time.

We can see that Strassen's remarkable algorithm, comprising steps 1–4, produces the correct matrix product using 7 submatrix multiplications and 18 submatrix additions. We can also see that recurrence (4.10) characterizes its running time. Since Section 4.5 shows that this recurrence has the solution T(n) = Θ(n^(lg 7)) = o(n³), Strassen's method asymptotically beats the Θ(n³) MATRIX-MULTIPLY and MATRIX-MULTIPLY-RECURSIVE procedures.

## **Exercises**

*Note:* You may wish to read Section 4.5 before attempting some of these exercises.

## *4.2-1*

Use Strassen's algorithm to compute the matrix product

$$\begin{pmatrix} 1 & 3 \\ 7 & 5 \end{pmatrix} \begin{pmatrix} 6 & 8 \\ 4 & 2 \end{pmatrix}$$

Show your work.

#### *4.2-2*

Write pseudocode for Strassen's algorithm.

## *4.2-3*

What is the largest k such that if you can multiply 3 × 3 matrices using k multiplications (not assuming commutativity of multiplication), then you can multiply n × n matrices in o(n^(lg 7)) time? What is the running time of this algorithm?

## *4.2-4*

V. Pan discovered a way of multiplying 68 × 68 matrices using 132,464 multiplications, a way of multiplying 70 × 70 matrices using 143,640 multiplications, and a way of multiplying 72 × 72 matrices using 155,424 multiplications. Which method yields the best asymptotic running time when used in a divide-and-conquer matrix-multiplication algorithm? How does it compare with Strassen's algorithm?

# *4.2-5*

Show how to multiply the complex numbers a + bi and c + di using only three multiplications of real numbers. The algorithm should take a, b, c, and d as input and produce the real component ac - bd and the imaginary component ad + bc separately.

## *4.2-6*

Suppose that you have a Θ(nᵅ)-time algorithm for squaring n × n matrices, where ᵅ ≥ 2. Show how to use that algorithm to multiply two different n × n matrices in Θ(nᵅ) time.

# **4.3 The substitution method for solving recurrences**

Now that you have seen how recurrences characterize the running times of divideand-conquer algorithms, let's learn how to solve them. We start in this section with the *substitution method*, which is the most general of the four methods in this chapter. The substitution method comprises two steps:

- 1. Guess the form of the solution using symbolic constants.
- 2. Use mathematical induction to show that the solution works, and find the constants.

To apply the inductive hypothesis, you substitute the guessed solution for the function on smaller values—hence the name "substitution method." This method is powerful, but you must guess the form of the answer. Although generating a good guess might seem difficult, a little practice can quickly improve your intuition.

You can use the substitution method to establish either an upper or a lower bound on a recurrence. It's usually best not to try to do both at the same time. That is, rather than trying to prove a Θ-bound directly, first prove an O-bound, and then prove an Ω-bound. Together, they give you a Θ-bound (Theorem 3.1 on page 56).

As an example of the substitution method, let's determine an asymptotic upper bound on the recurrence:

$$T(n) = 2T(\lfloor n/2 \rfloor) + \Theta(n). \tag{4.11}$$

This recurrence is similar to recurrence (2.3) on page 41 for merge sort, except for the floor function, which ensures that T(n) is defined over the integers. Let's guess that the asymptotic upper bound is the same—T(n) = O(n lg n)—and use the substitution method to prove it.

We'll adopt the inductive hypothesis that T(n) ≤ cn lg n for all n ≥ n₀, where we'll choose the specific constants c > 0 and n₀ > 0 later, after we see what