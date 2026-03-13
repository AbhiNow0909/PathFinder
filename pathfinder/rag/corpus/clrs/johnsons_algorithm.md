---
topic: johnsons_algorithm
pages: 684-691
---

that Dijkstra's algorithm applies. The new set of edge weights ŵ must satisfy two important properties:

- 1. For all pairs of vertices u, v ∈ V, a path p is a shortest path from u to v using weight function w if and only if p is also a shortest path from u to v using weight function ŵ.
- 2. For all edges (u, v), the new weight ŵ(u, v) is nonnegative.

As we'll see in a moment, preprocessing G to determine the new weight function ŵ takes O(VE) time.

## **Preserving shortest paths by reweighting**

The following lemma shows how to reweight the edges to satisfy the first property above. We use δ to denote shortest-path weights derived from weight function w and δ̂ to denote shortest-path weights derived from weight function ŵ.

#### *Lemma 23.1 (Reweighting does not change shortest paths)*

Given a weighted, directed graph G = (V, E) with weight function w: E → R, let h: V → R be any function mapping vertices to real numbers. For each edge (u, v) ∈ E, define

$$\widehat{w}(u,v) = w(u,v) + h(u) - h(v).$$
(23.10)

Let p = ⟨v₀, v₁, ..., vₖ⟩ be any path from vertex v₀ to vertex vₖ. Then p is a shortest path from v₀ to vₖ with weight function w if and only if it is a shortest path with weight function ŵ. That is, w(p) = δ(v₀, vₖ) if and only if ŵ(p) = δ̂(v₀, vₖ). Furthermore, G has a negative-weight cycle using weight function w if and only if G has a negative-weight cycle using weight function ŵ.

*Proof* We start by showing that

$$\widehat{w}(p) = w(p) + h(v_0) - h(v_k). \tag{23.11}$$

We have

$$\widehat{w}(p) = \sum_{i=1}^{k} \widehat{w}(v_{i-1}, v_i)$$

$$= \sum_{i=1}^{k} (w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i))$$

$$= \sum_{i=1}^{k} w(v_{i-1}, v_i) + h(v_0) - h(v_k) \quad \text{(because the sum telescopes)}$$

$$= w(p) + h(v_0) - h(v_k) .$$

Therefore, any path p from v₀ to vₖ has ŵ(p) = w(p) + h(v₀) − h(vₖ). Because h(v₀) and h(vₖ) do not depend on the path, if one path from v₀ to vₖ is shorter than another using weight function w, then it is also shorter using ŵ. Thus, w(p) = δ(v₀, vₖ) if and only if ŵ(p) = δ̂(v₀, vₖ).

Finally, we show that G has a negative-weight cycle using weight function w if and only if G has a negative-weight cycle using weight function ŵ. Consider any cycle c = ⟨v₀, v₁, ..., vₖ⟩, where v₀ = vₖ. By equation (23.11),

$$\widehat{w}(c) = w(c) + h(v_0) - h(v_k)$$
  
= w(c),

and thus c has negative weight using w if and only if it has negative weight using ŵ.

#### **Producing nonnegative weights by reweighting**

Our next goal is to ensure that the second property holds: ŵ(u, v) must be nonnegative for all edges (u, v) ∈ E. Given a weighted, directed graph G = (V, E) with weight function w: E → R, we'll see how to make a new graph G' = (V', E'), where V' = V ∪ {s} for some new vertex s ∉ V and E' = E ∪ {(s, v): v ∈ V}. To incorporate the new vertex s, extend the weight function w so that w(s, v) = 0 for all v ∈ V. Since no edges enter s, no shortest paths in G', other than those with source s, contain s. Moreover, G' has no negative-weight cycles if and only if G has no negative-weight cycles. Figure 23.6(a) shows the graph G' corresponding to the graph G of Figure 23.1.

Now suppose that G and G' have no negative-weight cycles. Define the function h(v) = δ(s, v) for all v ∈ V'. By the triangle inequality (Lemma 22.10 on page 633), we have h(v) ≤ h(u) + w(u, v) for all edges (u, v) ∈ E'. Thus, by defining reweighted edge weights ŵ according to equation (23.10), we have ŵ(u, v) = w(u, v) + h(u) − h(v) ≥ 0, thereby satisfying the second property. Figure 23.6(b) shows the graph G' from Figure 23.6(a) with reweighted edges.

#### **Computing all-pairs shortest paths**

Johnson's algorithm to compute all-pairs shortest paths uses the Bellman-Ford algorithm (Section 22.1) and Dijkstra's algorithm (Section 22.3) as subroutines. The pseudocode appears in the procedure JOHNSON on page 666. It assumes implicitly that the edges are stored in adjacency lists. The algorithm returns the usual |V| × |V| matrix D = (d_ij), where d_ij = δ(i, j), or it reports that the input graph contains a negative-weight cycle. As is typical for an all-pairs shortest-paths algorithm, it assumes that the vertices are numbered from 1 to |V|.

**Figure 23.6** Johnson's all-pairs shortest-paths algorithm run on the graph of Figure 23.1. Vertex numbers appear outside the vertices. **(a)** The graph G' with the original weight function w. The new vertex s is blue. Within each vertex v is h(v) = δ(s, v). **(b)** After reweighting each edge (u, v) with weight function ŵ(u, v) = w(u, v) + h(u) − h(v). **(c)–(g)** The result of running Dijkstra's algorithm on each vertex of G using weight function ŵ. In each part, the source vertex u is blue, and blue edges belong to the shortest-paths tree computed by the algorithm. Within each vertex v are the values δ̂(u, v) and δ(u, v), separated by a slash. The value d_uv = δ(u, v) is equal to δ̂(u, v) + h(v) − h(u).

```
JOHNSON(G, w)
1 compute G', where G':V = G:V ∪ {s}, 
       G':E = G:E ∪ {(s, v): v ∈ G:V}, and 
       w(s, v) = 0 for all v ∈ G:V 
2 if BELLMAN-FORD(G', w, s) == FALSE 
3 print "the input graph contains a negative-weight cycle"
4 else for each vertex v ∈ G':V 
5 set h(v) to the value of δ(s, v)
               computed by the Bellman-Ford algorithm
6 for each edge (u, v) ∈ G':E 
7 ŵ(u, v) = w(u, v) + h(u) − h(v)
8 let D = (d_uv) be a new n × n matrix 
9for each vertex u ∈ G:V 
10 run DIJKSTRA(G, ŵ, u) to compute δ̂(u, v) for all v ∈ G:V 
11 for each vertex v ∈ G:V 
12 d_uv = δ̂(u, v) + h(v) − h(u)
13 return D
```

The JOHNSON procedure simply performs the actions specified earlier. Line 1 produces G'. Line 2 runs the Bellman-Ford algorithm on G' with weight function w and source vertex s. If G', and hence G, contains a negative-weight cycle, line 3 reports the problem. Lines 4–12 assume that G' contains no negative-weight cycles. Lines 4–5 set h(v) to the shortest-path weight δ(s, v) computed by the Bellman-Ford algorithm for all v ∈ V'. Lines 6–7 compute the new weights ŵ. For each pair of vertices u, v ∈ V, the **for** loop of lines 9–12 computes the shortest-path weight δ̂(u, v) by calling Dijkstra's algorithm once from each vertex in V. Line 12 stores in matrix entry d_uv the correct shortest-path weight δ(u, v), calculated using equation (23.11). Finally, line 13 returns the completed D matrix. Figure 23.6 depicts the execution of Johnson's algorithm.

If the min-priority queue in Dijkstra's algorithm is implemented by a Fibonacci heap, Johnson's algorithm runs in O(V² lg V + VE) time. The simpler binary minheap implementation yields a running time of O(VE lg V), which is still asymptotically faster than the Floyd-Warshall algorithm if the graph is sparse.

#### **Exercises**

#### *23.3-1*

Use Johnson's algorithm to find the shortest paths between all pairs of vertices in the graph of Figure 23.2. Show the values of h and ŵ computed by the algorithm.

## *23.3-2*

What is the purpose of adding the new vertex s to V, yielding V'?

## *23.3-3*

Suppose that w(u, v) ≥ 0 for all edges (u, v) ∈ E. What is the relationship between the weight functions w and ŵ?

## *23.3-4*

Professor Greenstreet claims that there is a simpler way to reweight edges than the method used in Johnson's algorithm. Letting w* = min{w(u, v): (u, v) ∈ E}, just define ŵ(u, v) = w(u, v) − w* for all edges (u, v) ∈ E. What is wrong with the professor's method of reweighting?

## *23.3-5*

Show that if G contains a 0-weight cycle c, then ŵ(u, v) = 0 for every edge (u, v) in c.

## *23.3-6*

Professor Michener claims that there is no need to create a new source vertex in line 1 of JOHNSON. He suggests using G' = G instead and letting s be any vertex. Give an example of a weighted, directed graph G for which incorporating the professor's idea into JOHNSON causes incorrect answers. Assume that δ(s, s) is undefined, and in particular, it is not 0. Then show that if G is strongly connected (every vertex is reachable from every other vertex), the results returned by JOHNSON with the professor's modification are correct.

## **Problems**

#### *23-1 Transitive closure of a dynamic graph*

You wish to maintain the transitive closure of a directed graph G = (V, E) as you insert edges into E. That is, after inserting an edge, you update the transitive closure of the edges inserted so far. Start with G having no edges initially, and represent the transitive closure by a boolean matrix.

- *a.* Show how to update the transitive closure G* = (V, E*) of a graph G = (V, E) in O(V²) time when a new edge is added to G.
- *b.* Give an example of a graph G and an edge e such that Ω(V²) time is required to update the transitive closure after inserting e into G, no matter what algorithm is used.

*c.* Give an algorithm for updating the transitive closure as edges are inserted into the graph. For any sequence of r insertions, your algorithm should run in time ∑ʳᵢ₌₁ tᵢ = O(V³), where tᵢ is the time to update the transitive closure upon inserting the ith edge. Prove that your algorithm attains this time bound.

## *23-2 Shortest paths in ε-dense graphs*

A graph G = (V, E) is *ε-dense* if |E| = Θ(V^{1+ε}) for some constant ε in the range 0 < ε ≤ 1. d-ary min-heaps (see Problem 6-2 on page 179) provide a way to match the running times of Fibonacci-heap-based shortest-path algorithms on ε-dense graphs without using as complicated a data structure.

- *a.* What are the asymptotic running times for the operations INSERT, EXTRACT-MIN, and DECREASE-KEY, as a function of d and the number n of elements in a d-ary min-heap? What are these running times if you choose d = Θ(n^α) for some constant 0 < α ≤ 1? Compare these running times to the amortized costs of these operations for a Fibonacci heap.
- *b.* Show how to compute shortest paths from a single source on an ε-dense directed graph G = (V, E) with no negative-weight edges in O(E) time. (*Hint:* Pick d as a function of ε.)
- *c.* Show how to solve the all-pairs shortest-paths problem on an ε-dense directed graph G = (V, E) with no negative-weight edges in O(VE) time.
- *d.* Show how to solve the all-pairs shortest-paths problem in O(VE) time on an ε-dense directed graph G = (V, E) that may have negative-weight edges but has no negative-weight cycles.

## **Chapter notes**

Lawler [276] has a good discussion of the all-pairs shortest-paths problem. He attributes the matrix-multiplication algorithm to the folklore. The Floyd-Warshall algorithm is due to Floyd [144], who based it on a theorem of Warshall [450] that describes how to compute the transitive closure of boolean matrices. Johnson's algorithm is taken from [238].

Several researchers have given improved algorithms for computing shortest paths via matrix multiplication. Fredman [153] shows how to solve the allpairs shortest paths problem using O(V^{5/2}) comparisons between sums of edge weights and obtains an algorithm that runs in O(V³(lg lg V / lg V)^{1/3}) time, which is slightly better than the running time of the Floyd-Warshall algorithm. This bound 

has been improved several times, and the fastest algorithm is now by Williams [457], with a running time of O(V³/2^{Ω(√lg V)}).

Another line of research demonstrates how to apply algorithms for fast matrix multiplication (see the chapter notes for Chapter 4) to the all-pairs shortest paths problem. Let O(n^ω) be the running time of the fastest algorithm for multiplying two n × n matrices. Galil and Margalit [170, 171] and Seidel [403] designed algorithms that solve the all-pairs shortest paths problem in undirected, unweighted graphs in Õ(V^ω p(V)) time, where p(n) denotes a particular function that is polylogarithmically bounded in n. In dense graphs, these algorithms are faster than the O(VE) time needed to perform |V| breadth-first searches. Several researchers have extended these results to give algorithms for solving the all-pairs shortest paths problem in undirected graphs in which the edge weights are integers in the range {1, 2, ..., W}. The asymptotically fastest such algorithm, by Shoshan and Zwick [410], runs in Õ(W V^ω p(VW)) time. In directed graphs, the best algorithm to date is due to Zwick [467] and runs in O(W^{1/(4−ω)} V^{2+1/(4−ω)}) time.

Karger, Koller, and Phillips [244] and independently McGeoch [320] have given a time bound that depends on E*, the set of edges in E that participate in some shortest path. Given a graph with nonnegative edge weights, their algorithms run in O(VE* + V² lg V) time and improve upon running Dijkstra's algorithm |V| times when |E*| = o(E). Pettie [355] uses an approach based on component hierarchies to achieve a running time of O(VE* + V² lg lg V), and the same running time is also achieved by Hagerup [205].

Baswana, Hariharan, and Sen [37] examined decremental algorithms, which allow a sequence of intermixed edge deletions and queries, for maintaining all-pairs shortest paths and transitive-closure information. When a path exists, their randomized transitive-closure algorithm can fail to report it with probability 1/n^c for an arbitrary c > 0. The query times are O(1) with high probability. For transitive closure, the amortized time for each update is O(V^{4/3} lg^{1/3} V). By comparison, Problem 23-1, in which edges are inserted, asks for an incremental algorithm. For all-pairs shortest paths, the update times depend on the queries. For queries just giving the shortest-path weights, the amortized time per update is O(V³/E lg² V). To report the actual shortest path, the amortized update time is min{O(V^{3/2}√lg V), O(V³/E lg² V)}. Demetrescu and Italiano [111] showed how to handle update and query operations when edges are both inserted and deleted, as long as the range of edge weights is bounded.

Aho, Hopcroft, and Ullman [5] defined an algebraic structure known as a "closed semiring," which serves as a general framework for solving path problems in directed graphs. Both the Floyd-Warshall algorithm and the transitive-closure algorithm from Section 23.2 are instantiations of an all-pairs algorithm based on closed semirings. Maggs and Plotkin [309] showed how to find minimum spanning trees using a closed semiring.

# **24 Maximum Flow**

Just as you can model a road map as a directed graph in order to find the shortest path from one point to another, you can also interpret a directed graph as a "flow network" and use it to answer questions about material flows. Imagine a material coursing through a system from a source, where the material is produced, to a sink, where it is consumed. The source produces the material at some steady rate, and the sink consumes the material at the same rate. The "flow" of the material at any point in the system is intuitively the rate at which the material moves. Flow networks can model many problems, including liquids flowing through pipes, parts through assembly lines, current through electrical networks, and information through communication networks.

You can think of each directed edge in a flow network as a conduit for the material. Each conduit has a stated capacity, given as a maximum rate at which the material can flow through the conduit, such as 200 gallons of liquid per hour through a pipe or 20 amperes of electrical current through a wire. Vertices are conduit junctions, and other than the source and sink, material flows through the vertices without collecting in them. In other words, the rate at which material enters a vertex must equal the rate at which it leaves the vertex. We call this property "flow conservation," and it is equivalent to Kirchhoff's current law when the material is electrical current.

The goal of the maximum-flow problem is to compute the greatest rate for shipping material from the source to the sink without violating any capacity constraints. It is one of the simplest problems concerning flow networks and, as we shall see in this chapter, this problem can be solved by efficient algorithms. Moreover, other network-flow problems are solvable by adapting the basic techniques used in maximum-flow algorithms.

This chapter presents two general methods for solving the maximum-flow problem. Section 24.1 formalizes the notions of flow networks and flows, formally defining the maximum-flow problem. Section 24.2 describes the classical method