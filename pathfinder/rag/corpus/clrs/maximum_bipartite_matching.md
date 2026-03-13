---
topic: maximum_bipartite_matching
pages: 715-725
---

**Figure 24.8** A bipartite graph G = (V, E) with vertex partition V = L ∪ R. **(a)** A matching with cardinality 2, indicated by blue edges. **(b)** A maximum matching with cardinality 3. **(c)** The corresponding flow network G' with a maximum flow shown. Each edge has unit capacity. Blue edges have a flow of 1, and all other edges carry no flow. The blue edges from L to R correspond to those in the maximum matching from (b).

a particular machine u ∈ L is capable of performing a particular task v ∈ R. A maximum matching provides work for as many machines as possible.

#### **Finding a maximum bipartite matching**

The Ford-Fulkerson method provides a basis for finding a maximum matching in an undirected bipartite graph G = (V, E) in time polynomial in |V| and |E|. The trick is to construct a flow network in which flows correspond to matchings, as shown in Figure 24.8(c). We define the *corresponding flow network* G' = (V', E') for the bipartite graph G as follows. Let the source s and sink t be new vertices not in V, and let V' = V ∪ {s, t}. If the vertex partition of G is V = L ∪ R, the directed edges of G' are the edges of E, directed from L to R, along with |V| new directed edges:

$$E' = \{(s, u) : u \in L\}$$

$$\cup \{(u, v) : u \in L, v \in R, \text{ and } (u, v) \in E\}$$

$$\cup \{(v, t) : v \in R\}.$$

To complete the construction, assign unit capacity to each edge in E'. Since each vertex in V has at least one incident edge, |E| ≥ |V|/2. Thus, |E| ≤ |E'| = |E| + |V| ≤ 3|E|, and so |E'| = Θ(E).

The following lemma shows that a matching in G corresponds directly to a flow in G's corresponding flow network G'. We say that a flow f on a flow network G = (V, E) is *integer-valued* if f(u, v) is an integer for all (u, v) ∈ V × V.

#### *Lemma 24.9*

Let G = (V, E) be a bipartite graph with vertex partition V = L ∪ R, and let G' = (V', E') be its corresponding flow network. If M is a matching in G, then there is an integer-valued flow f in G' with value |f| = |M|. Conversely, if f is an integer-valued flow in G', then there is a matching M in G with cardinality |M| = |f| consisting of edges (u, v) ∈ E such that f(u, v) > 0.

*Proof* We first show that a matching M in G corresponds to an integer-valued flow f in G'. Define f as follows. If (u, v) ∈ M, then f(s, u) = f(u, v) = f(v, t) = 1. For all other edges (u, v) ∈ E', define f(u, v) = 0. It is simple to verify that f satisfies the capacity constraint and flow conservation.

Intuitively, each edge (u, v) ∈ M corresponds to 1 unit of flow in G' that traverses the path s → u → v → t. Moreover, the paths induced by edges in M are vertex-disjoint, except for s and t. The net flow across cut (L ∪ {s}, R ∪ {t}) is equal to |M|, and thus, by Lemma 24.4, the value of the flow is |f| = |M|.

To prove the converse, let f be an integer-valued flow in G' and, as in the statement of the lemma, let

$$M = \{(u, v) : u \in L, v \in R, \text{ and } f(u, v) > 0\}$$
.

Each vertex u ∈ L has only one entering edge, namely (s, u), and its capacity is 1. Thus, each u ∈ L has at most 1 unit of flow entering it, and if 1 unit of flow does enter, by flow conservation, 1 unit of flow must leave. Furthermore, since the flow f is integer-valued, for each u ∈ L, the 1 unit of flow can enter on at most one edge and can leave on at most one edge. Thus, 1 unit of flow enters u if and only if there is exactly one vertex v ∈ R such that f(u, v) = 1, and at most one edge leaving each u ∈ L carries positive flow. A symmetric argument applies to each v ∈ R. The set M is therefore a matching.

To see that |M| = |f|, observe that of the edges (u, v) ∈ E' such that u ∈ L and v ∈ R,

$$f(u,v) = \begin{cases} 1 & \text{if } (u,v) \in M, \\ 0 & \text{if } (u,v) \notin M. \end{cases}$$

Consequently, f(L ∪ {s}, R ∪ {t}), the net flow across cut (L ∪ {s}, R ∪ {t}), is equal to |M|. Lemma 24.4 gives that |f| = f(L ∪ {s}, R ∪ {t}) = |M|.

Based on Lemma 24.9, we would like to conclude that a maximum matching in a bipartite graph G corresponds to a maximum flow in its corresponding flow network G', and therefore running a maximum-flow algorithm on G' provides a maximum matching in G. The only hitch in this reasoning is that the maximum-flow algorithm might return a flow in G' for which some f(u, v) is not an integer, even though the flow value |f| must be an integer. The following theorem shows that the Ford-Fulkerson method cannot produce a solution with this problem.

## *Theorem 24.10 (Integrality theorem)*

If the capacity function c takes on only integer values, then the maximum flow f produced by the Ford-Fulkerson method has the property that |f| is an integer. Moreover, for all vertices u and v, the value of f(u, v) is an integer.

*Proof* Exercise 24.3-2 asks you to provide the proof by induction on the number of iterations.

We can now prove the following corollary to Lemma 24.9.

## *Corollary 24.11*

The cardinality of a maximum matching M in a bipartite graph G equals the value of a maximum flow f in its corresponding flow network G'.

*Proof* We use the nomenclature from Lemma 24.9. Suppose that M is a maximum matching in G and that the corresponding flow f in G' is not maximum. Then there is a maximum flow f' in G' such that |f'| > |f|. Since the capacities in G' are integer-valued, by Theorem 24.10, we can assume that f' is integer-valued. Thus, f' corresponds to a matching M' in G with cardinality |M'| = |f'| > |f| = |M|, contradicting our assumption that M is a maximum matching. In a similar manner, we can show that if f is a maximum flow in G', its corresponding matching is a maximum matching on G.

Thus, to find a maximum matching in a bipartite undirected graph G, create the flow network G', run the Ford-Fulkerson method on G', and convert the integer-valued maximum flow found into a maximum matching for G. Since any matching in a bipartite graph has cardinality at most min{|L|, |R|} = O(V), the value of the maximum flow in G' is O(V). Therefore, finding a maximum matching in a bipartite graph takes O(VE') = O(VE) time, since |E'| = Θ(E).

#### **Exercises**

#### *24.3-1*

Run the Ford-Fulkerson algorithm on the flow network in Figure 24.8(c) and show the residual network after each flow augmentation. Number the vertices in L top to bottom from 1 to 5 and in R top to bottom from 6 to 9. For each iteration, pick the augmenting path that is lexicographically smallest.

## *24.3-2*

Prove Theorem 24.10. Use induction on the number of iterations of the Ford-Fulkerson method.

## *24.3-3*

Let G = (V, E) be a bipartite graph with vertex partition V = L ∪ R, and let G' be its corresponding flow network. Give a good upper bound on the length of any augmenting path found in G' during the execution of FORD-FULKERSON.

## **Problems**

#### *24-1 Escape problem*

An n×n *grid* is an undirected graph consisting of n rows and n columns of vertices, as shown in Figure 24.9. We denote the vertex in the ith row and the jth column by (i, j). All vertices in a grid have exactly four neighbors, except for the boundary vertices, which are the points (i, j) for which i = 1, i = n, j = 1, or j = n.

Given m ≤ n² starting points (x₁, y₁), (x₂, y₂), ..., (xₘ, yₘ) in the grid, the *escape problem* is to determine whether there are m vertex-disjoint paths from the starting points to any m different points on the boundary. For example, the grid in Figure 24.9(a) has an escape, but the grid in Figure 24.9(b) does not.

**Figure 24.9** Grids for the escape problem. Starting points are blue, and other grid vertices are tan. **(a)** A grid with an escape, shown by blue paths. **(b)** A grid with no escape.

- *a.* Consider a flow network in which vertices, as well as edges, have capacities. That is, the total positive flow entering any given vertex is subject to a capacity constraint. Show how to reduce the problem of determining the maximum flow in a network with edge and vertex capacities to an ordinary maximum-flow problem on a flow network of comparable size.
- *b.* Describe an efficient algorithm to solve the escape problem, and analyze its running time.

#### *24-2 Minimum path cover*

A *path cover* of a directed graph G = (V, E) is a set P of vertex-disjoint paths such that every vertex in V is included in exactly one path in P. Paths may start and end anywhere, and they may be of any length, including 0. A *minimum path cover* of G is a path cover containing the fewest possible paths.

*a.* Give an efficient algorithm to find a minimum path cover of a directed acyclic graph G = (V, E). (*Hint:* Assuming that V = {1, 2, ..., n}, construct a flow network based on the graph G' = (V', E'), where

```
V' = {x₀, x₁, ..., xₙ} ∪ {y₀, y₁, ..., yₙ},
E' = {(x₀, xᵢ) : i ∈ V} ∪ {(yᵢ, y₀) : i ∈ V} ∪ {(xᵢ, yⱼ) : (i, j) ∈ E},
and run a maximum-flow algorithm.)
```

*b.* Does your algorithm work for directed graphs that contain cycles? Explain.

#### *24-3 Hiring consulting experts*

Professor Fieri wants to open a consulting company for the food industry. He has identified n important food categories, which he represents by the set C = {C₁, C₂, ..., Cₙ}. In each category Cₖ, he can hire an expert in that category for eₖ > 0 dollars. The consulting company has lined up a set J = {J₁, J₂, ..., Jₘ} of potential jobs. In order to perform job Jᵢ, the company needs to have hired experts in a subset Rᵢ ⊆ C of categories. Each expert can work on multiple jobs simultaneously. If the company chooses to accept job Jᵢ, it must have hired experts in all categories in Rᵢ, and it takes in revenue of pᵢ > 0 dollars.

Professor Fieri's job is to determine which categories to hire experts in and which jobs to accept in order to maximize the net revenue, which is the total income from jobs accepted minus the total cost of employing the experts.

Consider the following flow network G. It contains a source vertex s, vertices C₁, C₂, ..., Cₙ, vertices J₁, J₂, ..., Jₘ, and a sink vertex t. For k = 1, 2, ..., n, the flow network contains an edge (s, Cₖ) with capacity c(s, Cₖ) = eₖ, and for i = 1, 2, ..., m, the flow network contains an edge (Jᵢ, t) with capacity 

c(Jᵢ, t) = pᵢ. For k = 1, 2, ..., n and i = 1, 2, ..., m, if Cₖ ∈ Rᵢ, then G contains an edge (Cₖ, Jᵢ) with capacity c(Cₖ, Jᵢ) = 1.

- *a.* Show that if Jᵢ ∈ T for a finite-capacity cut (S, T) of G, then Cₖ ∈ T for each Cₖ ∈ Rᵢ.
- *b.* Show how to determine the maximum net revenue from the capacity of a minimum cut of G and the given pᵢ values.
- *c.* Give an efficient algorithm to determine which jobs to accept and which experts to hire. Analyze the running time of your algorithm in terms of m, n, and r = ∑ᵐᵢ₌₁ |Rᵢ|.

#### *24-4 Updating maximum flow*

Let G = (V, E) be a flow network with source s, sink t, and integer capacities. Suppose that you are given a maximum flow in G.

- *a.* Suppose that the capacity of a single edge (u, v) ∈ E increases by 1. Give an O(V + E)-time algorithm to update the maximum flow.
- *b.* Suppose that the capacity of a single edge (u, v) ∈ E decreases by 1. Give an O(V + E)-time algorithm to update the maximum flow.

#### *24-5 Maximum flow by scaling*

Let G = (V, E) be a flow network with source s, sink t, and an integer capacity c(u, v) on each edge (u, v) ∈ E. Let C = max{c(u, v) : (u, v) ∈ E}.

- *a.* Argue that a minimum cut of G has capacity at most C|E|.
- *b.* For a given number K, show how to find an augmenting path of capacity at least K in O(E) time, if such a path exists.

The procedure MAX-FLOW-BY-SCALING appearing on the following page modifies the basic FORD-FULKERSON-METHOD procedure to compute a maximum flow in G.

- *c.* Argue that MAX-FLOW-BY-SCALING returns a maximum flow.
- *d.* Show that the capacity of a minimum cut of the residual network Gf is less than 2K|E| each time line 4 executes.
- *e.* Argue that the inner **while** loop of lines 5-6 executes O(E) times for each value of K.

```
MAX-FLOW-BY-SCALING(G, s, t)
1 C = max{c(u, v) : (u, v) ∈ E}
2 initialize flow f to 0
3 K = 2^⌊lg C⌋
4 while K ≥ 1
5 while there exists an augmenting path p of capacity at least K
6 augment flow f along p
7 K = K/2
8 return f
```

*f.* Conclude that MAX-FLOW-BY-SCALING can be implemented so that it runs in O(E² lg C) time.

## *24-6 Widest augmenting path*

The Edmonds-Karp algorithm implements the Ford-Fulkerson algorithm by always choosing a shortest augmenting path in the residual network. Suppose instead that the Ford-Fulkerson algorithm chooses a *widest augmenting path*: an augmenting path with the greatest residual capacity. Assume that G = (V, E) is a flow network with source s and sink t, that all capacities are integer, and that the largest capacity is C. In this problem, you will show that choosing a widest augmenting path results in at most |E| ln |f*| augmentations to find a maximum flow f*.

- *a.* Show how to adjust Dijkstra's algorithm to find the widest augmenting path in the residual network.
- *b.* Show that a maximum flow in G can be formed by successive flow augmentations along at most |E| paths from s to t.
- *c.* Given a flow f, argue that the residual network Gf has an augmenting path p with residual capacity cf(p) ≥ (|f*| - |f|)/|E|.
- *d.* Assuming that each augmenting path is a widest augmenting path, let fᵢ be the flow after augmenting the flow by the ith augmenting path, where f₀ has f(u, v) = 0 for all edges (u, v). Show that |f*| - |fᵢ| ≤ |f*|(1 - 1/|E|)ⁱ.
- *e.* Show that |f*| - |fᵢ| < |f*|e^(-i/|E|).
- *f.* Conclude that after the flow is augmented at most |E| ln |f*| times, the flow is a maximum flow.

## *24-7 Global minimum cut*

A *global cut* in an undirected graph G = (V, E) is a partition (see page 1156) of V into two nonempty sets V₁ and V₂. This definition is like the definition of cut that we have used in this chapter, except that we no longer have distinguished vertices s and t. Any edge (u, v) with u ∈ V₁ and v ∈ V₂ is said to *cross* the cut.

We can extend this definition of a cut to a multigraph G = (V, E) (see page 1167), and we denote by c(u, v) the number of edges in the multigraph with endpoints u and v. A global cut in a multigraph is still a partition of the vertices, and the value of a global cut (V₁, V₂) is c(V₁, V₂) = ∑_{u∈V₁, v∈V₂} c(u, v). A solution to the *global-minimum-cut problem* is a cut (V₁, V₂) such that c(V₁, V₂) is minimum. Let λ(G) denote the value of a global minimum cut in a graph or multigraph G.

- *a.* Show how to find a global minimum cut of a graph G = (V, E) by solving (|V| choose 2) maximum-flow problems, each with a different pair of vertices as the source and sink, and taking the minimum value of the cuts found.
- *b.* Give an algorithm to find a global minimum cut by solving only Θ(V) maximum-flow problems. What is the running time of your algorithm?

The remainder of this problem develops an algorithm for the global-minimum-cut problem that does not use any maximum-flow computations. It uses the notion of an edge contraction, defined on page 1168, with one crucial difference. The algorithm maintains a multigraph, so that upon contracting an edge (u, v), it creates a new vertex x, and for any other vertex y ∈ V, the number of edges between x and y is c(u, y) + c(v, y). The algorithm does not maintain self-loops, and so it sets c(x, x) to 0. Denote by G/(u, v) the multigraph that results from contracting edge (u, v) in multigraph G.

Consider what can happen to the minimum cut when an edge is contracted. Assume that, at all points, the minimum cut in a multigraph G is unique. We'll remove this assumption later.

*c.* Show that for any edge (u, v), we have λ(G/(u,v)) ≤ λ(G). Under what conditions is λ(G/(u,v)) < λ(G)?

Next, you will show that if you pick an edge uniformly at random, the probability that it belongs to the minimum cut is small.

*d.* Show that for any multigraph G = (V, E), the value of the global minimum cut is at most the average degree of a vertex: that λ(G) ≤ 2|E|/|V|, where |E| denotes the total number of edges in the multigraph.

*e.* Using the results from parts (c) and (d), show that, if we pick an edge (u, v) uniformly at random, then the probability that (u, v) belongs to the minimum cut is at most 2/|V|.

Consider the algorithm that repeatedly chooses an edge at random and contracts it until the multigraph has exactly two vertices, say u and v. At that point, the multigraph corresponds to a cut in the original graph, with vertex u representing all the nodes in one side of the original graph, and v representing all the vertices on the other side. The number of edges given by c(u, v) corresponds exactly to the number of edges crossing the corresponding cut in the original graph. We call this algorithm the *contraction algorithm*.

- *f.* Suppose that the contraction algorithm terminates with a multigraph whose only vertices are u and v. Show that Pr{c(u, v) = λ(G)} ≥ 1/(|V| choose 2).
- *g.* Prove that if the contraction algorithm repeats (|V| choose 2) ln |V| times, then the probability that at least one of the runs returns the minimum cut is at least 1 - 1/|V|.
- *h.* Give a detailed implementation of the contraction algorithm that runs in O(V²) time.
- *i.* Combine the previous parts and remove the assumption that the minimum cut must be unique, to conclude that running the contraction algorithm (|V| choose 2) ln |V| times yields an algorithm that runs in O(V⁴ lg V) time and returns a minimum cut with probability at least 1 - 1/|V|.

## **Chapter notes**

Ahuja, Magnanti, and Orlin [7], Even [137], Lawler [276], Papadimitriou and Steiglitz [353], Tarjan [429], and Williamson [458] are good references for network flows and related algorithms. Schrijver [399] has written an interesting review of historical developments in the field of network flows.

The Ford-Fulkerson method is due to Ford and Fulkerson [149], who originated the formal study of many of the problems in the area of network flow, including the maximum-flow and bipartite-matching problems. Many early implementations of the Ford-Fulkerson method found augmenting paths using breadth-first search. Edmonds and Karp [132], and independently Dinic [119], proved that this strategy yields a polynomial-time algorithm. A related idea, that of using "blocking flows," was also first developed by Dinic [119].

A class of algorithms known as *push-relabel algorithms*, due to Goldberg [185] and Goldberg and Tarjan [188], takes a different approach from the Ford-Fulkerson method. Push-relabel algorithms allow flow conservation to be violated at vertices other than the source and sink as they execute. Using an idea first developed by Karzonov [251], they allow a *preflow* in which the flow into a vertex may exceed the flow out of the vertex. Such a vertex is said to be *overflowing*. Initially, every edge leaving the source is filled to capacity, so that all neighbors of the source are overflowing. In a push-relabel algorithm, each vertex is assigned an integer height. An overflowing vertex may push flow to a neighboring vertex to which it has a residual edge provided that it is higher than the neighbor. If all residual edges from an overflowing vertex go to neighbors with equal or greater heights, then the vertex may increase its height. Once all vertices other than the sink are no longer overflowing, the preflow is not only a legal flow, but also a maximum flow.

Goldberg and Tarjan [188] gave an O(V³)-time algorithm that uses a queue to maintain the set of overflowing vertices, as well as an algorithm that uses dynamic trees to achieve a running time of O(VE lg(V²/E + 2)). Several other researchers developed improved variants and implementations [9, 10, 15, 86, 87, 255, 358], the fastest of which, by King, Rao, and Tarjan [255], runs in O(VE log_{E/(V lg V)} V) time.

Another efficient algorithm for maximum flow, by Goldberg and Rao [187], runs in O(min{V^(2/3), E^(1/2)} E lg(V²/E + 2) lg C) time, where C is the maximum capacity of any edge. Orlin [350] gave an algorithm in the same spirit as this algorithm that runs in O(VE + E^(31/16) lg² V) time. Combining it with the algorithm of King, Rao, and Tarjan results in an O(VE)-time algorithm.

A different approach to maximum flows and related problems is to use techniques from continuous optimization including electrical flows and interior-point methods. The first breakthrough in this line of work is due to Madry [308], who gave an Õ(E^(10/7))-time algorithm for unit-capacity maximum flow and bipartite maximum matching. (See Problem 3-6 on page 73 for a definition of Õ.) There has been a series of papers in this area for matchings, maximum flows, and minimum-cost flows. The fastest algorithm to date in this line of work for maximum flow is due to Lee and Sidford [285], taking Õ(√V E lg^O(1) C) time. If the capacities are not too large, this algorithm is faster than the O(VE)-time algorithm mentioned above. Another algorithm, due to Liu and Sidford [303] runs in Õ(E^(11/8 + 1/4)) time, where C is the maximum capacity of any edge. This algorithm does not run in polynomial time, but for small enough capacities, it is faster than the previous ones.

In practice, push-relabel algorithms currently dominate algorithms based on augmenting paths, continuous-optimization, and linear programming for the maximum-flow problem [88].

# **25 Matchings in Bipartite Graphs**

Many real-world problems can be modeled as finding matchings in an undirected graph. For an undirected graph G = (V, E), a *matching* is a subset of edges M ⊆ E such that every vertex in V has at most one incident edge in M.

For example, consider the following scenario. You have one or more positions to fill and several candidates to interview. According to your schedule, you are able to interview candidates at certain time slots. You ask the candidates to indicate the subsets of time slots at which they are available. How can you schedule the interviews so that each time slot has at most one candidate scheduled, while maximizing the number of candidates that you can interview? You can model this scenario as a matching problem on a bipartite graph in which each vertex represents either a candidate or a time slot, with an edge between a candidate and a time slot if the candidate is available then. If an edge is included in the matching, that means you are scheduling a particular candidate for a particular time slot. Your goal is to find a *maximum matching*: a matching of maximum cardinality. One of the authors of this book was faced with exactly this situation when hiring teaching assistants for a large class. He used the Hopcroft-Karp algorithm in Section 25.1 to schedule the interviews.

Another application of matching is the U.S. National Resident Matching Program, in which medical students are matched to hospitals where they will be stationed as medical residents. Each student ranks the hospitals by preference, and each hospital ranks the students. The goal is to assign students to hospitals so that there is never a student and a hospital that both have regrets because the student was not assigned to the hospital, yet each ranked the other higher than who or where they were assigned. This scenario is perhaps the best-known real-world example of the "stable-marriage problem," which Section 25.2 examines.

Yet another instance where matching comes into play occurs when workers must be assigned to tasks in order to maximize the overall effectiveness of the assignment. For each worker and each task, the worker has some quantified effectiveness