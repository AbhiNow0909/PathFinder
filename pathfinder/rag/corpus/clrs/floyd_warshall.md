---
topic: floyd_warshall
pages: 677-683
---

p1: all intermediate vertices in {1, 2, ..., k − 1}
p2: all intermediate vertices in {1, 2, ..., k − 1}

p: all intermediate vertices in {1, 2, ..., k}

**Figure 23.3** Optimal substructure used by the Floyd-Warshall algorithm. Path p is a shortest path from vertex i to vertex j, and k is the highest-numbered intermediate vertex of p. Path p₁, the portion of path p from vertex i to vertex k, has all intermediate vertices in the set {1, 2, ..., k − 1}. The same holds for path p₂ from vertex k to vertex j.

minimum-weight path from among them. (Path p is simple.) The Floyd-Warshall algorithm exploits a relationship between path p and shortest paths from i to j with all intermediate vertices in the set {1, 2, ..., k − 1}. The details of the relationship depend on whether k is an intermediate vertex of path p or not.

- If k is not an intermediate vertex of path p, then all intermediate vertices of path p belong to the set {1, 2, ..., k − 1}. Thus a shortest path from vertex i to vertex j with all intermediate vertices in the set {1, 2, ..., k − 1} is also a shortest path from i to j with all intermediate vertices in the set {1, 2, ..., k}.
- If k is an intermediate vertex of path p, then decompose p into i ↦ p₁ k ↦ p₂ j, as Figure 23.3 illustrates. By Lemma 22.1, p₁ is a shortest path from i to k with all intermediate vertices in the set {1, 2, ..., k}. In fact, we can make a slightly stronger statement. Because vertex k is not an *intermediate* vertex of path p₁, all intermediate vertices of p₁ belong to the set {1, 2, ..., k − 1}. Therefore p₁ is a shortest path from i to k with all intermediate vertices in the set {1, 2, ..., k − 1}. Likewise, p₂ is a shortest path from vertex k to vertex j with all intermediate vertices in the set {1, 2, ..., k − 1}.

#### **A recursive solution to the all-pairs shortest-paths problem**

The above observations suggest a recursive formulation of shortest-path estimates that differs from the one in Section 23.1. Let dᵢⱼ^(k) be the weight of a shortest path from vertex i to vertex j for which all intermediate vertices belong to the set {1, 2, ..., k}. When k = 0, a path from vertex i to vertex j with no intermediate vertex numbered higher than 0 has no intermediate vertices at all. Such a path has at most one edge, and hence dᵢⱼ^(0) = wᵢⱼ. Following the above discussion, define dᵢⱼ^(k) recursively by

$$d_{ij}^{(k)} = \begin{cases} w_{ij} & \text{if } k = 0, \\ \min\left\{d_{ij}^{(k-1)}, d_{ik}^{(k-1)} + d_{kj}^{(k-1)}\right\} & \text{if } k \ge 1. \end{cases}$$
 (23.6)

Because for any path, all intermediate vertices belong to the set {1, 2, ..., n}, the matrix D^(n) = (dᵢⱼ^(n)) gives the final answer: dᵢⱼ^(n) = δ(i, j) for all i, j ∈ V.

#### **Computing the shortest-path weights bottom up**

Based on recurrence (23.6), the bottom-up procedure FLOYD-WARSHALL computes the values dᵢⱼ^(k) in order of increasing values of k. Its input is an n × n matrix W defined as in equation (23.1). The procedure returns the matrix D^(n) of shortest-path weights. Figure 23.4 shows the matrices D^(k) computed by the Floyd-Warshall algorithm for the graph in Figure 23.1.

```
FLOYD-WARSHALL(W, n)
1 D^(0) = W
2 for k = 1 to n
3    let D^(k) = (dᵢⱼ^(k)) be a new n × n matrix
4    for i = 1 to n
5       for j = 1 to n
6          dᵢⱼ^(k) = min{dᵢⱼ^(k−1), dᵢₖ^(k−1) + dₖⱼ^(k−1)}
7 return D^(n)
```

The running time of the Floyd-Warshall algorithm is determined by the triply nested **for** loops of lines 2–6. Because each execution of line 6 takes O(1) time, the algorithm runs in Θ(n³) time. As in the final algorithm in Section 23.1, the code is tight, with no elaborate data structures, and so the constant hidden in the Θ-notation is small. Thus, the Floyd-Warshall algorithm is quite practical for even moderate-sized input graphs.

#### **Constructing a shortest path**

There are a variety of different methods for constructing shortest paths in the Floyd-Warshall algorithm. One way is to compute the matrix D of shortest-path weights and then construct the predecessor matrix Π from the D matrix. Exercise 23.1-7 asks you to implement this method so that it runs in O(n³) time. Given the predecessor matrix Π, the PRINT-ALL-PAIRS-SHORTEST-PATH procedure prints the vertices on a given shortest path.

Alternatively, the predecessor matrix Π can be computed while the algorithm computes the matrices D^(0), D^(1), ..., D^(n). Specifically, compute a sequence of

$$D^{(0)} = \begin{pmatrix} 0 & 3 & 8 & \infty & -4 \\ \infty & 0 & \infty & 1 & 7 \\ \infty & 4 & 0 & \infty & \infty \\ 2 & \infty & -5 & 0 & \infty \\ \infty & \infty & \infty & 6 & 0 \end{pmatrix} \qquad \Pi^{(0)} = \begin{pmatrix} \text{NIL} & 1 & 1 & \text{NIL} & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & \text{NIL} & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & \text{NIL} \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & \text{NIL} & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 1 & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 5 \\ \text{NIL} & 1 & 4 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 2 \\ \text{NIL} & 3 & \text{NIL} & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2 & 1 \\ \text{NIL} & \text{NIL} & 1 & 2$$

**Figure 23.4** The sequence of matrices D.k/ and ….k/ computed by the Floyd-Warshall algorithm {or the }raph in Figure 23.1.

matrices ….0/; ….1/; : : : ; ….n/, where … D ….n/ and � .k/ ij is the predecessor of vertex j on a shortest path {rom vertex i with all intermediate vertices in the set {1; 2; : : : ; kg.

Here9s a recursive {ormulation of � .k/ ij . When k = 0, a shortest path {rom i to j has no intermediate vertices at all, and so

$$\pi_{ij}^{(0)} = \begin{cases} \text{NIL} & \text{if } i = j \text{ or } w_{ij} = \infty, \\ i & \text{if } i \neq j \text{ and } w_{ij} < \infty. \end{cases}$$
 (23.7)

For <sup>k</sup> <sup>1</sup>, if the path has <sup>k</sup> as an intermediate vertex, so that it is <sup>i</sup> ❀ <sup>k</sup> ❀ <sup>j</sup> where k ≠ j , then choose as the predecessor of j on this path the same vertex as the predecessor of j chosen on a shortest path {rom k with all intermediate vertices in the set {1; 2; : : : ; k 1g. Otherwise, when the path {rom i to j does not have k as an intermediate vertex, choose the same predecessor of j as on a shortest path {rom i with all intermediate vertices in the set {1; 2; : : : ; k 1g. Formally, {or k 1,

$$\pi_{ij}^{(k)} = \begin{cases} \pi_{kj}^{(k-1)} & \text{if } d_{ij}^{(k-1)} > d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \\ & (k \text{ is an intermediate vertex}), \\ \pi_{ij}^{(k-1)} & \text{if } d_{ij}^{(k-1)} \le d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \\ & (k \text{ is not an intermediate vertex}). \end{cases}$$

$$(23.8)$$

Exercise 23.2-3 asks you to show how to incorporate the Π^(k) matrix computations into the FLOYD-WARSHALL procedure. Figure 23.4 shows the sequence of Π^(k) matrices that the resulting algorithm computes for the graph of Figure 23.1. The exercise also asks for the more difficult task of proving that the predecessor subgraph G_{π,i} is a shortest-paths tree with root i. Exercise 23.2-7 asks for yet another way to reconstruct shortest paths.

#### **Transitive closure of a directed graph**

Given a directed graph G = (V, E) with vertex set V = {1, 2, ..., n}, you might wish to determine simply whether G contains a path from i to j for all vertex pairs i, j ∈ V, without regard to edge weights. We define the *transitive closure* of G as the graph G* = (V, E*), where

E* = {(i, j) : there is a path from vertex i to vertex j in G}.

One way to compute the transitive closure of a graph in Θ(n³) time is to assign a weight of 1 to each edge of E and run the Floyd-Warshall algorithm. If there is a path from vertex i to vertex j, you get dᵢⱼ < n. Otherwise, you get dᵢⱼ = ∞.

There is another, similar way to compute the transitive closure of G in Θ(n³) time, which can save time and space in practice. This method substitutes the logical operations ∨ (logical OR) and ∧ (logical AND) for the arithmetic operations min and + in the Floyd-Warshall algorithm. For i, j, k = 1, 2, ..., n, define tᵢⱼ^(k) to be 1 if there exists a path in graph G from vertex i to vertex j with all intermediate vertices in the set {1, 2, ..., k}, and 0 otherwise. To construct the transitive closure G* = (V, E*), put edge (i, j) into E* if and only if tᵢⱼ^(n) = 1. A recursive definition of tᵢⱼ^(k), analogous to recurrence (23.6), is

**Figure 23.5** A directed graph and the matrices T^(k) computed by the transitive-closure algorithm.

$$t_{ij}^{(0)} = \begin{cases} 0 & \text{if } i \neq j \text{ and } (i,j) \notin E, \\ 1 & \text{if } i = j \text{ or } (i,j) \in E, \end{cases}$$
and for $k \geq 1$,
$$t_{ij}^{(k)} = t_{ij}^{(k-1)} \vee \left( t_{ik}^{(k-1)} \wedge t_{kj}^{(k-1)} \right). \tag{23.9}$$

As in the Floyd-Warshall algorithm, the TRANSITIVE-CLOSURE procedure computes the matrices T^(k) = (tᵢⱼ^(k)) in order of increasing k.

```
TRANSITIVE-CLOSURE(G, n)
1 let T^(0) = (tᵢⱼ^(0)) be a new n × n matrix
2 for i = 1 to n
3    for j = 1 to n
4       if i == j or (i, j) ∈ G.E
5          tᵢⱼ^(0) = 1
6       else tᵢⱼ^(0) = 0
7 for k = 1 to n
8    let T^(k) = (tᵢⱼ^(k)) be a new n × n matrix
9    for i = 1 to n
10      for j = 1 to n
11         tᵢⱼ^(k) = tᵢⱼ^(k−1) ∨ (tᵢₖ^(k−1) ∧ tₖⱼ^(k−1))
12 return T^(n)
```

Figure 23.5 shows the matrices T^(k) computed by the TRANSITIVE-CLOSURE procedure on a sample graph. The TRANSITIVE-CLOSURE procedure, like the Floyd-Warshall algorithm, runs in Θ(n³) time. On some computers, though, logical operations on single-bit values execute faster than arithmetic operations on integer words of data. Moreover, because the direct transitive-closure algorithm

uses only boolean values rather than integer values, its space requirement is less than the Floyd-Warshall algorithm's by a factor corresponding to the size of a word of computer storage.

#### **Exercises**

## *23.2-1*

Run the Floyd-Warshall algorithm on the weighted, directed graph of Figure 23.2. Show the matrix D^(k) that results for each iteration of the outer loop.

#### *23.2-2*

Show how to compute the transitive closure using the technique of Section 23.1.

## *23.2-3*

Modify the FLOYD-WARSHALL procedure to compute the Π^(k) matrices according to equations (23.7) and (23.8). Prove rigorously that for all i ∈ V, the predecessor subgraph G_{π,i} is a shortest-paths tree with root i. (*Hint:* To show that G_{π,i} is acyclic, first show that π^(k)_ij = l implies d^(k)_ij ≥ d^(k)_il + w_lj, according to the definition of π^(k)_ij. Then adapt the proof of Lemma 22.16.)

#### *23.2-4*

As it appears on page 657, the Floyd-Warshall algorithm requires Θ(n³) space, since it creates d^(k)_ij for i, j, k = 1, 2, ..., n. Show that the procedure FLOYD-WARSHALL', which simply drops all the superscripts, is correct, and thus only Θ(n²) space is required.

```
FLOYD-WARSHALL'(W, n)
1 D = W
2 for k = 1 to n
3    for i = 1 to n
4       for j = 1 to n
5          d_ij = min{d_ij, d_ik + d_kj}
6 return D
```

#### *23.2-5*

Consider the following change to how equation (23.8) handles equality:

$$\pi_{ij}^{(k)} = \begin{cases} \pi_{kj}^{(k-1)} & \text{if } d_{ij}^{(k-1)} \ge d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \\ & (k \text{ is an intermediate vertex}), \\ \pi_{ij}^{(k-1)} & \text{if } d_{ij}^{(k-1)} < d_{ik}^{(k-1)} + d_{kj}^{(k-1)} \\ & (k \text{ is not an intermediate vertex}). \end{cases}$$

Is this alternative definition of the predecessor matrix Π correct?

## *23.2-6*

Show how to use the output of the Floyd-Warshall algorithm to detect the presence of a negative-weight cycle.

## *23.2-7*

Another way to reconstruct shortest paths in the Floyd-Warshall algorithm uses values � .k/ ij {or i; j; k = 1; 2; : : : ; n, where � .k/ ij is the highest-numbered intermediate vertex of a shortest path {rom i to j in which all intermediate vertices lie in the set {1; 2; : : : ; kg. Give a recursive {ormulation {or � .k/ ij , modify the FLOYD-WARSHALL procedure to compute the � .k/ ij values, and rewrite the PRINT-ALL-PAIRS-SHORTEST-PATH procedure to take the matrix ˆ = ã � .n/ ij ä as an input. How is the matrix ˆ like the s table in the matrix-chain multiplication problem of Section 14.2?

#### *23.2-8*

Give an O.VE/-time algorithm {or computing the transitive closure of a directed }raph G = .V; E/. Assume that jV j = O.E/ and that the }raph is represented with adjacency lists.

## *23.2-9*

Suppose that it takes { .jV j ; jEj/ time to compute the transitive closure of a directed acyclic }raph, where { is a monotonically increasing {unction of both jV j and jEj. Show that the time to compute the transitive closure G <sup>D</sup> .V; E / of a }eneral directed }raph <sup>G</sup> <sup>D</sup> .V; E/ is then { .jV <sup>j</sup> ; <sup>j</sup>Ej/ <sup>C</sup> O.V <sup>C</sup> <sup>E</sup> /.

## **23.3 Johnson's algorithm for sparse graphs**

Johnson's algorithm finds shortest paths between all pairs in O(V² lg V + VE) time. For sparse graphs, it is asymptotically faster than either repeated squaring of matrices or the Floyd-Warshall algorithm. The algorithm either returns a matrix of shortest-path weights for all pairs of vertices or reports that the input graph contains a negative-weight cycle. Johnson's algorithm uses as subroutines both Dijkstra's algorithm and the Bellman-Ford algorithm, which Chapter 22 describes.

Johnson's algorithm uses the technique of *reweighting*, which works as follows. If all edge weights w in a graph G = (V, E) are nonnegative, Dijkstra's algorithm can find shortest paths between all pairs of vertices by running it once from each vertex. With the Fibonacci-heap min-priority queue, the running time of this all-pairs algorithm is O(V² lg V + VE). If G has negative-weight edges but no negative-weight cycles, first compute a new set of nonnegative edge weights so