---
topic: strongly_connected_components
pages: 598-606
---

**Figure 20.9 (a)** A directed graph G. Each region shaded light blue is a strongly connected component of G. Each vertex is labeled with its discovery and finish times in a depth-first search, and tree edges are dark blue. **(b)** The graph G^T, the transpose of G, with the depth-first forest computed in line 3 of STRONGLY-CONNECTED-COMPONENTS shown and tree edges shaded dark blue. Each strongly connected component corresponds to one depth-first tree. Orange vertices b, c, g, and h are the roots of the depth-first trees produced by the depth-first search of G^T. **(c)** The acyclic component graph G_SCC obtained by contracting all edges within each strongly connected component of G so that only a single vertex remains in each component.

#### STRONGLY-CONNECTED-COMPONENTS(G)

- 1 call DFS(G) to compute finish times u:*f* for each vertex u
- 2 create G^T
- 3 call DFS(G^T), but in the main loop of DFS, consider the vertices in order of decreasing u:*f* (as computed in line 1)
- 4 output the vertices of each tree in the depth-first forest formed in line 3 as a separate strongly connected component

only a single vertex remains, the resulting graph is G_SCC. Figure 20.9(c) shows the component graph of the graph in Figure 20.9(a).

The following lemma gives the key property that the component graph is acyclic. We'll see that the algorithm uses this property to visit the vertices of the component graph in topologically sorted order, by considering vertices in the second depthfirst search in decreasing order of the finish times that were computed in the first depth-first search.

# *Lemma 20.13*

Let C and C′ be distinct strongly connected components in directed graph G = (V, E), let u, v ∈ C, let u′, v′ ∈ C′, and suppose that G contains a path u ❀ u′. Then G cannot also contain a path v′ ❀ v.

*Proof* If G contains a path v′ ❀ v, then it contains paths u ❀ u′ ❀ v′ and v′ ❀ v ❀ u. Thus, u and v′ are reachable from each other, thereby contradicting the assumption that C and C′ are distinct strongly connected components.

Because the STRONGLY-CONNECTED-COMPONENTS procedure performs two depth-first searches, there are two distinct sets of discovery and finish times. In this section, discovery and finish times always refer to those computed by the *first* call of DFS, in line 1.

The notation for discovery and finish times extends to sets of vertices. For a subset U of vertices, d(U) and f(U) are the earliest discovery time and latest finish time, respectively, of any vertex in U: d(U) = min{u:*d* : u ∈ U} and f(U) = max{u:*f* : u ∈ U}.

The following lemma and its corollary give a key property relating strongly connected components and finish times in the first depth-first search.

# *Lemma 20.14*

Let C and C′ be distinct strongly connected components in directed graph G = (V, E). Suppose that there is an edge (u, v) ∈ E, where u ∈ C′ and v ∈ C. Then f(C′) > f(C).

*Proof* We consider two cases, depending on which strongly connected component, C or C′, had the first discovered vertex during the first depth-first search.

If d(C′) < d(C), let x be the first vertex discovered in C′. At time x:*d*, all vertices in C and C′ are white. At that time, G contains a path from x to each vertex in C′ consisting only of white vertices. Because (u, v) ∈ E, for any vertex w ∈ C, there is also a path in G at time x:*d* from x to w consisting only of white vertices: x ❀ u → v ❀ w. By the white-path theorem, all vertices in C and C′ become descendants of x in the depth-first tree. By Corollary 20.8, x has the latest finish time of any of its descendants, and so x:*f* = f(C′) > f(C).

Otherwise, d(C′) > d(C). Let y be the first vertex discovered in C, so that y:*d* = d(C). At time y:*d*, all vertices in C are white and G contains a path from y to each vertex in C consisting only of white vertices. By the white-path theorem, all vertices in C become descendants of y in the depth-first tree, and by Corollary 20.8, y:*f* = f(C). Because d(C′) > d(C) = y:*d*, all vertices in C′ are white at time y:*d*. Since there is an edge (u, v) from C′ to C, Lemma 20.13 implies that there cannot be a path from C to C′. Hence, no vertex in C′ is reachable 

from y. At time y:*f*, therefore, all vertices in C′ are still white. Thus, for any vertex w ∈ C′, we have w:*f* > y:*f*, which implies that f(C′) > f(C).

# *Corollary 20.15*

Let C and C′ be distinct strongly connected components in directed graph G = (V, E), and suppose that f(C) > f(C′). Then E^T contains no edge (v, u) such that u ∈ C′ and v ∈ C.

*Proof* The contrapositive of Lemma 20.14 says that if f(C′) < f(C), then there is no edge (u, v) ∈ E such that u ∈ C′ and v ∈ C. Because the strongly connected components of G and G^T are the same, if there is no such edge (u, v) ∈ E, then there is no edge (v, u) ∈ E^T such that u ∈ C′ and v ∈ C.

Corollary 20.15 provides the key to understanding why the strongly connected components algorithm works. Let's examine what happens during the second depth-first search, which is on G^T. The search starts from the vertex x whose finish time from the first depth-first search is maximum. This vertex belongs to some strongly connected component C, and since x:*f* is maximum, f(C) is maximum over all strongly connected components. When the search starts from x, it visits all vertices in C. By Corollary 20.15, G^T contains no edges from C to any other strongly connected component, and so the search from x never visits vertices in any other component. Thus, the tree rooted at x contains exactly the vertices of C. Having completed visiting all vertices in C, the second depth-first search selects as a new root a vertex from some other strongly connected component C′ whose finish time f(C′) is maximum over all components other than C. Again, the search visits all vertices in C′. But by Corollary 20.15, if any edges in G^T go from C′ to any other component, they must go to C, which the second depth-first search has already visited. In general, when the depth-first search of G^T in line 3 visits any strongly connected component, any edges out of that component must be to components that the search has already visited. Each depth-first tree, therefore, corresponds to exactly one strongly connected component. The following theorem formalizes this argument.

#### *Theorem 20.16*

The STRONGLY-CONNECTED-COMPONENTS procedure correctly computes the strongly connected components of the directed graph G provided as its input.

*Proof* We argue by induction on the number of depth-first trees found in the depth-first search of G^T in line 3 that the vertices of each tree form a strongly connected component. The inductive hypothesis is that the first k trees produced

==================================================

in line 3 are strongly connected components. The basis for the induction, when k = 0, is trivial.

In the inductive step, we assume that each of the first k depth-first trees produced in line 3 is a strongly connected component, and we consider the (k + 1)st tree produced. Let the root of this tree be vertex u, and let u be in strongly connected component C. Because of how the depth-first search chooses roots in line 3, u:*f* = f(C) > f(C′) for any strongly connected component C′ other than C that has yet to be visited. By the inductive hypothesis, at the time that the search visits u, all other vertices of C are white. By the white-path theorem, therefore, all other vertices of C are descendants of u in its depth-first tree. Moreover, by the inductive hypothesis and by Corollary 20.15, any edges in G^T that leave C must be to strongly connected components that have already been visited. Thus, no vertex in any strongly connected component other than C is a descendant of u during the depth-first search of G^T. The vertices of the depth-first tree in G^T that is rooted at u form exactly one strongly connected component, which completes the inductive step and the proof.

Here is another way to look at how the second depth-first search operates. Consider the component graph (G^T)_SCC of G^T. If you map each strongly connected component visited in the second depth-first search to a vertex of (G^T)_SCC, the second depth-first search visits vertices of (G^T)_SCC in the reverse of a topologically sorted order. If you reverse the edges of (G^T)_SCC, you get the graph ((G^T)_SCC)^T. Because ((G^T)_SCC)^T = G_SCC (see Exercise 20.5-4), the second depth-first search visits the vertices of G_SCC in topologically sorted order.

#### **Exercises**

## *20.5-1*

How can the number of strongly connected components of a graph change if a new edge is added?

### *20.5-2*

Show how the procedure STRONGLY-CONNECTED-COMPONENTS works on the graph of Figure 20.6. Specifically, show the finish times computed in line 1 and the forest produced in line 3. Assume that the loop of lines 5–7 of DFS considers vertices in alphabetical order and that the adjacency lists are in alphabetical order.

#### *20.5-3*

Professor Bacon rewrites the algorithm for strongly connected components to use the original (instead of the transpose) graph in the second depth-first search and

scan the vertices in order of *increasing* finish times. Does this modified algorithm always produce correct results?

## *20.5-4*

Prove that for any directed graph G, the transpose of the component graph of G^T is the same as the component graph of G. That is, ((G^T)_SCC)^T = G_SCC.

## *20.5-5*

Give an O(V + E)-time algorithm to compute the component graph of a directed graph G = (V, E). Make sure that there is at most one edge between two vertices in the component graph your algorithm produces.

## *20.5-6*

Give an O(V + E)-time algorithm that, given a directed graph G = (V, E), constructs another graph G′ = (V, E′) such that G and G′ have the same strongly connected components, G′ has the same component graph as G, and |E′| is as small as possible.

## *20.5-7*

A directed graph G = (V, E) is *semiconnected* if, for all pairs of vertices u, v ∈ V, we have u ❀ v or v ❀ u. Give an efficient algorithm to determine whether G is semiconnected. Prove that your algorithm is correct, and analyze its running time.

#### *20.5-8*

Let G = (V, E) be a directed graph, and let l: V → ℝ be a function that assigns a real-valued label l to each vertex. For vertices s, t ∈ V, define

$$\Delta l(s,t) = \begin{cases} l(t) - l(s) & \text{if there is a path from } s \text{ to } t \text{ in } G, \\ -\infty & \text{otherwise}. \end{cases}$$

Give an O(V + E)-time algorithm to find vertices s and t such that Δl(s, t) is maximum over all pairs of vertices. (*Hint:* Use Exercise 20.5-5.)

## **Problems**

#### *20-1 Classifying edges by breadth-first search*

A depth-first forest classifies the edges of a graph into tree, back, forward, and cross edges. A breadth-first tree can also be used to classify the edges reachable from the source of the search into the same four categories.

**Figure 20.10** The articulation points, bridges, and biconnected components of a connected, undirected graph for use in Problem 20-2. The articulation points are the orange vertices, the bridges are the dark blue edges, and the biconnected components are the edges in the light blue regions, with a *bcc* numbering shown.

- *a.* Prove that in a breadth-first search of an undirected graph, the following properties hold:
  - 1. There are no back edges and no forward edges.
  - 2. If (u, v) is a tree edge, then v:*d* = u:*d* + 1.
  - 3. If (u, v) is a cross edge, then v:*d* = u:*d* or v:*d* = u:*d* + 1.
- *b.* Prove that in a breadth-first search of a directed graph, the following properties hold:
  - 1. There are no forward edges.
  - 2. If (u, v) is a tree edge, then v:*d* = u:*d* + 1.
  - 3. If (u, v) is a cross edge, then v:*d* ≤ u:*d* + 1.
  - 4. If (u, v) is a back edge, then 0 ≤ v:*d* ≤ u:*d*.

#### *20-2 Articulation points, bridges, and biconnected components*

Let G = (V, E) be a connected, undirected graph. An *articulation point* of G is a vertex whose removal disconnects G. A *bridge* of G is an edge whose removal disconnects G. A *biconnected component* of G is a maximal set of edges such that any two edges in the set lie on a common simple cycle. Figure 20.10 illustrates these definitions. You can determine articulation points, bridges, and biconnected components using depth-first search. Let Gπ = (V, Eπ) be a depth-first tree of G.

*a.* Prove that the root of Gπ is an articulation point of G if and only if it has at least two children in Gπ.

- *b.* Let v be a nonroot vertex of Gπ. Prove that v is an articulation point of G if and only if v has a child s such that there is no back edge from s or any descendant of s to a proper ancestor of v.
- *c.* Let

$$v.low = \min \begin{cases} v.d, \\ w.d: (u, w) \text{ is a back edge for some descendant } u \text{ of } v. \end{cases}$$

Show how to compute v:*low* for all vertices v ∈ V in O(E) time.

- *d.* Show how to compute all articulation points in O(E) time.
- *e.* Prove that an edge of G is a bridge if and only if it does not lie on any simple cycle of G.
- *f.* Show how to compute all the bridges of G in O(E) time.
- *g.* Prove that the biconnected components of G partition the nonbridge edges of G.
- *h.* Give an O(E)-time algorithm to label each edge e of G with a positive integer e:*bcc* such that e:*bcc* = e′:*bcc* if and only if e and e′ belong to the same biconnected component.

#### *20-3 Euler tour*

An *Euler tour* of a strongly connected, directed graph G = (V, E) is a cycle that traverses each edge of G exactly once, although it may visit a vertex more than once.

- *a.* Show that G has an Euler tour if and only if in-degree(v) = out-degree(v) for each vertex v ∈ V.
- *b.* Describe an O(E)-time algorithm to find an Euler tour of G if one exists. (*Hint:*  Merge edge-disjoint cycles.)

#### *20-4 Reachability*

Let G = (V, E) be a directed graph in which each vertex u ∈ V is labeled with a unique integer L(u) from the set {1, 2, ..., |V|}. For each vertex u ∈ V, let R(u) = {v ∈ V : u ❀ v} be the set of vertices that are reachable from u. Define min(u) to be the vertex in R(u) whose label is minimum, that is, min(u) is the vertex v such that L(v) = min{L(w) : w ∈ R(u)}. Give an O(V + E)-time algorithm that computes min(u) for all vertices u ∈ V.

#### *20-5 Inserting and querying vertices in planar graphs*

A *planar* graph is an undirected graph that can be drawn in the plane with no edges crossing. Euler proved that every planar graph has |E| < 3|V|.

Consider the following two operations on a planar graph G:

- INSERT(G, v, *neighbors*) inserts a new vertex v into G, where *neighbors* is an array (possibly empty) of vertices that have already been inserted into G and will become all the neighbors of v in G when v is inserted.
- NEWEST-NEIGHBOR(G, v) returns the neighbor of vertex v that was most recently inserted into G, or NIL if v has no neighbors.

Design a data structure that supports these two operations such that NEWEST-NEIGHBOR takes O(1) worst-case time and INSERT takes O(1) amortized time. Note that the length of the array *neighbors* given to INSERT may vary. (*Hint:* Use a potential function for the amortized analysis.)

## **Chapter notes**

Even [137] and Tarjan [429] are excellent references for graph algorithms.

Breadth-first search was discovered by Moore [334] in the context of finding paths through mazes. Lee [280] independently discovered the same algorithm in the context of routing wires on circuit boards.

Hopcroft and Tarjan [226] advocated the use of the adjacency-list representation over the adjacency-matrix representation for sparse graphs and were the first to recognize the algorithmic importance of depth-first search. Depth-first search has been widely used since the late 1950s, especially in artificial intelligence programs.

Tarjan [426] gave a linear-time algorithm for finding strongly connected components. The algorithm for strongly connected components in Section 20.5 is adapted from Aho, Hopcroft, and Ullman [6], who credit it to S. R. Kosaraju (unpublished) and Sharir [408]. Dijkstra [117, Chapter 25] also developed an algorithm for strongly connected components that is based on contracting cycles. Subsequently, Gabow [163] rediscovered this algorithm. Knuth [259] was the first to give a linear-time algorithm for topological sorting.

# **21 Minimum Spanning Trees**

Electronic circuit designs often need to make the pins of several components electrically equivalent by wiring them together. To interconnect a set of n pins, the designer can use an arrangement of n − 1 wires, each connecting two pins. Of all such arrangements, the one that uses the least amount of wire is usually the most desirable.

To model this wiring problem, use a connected, undirected graph G = (V, E), where V is the set of pins, E is the set of possible interconnections between pairs of pins, and for each edge (u, v) ∈ E, a weight w(u, v) specifies the cost (amount of wire needed) to connect u and v. The goal is to find an acyclic subset T ⊆ E that connects all of the vertices and whose total weight

$$w(T) = \sum_{(u,v)\in T} w(u,v)$$

is minimized. Since T is acyclic and connects all of the vertices, it must form a tree, which we call a *spanning tree* since it "spans" the graph G. We call the problem of determining the tree T the *minimum-spanning-tree problem*.¹ Figure 21.1 shows an example of a connected graph and a minimum spanning tree.

This chapter studies two ways to solve the minimum-spanning-tree problem. Kruskal's algorithm and Prim's algorithm both run in O(E lg V) time. Prim's algorithm achieves this bound by using a binary heap as a priority queue. By using Fibonacci heaps instead (see page 478), Prim's algorithm runs in O(E + V lg V) time. This bound is better than O(E lg V) whenever |E| grows asymptotically faster than |V|.

¹ The phrase "minimum spanning tree" is a shortened form of the phrase "minimum-weight spanning tree." There is no point in minimizing the number of edges in T, since all spanning trees have exactly |V| − 1 edges by Theorem B.2 on page 1169.