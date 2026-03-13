---
topic: dp_principles
pages: 404-414
---

You will find yourself following a common pattern in discovering optimal substructure:

- 1. You show that a solution to the problem consists of making a choice, such as choosing an initial cut in a rod or choosing an index at which to split the matrix chain. Making this choice leaves one or more subproblems to be solved.
- 2. You suppose that for a given problem, you are given the choice that leads to an optimal solution. You do not concern yourself yet with how to determine this choice. You just assume that it has been given to you.
- 3. Given this choice, you determine which subproblems ensue and how to best characterize the resulting space of subproblems.
- 4. You show that the solutions to the subproblems used within an optimal solution to the problem must themselves be optimal by using a "cut-and-paste" technique. You do so by supposing that each of the subproblem solutions is not optimal and then deriving a contradiction. In particular, by "cutting out" the nonoptimal solution to each subproblem and "pasting in" the optimal one, you show that you can get a better solution to the original problem, thus contradicting your supposition that you already had an optimal solution. If an optimal solution gives rise to more than one subproblem, they are typically so similar that you can modify the cut-and-paste argument for one to apply to the others with little effort.

To characterize the space of subproblems, a good rule of thumb says to try to keep the space as simple as possible and then expand it as necessary. For example, the space of subproblems for the rod-cutting problem contained the problems of optimally cutting up a rod of length i for each size i. This subproblem space worked well, and it was not necessary to try a more general space of subproblems.

Conversely, suppose that you tried to constrain the subproblem space for matrix-chain multiplication to matrix products of the form A₁A₂···Aⱼ. As before, an optimal parenthesization must split this product between Aₖ and Aₖ₊₁ for some 1 ≤ k < j. Unless you can guarantee that k always equals j − 1, you will find that you have subproblems of the form A₁A₂···Aₖ and Aₖ₊₁Aₖ₊₂···Aⱼ. Moreover, the latter subproblem does not have the form A₁A₂···Aⱼ. To solve this problem by dynamic programming, you need to allow the subproblems to vary at "both ends." That is, both i and j need to vary in the subproblem of parenthesizing the product AᵢAᵢ₊₁···Aⱼ.

Optimal substructure varies across problem domains in two ways:

- 1. how many subproblems an optimal solution to the original problem uses, and
- 2. how many choices you have in determining which subproblem(s) to use in an optimal solution.

In the rod-cutting problem, an optimal solution for cutting up a rod of size n uses just one subproblem (of size n−i), but we have to consider n choices for i in order to determine which one yields an optimal solution. Matrix-chain multiplication for the subchain AᵢAᵢ₊₁···Aⱼ serves an example with two subproblems and j − i choices. For a given matrix Aₖ where the product splits, two subproblems arise—parenthesizing AᵢAᵢ₊₁···Aₖ and parenthesizing Aₖ₊₁Aₖ₊₂···Aⱼ—and we have to solve *both* of them optimally. Once we determine the optimal solutions to subproblems, we choose from among j − i candidates for the index k.

Informally, the running time of a dynamic-programming algorithm depends on the product of two factors: the number of subproblems overall and how many choices you look at for each subproblem. In rod cutting, we had Θ(n) subproblems overall, and at most n choices to examine for each, yielding an O(n²) running time. Matrix-chain multiplication had Θ(n²) subproblems overall, and each had at most n − 1 choices, giving an O(n³) running time (actually, a Θ(n³) running time, by Exercise 14.2-5).

Usually, the subproblem graph gives an alternative way to perform the same analysis. Each vertex corresponds to a subproblem, and the choices for a subproblem are the edges incident from that subproblem. Recall that in rod cutting, the subproblem graph has n vertices and at most n edges per vertex, yielding an O(n²) running time. For matrix-chain multiplication, if you were to draw the subproblem graph, it would have Θ(n²) vertices and each vertex would have degree at most n − 1, giving a total of O(n³) vertices and edges.

Dynamic programming often uses optimal substructure in a bottom-up fashion. That is, you first find optimal solutions to subproblems and, having solved the subproblems, you find an optimal solution to the problem. Finding an optimal solution to the problem entails making a choice among subproblems as to which you will use in solving the problem. The cost of the problem solution is usually the subproblem costs plus a cost that is directly attributable to the choice itself. In rod cutting, for example, first we solved the subproblems of determining optimal ways to cut up rods of length i for i = 0, 1, ..., n − 1, and then we determined which of these subproblems yielded an optimal solution for a rod of length n, using equation (14.2). The cost attributable to the choice itself is the term pᵢ in equation (14.2). In matrix-chain multiplication, we determined optimal parenthesizations of subchains of AᵢAᵢ₊₁···Aⱼ, and then we chose the matrix Aₖ at which to split the product. The cost attributable to the choice itself is the term pᵢ₋₁pₖpⱼ.

Chapter 15 explores "greedy algorithms," which have many similarities to dynamic programming. In particular, problems to which greedy algorithms apply have optimal substructure. One major difference between greedy algorithms and dynamic programming is that instead of first finding optimal solutions to subproblems and then making an informed choice, greedy algorithms first make a "greedy" choice—the choice that looks best at the time—and then solve a resulting subproblem, without bothering to solve all possible related smaller subproblems. Surprisingly, in some cases this strategy works!

#### *Subtleties*

You should be careful not to assume that optimal substructure applies when it does not. Consider the following two problems whose input consists of a directed graph G = (V, E) and vertices u, v ∈ V.

**Unweighted shortest path:**⁵ Find a path from u to v consisting of the fewest edges. Such a path must be simple, since removing a cycle from a path produces a path with fewer edges.

**Unweighted longest simple path:** Find a simple path from u to v consisting of the most edges. (Without the requirement that the path must be simple, the problem is undefined, since repeatedly traversing a cycle creates paths with an arbitrarily large number of edges.)

The unweighted shortest-path problem exhibits optimal substructure. Here's how. Suppose that u ≠ v, so that the problem is nontrivial. Then, any path p from u to v must contain an intermediate vertex, say w. (Note that w may be u or v.) Then, we can decompose the path u ⇝ p v into subpaths u ⇝ p₁ w ⇝ p₂ v. The number of edges in p equals the number of edges in p₁ plus the number of edges in p₂. We claim that if p is an optimal (i.e., shortest) path from u to v, then p₁ must be a shortest path from u to w. Why? As suggested earlier, use a "cut-and-paste" argument: if there were another path, say p₁', from u to w with fewer edges than p₁, then we could cut out p₁ and paste in p₁' to produce a path u ⇝ p₁' w ⇝ p₂ v with fewer edges than p, thus contradicting p's optimality. Likewise, p₂ must be a shortest path from w to v. Thus, to find a shortest path from u to v, consider all intermediate vertices w, find a shortest path from u to w and a shortest path from w to v, and choose an intermediate vertex w that yields the overall shortest path. Section 23.2 uses a variant of this observation of optimal substructure to find a shortest path between every pair of vertices on a weighted, directed graph.

You might be tempted to assume that the problem of finding an unweighted longest simple path exhibits optimal substructure as well. After all, if we decompose a longest simple path u ⇝ p v into subpaths u ⇝ p₁ w ⇝ p₂ v, then mustn't p₁ be a longest simple path from u to w, and mustn't p₂ be a longest simple path from w to v? The answer is no! Figure 14.6 supplies an example. Consider the

⁵ We use the term "unweighted" to distinguish this problem from that of finding shortest paths with weighted edges, which we shall see in Chapters 22 and 23. You can use the breadth-first search technique of Chapter 20 to solve the unweighted problem.

**Figure 14.6** A directed graph showing that the problem of finding a longest simple path in an unweighted directed graph does not have optimal substructure. The path q → r → t is a longest simple path from q to t, but the subpath q → r is not a longest simple path from q to r, nor is the subpath r → t a longest simple path from r to t.

path q → r → t, which is a longest simple path from q to t. Is q → r a longest simple path from q to r? No, for the path q → s → t → r is a simple path that is longer. Is r → t a longest simple path from r to t? No again, for the path r → q → s → t is a simple path that is longer.

This example shows that for longest simple paths, not only does the problem lack optimal substructure, but you cannot necessarily assemble a "legal" solution to the problem from solutions to subproblems. If you combine the longest simple paths q → s → t → r and r → q → s → t, you get the path q → s → t → r → q → s → t, which is not simple. Indeed, the problem of finding an unweighted longest simple path does not appear to have any sort of optimal substructure. No efficient dynamic-programming algorithm for this problem has ever been found. In fact, this problem is NP-complete, which—as we shall see in Chapter 34—means that we are unlikely to find a way to solve it in polynomial time.

Why is the substructure of a longest simple path so different {rom that of a shortest path? Although a solution to a problem {or both longest and shortest paths uses two subproblems, the subproblems in {inding the longest simple path are not *independent*, whereas {or shortest paths they are. What do we mean by subproblems being independent? We mean that the solution to one subproblem does not affect the solution to another subproblem of the same problem. For the example of Figure 14.6, we have the problem of {inding a longest simple path {rom q to t with two subproblems: {inding longest simple paths {rom q to r and {rom r to t. For the {irst of these subproblems, we chose the path q ! s ! t ! r, which used the vertices s and t. These vertices cannot appear in a solution to the second subproblem, since the combination of the two solutions to subproblems yields a path that is not simple. If vertex t cannot be in the solution to the second problem, then there is no way to solve it, since t is required to be on the path that {orms the solution, and it is not the vertex where the subproblem solutions are <spliced= together (that vertex being r). Because vertices s and t appear in one subproblem solution, they cannot appear in the other subproblem solution. One of them must be in the solution to the other subproblem, however, and an optimal solution requires both. 

Thus, we say that these subproblems are not independent. Looked at another way, using resources in solving one subproblem (those resources being vertices) renders them unavailable {or the other subproblem.

Why, then, are the subproblems independent {or {inding a shortest path? The answer is that by nature, the subproblems do not share resources. We claim that if a vertex w is on a shortest path p {rom u to v, then we can splice together *any* shortest path <sup>u</sup> ❀ <sup>p</sup><sup>1</sup> <sup>w</sup> and *any* shortest path <sup>w</sup> ❀ p2 v to produce a shortest path {rom u to v. We are assured that, other than w, no vertex can appear in both paths p<sup>1</sup> and p2. Why? Suppose that some vertex x ≠ w appears in both p<sup>1</sup> and p2, so that we can decompose p<sup>1</sup> as u <sup>p</sup>❀ux <sup>x</sup> ❀ <sup>w</sup> and p<sup>2</sup> as <sup>w</sup> ❀ <sup>x</sup> <sup>p</sup>❀xv v. By the optimal substructure of this problem, path p has as many edges as p<sup>1</sup> and p<sup>2</sup> together. Let's say that p has e edges. Now let us construct a path p <sup>0</sup> D u <sup>p</sup>ux ❀ x <sup>p</sup>xv ❀ v {rom u to v. Because we have excised the paths {rom x to w and {rom w to x, each of which contains at least one edge, path p 0 contains at most e 2 edges, which contradicts the assumption that p is a shortest path. Thus, we are assured that the subproblems {or the shortest-path problem are independent.

The two problems examined in Sections 14.1 and 14.2 have independent subproblems. In matrix-chain multiplication, the subproblems are multiplying subchains AiAiC1 A<sup>k</sup> and AkC1AkC2 A<sup>j</sup> . These subchains are disjoint, so that no matrix could possibly be included in both of them. In rod cutting, to determine the best way to cut up a rod of length n, we looked at the best ways of cutting up rods of length i {or i = 0; 1; : : : ; n1. Because an optimal solution to the length-n problem includes just one of these subproblem solutions (after cutting off the {irst piece), independence of subproblems is not an issue.

#### **Overlapping subproblems**

The second ingredient that an optimization problem must have {or dynamic programming to apply is that the space of subproblems must be <small= in the sense that a recursive algorithm {or the problem solves the same subproblems over and over, rather than always }enerating new subproblems. Typically, the total number of distinct subproblems is a polynomial in the input size. When a recursive algorithm revisits the same problem repeatedly, we say that the optimization problem has *overlapping subproblems*. 6 In contrast, a problem {or which a divide-and-

<sup>6</sup> It may seem strange that dynamic programming relies on subproblems being both independent and overlapping. Although these requirements may sound contradictory, they describe two different notions, rather than two points on the same axis. Two subproblems of the same problem are independent if they do not share resources. Two subproblems are overlapping if they are really the same subproblem that occurs as a subproblem of different problems.

**Figure 14.7** The recursion tree {or the computation of RECURSIVE-MATRIX-CHAIN.p; 1; 4/. Each node contains the parameters i and j . The computations performed in a subtree shaded blue are replaced by a single table lookup in MEMOIZED-MATRIX-CHAIN.

conquer approach is suitable usually }enerates brand-new problems at each step of the recursion. Dynamic-programming algorithms typically take advantage of overlapping subproblems by solving each subproblem once and then storing the solution in a table where it can be looked up when needed, using constant time per lookup.

In Section 14.1, we briefly examined how a recursive solution to rod cutting makes exponentially many calls to {ind solutions of smaller subproblems. The dynamic-programming solution reduces the running time {rom the exponential time of the recursive algorithm down to quadratic time.

To illustrate the overlapping-subproblems property in }reater detail, let's revisit the matrix-chain multiplication problem. Referring back to Figure 14.5, observe that MATRIX-CHAIN-ORDER repeatedly looks up the solution to subproblems in lower rows when solving subproblems in higher rows. For example, it references entry m[3; 4� {our times: during the computations of m[2; 4�, m[1; 4�, m[3; 5�, and m[3; 6�. If the algorithm were to recompute m[3; 4� each time, rather than just looking it up, the running time would increase dramatically. To see how, consider the inefficient recursive procedure RECURSIVE-MATRIX-CHAIN on the {acing page, which determines m[i; j �, the minimum number of scalar multiplications needed to compute the matrix-chain product AiWj D AiAiC1 A<sup>j</sup> . The procedure is based directly on the recurrence (14.7). Figure 14.7 shows the recursion tree produced by the call RECURSIVE-MATRIX-CHAIN.p; 1; 4/. Each node is labeled by the values of the parameters i and j . Observe that some pairs of values occur many times.

In {act, the time to compute m[1; n� by this recursive procedure is at least exponential in n. To see why, let T .n/ denote the time taken by RECURSIVE-MATRIX-

```
RECURSIVE-MATRIX-CHAIN .p; i; j /
1 if i = = j
2 return 0
3 m[i; j � D 1
4 {or k = i to j  1
5 q = RECURSIVE-MATRIX-CHAIN .p; i; k/
          C RECURSIVE-MATRIX-CHAIN .p; k C 1; j /
          C pi1pkpj
6 if q < m[i; j �
7 m[i; j � D q
8 return m[i; j �
```

CHAIN to compute an optimal parenthesization of a chain of n matrices. Because the execution of lines 132 and of lines 637 each take at least unit time, as does the multiplication in line 5, inspection of the procedure yields the recurrence

$$T(n) \ge \begin{cases} 1 & \text{if } n = 1, \\ 1 + \sum_{k=1}^{n-1} (T(k) + T(n-k) + 1) & \text{if } n > 1. \end{cases}$$

Noting that {or i = 1; 2; : : : ; n 1, each term T .i / appears once as T .k/ and once as T .n k/, and collecting the n 1 1s in the summation together with the 1 out {ront, we can rewrite the recurrence as

$$T(n) \ge 2\sum_{i=1}^{n-1} T(i) + n.$$
(14.8)

Let's prove that T .n/ D �.2<sup>n</sup> / using the substitution method. Specifically, we'll show that T .n/ 2 n1 {or all n 1. For the base case n = 1, the summation is empty, and we }et T .1/ 1 = 2 0 . Inductively, {or n 2 we have

$$T(n) \ge 2\sum_{i=1}^{n-1} 2^{i-1} + n$$

$$= 2\sum_{j=0}^{n-2} 2^{j} + n \qquad \text{(letting } j = i - 1\text{)}$$

$$= 2(2^{n-1} - 1) + n \quad \text{(by equation (A.6) on page 1142)}$$

$$= 2^{n} - 2 + n$$

$$\ge 2^{n-1},$$

which completes the proof. Thus, the total amount of work performed by the call RECURSIVE-MATRIX-CHAIN .p; 1; n/ is at least exponential in n.

Compare this top-down, recursive algorithm (without memoization) with the bottom-up dynamic-programming algorithm. The latter is more efficient because it takes advantage of the overlapping-subproblems property. Matrix-chain multiplication has only '.n<sup>2</sup> / distinct subproblems, and the dynamic-programming algorithm solves each exactly once. The recursive algorithm, on the other hand, must solve each subproblem every time it reappears in the recursion tree. Whenever a recursion tree {or the natural recursive solution to a problem contains the same subproblem repeatedly, and the total number of distinct subproblems is small, dynamic programming can improve efficiency, sometimes dramatically.

#### **Reconstructing an optimal solution**

As a practical matter, you'll often want to store in a separate table which choice you made in each subproblem so that you do not have to reconstruct this information {rom the table of costs.

For matrix-chain multiplication, the table s[i; j � saves a significant amount of work when we need to reconstruct an optimal solution. Suppose that the MATRIX-CHAIN-ORDER procedure on page 378 did not maintain the s[i; j � table, so that it {illed in only the table m[i; j � containing optimal subproblem costs. The procedure chooses {rom among j i possibilities when determining which subproblems to use in an optimal solution to parenthesizing AiAiC1 A<sup>j</sup> , and j i is not a constant. Therefore, it would take '.j i / D !.1/ time to reconstruct which subproblems it chose {or a solution to a }iven problem. Because MATRIX-CHAIN-ORDER stores in s[i; j � the index of the matrix at which it split the product AiAiC1 A<sup>j</sup> , the PRINT-OPTIMAL-PARENS procedure on page 381 can look up each choice in O.1/ time.

### **Memoization**

As we saw {or the rod-cutting problem, there is an alternative approach to dynamic programming that often offers the efficiency of the bottom-up dynamicprogramming approach while maintaining a top-down strategy. The idea is to *memoize* the natural, but inefficient, recursive algorithm. As in the bottom-up approach, you maintain a table with subproblem solutions, but the control structure {or {illing in the table is more like the recursive algorithm.

A memoized recursive algorithm maintains an entry in a table {or the solution to each subproblem. Each table entry initially contains a special value to indicate that the entry has yet to be {illed in. When the subproblem is {irst encountered as the recursive algorithm unfolds, its solution is computed and then stored in the table. 

Each subsequent encounter of this subproblem simply looks up the value stored in the table and returns it. <sup>7</sup>

The procedure MEMOIZED-MATRIX-CHAIN is a memoized version of the procedure RECURSIVE-MATRIX-CHAIN on page 389. Note where it resembles the memoized top-down method on page 369 {or the rod-cutting problem.

```
MEMOIZED-MATRIX-CHAIN .p; n/
1 let m[1 W n; 1 W n� be a new table 
2 {or i = 1 to n
3 {or j = i to n
4 m[i; j � D 1
5 return LOOKUP-CHAIN.m; p; 1; n/
LOOKUP-CHAIN.m; p; i; j /
1 if m[i; j � < 1
2 return m[i; j �
3 if i = = j
4 m[i; j � D 0
5 else {or k = i to j  1
6 q = LOOKUP-CHAIN.m; p; i; k/
              C LOOKUP-CHAIN.m; p; k C 1; j / C pi1pkpj
7 if q < m[i; j �
8 m[i; j � D q
9 return m[i; j �
```

The MEMOIZED-MATRIX-CHAIN procedure, like the bottom-up MATRIX-CHAIN-ORDER procedure on page 378, maintains a table m[1 W n; 1 W n� of computed values of m[i; j �, the minimum number of scalar multiplications needed to compute the matrix AiWj . Each table entry initially contains the value 1 to indicate that the entry has yet to be {illed in. Upon calling LOOKUP-CHAIN.m; p; i; j /, if line 1 {inds that m[i; j � < 1, then the procedure simply returns the previously computed cost m[i; j � in line 2. Otherwise, the cost is computed as in RECURSIVE-MATRIX-CHAIN, stored in m[i; j �, and returned. Thus, LOOKUP-CHAIN.m; p; i; j / always returns the value of m[i; j �, but it computes it only upon the {irst call of LOOKUP-CHAIN with these specific values of i and j .

<sup>7</sup> This approach presupposes that you know the set of all possible subproblem parameters and that you have established the relationship between table positions and subproblems. Another, more }eneral, approach is to memoize by using hashing with the subproblem parameters as keys.

Figure 14.7 illustrates how MEMOIZED-MATRIX-CHAIN saves time compared with RECURSIVE-MATRIX-CHAIN. Subtrees shaded blue represent values that are looked up rather than recomputed.

Like the bottom-up procedure MATRIX-CHAIN-ORDER, the memoized procedure MEMOIZED-MATRIX-CHAIN runs in O.n<sup>3</sup> / time. To begin with, line 4 of MEMOIZED-MATRIX-CHAIN executes '.n<sup>2</sup> / times, which dominates the running time outside of the call to LOOKUP-CHAIN in line 5. We can categorize the calls of LOOKUP-CHAIN into two types:

- 1. calls in which m[i; j � D 1, so that lines 339 execute, and
- 2. calls in which m[i; j � < 1, so that LOOKUP-CHAIN simply returns in line 2.

There are '.n<sup>2</sup> / calls of the {irst type, one per table entry. All calls of the second type are made as recursive calls by calls of the {irst type. Whenever a }iven call of LOOKUP-CHAIN makes recursive calls, it makes O.n/ of them. Therefore, there are O.n<sup>3</sup> / calls of the second type in all. Each call of the second type takes O.1/ time, and each call of the {irst type takes O.n/ time plus the time spent in its recursive calls. The total time, therefore, is O.n<sup>3</sup> /. Memoization thus turns an �.2<sup>n</sup> /-time algorithm into an O.n<sup>3</sup> /-time algorithm.

We have seen how to solve the matrix-chain multiplication problem by either a top-down, memoized dynamic-programming algorithm or a bottom-up dynamicprogramming algorithm in O.n<sup>3</sup> / time. Both the bottom-up and memoized methods take advantage of the overlapping-subproblems property. There are only '.n<sup>2</sup> / distinct subproblems in total, and either of these methods computes the solution to each subproblem only once. Without memoization, the natural recursive algorithm runs in exponential time, since solved subproblems are repeatedly solved.

In }eneral practice, if all subproblems must be solved at least once, a bottom-up dynamic-programming algorithm usually outperforms the corresponding top-down memoized algorithm by a constant {actor, because the bottom-up algorithm has no overhead {or recursion and less overhead {or maintaining the table. Moreover, {or some problems you can exploit the regular pattern of table accesses in the dynamicprogramming algorithm to reduce time or space requirements even {urther. On the other hand, in certain situations, some of the subproblems in the subproblem space might not need to be solved at all. In that case, the memoized solution has the advantage of solving only those subproblems that are definitely required.

#### **Exercises**

#### *14.3-1*

Which is a more efficient way to determine the optimal number of multiplications in a matrix-chain multiplication problem: enumerating all the ways of parenthesiz

ing the product and computing the number of multiplications {or each, or running RECURSIVE-MATRIX-CHAIN? Justify your answer.

### *14.3-2*

Draw the recursion tree {or the MERGE-SORT procedure {rom Section 2.3.1 on an array of 16 elements. Explain why memoization {ails to speed up a }ood divideand-conquer algorithm such as MERGE-SORT.

### *14.3-3*

Consider the antithetical variant of the matrix-chain multiplication problem where the }oal is to parenthesize the sequence of matrices so as to maximize, rather than minimize, the number of scalar multiplications. Does this problem exhibit optimal substructure?

### *14.3-4*

As stated, in dynamic programming, you {irst solve the subproblems and then choose which of them to use in an optimal solution to the problem. Professor Capulet claims that she does not always need to solve all the subproblems in order to {ind an optimal solution. She suggests that she can {ind an optimal solution to the matrix-chain multiplication problem by always choosing the matrix A<sup>k</sup> at which to split the subproduct AiAiC1 A<sup>j</sup> (by selecting k to minimize the quantity pi1pkp<sup>j</sup> ) before solving the subproblems. Find an instance of the matrixchain multiplication problem {or which this }reedy approach yields a suboptimal solution.

### *14.3-5*

Suppose that the rod-cutting problem of Section 14.1 also had a limit l<sup>i</sup> on the number of pieces of length i allowed to be produced, {or i = 1; 2; : : : ; n. Show that the optimal-substructure property described in Section 14.1 no longer holds.

# **14.4 Longest common subsequence**

Biological applications often need to compare the DNA of two (or more) different organisms. A strand of DNA consists of a string of molecules called *bases*, where the possible bases are adenine, cytosine, guanine, and thymine. Representing each of these bases by its initial letter, we can express a strand of DNA as a string over the 4-element set {A, C, G, T}. (See Section C.1 for the definition of a string.) For example, the DNA of one organism may be S₁ = ACCGGTCGAGTGCGCGGAAGCCGGCCGAA, and the DNA of another organism may be S₂ = GTCGTTCGGAATGCCGTTGCTCTGTAAA. One reason to com