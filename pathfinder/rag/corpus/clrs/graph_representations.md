---
topic: graph_representations
pages: 571-575
---

**Figure 20.1** Two representations of an undirected graph. **(a)** An undirected graph G with 5 vertices and 7 edges. **(b)** An adjacency-list representation of G. **(c)** The adjacency-matrix representation of G.

**Figure 20.2** Two representations of a directed graph. **(a)** A directed graph G with 6 vertices and 8 edges. **(b)** An adjacency-list representation of G. **(c)** The adjacency-matrix representation of G.

all-pairs shortest-paths algorithms presented in Chapter 23 assume that their input graphs are represented by adjacency matrices.

The *adjacency-list representation* of a graph G = (V, E) consists of an array *Adj* of |V| lists, one for each vertex in V. For each u ∈ V, the adjacency list *Adj*[u] contains all the vertices v such that there is an edge (u, v) ∈ E. That is, *Adj*[u] consists of all the vertices adjacent to u in G. (Alternatively, it can contain pointers to these vertices.) Since the adjacency lists represent the edges of a graph, our pseudocode treats the array *Adj* as an attribute of the graph, just like the edge set E. In pseudocode, therefore, you will see notation such as G:*Adj*[u]. Figure 20.1(b) is an adjacency-list representation of the undirected graph in Figure 20.1(a). Similarly, Figure 20.2(b) is an adjacency-list representation of the directed graph in Figure 20.2(a).

If G is a directed graph, the sum of the lengths of all the adjacency lists is |E|, since an edge of the form (u, v) is represented by having v appear in *Adj*[u]. If G is 

an undirected graph, the sum of the lengths of all the adjacency lists is 2|E|, since if (u, v) is an undirected edge, then u appears in v's adjacency list and vice versa. For both directed and undirected graphs, the adjacency-list representation has the desirable property that the amount of memory it requires is Θ(V + E). Finding each edge in the graph also takes Θ(V + E) time, rather than just Θ(E), since each of the |V| adjacency lists must be examined. Of course, if |E| = Ω(V)—such as in a connected, undirected graph or a strongly connected, directed graph—we can say that finding each edge takes Θ(E) time.

Adjacency lists can also represent *weighted graphs*, that is, graphs for which each edge has an associated *weight* given by a *weight function* w : E → R. For example, let G = (V, E) be a weighted graph with weight function w. Then you can simply store the weight w(u, v) of the edge (u, v) ∈ E with vertex v in u's adjacency list. The adjacency-list representation is quite robust in that you can modify it to support many other graph variants.

A potential disadvantage of the adjacency-list representation is that it provides no quicker way to determine whether a given edge (u, v) is present in the graph than to search for v in the adjacency list *Adj*[u]. An adjacency-matrix representation of the graph remedies this disadvantage, but at the cost of using asymptotically more memory. (See Exercise 20.1-8 for suggestions of variations on adjacency lists that permit faster edge lookup.)

The *adjacency-matrix representation* of a graph G = (V, E) assumes that the vertices are numbered 1, 2, ..., |V| in some arbitrary manner. Then the adjacencymatrix representation of a graph G consists of a |V| × |V| matrix A = (aᵢⱼ) such that

$$a_{ij} = \begin{cases} 1 & \text{if } (i,j) \in E, \\ 0 & \text{otherwise}. \end{cases}$$

Figures 20.1(c) and 20.2(c) are the adjacency matrices of the undirected and directed graphs in Figures 20.1(a) and 20.2(a), respectively. The adjacency matrix of a graph requires Θ(V²) memory, independent of the number of edges in the graph. Because finding each edge in the graph requires examining the entire adjacency matrix, doing so takes Θ(V²) time.

Observe the symmetry along the main diagonal of the adjacency matrix in Figure 20.1(c). Since in an undirected graph, (u, v) and (v, u) represent the same edge, the adjacency matrix A of an undirected graph is its own transpose: A = A^T. In some applications, it pays to store only the entries on and above the diagonal of the adjacency matrix, thereby cutting the memory needed to store the graph almost in half.

Like the adjacency-list representation of a graph, an adjacency matrix can represent a weighted graph. For example, if G = (V, E) is a weighted graph with edge-weight function w, you can store the weight w(u, v) of the edge (u, v) ∈ E

as the entry in row u and column v of the adjacency matrix. If an edge does not exist, you can store a NIL value as its corresponding matrix entry, though for many problems it is convenient to use a value such as 0 or ∞.

Although the adjacency-list representation is asymptotically at least as spaceefficient as the adjacency-matrix representation, adjacency matrices are simpler, and so you might prefer them when graphs are reasonably small. Moreover, adjacency matrices carry a further advantage for unweighted graphs: they require only one bit per entry.

#### **Representing attributes**

Most algorithms that operate on graphs need to maintain attributes for vertices and/or edges. We indicate these attributes using our usual notation, such as v:*d* for an attribute d of a vertex v. When we indicate edges as pairs of vertices, we use the same style of notation. For example, if edges have an attribute f, then we denote this attribute for edge (u, v) by (u, v):*f*. For the purpose of presenting and understanding algorithms, our attribute notation suffices.

Implementing vertex and edge attributes in real programs can be another story entirely. There is no one best way to store and access vertex and edge attributes. For a given situation, your decision will likely depend on the programming language you are using, the algorithm you are implementing, and how the rest of your program uses the graph. If you represent a graph using adjacency lists, one design choice is to represent vertex attributes in additional arrays, such as an array d[1 : |V|] that parallels the *Adj* array. If the vertices adjacent to u belong to *Adj*[u], then the attribute u:*d* can actually be stored in the array entry d[u]. Many other ways of implementing attributes are possible. For example, in an objectoriented programming language, vertex attributes might be represented as instance variables within a subclass of a Vertex class.

### **Exercises**

#### *20.1-1*

Given an adjacency-list representation of a directed graph, how long does it take to compute the out-degree of every vertex? How long does it take to compute the in-degrees?

#### *20.1-2*

Give an adjacency-list representation for a complete binary tree on 7 vertices. Give an equivalent adjacency-matrix representation. Assume that the edges are undirected and that the vertices are numbered from 1 to 7 as in a binary heap.

# *20.1-3*

The *transpose* of a directed graph G = (V, E) is the graph G^T = (V, E^T), where E^T = {(v, u) ∈ V × V : (u, v) ∈ E}. That is, G^T is G with all its edges reversed. Describe efficient algorithms for computing G^T from G, for both the adjacencylist and adjacency-matrix representations of G. Analyze the running times of your algorithms.

# *20.1-4*

Given an adjacency-list representation of a multigraph G = (V, E), describe an O(V + E)-time algorithm to compute the adjacency-list representation of the "equivalent" undirected graph G' = (V, E'), where E' consists of the edges in E with all multiple edges between two vertices replaced by a single edge and with all self-loops removed.

# *20.1-5*

The *square* of a directed graph G = (V, E) is the graph G² = (V, E²) such that (u, v) ∈ E² if and only if G contains a path with at most two edges between u and v. Describe efficient algorithms for computing G² from G for both the adjacency-list and adjacency-matrix representations of G. Analyze the running times of your algorithms.

#### *20.1-6*

Most graph algorithms that take an adjacency-matrix representation as input require Ω(V²) time, but there are some exceptions. Show how to determine whether a directed graph G contains a *universal sink*—a vertex with in-degree |V| − 1 and out-degree 0—in O(V) time, given an adjacency matrix for G.

#### *20.1-7*

The *incidence matrix* of a directed graph G = (V, E) with no self-loops is a |V| × |E| matrix B = (bᵢⱼ) such that

$$b_{ij} = \begin{cases} -1 & \text{if edge } j \text{ leaves vertex } i, \\ 1 & \text{if edge } j \text{ enters vertex } i, \\ 0 & \text{otherwise}. \end{cases}$$

Describe what the entries of the matrix product BB^T represent, where B^T is the transpose of B.

#### *20.1-8*

Suppose that instead of a linked list, each array entry *Adj*[u] is a hash table containing the vertices v for which (u, v) ∈ E, with collisions resolved by chaining. Under the assumption of uniform independent hashing, if all edge lookups are equally likely, what is the expected time to determine whether an edge is in the graph?

What disadvantages does this scheme have? Suggest an alternate data structure for each edge list that solves these problems. Does your alternative have disadvantages compared with the hash table?

# **20.2 Breadth-first search**

*Breadth-first search* is one of the simplest algorithms for searching a graph and the archetype for many important graph algorithms. Prim's minimum-spanningtree algorithm (Section 21.2) and Dijkstra's single-source shortest-paths algorithm (Section 22.3) use ideas similar to those in breadth-first search.

Given a graph G = (V, E) and a distinguished *source* vertex s, breadth-first search systematically explores the edges of G to "discover" every vertex that is reachable from s. It computes the distance from s to each reachable vertex, where the distance to a vertex v equals the smallest number of edges needed to go from s to v. Breadth-first search also produces a "breadth-first tree" with root s that contains all reachable vertices. For any vertex v reachable from s, the simple path in the breadth-first tree from s to v corresponds to a shortest path from s to v in G, that is, a path containing the smallest number of edges. The algorithm works on both directed and undirected graphs.

Breadth-first search is so named because it expands the frontier between discovered and undiscovered vertices uniformly across the breadth of the frontier. You can think of it as discovering vertices in waves emanating from the source vertex. That is, starting from s, the algorithm first discovers all neighbors of s, which have distance 1. Then it discovers all vertices with distance 2, then all vertices with distance 3, and so on, until it has discovered every vertex reachable from s.

In order to keep track of the waves of vertices, breadth-first search could maintain separate arrays or lists of the vertices at each distance from the source vertex. Instead, it uses a single first-in, first-out queue (see Section 10.1.3) containing some vertices at a distance k, possibly followed by some vertices at distance k + 1. The queue, therefore, contains portions of two consecutive waves at any time.

To keep track of progress, breadth-first search colors each vertex white, gray, or black. All vertices start out white, and vertices not reachable from the source vertex s stay white the entire time. A vertex that is reachable from s is *discovered* the first time it is encountered during the search, at which time it becomes gray, indicating that is now on the frontier of the search: the boundary between discovered and undiscovered vertices. The queue contains all the gray vertices. Eventually, all the edges of a gray vertex will be explored, so that all of its neighbors will be