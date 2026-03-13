---
topic: matrix_multiplication
pages: 102-106
---

you should read Section D.1.) Let A = .aik/ and B = .bjk/ be square n n matrices. The matrix product C = A B is also an n n matrix, where for i; j = 1; 2; : : : ; n, the .i; j / entry of C is given by

$$c_{ij} = \sum_{k=1}^{n} a_{ik} \cdot b_{kj} . (4.1)$$

Generally, we'll assume that the matrices are *dense*, meaning that most of the n 2 entries are not 0, as opposed to *sparse*, where most of the n 2 entries are 0 and the nonzero entries can be stored more compactly than in an n n array.

Computing the matrix C requires computing n <sup>2</sup> matrix entries, each of which is the sum of n pairwise products of input elements from A and B. The MATRIX-MULTIPLY procedure implements this strategy in a straightforward manner, and it generalizes the problem slightly. It takes as input three n n matrices A, B, and C, and it adds the matrix product A B to C, storing the result in C. Thus, it computes C = C C A B, instead of just C = A B. If only the product A B is needed, just initialize all n 2 entries of C to 0 before calling the procedure, which takes an additional '.n<sup>2</sup> / time. We'll see that the cost of matrix multiplication asymptotically dominates this initialization cost.

```
MATRIX-MULTIPLY .A; B; C; n/
1 for i = 1 to n // compute entries in each of n rows 
2 for j = 1 to n // compute n entries in row i
3 for k = 1 to n
4 cij D cij C aik  bkj // add in another term of equation (4.1)
```

The pseudocode for MATRIX-MULTIPLY works as follows. The **for** loop of lines 1–4 computes the entries of each row i, and within a given row i, the **for** loop of lines 2–4 computes each of the entries cij for each column j . Each iteration of the **for** loop of lines 3–4 adds in one more term of equation (4.1).

Because each of the triply nested **for** loops runs for exactly n iterations, and each execution of line 4 takes constant time, the MATRIX-MULTIPLY procedure operates in '.n<sup>3</sup> / time. Even if we add in the '.n<sup>2</sup> / time for initializing C to 0, the running time is still '.n<sup>3</sup> /.

#### **A simple divide-and-conquer algorithm**

Let's see how to compute the matrix product A B using divide-and-conquer. For n > 1, the divide step partitions the nn matrices into four n=2n=2 submatrices. We'll assume that n is an exact power of 2, so that as the algorithm recurses, we are guaranteed that the submatrix dimensions are integer. (Exercise 4.1-1 asks you to relax this assumption.) As with MATRIX-MULTIPLY, we'll actually compute C = C CAB. But to simplify the math behind the algorithm, let's assume that C has been initialized to the zero matrix, so that we are indeed computing C = AB.

The divide step views each of the nn matrices A, B, and C as four n=2n=2 submatrices:

$$A = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix}, \quad B = \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}, \quad C = \begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix}. \tag{4.2}$$

Then we can write the matrix product as

$$\begin{pmatrix} C_{11} & C_{12} \\ C_{21} & C_{22} \end{pmatrix} = \begin{pmatrix} A_{11} & A_{12} \\ A_{21} & A_{22} \end{pmatrix} \begin{pmatrix} B_{11} & B_{12} \\ B_{21} & B_{22} \end{pmatrix}$$
(4.3)

$$= \begin{pmatrix} A_{11} \cdot B_{11} + A_{12} \cdot B_{21} & A_{11} \cdot B_{12} + A_{12} \cdot B_{22} \\ A_{21} \cdot B_{11} + A_{22} \cdot B_{21} & A_{21} \cdot B_{12} + A_{22} \cdot B_{22} \end{pmatrix}, \tag{4.4}$$

which corresponds to the equations

$$C_{11} = A_{11} \cdot B_{11} + A_{12} \cdot B_{21} , (4.5)$$

$$C_{12} = A_{11} \cdot B_{12} + A_{12} \cdot B_{22} , (4.6)$$

$$C_{21} = A_{21} \cdot B_{11} + A_{22} \cdot B_{21} , (4.7)$$

$$C_{22} = A_{21} \cdot B_{12} + A_{22} \cdot B_{22} . (4.8)$$

Equations (4.5)–(4.8) involve eight n=2 n=2 multiplications and four additions of n=2 n=2 submatrices.

As we look to transform these equations to an algorithm that can be described with pseudocode, or even implemented for real, there are two common approaches for implementing the matrix partitioning.

One strategy is to allocate temporary storage to hold A's four submatrices A11, A12, A21, and A22 and B's four submatrices B11, B12, B21, and B22. Then copy each element in A and B to its corresponding location in the appropriate submatrix. After the recursive conquer step, copy the elements in each of C's four submatrices C11, C12, C21, and C22 to their corresponding locations in C. This approach takes '.n<sup>2</sup> / time, since 3n<sup>2</sup> elements are copied.

The second approach uses index calculations and is faster and more practical. A submatrix can be specified within a matrix by indicating where within the matrix the submatrix lies without touching any matrix elements. Partitioning a matrix (or recursively, a submatrix) only involves arithmetic on this location information, which has constant size independent of the size of the matrix. Changes to the submatrix elements update the original matrix, since they occupy the same storage.

Going forward, we'll assume that index calculations are used and that partitioning can be performed in '.1/ time. Exercise 4.1-3 asks you to show that it makes no difference to the overall asymptotic running time of matrix multiplication, however, whether the partitioning of matrices uses the first method of copying or the second method of index calculation. But for other divide-and-conquer matrix calculations, such as matrix addition, it can make a difference, as Exercise 4.1-4 asks you to show.

The procedure MATRIX-MULTIPLY-RECURSIVE uses equations (4.5)–(4.8) to implement a divide-and-conquer strategy for square-matrix multiplication. Like MATRIX-MULTIPLY, the procedure MATRIX-MULTIPLY-RECURSIVE computes C = C C A B since, if necessary, C can be initialized to 0 before the procedure is called in order to compute only C = A B.

```
MATRIX-MULTIPLY-RECURSIVE .A; B; C; n/
1 if n == 1
2 // Base case. 
3 c11 D c11 C a11  b11
4 return
5 // Divide. 
6 partition A, B, and C into n=2  n=2 submatrices 
       A11; A12; A21; A22; B11; B12; B21; B22; 
       and C11; C12; C21; C22; respectively 
7 // Conquer. 
8 MATRIX-MULTIPLY-RECURSIVE .A11; B11; C11; n=2/
9 MATRIX-MULTIPLY-RECURSIVE .A11; B12; C12; n=2/
10 MATRIX-MULTIPLY-RECURSIVE .A21; B11; C21; n=2/
11 MATRIX-MULTIPLY-RECURSIVE .A21; B12; C22; n=2/
12 MATRIX-MULTIPLY-RECURSIVE .A12; B21; C11; n=2/
13 MATRIX-MULTIPLY-RECURSIVE .A12; B22; C12; n=2/
14 MATRIX-MULTIPLY-RECURSIVE .A22; B21; C21; n=2/
15 MATRIX-MULTIPLY-RECURSIVE .A22; B22; C22; n=2/
```

As we walk through the pseudocode, we'll derive a recurrence to characterize its running time. Let T .n/ be the worst-case time to multiply two n n matrices using this procedure.

In the base case, when n = 1, line 3 performs just the one scalar multiplication and one addition, which means that T .1/ D '.1/. As is our convention for constant base cases, we can omit this base case in the statement of the recurrence.

The recursive case occurs when n > 1. As discussed, we'll use index calculations to partition the matrices in line 6, taking '.1/ time. Lines 8–15 recursively call MATRIX-MULTIPLY-RECURSIVE a total of eight times. The first four recursive calls compute the first terms of equations (4.5)–(4.8), and the subsequent four recursive calls compute and add in the second terms. Each recursive call adds the product of a submatrix of A and a submatrix of B to the appropriate submatrix of C in place, thanks to index calculations. Because each recursive call multiplies two n=2 n=2 matrices, thereby contributing T .n=2/ to the overall running time, the time taken by all eight recursive calls is 8T .n=2/. There is no combine step, because the matrix C is updated in place. The total time for the recursive case, therefore, is the sum of the partitioning time and the time for all the recursive calls, or '.1/ C 8T .n=2/.

Thus, omitting the statement of the base case, our recurrence for the running time of MATRIX-MULTIPLY-RECURSIVE is

$$T(n) = 8T(n/2) + \Theta(1). \tag{4.9}$$

As we'll see from the master method in Section 4.5, recurrence (4.9) has the solution T .n/ D '.n<sup>3</sup> /, which means that it has the same asymptotic running time as the straightforward MATRIX-MULTIPLY procedure.

Why is the '.n<sup>3</sup> / solution to this recurrence so much larger than the '.n lg n/ solution to the merge-sort recurrence (2.3) on page 41? After all, the recurrence for merge sort contains a '.n/ term, whereas the recurrence for recursive matrix multiplication contains only a '.1/ term.

Let's think about what the recursion tree for recurrence (4.9) would look like as compared with the recursion tree for merge sort, illustrated in Figure 2.5 on page 43. The factor of 2 in the merge-sort recurrence determines how many children each tree node has, which in turn determines how many terms contribute to the sum at each level of the tree. In comparison, for the recurrence (4.9) for MATRIX-MULTIPLY-RECURSIVE, each internal node in the recursion tree has eight children, not two, leading to a "bushier" recursion tree with many more leaves, despite the fact that the internal nodes are each much smaller. Consequently, the solution to recurrence (4.9) grows much more quickly than the solution to recurrence (2.3), which is borne out in the actual solutions: '.n<sup>3</sup> / versus '.n lg n/.

### **Exercises**

*Note:* You may wish to read Section 4.5 before attempting some of these exercises.

## *4.1-1*

Generalize MATRIX-MULTIPLY-RECURSIVE to multiply nn matrices for which n is not necessarily an exact power of 2. Give a recurrence describing its running time. Argue that it runs in '.n<sup>3</sup> / time in the worst case.

## *4.1-2*

How quickly can you multiply a kn n matrix (kn rows and n columns) by an n kn matrix, where k 1, using MATRIX-MULTIPLY-RECURSIVE as a subroutine? Answer the same question for multiplying an n kn matrix by a kn n matrix. Which is asymptotically faster, and by how much?

# *4.1-3*

Suppose that instead of partitioning matrices by index calculation in MATRIX-MULTIPLY-RECURSIVE, you copy the appropriate elements of A, B, and C into separate n=2 n=2 submatrices A11, A12, A21, A22; B11, B12, B21, B22; and C11, C12, C21, C22, respectively. After the recursive calls, you copy the results from C11, C12, C21, and C22 back into the appropriate places in C. How does recurrence (4.9) change, and what is its solution?

# *4.1-4*

Write pseudocode for a divide-and-conquer algorithm MATRIX-ADD-RECURSIVE that sums two n n matrices A and B by partitioning each of them into four n=2 n=2 submatrices and then recursively summing corresponding pairs of submatrices. Assume that matrix partitioning uses '.1/-time index calculations. Write a recurrence for the worst-case running time of MATRIX-ADD-RECURSIVE, and solve your recurrence. What happens if you use '.n<sup>2</sup> /-time copying to implement the partitioning instead of index calculations?

# **4.2 Strassen's algorithm for matrix multiplication**

You might find it hard to imagine that any matrix multiplication algorithm could take less than '.n<sup>3</sup> / time, since the natural definition of matrix multiplication requires n 3 scalar multiplications. Indeed, many mathematicians presumed that it was not possible to multiply matrices in o.n<sup>3</sup> / time until 1969, when V. Strassen [424] published a remarkable recursive algorithm for multiplying n n matrices. Strassen's algorithm runs in '.nlg <sup>7</sup> / time. Since lg 7 = 2:8073549 : : :, Strassen's algorithm runs in O.n2:81/ time, which is asymptotically better than the '.n<sup>3</sup> / MATRIX-MULTIPLY and MATRIX-MULTIPLY-RECURSIVE procedures.

The key to Strassen's method is to use the divide-and-conquer idea from the MATRIX-MULTIPLY-RECURSIVE procedure, but make the recursion tree less bushy. We'll actually increase the work for each divide and combine step by a constant factor, but the reduction in bushiness will pay off. We won't reduce the bushiness from the eight-way branching of recurrence (4.9) all the way down to the two-way branching of recurrence (2.3), but we'll improve it just a little, and that will make a big difference. Instead of performing eight recursive multiplications of n=2 n=2 matrices, Strassen's algorithm performs only seven. The cost of eliminating one matrix multiplication is several new additions and subtractions of n=2 n=2 matrices, but still only a constant number. Rather than saying "additions and subtractions" everywhere, we'll adopt the common terminology of calling