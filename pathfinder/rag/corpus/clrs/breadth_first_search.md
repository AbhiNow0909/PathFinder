---
topic: breadth_first_search
pages: 576-584
---


Breadth-first search constructs a breadth-first tree, initially containing only its root, which is the source vertex s. Whenever the search discovers a white vertex v in the course of scanning the adjacency list of a gray vertex u, the vertex v and the edge (u, v) are added to the tree. We say that u is the *predecessor* or *parent* of v in the breadth-first tree. Since every vertex reachable from s is discovered at most once, each vertex reachable from s has exactly one parent. (There is one exception: because s is the root of the breadth-first tree, it has no parent.) Ancestor and descendant relationships in the breadth-first tree are defined relative to the root s as usual: if u is on the simple path in the tree from the root s to vertex v, then u is an ancestor of v and v is a descendant of u.

The breadth-first-search procedure BFS on the following page assumes that the graph G = (V, E) is represented using adjacency lists. It denotes the queue by Q, and it attaches three additional attributes to each vertex v in the graph:

- v.color is the color of v: WHITE, GRAY, or BLACK.
- v.d holds the distance from the source vertex s to v, as computed by the algorithm.
- v.π is v's predecessor in the breadth-first tree. If v has no predecessor because it is the source vertex or is undiscovered, then v.π = NIL.

Figure 20.3 illustrates the progress of BFS on an undirected graph.

The procedure BFS works as follows. With the exception of the source vertex s, lines 1–4 paint every vertex white, set u.d = ∞ for each vertex u, and set the parent of every vertex to be NIL. Because the source vertex s is always the first vertex discovered, lines 5–7 paint s gray, set s.d to 0, and set the predecessor of s to NIL. Lines 8–9 create the queue Q, initially containing just the source vertex.

The **while** loop of lines 10-18 iterates as long as there remain gray vertices, which are on the frontier: discovered vertices that have not yet had their adjacency lists fully examined. This **while** loop maintains the following invariant:

At the test in line 10, the queue Q consists of the set of gray vertices.

Although we won't use this loop invariant to prove correctness, it is easy to see that it holds prior to the first iteration and that each iteration of the loop maintains the invariant. Prior to the first iteration, the only gray vertex, and the only vertex

<sup>1</sup> We distinguish between gray and black vertices to help us understand how breadth-first search operates. In fact, as Exercise 20.2-3 shows, we get the same result even if we do not distinguish between gray and black vertices.

```
BFS(G, s)
1 for each vertex u ∈ G.V - {s}
2     u.color = WHITE
3     u.d = ∞
4     u.π = NIL
5 s.color = GRAY
6 s.d = 0
7 s.π = NIL
8 Q = ∅
9 ENQUEUE(Q, s)
10 while Q ≠ ∅
11     u = DEQUEUE(Q)
12     for each vertex v in G.Adj[u] // search the neighbors of u
13         if v.color == WHITE // is v being discovered now?
14             v.color = GRAY
15             v.d = u.d + 1
16             v.π = u
17             ENQUEUE(Q, v) // v is now on the frontier
18     u.color = BLACK // u is now behind the frontier
```

in Q, is the source vertex s. Line 11 determines the gray vertex u at the head of the queue Q and removes it from Q. The **for** loop of lines 12–17 considers each vertex v in the adjacency list of u. If v is white, then it has not yet been discovered, and the procedure discovers it by executing lines 14–17. These lines paint vertex v gray, set v's distance v.d to u.d + 1, record u as v's parent v.π, and place v at the tail of the queue Q. Once the procedure has examined all the vertices on u's adjacency list, it blackens u in line 18, indicating that u is now behind the frontier. The loop invariant is maintained because whenever a vertex is painted gray (in line 14) it is also enqueued (in line 17), and whenever a vertex is dequeued (in line 11) it is also painted black (in line 18).

The results of breadth-first search may depend upon the order in which the neighbors of a given vertex are visited in line 12: the breadth-first tree may vary, but the distances d computed by the algorithm do not. (See Exercise 20.2-5.)

A simple change allows the BFS procedure to terminate in many cases before the queue Q becomes empty. Because each vertex is discovered at most once and receives a finite d value only when it is discovered, the algorithm can terminate once every vertex has a finite d value. If BFS keeps count of how many vertices have been discovered, it can terminate once either the queue Q is empty or all |V| vertices are discovered.

**Figure 20.3** The operation of BFS on an undirected graph. Each part shows the graph and the queue Q at the beginning of each iteration of the **while** loop of lines 10–18. Vertex distances appear within each vertex and below vertices in the queue. The tan region surrounds the frontier of the search, consisting of the vertices in the queue. The light blue region surrounds the vertices behind the frontier, which have been dequeued. Each part highlights in orange the vertex dequeued and the breadth-first tree edges added, if any, in the previous iteration. Blue edges belong to the breadth-first tree constructed so far.

## **Analysis**

Before proving the various properties of breadth-first search, let's take on the easier job of analyzing its running time on an input graph G = (V, E). We use aggregate analysis, as we saw in Section 16.1. After initialization, breadth-first search never whitens a vertex, and thus the test in line 13 ensures that each vertex is enqueued at most once, and hence dequeued at most once. The operations of enqueuing and dequeuing take O(1) time, and so the total time devoted to queue operations is O(V). Because the procedure scans the adjacency list of each vertex only when the vertex is dequeued, it scans each adjacency list at most once. Since the sum of the lengths of all |V| adjacency lists is Θ(E), the total time spent in scanning adjacency lists is O(V + E). The overhead for initialization is O(V), and thus the total running time of the BFS procedure is O(V + E). Thus, breadth-first search runs in time linear in the size of the adjacency-list representation of G.

#### **Shortest paths**

Now, let's see why breadth-first search finds the shortest distance from a given source vertex s to each vertex in a graph. Define the *shortest-path distance* δ(s, v) from s to v as the minimum number of edges in any path from vertex s to vertex v. If there is no path from s to v, then δ(s, v) = ∞. We call a path of length δ(s, v) from s to v a *shortest path*² from s to v. Before showing that breadth-first search correctly computes shortest-path distances, we investigate an important property of shortest-path distances.

## *Lemma 20.1*

Let G = (V, E) be a directed or undirected graph, and let s ∈ V be an arbitrary vertex. Then, for any edge (u, v) ∈ E,

$$\delta(s, v) \le \delta(s, u) + 1.$$

*Proof* If u is reachable from s, then so is v. In this case, the shortest path from s to v cannot be longer than the shortest path from s to u followed by the edge (u, v), and thus the inequality holds. If u is not reachable from s, then δ(s, u) = ∞, and again, the inequality holds.

Our goal is to show that the BFS procedure properly computes v.d = δ(s, v) for each vertex v ∈ V. We first show that v.d bounds δ(s, v) from above.

² Chapters 22 and 23 generalize shortest paths to weighted graphs, in which every edge has a realvalued weight and the weight of a path is the sum of the weights of its constituent edges. The graphs considered in the present chapter are unweighted or, equivalently, all edges have unit weight.

## *Lemma 20.2*

Let G = (V, E) be a directed or undirected graph, and suppose that BFS is run on G from a given source vertex s ∈ V. Then, for each vertex v ∈ V, the value v.d computed by BFS satisfies v.d ≥ δ(s, v) at all times, including at termination.

*Proof* The lemma is true intuitively, because any finite value assigned to v.d equals the number of edges on some path from s to v. The formal proof is by induction on the number of ENQUEUE operations. The inductive hypothesis is that v.d ≥ δ(s, v) for all v ∈ V.

The base case of the induction is the situation immediately after enqueuing s in line 9 of BFS. The inductive hypothesis holds here, because s.d = 0 = δ(s, s) and v.d = ∞ ≥ δ(s, v) for all v ∈ V - {s}.

For the inductive step, consider a white vertex v that is discovered during the search from a vertex u. The inductive hypothesis implies that u.d ≥ δ(s, u). The assignment performed by line 15 and Lemma 20.1 give

```
v.d = u.d + 1
    ≥ δ(s, u) + 1
    ≥ δ(s, v).
```
```

Vertex v is then enqueued, and it is never enqueued again because it is also grayed and lines 14-17 execute only for white vertices. Thus, the value of v.d never changes again, and the inductive hypothesis is maintained.

To prove that v.d = δ(s, v), we first show more precisely how the queue Q operates during the course of BFS. The next lemma shows that at all times, the d values of vertices in the queue either are all the same or form a sequence ⟨k, k, ..., k, k + 1, k + 1, ..., k + 1⟩ for some integer k ≥ 0.

## *Lemma 20.3*

Suppose that during the execution of BFS on a graph G = (V, E), the queue Q contains the vertices ⟨v₁, v₂, ..., vᵣ⟩, where v₁ is the head of Q and vᵣ is the tail. Then, vᵣ.d ≤ v₁.d + 1 and vᵢ.d ≤ vᵢ₊₁.d for i = 1, 2, ..., r - 1.

*Proof* The proof is by induction on the number of queue operations. Initially, when the queue contains only s, the lemma trivially holds.

For the inductive step, we must prove that the lemma holds after both dequeuing and enqueuing a vertex. First, we examine dequeuing. When the head v₁ of the queue is dequeued, v₂ becomes the new head. (If the queue becomes empty, then the lemma holds vacuously.) By the inductive hypothesis, v₁.d ≤ v₂.d. But then we have vᵣ.d ≤ v₁.d + 1 ≤ v₂.d + 1, and the remaining inequalities are unaffected. Thus, the lemma follows with v₂ as the new head.

Now, we examine enqueuing. When line 17 of BFS enqueues a vertex v onto a queue containing vertices ⟨v₁, v₂, ..., vᵣ⟩, the enqueued vertex becomes vᵣ₊₁. If the queue was empty before v was enqueued, then after enqueuing v, we have r = 1 and the lemma trivially holds. Now suppose that the queue was nonempty when v was enqueued. At that time, the procedure has most recently removed vertex u, whose adjacency list is currently being scanned, from the queue Q. Just before u was removed, we had u = v₁ and the inductive hypothesis held, so that u.d ≤ v₂.d and vᵣ.d ≤ u.d + 1. After u is removed from the queue, the vertex that had been v₂ becomes the new head v₁ of the queue, so that now u.d ≤ v₁.d. Thus, vᵣ₊₁.d = v.d = u.d + 1 ≤ v₁.d + 1. Since vᵣ.d ≤ u.d + 1, we have vᵣ.d ≤ u.d + 1 = v.d = vᵣ₊₁.d, and the remaining inequalities are unaffected. Thus, the lemma follows when v is enqueued.

The following corollary shows that the d values at the time that vertices are enqueued monotonically increase over time.

### *Corollary 20.4*

Suppose that vertices vᵢ and vⱼ are enqueued during the execution of BFS, and that vᵢ is enqueued before vⱼ. Then vᵢ.d ≤ vⱼ.d at the time that vⱼ is enqueued.

*Proof* Immediate from Lemma 20.3 and the property that each vertex receives a finite d value at most once during the course of BFS.

We can now prove that breadth-first search correctly finds shortest-path distances.

#### *Theorem 20.5 (Correctness of breadth-first search)*

Let G = (V, E) be a directed or undirected graph, and suppose that BFS is run on G from a given source vertex s ∈ V. Then, during its execution, BFS discovers every vertex v ∈ V that is reachable from the source s, and upon termination, v.d = δ(s, v) for all v ∈ V. Moreover, for any vertex v ≠ s that is reachable from s, one of the shortest paths from s to v is a shortest path from s to v.π followed by the edge (v.π, v).

*Proof* Assume for the purpose of contradiction that some vertex receives a d value not equal to its shortest-path distance. Of all such vertices, let v be a vertex that has the minimum δ(s, v). By Lemma 20.2, we have v.d ≥ δ(s, v), and thus v.d > δ(s, v). We cannot have v = s, because s.d = 0 and δ(s, s) = 0. Vertex v must be reachable from s, for otherwise we would have δ(s, v) = ∞ ≥ v.d. Let u be the vertex immediately preceding v on some shortest path from s to v (since v ≠ s, vertex u must exist), so that δ(s, v) = δ(s, u) + 1. Because δ(s, u) < δ(s, v), and because of how we chose v, we have u.d = δ(s, u). Putting these properties together gives

$$v.d > \delta(s, v) = \delta(s, u) + 1 = u.d + 1.$$
(20.1)

Now consider the time when BFS chooses to dequeue vertex u from Q in line 11. At this time, vertex v is either white, gray, or black. We shall show that each of these cases leads to a contradiction of inequality (20.1). If v is white, then line 15 sets v.d = u.d + 1, contradicting inequality (20.1). If v is black, then it was already removed from the queue and, by Corollary 20.4, we have v.d ≤ u.d, again contradicting inequality (20.1). If v is gray, then it was painted gray upon dequeuing some vertex w, which was removed from Q earlier than u and for which v.d = w.d + 1. By Corollary 20.4, however, w.d ≤ u.d, and so v.d = w.d + 1 ≤ u.d + 1, once again contradicting inequality (20.1).

Thus we conclude that v.d = δ(s, v) for all v ∈ V. All vertices v reachable from s must be discovered, for otherwise they would have ∞ = v.d > δ(s, v). To conclude the proof of the theorem, observe from lines 15-16 that if v.π = u, then v.d = u.d + 1. Thus, to form a shortest path from s to v, take a shortest path from s to v.π and then traverse the edge (v.π, v).

#### **Breadth-first trees**

The blue edges in Figure 20.3 show the breadth-first tree built by the BFS procedure as it searches the graph. The tree corresponds to the π attributes. More formally, for a graph G = (V, E) with source s, we define the *predecessor subgraph* of G as Gπ = (Vπ, Eπ), where

$$V_{\pi} = \{ v \in V : v.\pi \neq \text{NIL} \} \cup \{ s \}$$
 (20.2)

and

$$E_{\pi} = \{ (v.\pi, v) : v \in V_{\pi} - \{s\} \} . \tag{20.3}$$

The predecessor subgraph Gπ is a *breadth-first tree* if Vπ consists of the vertices reachable from s and, for all v ∈ Vπ, the subgraph Gπ contains a unique simple path from s to v that is also a shortest path from s to v in G. A breadth-first tree is in fact a tree, since it is connected and |Eπ| = |Vπ| - 1 (see Theorem B.2 on page 1169). We call the edges in Eπ *tree edges*.

The following lemma shows that the predecessor subgraph produced by the BFS procedure is a breadth-first tree.

#### *Lemma 20.6*

When applied to a directed or undirected graph G = (V, E), procedure BFS constructs π so that the predecessor subgraph Gπ = (Vπ, Eπ) is a breadth-first tree.

*Proof* Line 16 of BFS sets v.π = u if and only if (u, v) ∈ E and δ(s, v) < ∞—that is, if v is reachable from s—and thus Vπ consists of the vertices in V reachable from s. Since the predecessor subgraph Gπ forms a tree, by Theorem B.2, it contains a unique simple path from s to each vertex in Vπ. Applying Theorem 20.5 inductively yields that every such path is a shortest path in G.

The PRINT-PATH procedure prints out the vertices on a shortest path from s to v, assuming that BFS has already computed a breadth-first tree. This procedure runs in time linear in the number of vertices in the path printed, since each recursive call is for a path one vertex shorter.

```
PRINT-PATH(G, s, v)
1 if v == s
2     print s
3 elseif v.π == NIL 
4     print "no path from" s "to" v "exists" 
5 else PRINT-PATH(G, s, v.π)
6     print v
```

#### **Exercises**

## *20.2-1*

Show the d and π values that result from running breadth-first search on the directed graph of Figure 20.2(a), using vertex 3 as the source.

#### *20.2-2*

Show the d and π values that result from running breadth-first search on the undirected graph of Figure 20.3, using vertex u as the source. Assume that neighbors of a vertex are visited in alphabetical order.

### *20.2-3*

Show that using a single bit to store each vertex color suffices by arguing that the BFS procedure produces the same result if line 18 is removed. Then show how to obviate the need for vertex colors altogether.

#### *20.2-4*

What is the running time of BFS if we represent its input graph by an adjacency matrix and modify the algorithm to handle this form of input?

### *20.2-5*

Arguethat in a breadth-first search, the value u.d assigned to a vertex u is independent of the order in which the vertices appear in each adjacency list. Using Figure 20.3 as an example, show that the breadth-first tree computed by BFS can depend on the ordering within adjacency lists.

# *20.2-6*

Give an example of a directed graph G = (V, E), a source vertex s ∈ V, and a set of tree edges Eπ ⊆ E such that for each vertex v ∈ V, the unique simple path in the graph (V, Eπ) from s to v is a shortest path in G, yet the set of edges Eπ cannot be produced by running BFS on G, no matter how the vertices are ordered in each adjacency list.

# *20.2-7*

There are two types of professional wrestlers: "faces" (short for "babyfaces," i.e., "good guys") and "heels" ("bad guys"). Between any pair of professional wrestlers, there may or may not be a rivalry. You are given the names of n professional wrestlers and a list of r pairs of wrestlers for which there are rivalries. Give an O(n + r)-time algorithm that determines whether it is possible to designate some of the wrestlers as faces and the remainder as heels such that each rivalry is between a face and a heel. If it is possible to perform such a designation, your algorithm should produce it.

# ★ *20.2-8*

The *diameter* of a tree T = (V, E) is defined as max {δ(u, v) : u, v ∈ V}, that is, the largest of all shortest-path distances in the tree. Give an efficient algorithm to compute the diameter of a tree, and analyze the running time of your algorithm.

# **20.3 Depth-first search**

As its name implies, depth-first search searches "deeper" in the graph whenever possible. Depth-first search explores edges out of the most recently discovered vertex v that still has unexplored edges leaving it. Once all of v's edges have been explored, the search "backtracks" to explore edges leaving the vertex from which v was discovered. This process continues until all vertices that are reachable from the original source vertex have been discovered. If any undiscovered vertices remain, then depth-first search selects one of them as a new source, repeating the search