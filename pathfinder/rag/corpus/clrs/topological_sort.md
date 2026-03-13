---
topic: topological_sort
pages: 595-597
---

**Figure 20.7 (a)** Professor Bumstead topologically sorts his clothing when getting dressed. Each directed edge (u, v) means that garment u must be put on before garment v. The discovery and finish times from a depth-first search are shown next to each vertex. **(b)** The same graph shown topologically sorted, with its vertices arranged from left to right in order of decreasing finish time. All directed edges go from left to right.

*Proof* ⇒: Suppose that a depth-first search produces a back edge (u, v). Then vertex v is an ancestor of vertex u in the depth-first forest. Thus, G contains a path from v to u, and the back edge (u, v) completes a cycle.

⇐: Suppose that G contains a cycle c. We show that a depth-first search of G yields a back edge. Let v be the first vertex to be discovered in c, and let (u, v) be the preceding edge in c. At time v:*d*, the vertices of c form a path of white vertices from v to u. By the white-path theorem, vertex u becomes a descendant of v in the depth-first forest. Therefore, (u, v) is a back edge.

#### *Theorem 20.12*

TOPOLOGICAL-SORT produces a topological sort of the directed acyclic graph provided as its input.

*Proof* Suppose that DFS is run on a given dag G = (V, E) to determine finish times for its vertices. It suffices to show that for any pair of distinct vertices u, v ∈ V, if G contains an edge from u to v, then v:*f* < u:*f*. Consider any edge (u, v) explored by DFS(G). When this edge is explored, v cannot be gray, since then v would be an ancestor of u and (u, v) would be a back edge, contradicting Lemma 20.11. Therefore, v must be either white or black. If v is

**Figure 20.8** A dag for topological sorting.

white, it becomes a descendant of u, and so v:*f* < u:*f*. If v is black, it has already been finished, so that v:*f* has already been set. Because the search is still exploring from u, it has yet to assign a timestamp to u:*f*, so that the timestamp eventually assigned to u:*f* is greater than v:*f*. Thus, v:*f* < u:*f* for any edge (u, v) in the dag, proving the theorem.

#### **Exercises**

#### *20.4-1*

Show the ordering of vertices produced by TOPOLOGICAL-SORT when it is run on the dag of Figure 20.8. Assume that the **for** loop of lines 5–7 of the DFS procedure considers the vertices in alphabetical order, and assume that each adjacency list is ordered alphabetically.

#### *20.4-2*

Give a linear-time algorithm that, given a directed acyclic graph G = (V, E) and two vertices a, b ∈ V, returns the number of simple paths from a to b in G. For example, the directed acyclic graph of Figure 20.8 contains exactly four simple paths from vertex p to vertex v: ⟨p, o, v⟩, ⟨p, o, r, y, v⟩, ⟨p, o, s, r, y, v⟩, and ⟨p, s, r, y, v⟩. Your algorithm needs only to count the simple paths, not list them.

# *20.4-3*

Give an algorithm that determines whether an undirected graph G = (V, E) contains a simple cycle. Your algorithm should run in O(V) time, independent of |E|.

#### *20.4-4*

Prove or disprove: If a directed graph G contains cycles, then the vertex ordering produced by TOPOLOGICAL-SORT(G) minimizes the number of "bad" edges that are inconsistent with the ordering produced.

# *20.4-5*

Another way to topologically sort a directed acyclic graph G = (V, E) is to repeatedly find a vertex of in-degree 0, output it, and remove it and all of its outgoing edges from the graph. Explain how to implement this idea so that it runs in time O(V + E). What happens to this algorithm if G has cycles?

# **20.5 Strongly connected components**

We now consider a classic application of depth-first search: decomposing a directed graph into its strongly connected components. This section shows how to do so using two depth-first searches. Many algorithms that work with directed graphs begin with such a decomposition. After decomposing the graph into strongly connected components, such algorithms run separately on each one and then combine the solutions according to the structure of connections among components.

Recall from Appendix B that a strongly connected component of a directed graph G = (V, E) is a maximal set of vertices C ⊆ V such that for every pair of vertices u, v ∈ C, both u ❀ v and v ❀ u, that is, vertices u and v are reachable from each other. Figure 20.9 shows an example.

The algorithm for finding the strongly connected components of a directed graph G = (V, E) uses the transpose of G, which we defined in Exercise 20.1-3 to be the graph G^T = (V, E^T), where E^T = {(u, v) : (v, u) ∈ E}. That is, E^T consists of the edges of G with their directions reversed. Given an adjacency-list representation of G, the time to create G^T is Θ(V + E). The graphs G and G^T have exactly the same strongly connected components: u and v are reachable from each other in G if and only if they are reachable from each other in G^T. Figure 20.9(b) shows the transpose of the graph in Figure 20.9(a), with the strongly connected components shaded blue in both parts.

The linear-time (i.e., Θ(V + E)-time) procedure STRONGLY-CONNECTED-COMPONENTS on the next page computes the strongly connected components of a directed graph G = (V, E) using two depth-first searches, one on G and one on G^T.

The idea behind this algorithm comes from a key property of the *component graph* G_SCC = (V_SCC, E_SCC), defined as follows. Suppose that G has strongly connected components C₁, C₂, ..., Cₖ. The vertex set V_SCC is {v₁, v₂, ..., vₖ}, and it contains one vertex vᵢ for each strongly connected component Cᵢ of G. There is an edge (vᵢ, vⱼ) ∈ E_SCC if G contains a directed edge (x, y) for some x ∈ Cᵢ and some y ∈ Cⱼ. Looked at another way, if we contract all edges whose incident vertices are within the same strongly connected component of G so that