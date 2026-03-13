---
topic: apsp_matrix_multiplication
pages: 670-676
---

We reserve the fourth step—constructing an optimal solution from computed information—for the exercises.

#### **The structure of a shortest path**

Let's start by characterizing the structure of an optimal solution. Lemma 22.1 tells us that all subpaths of a shortest path are shortest paths. Consider a shortest path p from vertex i to vertex j, and suppose that p contains at most r edges. Assuming that there are no negative-weight cycles, r is finite. If i = j, then p has weight 0 and no edges. If vertices i and j are distinct, then decompose path p into i ❀ k → j, where path p' now contains at most r - 1 edges. Lemma 22.1 says that p' is a shortest path from i to k, and so δ(i, j) = δ(i, k) + w_kj.

#### **A recursive solution to the all-pairs shortest-paths problem**

Now, let l^(r)_ij be the minimum weight of any path from vertex i to vertex j that contains at most r edges. When r = 0, there is a shortest path from i to j with no edges if and only if i = j, yielding

$$l_{ij}^{(0)} = \begin{cases} 0 & \text{if } i = j, \\ \infty & \text{if } i \neq j. \end{cases}$$
 (23.2)

For r ≥ 1, one way to achieve a minimum-weight path from i to j with at most r edges is by taking a path containing at most r - 1 edges, so that l^(r)_ij = l^(r-1)_ij. Another way is by taking a path of at most r - 1 edges from i to some vertex k and then taking the edge (k, j), so that l^(r)_ij = l^(r-1)_ik + w(k, j). Therefore, to examine paths from i to j consisting of at most r edges, try all possible predecessors k of j, giving the recursive definition

$$l_{ij}^{(r)} = \min \left\{ l_{ij}^{(r-1)}, \min \left\{ l_{ik}^{(r-1)} + w_{kj} : 1 \le k \le n \right\} \right\}$$

$$= \min \left\{ l_{ik}^{(r-1)} + w_{kj} : 1 \le k \le n \right\}.$$
(23.3)

The last equality follows from the observation that w_jj = 0 for all j.

What are the actual shortest-path weights δ(i, j)? If the graph contains no negative-weight cycles, then whenever δ(i, j) < ∞, there is a shortest path from vertex i to vertex j that is simple. (A path p from i to j that is not simple contains a cycle. Since each cycle's weight is nonnegative, removing all cycles from the path leaves a simple path with weight no greater than p's weight.) Because any simple path contains at most n - 1 edges, a path from vertex i to vertex j with more than n - 1 edges cannot have lower weight than a shortest path from i to j. The actual shortest-path weights are therefore given by

$$\delta(i,j) = l_{ij}^{(n-1)} = l_{ij}^{(n)} = l_{ij}^{(n+1)} = \cdots$$
 (23.4)

### **Computing the shortest-path weights bottom up**

Taking as input the matrix W = (w_ij), let's see how to compute a series of matrices L^(0), L^(1), ..., L^(n-1), where L^(r) = (l^(r)_ij) for r = 0, 1, ..., n - 1. The initial matrix is L^(0) given by equation (23.2). The final matrix L^(n-1) contains the actual shortest-path weights.

The heart of the algorithm is the procedure EXTEND-SHORTEST-PATHS, which implements equation (23.3) for all i and j. The four inputs are the matrix L^(r-1) computed so far; the edge-weight matrix W; the output matrix L^(r), which will hold the computed result and whose elements are all initialized to ∞ before invoking the procedure; and the number n of vertices. The superscripts r and r - 1 help to make the correspondence of the pseudocode with equation (23.3) plain, but they play no actual role in the pseudocode. The procedure extends the shortest paths computed so far by one more edge, producing the matrix L^(r) of shortest-path weights from the matrix L^(r-1) computed so far. Its running time is Θ(n^3) due to the three nested **for** loops.

```
EXTEND-SHORTEST-PATHS(L^(r-1), W, L^(r), n)
1 // Assume that the elements of L^(r) are initialized to ∞.
2 for i = 1 to n
3 for j = 1 to n
4 for k = 1 to n
5 l^(r)_ij = min{l^(r)_ij, l^(r-1)_ik + w_kj}
```

Let's now understand the relation of this computation to matrix multiplication. Consider how to compute the matrix product C = A · B of two n × n matrices A and B. The straightforward method used by MATRIX-MULTIPLY on page 81 uses a triply nested loop to implement equation (4.1), which we repeat here for convenience:

$$c_{ij} = \sum_{k=1}^{n} a_{ik} \cdot b_{kj} , \qquad (23.5)$$

for i; j = 1; 2; : : : ; n. Now make the substitutions

$$l^{(r-1)} \rightarrow a ,$$

$$w \rightarrow b ,$$

$$l^{(r)} \rightarrow c ,$$

$$\min \rightarrow + ,$$

$$+ \rightarrow \cdot$$

in equation (23.3). You get equation (23.5)! Making these changes to EXTEND-SHORTEST-PATHS, and also replacing ∞ (the identity for min) by 0 (the identity for +), yields the procedure MATRIX-MULTIPLY. We can see that the procedure EXTEND-SHORTEST-PATHS(L^(r-1), W, L^(r), n) computes the matrix "product" L^(r) = L^(r-1) · W using this unusual definition of matrix multiplication.<sup>2</sup>

Thus, we can solve the all-pairs shortest-paths problem by repeatedly multiplying matrices. Each step extends the shortest-path weights computed so far by one more edge using EXTEND-SHORTEST-PATHS(L^(r-1), W, L^(r), n) to perform the matrix multiplication. Starting with the matrix L^(0), we produce the following sequence of n - 1 matrices corresponding to powers of W:

$$L^{(1)} = L^{(0)} \cdot W = W^{1},$$

$$L^{(2)} = L^{(1)} \cdot W = W^{2},$$

$$L^{(3)} = L^{(2)} \cdot W = W^{3},$$

$$\vdots$$

$$L^{(n-1)} = L^{(n-2)} \cdot W = W^{n-1}.$$

At the end, the matrix L^(n-1) = W^(n-1) contains the shortest-path weights.

The procedure SLOW-APSP on the next page computes this sequence in Θ(n^4) time. The procedure takes the n × n matrices W and L^(0) as inputs, along with n. Figure 23.1 illustrates its operation. The pseudocode uses two n × n matrices L and M to store powers of W, computing M = L · W on each iteration. Line 2 initializes L = L^(0). For each iteration r, line 4 initializes M = ∞, where ∞ in this context is a matrix of scalar ∞ values. The rth iteration starts with the invariant L = L^(r-1) = W^(r-1). Line 6 computes M = L · W = L^(r-1) · W = W^(r-1) · W = W^r = L^(r) so that the invariant can be restored for the next iteration by line 7, which sets L = M. At the end, the matrix L = L^(n-1) = W^(n-1) of shortest-path weights is returned. The assignments to n × n matrices in lines 2, 4, and 7 implicitly run doubly nested loops that take Θ(n^2) time for each assignment.

<sup>2</sup> An algebraic *semiring* contains operations ⊕, which is commutative with identity I_⊕, and ⊗, with identity I_⊗, where ⊗ distributes over ⊕ on both the left and right, and where I_⊕ ⊗ x = x ⊗ I_⊕ = I_⊕ for all x. Standard matrix multiplication, as in MATRIX-MULTIPLY, uses the semiring with + for ⊕, · for ⊗, 0 for I_⊕, and 1 for I_⊗. The procedure EXTEND-SHORTEST-PATHS uses another semiring, known as the *tropical semiring*, with min for ⊕, + for ⊗, ∞ for I_⊕, and 0 for I_⊗.

**Figure 23.1** A directed graph and the sequence of matrices L^(r) computed by SLOW-APSP. You might want to verify that L^(5), defined as L^(4) · W, equals L^(4), and thus L^(r) = L^(4) for all r ≥ 4.

The n - 1 invocations of EXTEND-SHORTEST-PATHS, each of which takes Θ(n³) time, dominate the computation, yielding a total running time of Θ(n⁴).

```
SLOW-APSP(W, L^(0), n)
1 let L = (l_ij) and M = (m_ij) be new n × n matrices
2 L = L^(0)
3 for r = 1 to n - 1
4 M = ∞ // initialize M
5 // Compute the matrix "product" M = L · W.
6 EXTEND-SHORTEST-PATHS(L, W, M, n)
7 L = M
8 return L
```

## **Improving the running time**

Bear in mind that the goal is not to compute *all* the L^(r) matrices: only the matrix L^(n-1) matters. Recall that in the absence of negative-weight cycles, equation (23.4) implies L^(r) = L^(n-1) for all integers r ≥ n - 1. Just as traditional matrix multiplication is associative, so is matrix multiplication defined by the EXTEND-SHORTEST-PATHS procedure (see Exercise 23.1-4). In fact, we can compute L^(n-1) with only ⌈lg(n - 1)⌉ matrix products by using the technique of *repeated squaring*:

```
L^(1) = W,
L^(2) = W^2 = W · W,
L^(4) = W^4 = W^2 · W^2,
L^(8) = W^8 = W^4 · W^4,
...
L^(2^(⌈lg(n-1)⌉)) = W^(2^(⌈lg(n-1)⌉)) = W^(2^(⌈lg(n-1)⌉-1)) · W^(2^(⌈lg(n-1)⌉-1)).
```

Since 2^(⌈lg(n-1)⌉) ≥ n - 1, the final product is L^(2^(⌈lg(n-1)⌉)) = L^(n-1).

The procedure FASTER-APSP implements this idea. It takes just the n × n matrix W and the size n as inputs. Each iteration of the **while** loop of lines 4–8 starts with the invariant L = W^r, which it squares using EXTEND-SHORTEST-PATHS to obtain the matrix M = L^2 = (W^r)^2 = W^(2r). At the end of each iteration, the value of r doubles, and L for the next iteration becomes M, restoring the invariant. Upon exiting the loop when r ≥ n - 1, the procedure returns L = W^r = L^(r) = L^(n-1) by equation (23.4). As in SLOW-APSP, the assignments to n × n matrices in lines 2, 5, and 8 implicitly run doubly nested loops, taking Θ(n^2) time for each assignment.

```
FASTER-APSP(W, n)
1 let L and M be new n × n matrices
2 L = W
3 r = 1
4 while r < n - 1
5 M = ∞ // initialize M
6 EXTEND-SHORTEST-PATHS(L, L, M, n) // compute M = L^2
7 r = 2r
8 L = M // ready for the next iteration
9 return L
```

Because each of the ⌈lg(n - 1)⌉ matrix products takes Θ(n^3) time, FASTER-APSP runs in Θ(n^3 lg n) time. The code is tight, containing no elaborate data structures, and the constant hidden in the Θ-notation is therefore small.

#### **Exercises**

#### *23.1-1*

Run SLOW-APSP on the weighted, directed graph of Figure 23.2, showing the matrices that result for each iteration of the loop. Then do the same for FASTER-APSP.

**Figure 23.2** A weighted, directed graph for use in Exercises 23.1-1, 23.2-1, and 23.3-1.

## *23.1-2*

Why is it convenient for both SLOW-APSP and FASTER-APSP that w_ii = 0 for i = 1, 2, ..., n?

#### *23.1-3*

What does the matrix

$$L^{(0)} = \begin{pmatrix} 0 & \infty & \infty & \cdots & \infty \\ \infty & 0 & \infty & \cdots & \infty \\ \infty & \infty & 0 & \cdots & \infty \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ \infty & \infty & \infty & \cdots & 0 \end{pmatrix}$$

used in the shortest-paths algorithms correspond to in regular matrix multiplication?

#### *23.1-4*

Show that matrix multiplication defined by EXTEND-SHORTEST-PATHS is associative.

#### *23.1-5*

Show how to express the single-source shortest-paths problem as a product of matrices and a vector. Describe how evaluating this product corresponds to a Bellman-Ford-like algorithm (see Section 22.1).

#### *23.1-6*

Argue that we don't need the matrix M in SLOW-APSP because by substituting L for M and leaving out the initialization of M, the code still works correctly. (*Hint:* Relate line 5 of EXTEND-SHORTEST-PATHS to RELAX on page 610.) Do we need the matrix M in FASTER-APSP?

## *23.1-7*

Suppose that you also want to compute the vertices on shortest paths in the algorithms of this section. Show how to compute the predecessor matrix Π from the completed matrix L of shortest-path weights in O(n^3) time.

### *23.1-8*

You can also compute the vertices on shortest paths along with computing the shortest-path weights. Define π^(r)_ij as the predecessor of vertex j on any minimum-weight path from vertex i to vertex j that contains at most r edges. Modify the EXTEND-SHORTEST-PATHS and SLOW-APSP procedures to compute the matrices Π^(1), Π^(2), ..., Π^(n-1) as they compute the matrices L^(1), L^(2), ..., L^(n-1).

## *23.1-9*

Modify FASTER-APSP so that it can determine whether the graph contains a negative-weight cycle.

#### *23.1-10*

Give an efficient algorithm to find the length (number of edges) of a minimum-length negative-weight cycle in a graph.

## **23.2 The Floyd-Warshall algorithm**

Having already seen one dynamic-programming solution to the all-pairs shortest-paths problem, in this section we'll see another: the *Floyd-Warshall algorithm*, which runs in Θ(V^3) time. As before, negative-weight edges may be present, but not negative-weight cycles. As in Section 23.1, we develop the algorithm by following the dynamic-programming process. After studying the resulting algorithm, we present a similar method for finding the transitive closure of a directed graph.

#### **The structure of a shortest path**

In the Floyd-Warshall algorithm, we characterize the structure of a shortest path differently from how we characterized it in Section 23.1. The Floyd-Warshall algorithm considers the intermediate vertices of a shortest path, where an *intermediate* vertex of a simple path p = 〈v_1, v_2, ..., v_l〉 is any vertex of p other than v_1 or v_l, that is, any vertex in the set {v_2, v_3, ..., v_(l-1)}.

The Floyd-Warshall algorithm relies on the following observation. Numbering the vertices of G by V = {1, 2, ..., n}, take a subset {1, 2, ..., k} of vertices for some 1 ≤ k ≤ n. For any pair of vertices i, j ∈ V, consider all paths from i to j whose intermediate vertices are all drawn from {1, 2, ..., k}, and let p be a