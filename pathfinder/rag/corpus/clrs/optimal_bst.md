---
topic: optimal_bst
pages: 422-438
---

| node  | depth | probability | contribution |
|-------|-------|||
| k1    | 1     | 0.15        | 0.30         |
| k2    | 0     | 0.10        | 0.10         |
| k3    | 2     | 0.05        | 0.15         |
| k4    | 1     | 0.10        | 0.20         |
| k5    | 2     | 0.20        | 0.60         |
| d0    | 2     | 0.05        | 0.15         |
| d1    | 2     | 0.10        | 0.30         |
| d2    | 3     | 0.05        | 0.20         |
| d3    | 3     | 0.05        | 0.20         |
| d4    | 3     | 0.05        | 0.20         |
| d5    | 3     | 0.10        | 0.40         |
| Total |       |             | 2.80         |
|       |       |             |              |

| node  | depth | probability | contribution |
|-------|-------|||
| k1    | 1     | 0.15        | 0.30         |
| k2    | 0     | 0.10        | 0.10         |
| k3    | 3     | 0.05        | 0.20         |
| k4    | 2     | 0.10        | 0.30         |
| k5    | 1     | 0.20        | 0.40         |
| d0    | 2     | 0.05        | 0.15         |
| d1    | 2     | 0.10        | 0.30         |
| d2    | 4     | 0.05        | 0.25         |
| d3    | 4     | 0.05        | 0.25         |
| d4    | 3     | 0.05        | 0.20         |
| d5    | 2     | 0.10        | 0.30         |
| Total |       |             | 2.75         |
|       |       | (b)         |              |
|       |       |             |              |

**(a)** A binary search tree with expected search cost 2.80. **(b)** A binary search tree with expected search cost 2.75. This tree is optimal.

Knowing the probabilities of searches for each key and each dummy key allows us to determine the expected cost of a search in a given binary search tree T . Let us assume that the actual cost of a search equals the number of nodes examined, which is the depth of the node found by the search in T , plus 1. Then the expected cost of a search in T is

$$E[\operatorname{search cost in} T] = \sum_{i=1}^{n} (\operatorname{depth}_{T}(k_{i}) + 1) \cdot p_{i} + \sum_{i=0}^{n} (\operatorname{depth}_{T}(d_{i}) + 1) \cdot q_{i}$$

$$= 1 + \sum_{i=1}^{n} \operatorname{depth}_{T}(k_{i}) \cdot p_{i} + \sum_{i=0}^{n} \operatorname{depth}_{T}(d_{i}) \cdot q_{i} , \quad (14.11)$$

where depthT denotes a node's depth in the tree T . The last equation follows from equation (14.10). Figure 14.9 shows how to calculate the expected search cost node by node.

For a given set of probabilities, your goal is to construct a binary search tree whose expected search cost is smallest. We call such a tree an *optimal binary search tree*. Figure 14.9(a) shows one binary search tree, with expected cost 2:80, for the probabilities given in the figure caption. Part (b) of the figure displays an optimal binary search tree, with expected cost 2:75. This example demonstrates that an optimal binary search tree is not necessarily a tree whose overall height is smallest. Nor does an optimal binary search tree always have the key with the greatest search probability at the root. Here, key k₅ has the greatest search probability of any key, yet the root of the optimal binary search tree shown is k2. (The lowest expected cost of any binary search tree with k₅ at the root is 2.85.)

As with matrix-chain multiplication, exhaustive checking of all possibilities fails to yield an efficient algorithm. You can label the nodes of any n-node binary tree with the keys k₁, k₂, ..., kₙ to construct a binary search tree, and then add in the dummy keys as leaves. In Problem 12-4 on page 329, we saw that the number of binary trees with n nodes is Θ(4ⁿ/n³/²). Thus you would need to examine an exponential number of binary search trees to perform an exhaustive search. We'll see how to solve this problem more efficiently with dynamic programming.

### **Step 1: The structure of an optimal binary search tree**

To characterize the optimal substructure of optimal binary search trees, we start with an observation about subtrees. Consider any subtree of a binary search tree. It must contain keys in a contiguous range kᵢ, ..., kⱼ, for some 1 ≤ i ≤ j ≤ n. In addition, a subtree that contains keys kᵢ, ..., kⱼ must also have as its leaves the dummy keys dᵢ₋₁, ..., dⱼ.

Now we can state the optimal substructure: if an optimal binary search tree T has a subtree T' containing keys kᵢ, ..., kⱼ, then this subtree T' must be optimal as well for the subproblem with keys kᵢ, ..., kⱼ and dummy keys dᵢ₋₁, ..., dⱼ. The usual cut-and-paste argument applies. If there were a subtree T'' whose expected cost is lower than that of T', then cutting T' out of T and pasting in T'' would result in a binary search tree of lower expected cost than T, thus contradicting the optimality of T.

With the optimal substructure in hand, here is how to construct an optimal solution to the problem from optimal solutions to subproblems. Given keys kᵢ, ..., kⱼ, one of these keys, say kᵣ (i ≤ r ≤ j), is the root of an optimal subtree containing these keys. The left subtree of the root kᵣ contains the keys kᵢ, ..., kᵣ₋₁ (and dummy keys dᵢ₋₁, ..., dᵣ₋₁), and the right subtree contains the keys kᵣ₊₁, ..., kⱼ (and dummy keys dᵣ, ..., dⱼ). As long as you examine all candidate roots kᵣ, where i ≤ r ≤ j, and you determine all optimal binary search trees containing kᵢ, ..., kᵣ₋₁ and those containing kᵣ₊₁, ..., kⱼ, you are guaranteed to find an optimal binary search tree.

There is one technical detail worth understanding about "empty" subtrees. Suppose that in a subtree with keys kᵢ, ..., kⱼ, you select kᵢ as the root. By the above argument, kᵢ's left subtree contains the keys kᵢ, ..., kᵢ₋₁: no keys at all. Bear in mind, however, that subtrees also contain dummy keys. We adopt the convention that a subtree containing keys kᵢ, ..., kᵢ₋₁ has no actual keys but does contain the single dummy key dᵢ₋₁. Symmetrically, if you select kⱼ as the root, then kⱼ's right subtree contains the keys kⱼ₊₁, ..., kⱼ. This right subtree contains no actual keys, but it does contain the dummy key dⱼ.

### **Step 2: A recursive solution**

To define the value of an optimal solution recursively, the subproblem domain is finding an optimal binary search tree containing the keys kᵢ, ..., kⱼ, where i ≥ 1, j ≤ n, and j ≥ i − 1. (When j = i − 1, there is just the dummy key dᵢ₋₁, but no actual keys.) Let e[i, j] denote the expected cost of searching an optimal binary search tree containing the keys kᵢ, ..., kⱼ. Your goal is to compute e[1, n], the expected cost of searching an optimal binary search tree for all the actual and dummy keys.

The easy case occurs when j = i − 1. Then the subproblem consists of just the dummy key dᵢ₋₁. The expected search cost is e[i, i − 1] = qᵢ₋₁.

When j ≥ i, you need to select a root kᵣ from among kᵢ, ..., kⱼ and then make an optimal binary search tree with keys kᵢ, ..., kᵣ₋₁ as its left subtree and an optimal binary search tree with keys kᵣ₊₁, ..., kⱼ as its right subtree. What happens to the expected search cost of a subtree when it becomes a subtree of a node? The depth of each node in the subtree increases by 1. By equation (14.11), the expected search cost of this subtree increases by the sum of all the probabilities in the subtree. For a subtree with keys kᵢ, ..., kⱼ, denote this sum of probabilities as

$$w(i,j) = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l.$$
 (14.12)

Thus, if k_r is the root of an optimal subtree containing keys k_i, ..., k_j, we have

$$e[i,j] = p_r + (e[i,r-1] + w(i,r-1)) + (e[r+1,j] + w(r+1,j)).$$

Noting that

$$w(i,j) = w(i,r-1) + p_r + w(r+1,j) ,$$

we rewrite e[i, j] as

$$e[i,j] = e[i,r-1] + e[r+1,j] + w(i,j).$$
(14.13)

The recursive equation (14.13) assumes that you know which node kᵣ to use as the root. Of course, you choose the root that gives the lowest expected search cost, giving the final recursive formulation:

$$e[i,j] = \begin{cases} q_{i-1} & \text{if } j = i-1, \\ \min\{e[i,r-1] + e[r+1,j] + w(i,j) : i \le r \le j\} & \text{if } i \le j. \end{cases}$$
(14.14)

The e[i, j] values give the expected search costs in optimal binary search trees. To help keep track of the structure of optimal binary search trees, define *root*[i, j], for 1 ≤ i ≤ j ≤ n, to be the index r for which kᵣ is the root of an optimal binary search tree containing keys kᵢ, ..., kⱼ. Although we'll see how to compute the values of *root*[i, j], the construction of an optimal binary search tree from these values is left as Exercise 14.5-1.

### **Step 3: Computing the expected search cost of an optimal binary search tree**

At this point, you may have noticed some similarities between our characterizations of optimal binary search trees and matrix-chain multiplication. For both problem domains, the subproblems consist of contiguous index subranges. A direct, recursive implementation of equation (14.14) would be just as inefficient as a direct, recursive matrix-chain multiplication algorithm. Instead, you can store the e[i, j] values in a table e[1:n+1, 0:n]. The first index needs to run to n+1 rather than n because in order to have a subtree containing only the dummy key dₙ, you need to compute and store e[n + 1, n]. The second index needs to start from 0 because in order to have a subtree containing only the dummy key d₀, you need to compute and store e[1, 0]. Only the entries e[i, j] for which j ≥ i − 1 are filled in. The table *root*[i, j] records the root of the subtree containing keys kᵢ, ..., kⱼ and uses only the entries for which 1 ≤ i ≤ j ≤ n.

One other table makes the dynamic-programming algorithm a little faster. Instead of computing the value of w(i, j) from scratch every time you compute e[i, j], which would take Θ(j − i) additions, store these values in a table w[1:n + 1, 0:n]. For the base case, compute w[i, i − 1] = qᵢ₋₁ for 1 ≤ i ≤ n+1. For j ≥ i, compute

$$w[i,j] = w[i,j-1] + p_j + q_j. (14.15)$$

Thus, you can compute the Θ(n²) values of w[i, j] in Θ(1) time each.

The OPTIMAL-BST procedure on the next page takes as inputs the probabilities p₁, ..., pₙ and q₀, ..., qₙ and the size n, and it returns the tables e and *root*. From the description above and the similarity to the MATRIX-CHAIN-ORDER procedure 

in Section 14.2, you should find the operation of this procedure to be fairly straightforward. The **for** loop of lines 2–4 initializes the values of e[i, i − 1] and w[i, i − 1]. Then the **for** loop of lines 5–14 uses the recurrences (14.14) and (14.15) to compute e[i, j] and w[i, j] for all 1 ≤ i ≤ j ≤ n. In the first iteration, when l = 1, the loop computes e[i, i] and w[i, i] for i = 1, 2, ..., n. The second iteration, with l = 2, computes e[i, i + 1] and w[i, i + 1] for i = 1, 2, ..., n − 1, and so on. The innermost **for** loop, in lines 10–14, tries each candidate index r to determine which key kᵣ to use as the root of an optimal binary search tree containing keys kᵢ, ..., kⱼ. This **for** loop saves the current value of the index r in *root*[i, j] whenever it finds a better key to use as the root.

```
OPTIMAL-BST(p, q, n)
1 let e[1:n + 1, 0:n], w[1:n + 1, 0:n],
          and root[1:n, 1:n] be new tables
2 for i = 1 to n + 1 // base cases
3     e[i, i − 1] = qᵢ₋₁ // equation (14.14)
4     w[i, i − 1] = qᵢ₋₁
5 for l = 1 to n
6     for i = 1 to n − l + 1
7         j = i + l − 1
8         e[i, j] = ∞
9         w[i, j] = w[i, j − 1] + pⱼ + qⱼ // equation (14.15)
10         for r = i to j // try all possible roots r
11             t = e[i, r − 1] + e[r + 1, j] + w[i, j] // equation (14.14)
12             if t < e[i, j] // new minimum?
13                 e[i, j] = t
14                 root[i, j] = r
15 return e and root
```

Figure 14.10 shows the tables e[i, j], w[i, j], and *root*[i, j] computed by the procedure OPTIMAL-BST on the key distribution shown in Figure 14.9. As in the matrix-chain multiplication example of Figure 14.5, the tables are rotated to make the diagonals run horizontally. OPTIMAL-BST computes the rows from bottom to top and from left to right within each row.

The OPTIMAL-BST procedure takes Θ(n³) time, just like MATRIX-CHAIN-ORDER. Its running time is O(n³), since its **for** loops are nested three deep and each loop index takes on at most n values. The loop indices in OPTIMAL-BST do not have exactly the same bounds as those in MATRIX-CHAIN-ORDER, but they are within at most 1 in all directions. Thus, like MATRIX-CHAIN-ORDER, the OPTIMAL-BST procedure takes Ω(n³) time.

**Figure 14.10** The tables e[i, j], w[i, j], and *root*[i, j] computed by OPTIMAL-BST on the key distribution shown in Figure 14.9. The tables are rotated so that the diagonals run horizontally.

### **Exercises**

#### *14.5-1*

Write pseudocode for the procedure CONSTRUCT-OPTIMAL-BST(*root*, n) which, given the table *root*[1:n, 1:n], outputs the structure of an optimal binary search tree. For the example in Figure 14.10, your procedure should print out the structure

```
k2 is the root 
k1 is the left child of k2
d0 is the left child of k1
d1 is the right child of k1
k5 is the right child of k2
k4 is the left child of k5
k3 is the left child of k4
d2 is the left child of k3
d3 is the right child of k3
d4 is the right child of k4
d5 is the right child of k5
```

corresponding to the optimal binary search tree shown in Figure 14.9(b).

*14.5-2*

Determine the cost and structure of an optimal binary search tree for a set of n = 7 keys with the following probabilities:

| i  | 0    | 1    | 2    | 3    | 4    | 5    | 6    | 7    |
|----|------|------|------|------|------|------|------|------|
| pi |      | 0.04 | 0.06 | 0.08 | 0.02 | 0.10 | 0.12 | 0.14 |
| qi | 0.06 | 0.06 | 0.06 | 0.06 | 0.05 | 0.05 | 0.05 | 0.05 |

### *14.5-3*

Suppose that instead of maintaining the table w[i, j], you computed the value of w(i, j) directly from equation (14.12) in line 9 of OPTIMAL-BST and used this computed value in line 11. How would this change affect the asymptotic running time of OPTIMAL-BST?

# ⋆ *14.5-4*

Knuth [264] has shown that there are always roots of optimal subtrees such that *root*[i, j - 1] ≤ *root*[i, j] ≤ *root*[i + 1, j] for all 1 ≤ i < j ≤ n. Use this fact to modify the OPTIMAL-BST procedure to run in Θ(n²) time.

## **Problems**

### *14-1 Longest simple path in a directed acyclic graph*

You are given a directed acyclic graph G = (V, E) with real-valued edge weights and two distinguished vertices s and t. The *weight* of a path is the sum of the weights of the edges in the path. Describe a dynamic-programming approach for finding a longest weighted simple path from s to t. What is the running time of your algorithm?

#### *14-2 Longest palindrome subsequence*

A *palindrome* is a nonempty string over some alphabet that reads the same forward and backward. Examples of palindromes are all strings of length 1, civic, racecar, and aibohphobia (fear of palindromes).

Give an efficient algorithm to find the longest palindrome that is a subsequence of a given input string. For example, given the input character, your algorithm should return carac. What is the running time of your algorithm?

#### *14-3 Bitonic euclidean traveling-salesperson problem*

In the *euclidean traveling-salesperson problem*, you are given a set of n points in the plane, and your goal is to find the shortest closed tour that connects all n points.

**Figure 14.11** Seven points in the plane, shown on a unit grid. **(a)** The shortest closed tour, with length approximately 24:89. This tour is not bitonic. **(b)** The shortest bitonic tour for the same set of points. Its length is approximately 25:58.

Figure 14.11(a) shows the solution to a 7-point problem. The general problem is NP-hard, and its solution is therefore believed to require more than polynomial time (see Chapter 34).

J. L. Bentley has suggested simplifying the problem by considering only *bitonic tours*, that is, tours that start at the leftmost point, go strictly rightward to the rightmost point, and then go strictly leftward back to the starting point. Figure 14.11(b) shows the shortest bitonic tour of the same 7 points. In this case, a polynomial-time algorithm is possible.

Describe an O(n²)-time algorithm for determining an optimal bitonic tour. You may assume that no two points have the same x-coordinate and that all operations on real numbers take unit time. (*Hint:* Scan left to right, maintaining optimal possibilities for the two parts of the tour.)

#### *14-4 Printing neatly*

Consider the problem of neatly printing a paragraph with a monospaced font (all characters having the same width). The input text is a sequence of n words of lengths l₁, l₂, ..., lₙ, measured in characters, which are to be printed neatly on a number of lines that hold a maximum of M characters each. No word exceeds the line length, so that lᵢ ≤ M for i = 1, 2, ..., n. The criterion of "neatness" is as follows. If a given line contains words i through j, where i ≤ j, and exactly one space appears between words, then the number of extra space characters at the end of the line is M - j + i - ∑ᵏ₌ᵢʲ lₖ, which must be nonnegative so that the words fit on the line. The goal is to minimize the sum, over all lines except the last, of the cubes of the numbers of extra space characters at the ends of lines. Give a dynamic-programming algorithm to print a paragraph of n words neatly. Analyze the running time and space requirements of your algorithm.

### *14-5 Edit distance*

In order to transform a source string of text x[1:m] to a target string y[1:n], you can perform various transformation operations. The goal is, given x and y, to produce a series of transformations that changes x to y. An array z—assumed to be large enough to hold all the characters it needs—holds the intermediate results. Initially, z is empty, and at termination, you should have z[j] = y[j] for j = 1, 2, ..., n. The procedure for solving this problem maintains current indices i into x and j into z, and the operations are allowed to alter z and these indices. Initially, i = j = 1. Every character in x must be examined during the transformation, which means that at the end of the sequence of transformation operations, i = m + 1.

You may choose from among six transformation operations, each of which has a constant cost that depends on the operation:

**Copy** a character from x to z by setting z[j] = x[i] and then incrementing both i and j. This operation examines x[i] and has cost Q_C.

**Replace** a character from x by another character c, by setting z[j] = c, and then incrementing both i and j. This operation examines x[i] and has cost Q_R.

**Delete** a character from x by incrementing i but leaving j alone. This operation examines x[i] and has cost Q_D.

**Insert** the character c into z by setting z[j] = c and then incrementing j, but leaving i alone. This operation examines no characters of x and has cost Q_I.

**Twiddle** (i.e., exchange) the next two characters by copying them from x to z but in the opposite order: setting z[j] = x[i + 1] and z[j + 1] = x[i], and then setting i = i + 2 and j = j + 2. This operation examines x[i] and x[i + 1] and has cost Q_T.

**Kill** the remainder of x by setting i = m + 1. This operation examines all characters in x that have not yet been examined. This operation, if performed, must be the final operation. It has cost Q_K.

Figure 14.12 gives one way to transform the source string algorithm to the target string altruistic. Several other sequences of transformation operations can transform algorithm to altruistic.

Assume that Q_C < Q_D + Q_I and Q_R < Q_D + Q_I, since otherwise, the copy and replace operations would not be used. The cost of a given sequence of transformation operations is the sum of the costs of the individual operations in the sequence. For the sequence above, the cost of transforming algorithm to altruistic is 3Q_C + Q_R + Q_D + 4Q_I + Q_T + Q_K.

*a.* Given two sequences x[1:m] and y[1:n] and the costs of the transformation operations, the *edit distance* from x to y is the cost of the least expensive op-

| Operation       | x         | z          |
||||
| initial strings | algorithm |            |
| copy            | algorithm | a          |
| copy            | algorithm | al         |
| replace by t    | algorithm | alt        |
| delete          | algorithm | alt        |
| copy            | algorithm | altr       |
| insert u        | algorithm | altru      |
| insert i        | algorithm | altrui     |
| insert s        | algorithm | altruis    |
| twiddle         | algorithm | altruisti  |
| insert c        | algorithm | altruistic |
| kill            | algorithm | altruistic |

**Figure 14.12** A sequence of operations that transforms the source algorithm to the target string altruistic. The underlined characters are x[i] and z[j] after the operation.

eration sequence that transforms x to y. Describe a dynamic-programming algorithm that finds the edit distance from x[1:m] to y[1:n] and prints an optimal operation sequence. Analyze the running time and space requirements of your algorithm.

The edit-distance problem generalizes the problem of aligning two DNA sequences (see, for example, Setubal and Meidanis [405, Section 3.2]). There are several methods for measuring the similarity of two DNA sequences by aligning them. One such method to align two sequences x and y consists of inserting spaces at arbitrary locations in the two sequences (including at either end) so that the resulting sequences x' and y' have the same length but do not have a space in the same position (i.e., for no position j are both x'[j] and y'[j] a space). Then we assign a "score" to each position. Position j receives a score as follows:

- +1 if x'[j] = y'[j] and neither is a space,
- -1 if x'[j] ≠ y'[j] and neither is a space,
- -2 if either x'[j] or y'[j] is a space.

The score for the alignment is the sum of the scores of the individual positions. For example, given the sequences x = GATCGGCAT and y = CAATGTGAATC, one alignment is

G ATCG GCAT CAAT GTGAATC -\*++\*+\*+-++\* 

A + under a position indicates a score of +1 for that position, a - indicates a score of -1, and a \* indicates a score of -2, so that this alignment has a total score of 6 - 1 - 2 - 1 - 4 - 2 = -4.

*b.* Explain how to cast the problem of finding an optimal alignment as an editdistance problem using a subset of the transformation operations copy, replace, delete, insert, twiddle, and kill.

### *14-6 Planning a company party*

Professor Blutarsky is consulting for the president of a corporation that is planning a company party. The company has a hierarchical structure, that is, the supervisor relation forms a tree rooted at the president. The human resources department has ranked each employee with a conviviality rating, which is a real number. In order to make the party fun for all attendees, the president does not want both an employee and his or her immediate supervisor to attend.

Professor Blutarsky is given the tree that describes the structure of the corporation, using the left-child, right-sibling representation described in Section 10.3. Each node of the tree holds, in addition to the pointers, the name of an employee and that employee's conviviality ranking. Describe an algorithm to make up a guest list that maximizes the sum of the conviviality ratings of the guests. Analyze the running time of your algorithm.

### *14-7 Viterbi algorithm*

Dynamic programming on a directed graph can play a part in speech recognition. A directed graph G = (V, E) with labeled edges forms a formal model of a person speaking a restricted language. Each edge (u, v) ∈ E is labeled with a sound σ(u, v) from a finite set Σ of sounds. Each directed path in the graph starting from a distinguished vertex v₀ ∈ V corresponds to a possible sequence of sounds produced by the model, with the label of a path being the concatenation of the labels of the edges on that path.

*a.* Describe an efficient algorithm that, given an edge-labeled directed graph G with distinguished vertex v₀ and a sequence s = ⟨σ₁, σ₂, ..., σₖ⟩ of sounds from Σ, returns a path in G that begins at v₀ and has s as its label, if any such path exists. Otherwise, the algorithm should return NO-SUCH-PATH. Analyze the running time of your algorithm. (*Hint:* You may find concepts from Chapter 20 useful.)

Now suppose that every edge (u, v) ∈ E has an associated nonnegative probability p(u, v) of being traversed, so that the corresponding sound is produced. The sum of the probabilities of the edges leaving any vertex equals 1. The probability of a path is defined to be the product of the probabilities of its edges. Think of 

the probability of a path beginning at vertex v₀ as the probability that a "random walk" beginning at v₀ follows the specified path, where the edge leaving a vertex u is taken randomly, according to the probabilities of the available edges leaving u.

*b.* Extend your answer to part (a) so that if a path is returned, it is a *most probable path* starting at vertex v₀ and having label s. Analyze the running time of your algorithm.

#### *14-8 Image compression by seam carving*

Suppose that you are given a color picture consisting of an mn array A[1:m, 1:n] of pixels, where each pixel specifies a triple of red, green, and blue (RGB) intensities. You want to compress this picture slightly, by removing one pixel from each of the m rows, so that the whole picture becomes one pixel narrower. To avoid incongruous visual effects, however, the pixels removed in two adjacent rows must lie in either the same column or adjacent columns. In this way, the pixels removed form a "seam" from the top row to the bottom row, where successive pixels in the seam are adjacent vertically or diagonally.

- *a.* Show that the number of such possible seams grows at least exponentially in m, assuming that n > 1.
- *b.* Suppose now that along with each pixel A[i, j], you are given a real-valued disruption measure d[i, j], indicating how disruptive it would be to remove pixel A[i, j]. Intuitively, the lower a pixel's disruption measure, the more similar the pixel is to its neighbors. Define the disruption measure of a seam as the sum of the disruption measures of its pixels.

Give an algorithm to find a seam with the lowest disruption measure. How efficient is your algorithm?

#### *14-9 Breaking a string*

A certain string-processing programming language allows you to break a string into two pieces. Because this operation copies the string, it costs n time units to break a string of n characters into two pieces. Suppose that you want to break a string into many pieces. The order in which the breaks occur can affect the total amount of time used. For example, suppose that you want to break a 20-character string after characters 2, 8, and 10 (numbering the characters in ascending order from the left-hand end, starting from 1). If you program the breaks to occur in left-to-right order, then the first break costs 20 time units, the second break costs 18 time units (breaking the string from characters 3 to 20 at character 8), and the third break costs 12 time units, totaling 50 time units. If you program the breaks to occur in right-to-left order, however, then the first break costs 20 time units, the 

second break costs 10 time units, and the third break costs 8 time units, totaling 38 time units. In yet another order, you could break first at 8 (costing 20), then break the left piece at 2 (costing another 8), and finally the right piece at 10 (costing 12), for a total cost of 40.

Design an algorithm that, given the numbers of characters after which to break, determines a least-cost way to sequence those breaks. More formally, given an array L[1:m] containing the break points for a string of n characters, compute the lowest cost for a sequence of breaks, along with a sequence of breaks that achieves this cost.

### *14-10 Planning an investment strategy*

Your knowledge of algorithms helps you obtain an exciting job with a hot startup, along with a \$10,000 signing bonus. You decide to invest this money with the goal of maximizing your return at the end of 10 years. You decide to use your investment manager, G. I. Luvcache, to manage your signing bonus. The company that Luvcache works with requires you to observe the following rules. It offers n different investments, numbered 1 through n. In each year j, investment i provides a return rate of r_ij. In other words, if you invest d dollars in investment i in year j, then at the end of year j, you have dr_ij dollars. The return rates are guaranteed, that is, you are given all the return rates for the next 10 years for each investment. You make investment decisions only once per year. At the end of each year, you can leave the money made in the previous year in the same investments, or you can shift money to other investments, by either shifting money between existing investments or moving money to a new investment. If you do not move your money between two consecutive years, you pay a fee of f₁ dollars, whereas if you switch your money, you pay a fee of f₂ dollars, where f₂ > f₁. You pay the fee once per year at the end of the year, and it is the same amount, f₂, whether you move money in and out of only one investment, or in and out of many investments.

- *a.* The problem, as stated, allows you to invest your money in multiple investments in each year. Prove that there exists an optimal investment strategy that, in each year, puts all the money into a single investment. (Recall that an optimal investment strategy maximizes the amount of money after 10 years and is not concerned with any other objectives, such as minimizing risk.)
- *b.* Prove that the problem of planning your optimal investment strategy exhibits optimal substructure.
- *c.* Design an algorithm that plans your optimal investment strategy. What is the running time of your algorithm?

*d.* Suppose that Luvcache's company imposes the additional restriction that, at any point, you can have no more than \$15,000 in any one investment. Show that the problem of maximizing your income at the end of 10 years no longer exhibits optimal substructure.

#### *14-11 Inventory planning*

The Rinky Dink Company makes machines that resurface ice rinks. The demand for such products varies from month to month, and so the company needs to develop a strategy to plan its manufacturing given the fluctuating, but predictable, demand. The company wishes to design a plan for the next n months. For each month i, the company knows the demand dᵢ, that is, the number of machines that it will sell. Let D = ∑ⁿᵢ₌₁ dᵢ be the total demand over the next n months. The company keeps a full-time staff who provide labor to manufacture up to m machines per month. If the company needs to make more than m machines in a given month, it can hire additional, part-time labor, at a cost that works out to c dollars per machine. Furthermore, if the company is holding any unsold machines at the end of a month, it must pay inventory costs. The company can hold up to D machines, with the cost for holding j machines given as a function h(j) for j = 1, 2, ..., D that monotonically increases with j.

Give an algorithm that calculates a plan for the company that minimizes its costs while fulfilling all the demand. The running time should be polynomial in n and D.

#### *14-12 Signing free-agent baseball players*

Suppose that you are the general manager for a major-league baseball team. During the off-season, you need to sign some free-agent players for your team. The team owner has given you a budget of \$X to spend on free agents. You are allowed to spend less than \$X, but the owner will fire you if you spend any more than \$X.

You are considering N different positions, and for each position, P free-agent players who play that position are available. <sup>10</sup> Because you do not want to overload your roster with too many players at any position, for each position you may sign at most one free agent who plays that position. (If you do not sign any players at a particular position, then you plan to stick with the players you already have at that position.)

<sup>10</sup> Although there are nine positions on a baseball team, N is not necessarily equal to 9 because some general managers have particular ways of thinking about positions. For example, a general manager might consider right-handed pitchers and left-handed pitchers to be separate "positions," as well as starting pitchers, long relief pitchers (relief pitchers who can pitch several innings), and short relief pitchers (relief pitchers who normally pitch at most only one inning).

To determine how valuable a player is going to be, you decide to use a sabermetric statistic <sup>11</sup> known as "WAR," or "wins above replacement." A player with a higher WAR is more valuable than a player with a lower WAR. It is not necessarily more expensive to sign a player with a higher WAR than a player with a lower WAR, because factors other than a player's value determine how much it costs to sign them.

For each available free-agent player p, you have three pieces of information:

- the player's position,
- p.*cost*, the amount of money it costs to sign the player, and
- p.*war*, the player's WAR.

Devise an algorithm that maximizes the total WAR of the players you sign while spending no more than \$X. You may assume that each player signs for a multiple of \$100,000. Your algorithm should output the total WAR of the players you sign, the total amount of money you spend, and a list of which players you sign. Analyze the running time and space requirement of your algorithm.

### **Chapter notes**

Bellman [44] began the systematic study of dynamic programming in 1955, publishing a book about it in 1957. The word "programming," both here and in linear programming, refers to using a tabular solution method. Although optimization techniques incorporating elements of dynamic programming were known earlier, Bellman provided the area with a solid mathematical basis.

Galil and Park [172] classify dynamic-programming algorithms according to the size of the table and the number of other table entries each entry depends on. They call a dynamic-programming algorithm tD=eD if its table size is O(n^t) and each entry depends on O(n^e) other entries. For example, the matrix-chain multiplication algorithm in Section 14.2 is 2D=1D, and the longest-common-subsequence algorithm in Section 14.4 is 2D=0D.

The MATRIX-CHAIN-ORDER algorithm on page 378 is by Muraoka and Kuck [339]. Hu and Shing [230, 231] give an O(n lg n)-time algorithm for the matrixchain multiplication problem.

The O(mn)-time algorithm for the longest-common-subsequence problem appears to be a folk algorithm. Knuth [95] posed the question of whether subquadratic

<sup>11</sup> *Sabermetrics* is the application of statistical analysis to baseball records. It provides several ways to compare the relative values of individual players.

algorithms for the LCS problem exist. Masek and Paterson [316] answered this question in the affirmative by giving an algorithm that runs in O(mn/lg n) time, where n ≤ m and the sequences are drawn from a set of bounded size. For the special case in which no element appears more than once in an input sequence, Szymanski [425] shows how to solve the problem in O((n + m)lg(n + m)) time. Many of these results extend to the problem of computing string edit distances (Problem 14-5).

An early paper on variable-length binary encodings by Gilbert and Moore [181], which had applications to constructing optimal binary search trees for the case in which all probabilities pᵢ are 0, contains an O(n³)-time algorithm. Aho, Hopcroft, and Ullman [5] present the algorithm from Section 14.5. Splay trees [418], which modify the tree in response to the search queries, come within a constant factor of the optimal bounds without being initialized with the frequencies. Exercise 14.5-4 is due to Knuth [264]. Hu and Tucker [232] devised an algorithm for the case in which all probabilities pᵢ are 0 that uses O(n²) time and O(n) space. Subsequently, Knuth [261] reduced the time to O(n lg n).

Problem 14-8 is due to Avidan and Shamir [30], who have posted on the web a wonderful video illustrating this image-compression technique.

# **15 Greedy Algorithms**

Algorithms for optimization problems typically go through a sequence of steps, with a set of choices at each step. For many optimization problems, using dynamic programming to determine the best choices is overkill, and simpler, more efficient algorithms will do. A *greedy algorithm* always makes the choice that looks best at the moment. That is, it makes a locally optimal choice in the hope that this choice leads to a globally optimal solution. This chapter explores optimization problems for which greedy algorithms provide optimal solutions. Before reading this chapter, you should read about dynamic programming in Chapter 14, particularly Section 14.3.

Greedy algorithms do not always yield optimal solutions, but for many problems they do. We first examine, in Section 15.1, a simple but nontrivial problem, the activity-selection problem, for which a greedy algorithm efficiently computes an optimal solution. We'll arrive at the greedy algorithm by first considering a dynamic-programming approach and then showing that an optimal solution can result from always making greedy choices. Section 15.2 reviews the basic elements of the greedy approach, giving a direct approach for proving greedy algorithms correct. Section 15.3 presents an important application of greedy techniques: designing data-compression (Huffman) codes. Finally, Section 15.4 shows that in order to decide which blocks to replace when a miss occurs in a cache, the "furthest-infuture" strategy is optimal if the sequence of block accesses is known in advance.

The greedy method is quite powerful and works well for a wide range of problems. Later chapters will present many algorithms that you can view as applications of the greedy method, including minimum-spanning-tree algorithms (Chapter 21), Dijkstra's algorithm for shortest paths from a single source (Section 22.3), and a greedy set-covering heuristic (Section 35.3). Minimum-spanning-tree algorithms furnish a classic example of the greedy method. Although you can read this chapter and Chapter 21 independently of each other, you might find it useful to read them together.