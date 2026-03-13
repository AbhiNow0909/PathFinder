---
topic: bellman_ford
pages: 634-637
---

**Figure 22.4** The execution of the Bellman-Ford algorithm. The source is vertex s. The d values appear within the vertices, and blue edges indicate predecessor values: if edge (u, v) is blue, then v.π = u. In this particular example, each pass relaxes the edges in the order (t, x); (t, y); (t, z); (x, t); (y, x); (y, z); (z, x); (z, s); (s, t); (s, y). **(a)** The situation just before the first pass over the edges. **(b)–(e)** The situation after each successive pass over the edges. Vertices whose shortest-path estimates and predecessors have changed due to a pass are highlighted in orange. The d and π values in part (e) are the final values. The Bellman-Ford algorithm returns TRUE in this example.

The Bellman-Ford algorithm runs in O(V² + VE) time when the graph is represented by adjacency lists, since the initialization in line 1 takes Θ(V) time, each of the |V| - 1 passes over the edges in lines 2–4 takes Θ(V + E) time (examining |V| adjacency lists to find the |E| edges), and the **for** loop of lines 5–7 takes O(V + E) time. Fewer than |V| - 1 passes over the edges sometimes suffice (see Exercise 22.1-3), which is why we say O(V² + VE) time, rather than Θ(V² + VE) time. In the frequent case where |E| = Ω(V), we can express this running time as O(VE). Exercise 22.1-5 asks you to make the Bellman-Ford algorithm run in O(VE) time even when |E| = o(V).

To prove the correctness of the Bellman-Ford algorithm, we start by showing that if there are no negative-weight cycles, the algorithm computes correct shortest-path weights for all vertices reachable from the source.

## *Lemma 22.2*

Let G = (V, E) be a weighted, directed graph with source vertex s and weight function w: E → R, and assume that G contains no negative-weight cycles that are reachable from s. Then, after the |V| - 1 iterations of the **for** loop of lines 2–4 of BELLMAN-FORD, v.d = δ(s, v) for all vertices v that are reachable from s.

*Proof* We prove the lemma by appealing to the path-relaxation property. Consider any vertex v that is reachable from s, and let p = ⟨v₀, v₁, ..., vₖ⟩, where v₀ = s and vₖ = v, be any shortest path from s to v. Because shortest paths are simple, p has at most |V| - 1 edges, and so k ≤ |V| - 1. Each of the |V| - 1 iterations of the **for** loop of lines 2–4 relaxes all |E| edges. Among the edges relaxed in the ith iteration, for i = 1, 2, ..., k, is (v_{i-1}, v_i). By the path-relaxation property, therefore, v.d = vₖ.d = δ(s, vₖ) = δ(s, v).

## *Corollary 22.3*

Let G = (V, E) be a weighted, directed graph with source vertex s and weight function w: E → R. Then, for each vertex v ∈ V, there is a path from s to v if and only if BELLMAN-FORD terminates with v.d < ∞ when it is run on G.

*Proof* The proof is left as Exercise 22.1-2.

## *Theorem 22.4 (Correctness of the Bellman-Ford algorithm)*

Let BELLMAN-FORD be run on a weighted, directed graph G = (V, E) with source vertex s and weight function w: E → R. If G contains no negative-weight cycles that are reachable from s, then the algorithm returns TRUE, v.d = δ(s, v) for all vertices v ∈ V, and the predecessor subgraph Gπ is a shortest-paths tree rooted at s. If G does contain a negative-weight cycle reachable from s, then the algorithm returns FALSE.

*Proof* Suppose that graph G contains no negative-weight cycles that are reachable from the source s. We first prove the claim that at termination, v.d = δ(s, v) for all vertices v ∈ V. If vertex v is reachable from s, then Lemma 22.2 proves this claim. If v is not reachable from s, then the claim follows from the no-path property. Thus, the claim is proven. The predecessor-subgraph property, along with the claim, implies that Gπ is a shortest-paths tree. Now we use the claim to show that BELLMAN-FORD returns TRUE. At termination, for all edges (u, v) ∈ E we have

```
v.d = δ(s, v)
    ≤ δ(s, u) + w(u, v) (by the triangle inequality)
    = u.d + w(u, v) ,
```

and so none of the tests in line 6 causes BELLMAN-FORD to return FALSE. Therefore, it returns TRUE.

Now, suppose that graph G contains a negative-weight cycle reachable from the source s. Let this cycle be c = ⟨v₀, v₁, ..., vₖ⟩, where v₀ = vₖ, in which case we have

$$\sum_{i=1}^{k} w(v_{i-1}, v_i) < 0.$$
(22.1)

Assume for the purpose of contradiction that the Bellman-Ford algorithm returns TRUE. Thus, vᵢ.d ≤ vᵢ₋₁.d + w(vᵢ₋₁, vᵢ) for i = 1, 2, ..., k. Summing the inequalities around cycle c gives

$$\sum_{i=1}^{k} v_i \cdot d \leq \sum_{i=1}^{k} (v_{i-1} \cdot d + w(v_{i-1}, v_i))$$

$$= \sum_{i=1}^{k} v_{i-1} \cdot d + \sum_{i=1}^{k} w(v_{i-1}, v_i).$$

Since v₀ = vₖ, each vertex in c appears exactly once in each of the summations Σᵏᵢ₌₁ vᵢ.d and Σᵏᵢ₌₁ vᵢ₋₁.d, and so

$$\sum_{i=1}^{k} v_i.d = \sum_{i=1}^{k} v_{i-1}.d.$$

Moreover, by Corollary 22.3, vᵢ.d is finite for i = 1, 2, ..., k. Thus,

$$0 \le \sum_{i=1}^k w(v_{i-1}, v_i) ,$$

which contradicts inequality (22.1). We conclude that the Bellman-Ford algorithm returns TRUE if graph G contains no negative-weight cycles reachable from the source, and FALSE otherwise.

#### **Exercises**

#### *22.1-1*

Run the Bellman-Ford algorithm on the directed graph of Figure 22.4, using vertex z as the source. In each pass, relax edges in the same order as in the figure, and show the d and π values after each pass. Now, change the weight of edge (z, x) to 4 and run the algorithm again, using s as the source.

#### *22.1-2*

Prove Corollary 22.3.

## *22.1-3*

Given a weighted, directed graph G = (V, E) with no negative-weight cycles, let m be the maximum over all vertices v ∈ V of the minimum number of edges in a shortest path from the source s to v. (Here, the shortest path is by weight, not the number of edges.) Suggest a simple change to the Bellman-Ford algorithm that allows it to terminate in m + 1 passes, even if m is not known in advance.

### *22.1-4*

Modify the Bellman-Ford algorithm so that it sets v.d to -∞ for all vertices v for which there is a negative-weight cycle on some path from the source to v.

## *22.1-5*

Suppose that the graph given as input to the Bellman-Ford algorithm is represented with a list of |E| edges, where each edge indicates the vertices it leaves and enters, along with its weight. Argue that the Bellman-Ford algorithm runs in O(VE) time without the constraint that |E| = Ω(V). Modify the Bellman-Ford algorithm so that it runs in O(VE) time in all cases when the input graph is represented with adjacency lists.

## *22.1-6*

Let G = (V, E) be a weighted, directed graph with weight function w: E → R. Give an O(VE)-time algorithm to find, for all vertices v ∈ V, the value δ*(v) = min{δ(u, v): u ∈ V}.

## *22.1-7*

Suppose that a weighted, directed graph G = (V, E) contains a negative-weight cycle. Give an efficient algorithm to list the vertices of one such cycle. Prove that your algorithm is correct.

## **22.2 Single-source shortest paths in directed acyclic graphs**

In this section, we introduce one further restriction on weighted, directed graphs: they are acyclic. That is, we are concerned with weighted dags. Shortest paths are always well defined in a dag, since even if there are negative-weight edges, no negative-weight cycles can exist. We'll see that if the edges of a weighted dag G = (V, E) are relaxed according to a topological sort of its vertices, it takes only Θ(V + E) time to compute shortest paths from a single source.

The algorithm starts by topologically sorting the dag (see Section 20.4) to impose a linear ordering on the vertices. If the dag contains a path from vertex u to vertex v, then u precedes v in the topological sort. The DAG-SHORTEST-PATHS