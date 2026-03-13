---
topic: dijkstra_algorithm
pages: 642-647
---

**Figure 22.6** The execution of Dijkstra's algorithm. The source s is the leftmost vertex. The shortest-path estimates appear within the vertices, and blue edges indicate predecessor values. Blue vertices belong to the set S, and tan vertices are in the min-priority queue Q = V − S. **(a)** The situation just before the first iteration of the **while** loop of lines 6–12. **(b)–(f)** The situation after each successive iteration of the **while** loop. In each part, the vertex highlighted in orange was chosen as vertex u in line 7, and each edge highlighted in orange caused a d value and a predecessor to change when the edge was relaxed. The d values and predecessors shown in part (f) are the final values.

of the **while** loop of lines 6–12. Lines 3–5 initialize the min-priority queue Q to contain all the vertices in V. Since S = ∅ at that time, the invariant is true upon first reaching line 6. Each time through the **while** loop of lines 6–12, line 7 extracts a vertex u from Q = V − S and line 8 adds it to set S, thereby maintaining the invariant. (The first time through this loop, u = s.) Vertex u, therefore, has the smallest shortest-path estimate of any vertex in V − S. Then, lines 9–12 relax each edge (u, v) leaving u, thus updating the estimate v.*d* and the predecessor v.π if the shortest path to v found so far improves by going through u. Whenever a relaxation step changes the d and π values, the call to DECREASE-KEY in line 12 updates the min-priority queue. The algorithm never inserts vertices into Q after the **for** loop of lines 4–5, and each vertex is extracted from Q and added to S exactly once, so that the **while** loop of lines 6–12 iterates exactly |V| times.

Because Dijkstra's algorithm always chooses the "lightest" or "closest" vertex in V − S to add to set S, you can think of it as using a greedy strategy. Chapter 15 explains greedy strategies in detail, but you need not have read that chapter to understand Dijkstra's algorithm. Greedy strategies do not always yield optimal

**Figure 22.7** The proof of Theorem 22.6. Vertex u is selected to be added into set S in line 7 of DIJKSTRA. Vertex y is the first vertex on a shortest path from the source s to vertex u that is not in set S, and x ∈ S is y's predecessor on that shortest path. The subpath from y to u may or may not re-enter set S.

results in general, but as the following theorem and its corollary show, Dijkstra's algorithm does indeed compute shortest paths. The key is to show that u.*d* = δ(s, u) each time it adds a vertex u to set S.

#### *Theorem 22.6 (Correctness of Dijkstra's algorithm)*

Dijkstra's algorithm, run on a weighted, directed graph G = (V, E) with nonnegative weight function w and source vertex s, terminates with u.*d* = δ(s, u) for all vertices u ∈ V.

*Proof* We will show that at the start of each iteration of the **while** loop of lines 6–12, we have v.*d* = δ(s, v) for all v ∈ S. The algorithm terminates when S = V, so that v.*d* = δ(s, v) for all v ∈ V.

The proof is by induction on the number of iterations of the **while** loop, which equals |S| at the start of each iteration. There are two bases: for |S| = 0, so that S = ∅ and the claim is trivially true, and for |S| = 1, so that S = {s} and s.*d* = δ(s, s) = 0.

For the inductive step, the inductive hypothesis is that v.*d* = δ(s, v) for all v ∈ S. The algorithm extracts vertex u from V − S. Because the algorithm adds u into S, we need to show that u.*d* = δ(s, u) at that time. If there is no path from s to u, then we are done, by the no-path property. If there is a path from s to u, then, as Figure 22.7 shows, let y be the first vertex on a shortest path from s to u that is not in S, and let x ∈ S be the predecessor of y on that shortest path. (We could have y = u or x = s.) Because y appears no later than u on the shortest path and all edge weights are nonnegative, we have δ(s, y) ≤ δ(s, u). Because the call of EXTRACT-MIN in line 7 returned u as having the minimum d value in V − S, we also have u.*d* ≤ y.*d*, and the upper-bound property gives δ(s, u) ≤ u.*d*.

Since x ∈ S, the inductive hypothesis implies that x.*d* = δ(s, x). During the iteration of the **while** loop that added x into S, edge (x, y) was relaxed. By the convergence property, y.*d* received the value of δ(s, y) at that time. Thus, we have

$$\delta(s, y) \le \delta(s, u) \le u.d \le y.d$$
 and  $y.d = \delta(s, y)$ ,

so that

$$\delta(s, y) = \delta(s, u) = u.d = y.d.$$

Hence, u.*d* = δ(s, u), and by the upper-bound property, this value never changes again.

## *Corollary 22.7*

After Dijkstra's algorithm is run on a weighted, directed graph G = (V, E) with nonnegative weight function w and source vertex s, the predecessor subgraph Gπ is a shortest-paths tree rooted at s.

*Proof* Immediate from Theorem 22.6 and the predecessor-subgraph property.

#### **Analysis**

How fast is Dijkstra's algorithm? It maintains the min-priority queue Q by calling three priority-queue operations: INSERT (in line 5), EXTRACT-MIN (in line 7), and DECREASE-KEY (in line 12). The algorithm calls both INSERT and EXTRACT-MIN once per vertex. Because each vertex u ∈ V is added to set S exactly once, each edge in the adjacency list *Adj*[u] is examined in the **for** loop of lines 9–12 exactly once during the course of the algorithm. Since the total number of edges in all the adjacency lists is |E|, this **for** loop iterates a total of |E| times, and thus the algorithm calls DECREASE-KEY at most |E| times overall. (Observe once again that we are using aggregate analysis.)

Just as in Prim's algorithm, the running time of Dijkstra's algorithm depends on the specific implementation of the min-priority queue Q. A simple implementation takes advantage of the vertices being numbered 1 to |V|: simply store v.*d* in the vth entry of an array. Each INSERT and DECREASE-KEY operation takes O(1) time, and each EXTRACT-MIN operation takes O(V) time (since it has to search through the entire array), for a total time of O(V² + E) = O(V²).

If the graph is sufficiently sparse—in particular, E = o(V²/lg V)—you can improve the running time by implementing the min-priority queue with a binary min-heap that includes a way to map between vertices and their corresponding heap elements. Each EXTRACT-MIN operation then takes O(lg V) time. As before, there are |V| such operations. The time to build the binary min-heap is O(V). (As noted in Section 21.2, you don't even need to call BUILD-MIN-HEAP.) Each DECREASE-KEY operation takes O(lg V) time, and there are still at most |E| such operations. The total running time is therefore O((V + E) lg V), which is O(E lg V) in the typical case that |E| = Θ(V). This running time improves upon the straightforward O(V²)-time implementation if E = o(V²/lg V).

By implementing the min-priority queue with a Fibonacci heap (see page 478), you can improve the running time to O(V lg V + E). The amortized cost of each of the |V| EXTRACT-MIN operations is O(lg V), and each DECREASE-KEY call, of which there are at most |E|, takes only O(1) amortized time. Historically, the development of Fibonacci heaps was motivated by the observation that Dijkstra's algorithm typically makes many more DECREASE-KEY calls than EXTRACT-MIN calls, so that any method of reducing the amortized time of each DECREASE-KEY operation to o(lg V) without increasing the amortized time of EXTRACT-MIN would yield an asymptotically faster implementation than with binary heaps.

Dijkstra's algorithm resembles both breadth-first search (see Section 20.2) and Prim's algorithm for computing minimum spanning trees (see Section 21.2). It is like breadth-first search in that set S corresponds to the set of black vertices in a breadth-first search. Just as vertices in S have their final shortest-path weights, so do black vertices in a breadth-first search have their correct breadth-first distances. Dijkstra's algorithm is like Prim's algorithm in that both algorithms use a min-priority queue to find the "lightest" vertex outside a given set (the set S in Dijkstra's algorithm and the tree being grown in Prim's algorithm), add this vertex into the set, and adjust the weights of the remaining vertices outside the set accordingly.

#### **Exercises**

#### *22.3-1*

Run Dijkstra's algorithm on the directed graph of Figure 22.2, first using vertex s as the source and then using vertex z as the source. In the style of Figure 22.6, show the d and π values and the vertices in set S after each iteration of the **while** loop.

#### *22.3-2*

#### *22.3-2*

Give a simple example of a directed graph with negative-weight edges for which Dijkstra's algorithm produces an incorrect answer. Why doesn't the proof of Theorem 22.6 go through when negative-weight edges are allowed?

#### *22.3-3*

Suppose that you change line 6 of Dijkstra's algorithm to read

6 **while** 
$$|Q| > 1$$

This change causes the **while** loop to execute jV j 1 times instead of jV j times. Is this proposed algorithm correct?

## *22.3-4*

Modify the DIJKSTRA procedure so that the priority queue Q is more like the queue in the BFS procedure in that it contains only vertices that have been reached from source s so far: Q ⊆ V − S and v ∈ Q implies v.*d* ≠ ∞.

### *22.3-5*

Professor Gaedel has written a program that he claims implements Dijkstra's algorithm. The program produces v.*d* and v.π for each vertex v ∈ V. Give an O(V + E)-time algorithm to check the output of the professor's program. It should determine whether the d and π attributes match those of some shortest-paths tree. You may assume that all edge weights are nonnegative.

## *22.3-6*

Professor Newman thinks that he has worked out a simpler proof of correctness for Dijkstra's algorithm. He claims that Dijkstra's algorithm relaxes the edges of every shortest path in the graph in the order in which they appear on the path, and therefore the path-relaxation property applies to every vertex reachable from the source. Show that the professor is mistaken by constructing a directed graph for which Dijkstra's algorithm relaxes the edges of a shortest path out of order.

## *22.3-7*

Consider a directed graph G = (V, E) on which each edge (u, v) ∈ E has an associated value r(u, v), which is a real number in the range 0 ≤ r(u, v) ≤ 1 that represents the reliability of a communication channel from vertex u to vertex v. Interpret r(u, v) as the probability that the channel from u to v will not fail, and assume that these probabilities are independent. Give an efficient algorithm to find the most reliable path between two given vertices.

#### *22.3-8*

Let G = (V, E) be a weighted, directed graph with positive weight function w: E → {1, 2, ..., W} for some positive integer W, and assume that no two vertices have the same shortest-path weights from source vertex s. Now define an unweighted, directed graph G' = (V ∪ V', E') by replacing each edge (u, v) ∈ E with w(u, v) unit-weight edges in series. How many vertices does G' have? Now suppose that you run a breadth-first search on G'. Show that the order in which the breadth-first search of G' colors vertices in V black is the same as the order in which Dijkstra's algorithm extracts the vertices of V from the priority queue when it runs on G.

#### *22.3-9*

Let G = (V, E) be a weighted, directed graph with nonnegative weight function w: E → {0, 1, ..., W} for some nonnegative integer W. Modify Dijkstra's algorithm to compute the shortest paths from a given source vertex s in O(WV + E) time.

## *22.3-10*

Modify your algorithm from Exercise 22.3-9 to run in O((V + E) lg W) time. (*Hint:* How many distinct shortest-path estimates can V − S contain at any point in time?)

### *22.3-11*

Suppose that you are given a weighted, directed graph G = (V, E) in which edges that leave the source vertex s may have negative weights, all other edge weights are nonnegative, and there are no negative-weight cycles. Argue that Dijkstra's algorithm correctly finds shortest paths from s in this graph.

#### *22.3-12*

Suppose that you have a weighted directed graph G = (V, E) in which all edge weights are positive real values in the range [C, 2C] for some positive constant C. Modify Dijkstra's algorithm so that it runs in O(V + E) time.

## **22.4 Difference constraints and shortest paths**

Chapter 29 studies the general linear-programming problem, showing how to optimize a linear function subject to a set of linear inequalities. This section investigates a special case of linear programming that reduces to finding shortest paths from a single source. The Bellman-Ford algorithm then solves the resulting single-source shortest-paths problem, thereby also solving the linear-programming problem.

#### **Linear programming**

In the general *linear-programming problem*, the input is an m × n matrix A, an m-vector b, and an n-vector c. The goal is to find a vector x of n elements that maximizes the *objective function* ∑ᵢ₌₁ⁿ cᵢxᵢ subject to the m constraints given by Ax ≤ b.

The most popular method for solving linear programs is the *simplex algorithm*, which Section 29.1 discusses. Although the simplex algorithm does not always run in time polynomial in the size of its input, there are other linear-programming algorithms that do run in polynomial time. We offer here two reasons to understand the setup of linear-programming problems. First, if you know that you can cast a given problem as a polynomial-sized linear-programming problem, then you immediately have a polynomial-time algorithm to solve the problem. Second, faster algorithms exist for many special cases of linear programming.