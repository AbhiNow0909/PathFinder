---
topic: dynamic_programming_intro
pages: 384-394
---

*14.1 Rod cutting 363* 

rods of smaller length in a way that maximizes their total value. Section 14.2 shows how to multiply a chain of matrices while performing the fewest total scalar multiplications. Given these examples of dynamic programming, Section 14.3 discusses two key characteristics that a problem must have for dynamic programming to be a viable solution technique. Section 14.4 then shows how to find the longest common subsequence of two sequences via dynamic programming. Finally, Section 14.5 uses dynamic programming to construct binary search trees that are optimal, given a known distribution of keys to be looked up.

### **14.1 Rod cutting**

Our first example uses dynamic programming to solve a simple problem in deciding where to cut steel rods. Serling Enterprises buys long steel rods and cuts them into shorter rods, which it then sells. Each cut is free. The management of Serling Enterprises wants to know the best way to cut up the rods.

Serling Enterprises has a table giving, for i = 1, 2, ..., the price pᵢ in dollars that they charge for a rod of length i inches. The length of each rod in inches is always an integer. Figure 14.1 gives a sample price table.

The *rod-cutting problem* is the following. Given a rod of length n inches and a table of prices pᵢ for i = 1, 2, ..., n, determine the maximum revenue rₙ obtainable by cutting up the rod and selling the pieces. If the price pₙ for a rod of length n is large enough, an optimal solution might require no cutting at all.

Serling Enterprises can cut up a rod of length n in 2 n1 different ways, since they have an independent option of cutting, or not cutting, at distance i inches {rom the left end, {or i = 1; 2; : : : ; n 1. <sup>1</sup> We denote a decomposition into pieces using ordinary additive notation, so that 7 = 2 C 2 C 3 indicates that a rod of length 7 is cut into three pieces4two of length 2 and one of length 3. If an optimal solution cuts the rod into k pieces, {or some 1 ≤ k ≤ n, then an optimal decomposition

$$n = i_1 + i_2 + \dots + i_k$$

<sup>1</sup> If pieces are required to be cut in order of monotonically increasing size, there are {ewer ways to consider. For n = 4, only 5 such ways are possible: parts (a), (b), (c), (e), and (h) in Figure 14.2. The number of ways is called the *partition {unction*, which is approximately equal to e p 2n=3=4n<sup>p</sup> 3. This quantity is less than 2 n1 , but still much }reater than any polynomial in n. We won't pursue this line of inquiry {urther, however.

| length i | 1 | 2 | 3 | 4 | 5  | 6  | 7  | 8  | 9  | 10 |
||---|---|---|---|----|----|----|----|----|----|
| price pi | 1 | 5 | 8 | 9 | 10 | 17 | 17 | 20 | 24 | 30 |

**Figure 14.1** A sample price table {or rods. Each rod of length i inches earns the company pi dollars of revenue.

**Figure 14.2** The 8 possible ways of cutting up a rod of length 4. Above each piece is the value of that piece, according to the sample price chart of Figure 14.1. The optimal strategy is part (c)4 cutting the rod into two pieces of length 24which has total value 10.

of the rod into pieces of lengths i1, i2, . . . , i<sup>k</sup> provides maximum corresponding revenue

$$r_n = p_{i_1} + p_{i_2} + \cdots + p_{i_k}$$
.

For the sample problem in Figure 14.1, you can determine the optimal revenue {igures r<sup>i</sup> , {or i = 1; 2; : : : ; 10, by inspection, with the corresponding optimal decompositions

```
r1 D 1 {rom solution 1 = 1 (no cuts) ;
r2 D 5 {rom solution 2 = 2 (no cuts) ;
r3 D 8 {rom solution 3 = 3 (no cuts) ;
r4 D 10 {rom solution 4 = 2 C 2 ;
r5 D 13 {rom solution 5 = 2 C 3 ;
r6 D 17 {rom solution 6 = 6 (no cuts) ;
r7 D 18 {rom solution 7 = 1 C 6 or 7 = 2 C 2 C 3 ;
r8 D 22 {rom solution 8 = 2 C 6 ;
r9 D 25 {rom solution 9 = 3 C 6 ;
r10 D 30 {rom solution 10 D 10 (no cuts) :
```

*14.1 Rod cutting 365* 

More generally, we can express the values rₙ for n ≥ 1 in terms of optimal revenues from shorter rods:

$$r_n = \max\{p_n, r_1 + r_{n-1}, r_2 + r_{n-2}, \dots, r_{n-1} + r_1\}.$$
(14.1)

The first argument, pₙ, corresponds to making no cuts at all and selling the rod of length n as is. The other n − 1 arguments to max correspond to the maximum revenue obtained by making an initial cut of the rod into two pieces of size i and n − i, for each i = 1, 2, ..., n−1, and then optimally cutting up those pieces further, obtaining revenues rᵢ and rₙ₋ᵢ from those two pieces. Since you don't know ahead of time which value of i optimizes revenue, you have to consider all possible values for i and pick the one that maximizes revenue. You also have the option of picking no i at all if the greatest revenue comes from selling the rod uncut.

To solve the original problem of size n, you solve smaller problems of the same type. Once you make the first cut, the two resulting pieces form independent instances of the rod-cutting problem. The overall optimal solution incorporates optimal solutions to the two resulting subproblems, maximizing revenue from each of those two pieces. We say that the rod-cutting problem exhibits *optimal substructure*: optimal solutions to a problem incorporate optimal solutions to related subproblems, which you may solve independently.

In a related, but slightly simpler, way to arrange a recursive structure for the rod-cutting problem, let's view a decomposition as consisting of a first piece of length i cut off the left-hand end, and then a right-hand remainder of length n − i. Only the remainder, and not the first piece, may be further divided. Think of every decomposition of a length-n rod in this way: as a first piece followed by some decomposition of the remainder. Then we can express the solution with no cuts at all by saying that the first piece has size i = n and revenue pₙ and that the remainder has size 0 with corresponding revenue r₀ = 0. We thus obtain the following simpler version of equation (14.1):

$$r_n = \max\{p_i + r_{n-i} : 1 \le i \le n\} . {(14.2)}$$

In this formulation, an optimal solution embodies the solution to only *one* related subproblem—the remainder—rather than two.

The CUT-ROD procedure on the {ollowing page implements the computation implicit in equation (14.2) in a straightforward, top-down, recursive manner. It takes as input an array p[1 W n� of prices and an integer n, and it returns the maximum revenue possible {or a rod of length n. For length n = 0, no revenue is possible, and so CUT-ROD returns 0 in line 2. Line 3 initializes the maximum revenue q to 1, so that the **for** loop in lines 435 correctly computes

q D max {p<sup>i</sup> C CUT-ROD.p; n i / W 1 ≤ i ≤ ng. Line 6 then returns this value. A simple induction on n proves that this answer is equal to the desired answer rn, using equation (14.2).

```
CUT-ROD.p; n/
1 if n == 0
2 return 0 
3 q = 1
4 {or i = 1 to n
5 q = max {q; p[i� C CUT-ROD.p; n  i /g
6 return q
```

If you code up CUT-ROD in your {avorite programming language and run it on your computer, you'll {ind that once the input size becomes moderately large, your program takes a long time to run. For n = 40, your program may take several minutes and possibly more than an hour. For large values of n, you'll also discover that each time you increase n by 1, your program's running time approximately doubles.

Why is CUT-ROD so inefficient? The problem is that CUT-ROD calls itself recursively over and over again with the same parameter values, which means that it solves the same subproblems repeatedly. Figure 14.3 shows a recursion tree demonstrating what happens {or n = 4: CUT-ROD.p; n/ calls CUT-ROD.p; n i / {or i = 1; 2; : : : ; n. Equivalently, CUT-ROD.p; n/ calls CUT-ROD.p; j / {or each j = 0; 1; : : : ; n 1. When this process unfolds recursively, the amount of work done, as a {unction of n, }rows explosively.

To analyze the running time of CUT-ROD, let T .n/ denote the total number of calls made to CUT-ROD.p; n/ {or a particular value of n. This expression equals the number of nodes in a subtree whose root is labeled n in the recursion tree. The count includes the initial call at its root. Thus, T .0/ D 1 and

$$T(n) = 1 + \sum_{j=0}^{n-1} T(j).$$
(14.3)

The initial 1 is {or the call at the root, and the term T .j / counts the number of calls (including recursive calls) due to the call CUT-ROD.p; n i /, where j = n i. As Exercise 14.1-1 asks you to show,

$$T(n) = 2^n (14.4)$$

and so the running time of CUT-ROD is exponential in n.

In retrospect, this exponential running time is not so surprising. CUT-ROD explicitly considers all possible ways of cutting up a rod of length n. How many ways 

*14.1 Rod cutting 367* 

**Figure 14.3** The recursion tree showing recursive calls resulting {rom a call C UT-ROD.p; n/ {or n = 4. Each node label }ives the size n of the corresponding subproblem, so that an edge {rom a parent with label s to a child with label t corresponds to cutting off an initial piece of size s t and leaving a remaining subproblem of size t. A path {rom the root to a leaf corresponds to one of the 2 n1 ways of cutting up a rod of length n. In }eneral, this recursion tree has 2 <sup>n</sup> nodes and 2 n1 leaves.

are there? A rod of length n has n 1 potential locations to cut. Each possible way to cut up the rod makes a cut at some subset of these n 1 locations, including the empty set, which makes {or no cuts. Viewing each cut location as a distinct member of a set of n 1 elements, you can see that there are 2 n1 subsets. Each leaf in the recursion tree of Figure 14.3 corresponds to one possible way to cut up the rod. Hence, the recursion tree has 2 n1 leaves. The labels on the simple path {rom the root to a leaf }ive the sizes of each remaining right-hand piece before making each cut. That is, the labels }ive the corresponding cut points, measured {rom the right-hand end of the rod.

#### **Using dynamic programming {or optimal rod cutting**

Now, let's see how to use dynamic programming to convert CUT-ROD into an efficient algorithm.

The dynamic-programming method works as {ollows. Instead of solving the same subproblems repeatedly, as in the naive recursion solution, arrange {or each subproblem to be solved *only once*. There's actually an obvious way to do so: the {irst time you solve a subproblem, *save its solution*. If you need to refer to this subproblem's solution again later, just look it up, rather than recomputing it.

Saving subproblem solutions comes with a cost: the additional memory needed to store solutions. Dynamic programming thus serves as an example of a *timememory trade-off*. The savings may be dramatic. For example, we're about to use dynamic programming to }o {rom the exponential-time algorithm {or rod cutting 

down to a '.n<sup>2</sup> /-time algorithm. A dynamic-programming approach runs in polynomial time when the number of *distinct* subproblems involved is polynomial in the input size and you can solve each such subproblem in polynomial time.

There are usually two equivalent ways to implement a dynamic-programming approach. Solutions to the rod-cutting problem illustrate both of them.

The {irst approach is *top-down* with *memoization*. <sup>2</sup>In this approach, you write the procedure recursively in a natural manner, but modified to save the result of each subproblem (usually in an array or hash table). The procedure now {irst checks to see whether it has previously solved this subproblem. If so, it returns the saved value, saving {urther computation at this level. If not, the procedure computes the value in the usual manner but also saves it. We say that the recursive procedure has been *memoized*: it <remembers= what results it has computed previously.

The second approach is the *bottom-up method*. This approach typically depends on some natural notion of the <size= of a subproblem, such that solving any particular subproblem depends only on solving <smaller= subproblems. Solve the subproblems in size order, smallest {irst, storing the solution to each subproblem when it is {irst solved. In this way, when solving a particular subproblem, there are already saved solutions {or all of the smaller subproblems its solution depends upon. You need to solve each subproblem only once, and when you {irst see it, you have already solved all of its prerequisite subproblems.

These two approaches yield algorithms with the same asymptotic running time, except in unusual circumstances where the top-down approach does not actually recurse to examine all possible subproblems. The bottom-up approach often has much better constant {actors, since it has lower overhead {or procedure calls.

The procedures MEMOIZED-CUT-ROD and MEMOIZED-CUT-ROD-AUX on the {acing page demonstrate how to memoize the top-down CUT-ROD procedure. The main procedure MEMOIZED-CUT-ROD initializes a new auxiliary array r[0 W n� with the value 1 which, since known revenue values are always nonnegative, is a convenient choice {or denoting <unknown.= MEMOIZED-CUT-ROD then calls its helper procedure, MEMOIZED-CUT-ROD-AUX, which is just the memoized version of the exponential-time procedure, CUT-ROD. It {irst checks in line 1 to see whether the desired value is already known and, if it is, then line 2 returns it. Otherwise, lines 337 compute the desired value q in the usual manner, line 8 saves it in r[n�, and line 9 returns it.

The bottom-up version, BOTTOM-UP-CUT-ROD on the next page, is even simpler. Using the bottom-up dynamic-programming approach, BOTTOM-UP-CUT-ROD takes advantage of the natural ordering of the subproblems: a subproblem of

<sup>2</sup> The technical term <memoization= is not a misspelling of <memorization.= The word <memoization= comes {rom <memo,= since the technique consists of recording a value to be looked up later.

*14.1 Rod cutting 369* 

```
MEMOIZED-CUT-ROD.p; n/
1 let r[0 W n� be a new array // will remember solution values in r
2for i = 0 to n
3 r[i� D 1
4 return MEMOIZED-CUT-ROD-AUX .p; n; r/
MEMOIZED-CUT-ROD-AUX .p; n; r/
1 if r[n�  0 // already have a solution {or length n?
2 return r[n�
3 if n = = 0
4 q = 0
5 else q = 1
6 {or i = 1 to n // i is the position of the {irst cut
7 q = max {q; p[i� C MEMOIZED-CUT-ROD-AUX .p; n  i; r/g
8 r[n� D q // remember the solution value {or length n
9 return q
BOTTOM-UP-CUT-ROD.p; n/
1 let r[0 W n� be a new array // will remember solution values in r
2r[0� D 0
3 {or j = 1 to n // {or increasing rod length j
4 q = 1
5 {or i = 1 to j // i is the position of the {irst cut
6 q = max {q; p[i� C r[j  i�g
7 r[j � D q // remember the solution value {or length j
8 return r[n�
```

size i is <smaller= than a subproblem of size j if i < j . Thus, the procedure solves subproblems of sizes j = 0; 1; : : : ; n, in that order.

Line 1 of BOTTOM-UP-CUT-ROD creates a new array r[0 W n� in which to save the results of the subproblems, and line 2 initializes r[0� to 0, since a rod of length 0 earns no revenue. Lines 336 solve each subproblem of size j , {or j = 1; 2; : : : ; n, in order of increasing size. The approach used to solve a problem of a particular size j is the same as that used by CUT-ROD, except that line 6 now directly references array entry r[j i� instead of making a recursive call to solve the subproblem of size j i. Line 7 saves in r[j � the solution to the subproblem of size j . Finally, line 8 returns r[n�, which equals the optimal value rn.

The bottom-up and top-down versions have the same asymptotic running time. The running time of BOTTOM-UP-CUT-ROD is '.n<sup>2</sup> /, due to its doubly nested

**Figure 14.4** The subproblem }raph {or the rod-cutting problem with n = 4. The vertex labels }ive the sizes of the corresponding subproblems. A directed edge .x; y/ indicates that solving subproblem x requires a solution to subproblem y. This }raph is a reduced version of the recursion tree of Figure 14.3, in which all nodes with the same label are collapsed into a single vertex and all edges }o {rom parent to child.

loop structure. The number of iterations of its inner **for** loop, in lines 536, {orms an arithmetic series. The running time of its top-down counterpart, MEMOIZED-CUT-ROD, is also '.n<sup>2</sup> /, although this running time may be a little harder to see. Because a recursive call to solve a previously solved subproblem returns immediately, MEMOIZED-CUT-ROD solves each subproblem just once. It solves subproblems {or sizes 0; 1; : : : ; n. To solve a subproblem of size n, the **for** loop of lines 637 iterates n times. Thus, the total number of iterations of this **for** loop, over all recursive calls of MEMOIZED-CUT-ROD, {orms an arithmetic series, }iving a total of '.n<sup>2</sup> / iterations, just like the inner **for** loop of BOTTOM-UP-CUT-ROD. (We actually are using a {orm of aggregate analysis here. We'll see aggregate analysis in detail in Section 16.1.)

#### **Subproblem }raphs**

When you think about a dynamic-programming problem, you need to understand the set of subproblems involved and how subproblems depend on one another.

The *subproblem }raph* {or the problem embodies exactly this information. Figure 14.4 shows the subproblem }raph {or the rod-cutting problem with n = 4. It is a directed }raph, containing one vertex {or each distinct subproblem. The subproblem }raph has a directed edge {rom the vertex {or subproblem x to the vertex {or subproblem y if determining an optimal solution {or subproblem x involves directly considering an optimal solution {or subproblem y. For example, the subproblem }raph contains an edge {rom x to y if a top-down recursive procedure {or solving x directly calls itself to solve y. You can think of the subproblem }raph as 

*14.1 Rod cutting 371* 

a <reduced= or <collapsed= version of the recursion tree {or the top-down recursive method, with all nodes {or the same subproblem coalesced into a single vertex and all edges directed {rom parent to child.

The bottom-up method {or dynamic programming considers the vertices of the subproblem }raph in such an order that you solve the subproblems y adjacent to a }iven subproblem x before you solve subproblem x. (As Section B.4 notes, the adjacency relation in a directed }raph is not necessarily symmetric.) Using terminology that we'll see in Section 20.4, in a bottom-up dynamic-programming algorithm, you consider the vertices of the subproblem }raph in an order that is a <reverse topological sort,= or a <topological sort of the transpose= of the subproblem }raph. In other words, no subproblem is considered until all of the subproblems it depends upon have been solved. Similarly, using notions that we'll visit in Section 20.3, you can view the top-down method (with memoization) {or dynamic programming as a <depth-first search= of the subproblem }raph.

The size of the subproblem }raph G = .V; E/ can help you determine the running time of the dynamic-programming algorithm. Since you solve each subproblem just once, the running time is the sum of the times needed to solve each subproblem. Typically, the time to compute the solution to a subproblem is proportional to the degree (number of outgoing edges) of the corresponding vertex in the subproblem }raph, and the number of subproblems is equal to the number of vertices in the subproblem }raph. In this common case, the running time of dynamic programming is linear in the number of vertices and edges.

#### **Reconstructing a solution**

The procedures MEMOIZED-CUT-ROD and BOTTOM-UP-CUT-ROD return the *value* of an optimal solution to the rod-cutting problem, but they do not return the solution *itself* : a list of piece sizes.

Let's see how to extend the dynamic-programming approach to record not only the optimal *value* computed {or each subproblem, but also a *choice* that led to the optimal value. With this information, you can readily print an optimal solution. The procedure EXTENDED-BOTTOM-UP-CUT-ROD on the next page computes, {or each rod size j , not only the maximum revenue r<sup>j</sup> , but also s<sup>j</sup> , the optimal size of the {irst piece to cut off. It's similar to BOTTOM-UP-CUT-ROD, except that it creates the array s in line 1, and it updates s[j � in line 8 to hold the optimal size i of the {irst piece to cut off when solving a subproblem of size j .

The procedure PRINT-CUT-ROD-SOLUTION on the {ollowing page takes as input an array p[1 W n� of prices and a rod size n. It calls EXTENDED-BOTTOM-UP-CUT-ROD to compute the array s[1 W n� of optimal {irst-piece sizes. Then it prints out the complete list of piece sizes in an optimal decomposition of a 

rod of length n. For the sample price chart appearing in Figure 14.1, the call EXTENDED-BOTTOM-UP-CUT-ROD.p; 10/ returns the {ollowing arrays:

$$\begin{array}{c|ccccccccccccccccccccccccccccccccccc$$

A call to PRINT-CUT-ROD-SOLUTION.p; 10/ prints just 10, but a call with n = 7 prints the cuts 1 and 6, which correspond to the {irst optimal decomposition {or r<sup>7</sup> }iven earlier.

```
EXTENDED-BOTTOM-UP-CUT-ROD.p; n/
1 let r[0 W n� and s[1 W n� be new arrays 
2r[0� D 0
3 {or j = 1 to n // {or increasing rod length j
4 q = 1
5 {or i = 1 to j // i is the position of the {irst cut
6 if q < p[i� C r[j  i�
7 q = p[i� C r[j  i�
8 s[j � D i // best cut location so {ar {or length j
9r[j � D q // remember the solution value {or length j
10 return r and s
PRINT-CUT-ROD-SOLUTION.p; n/
1 .r; s/ D EXTENDED-BOTTOM-UP-CUT-ROD.p; n/
2 while n > 0
3 print s[n� // cut location {or length n
4 n = n  s[n� // length of the remainder of the rod
```

#### **Exercises**

#### *14.1-1*

Show that equation (14.4) {ollows {rom equation (14.3) and the initial condition T .0/ D 1.

#### *14.1-2*

Show, by means of a counterexample, that the {ollowing <greedy= strategy does not always determine an optimal way to cut rods. Define the *density* of a rod of length i to be pi= i, that is, its value per inch. The }reedy strategy {or a rod of length n cuts off a {irst piece of length i, where 1 ≤ i ≤ n, having maximum 

density. It then continues by applying the }reedy strategy to the remaining piece of length n i.

### *14.1-3*

Consider a modification of the rod-cutting problem in which, in addition to a price p<sup>i</sup> {or each rod, each cut incurs a {ixed cost of c. The revenue associated with a solution is now the sum of the prices of the pieces minus the costs of making the cuts. Give a dynamic-programming algorithm to solve this modified problem.

### *14.1-4*

Modify CUT-ROD and MEMOIZED-CUT-ROD-AUX so that their **for** loops }o up to only bn=2c, rather than up to n. What other changes to the procedures do you need to make? How are their running times affected?

### *14.1-5*

Modify MEMOIZED-CUT-ROD to return not only the value but the actual solution.

### *14.1-6*

The Fibonacci numbers are defined by recurrence (3.31) on page 69. Give an O.n/-time dynamic-programming algorithm to compute the nth Fibonacci number. Draw the subproblem }raph. How many vertices and edges does the }raph contain?

# **14.2 Matrix-chain multiplication**

Our next example of dynamic programming is an algorithm that solves the problem of matrix-chain multiplication. Given a sequence (chain) hA1; A2; : : : ; Ani of n matrices to be multiplied, where the matrices aren't necessarily square, the }oal is to compute the product

$$A_1 A_2 \cdots A_n . \tag{14.5}$$

using the standard algorithm <sup>3</sup> {or multiplying rectangular matrices, which we'll see in a moment, while minimizing the number of scalar multiplications.

You can evaluate the expression (14.5) using the algorithm {or multiplying pairs of rectangular matrices as a subroutine once you have parenthesized it to resolve all ambiguities in how the matrices are multiplied together. Matrix multiplication is associative, and so all parenthesizations yield the same product. A product of

<sup>3</sup> None of the three methods {rom Sections 4.1 and Section 4.2 can be used directly, because they apply only to square matrices.