---
topic: kruskal_and_prim
pages: 613-625
---

**Figure 21.4** The execution of Kruskal's algorithm on the graph from Figure 21.1. Blue edges belong to the forest A being grown. The algorithm considers each edge in sorted order by weight. A red arrow points to the edge under consideration at each step of the algorithm. If the edge joins two distinct trees in the forest, it is added to the forest, thereby merging the two trees.

#### **Kruskal's algorithm**

Kruskal's algorithm finds a safe edge to add to the growing forest by finding, of all the edges that connect any two trees in the forest, an edge (u, v) with the lowest weight. Let C₁ and C₂ denote the two trees that are connected by (u, v). Since (u, v) must be a light edge connecting C₁ to some other tree, Corollary 21.2 implies

**Figure 21.4, continued** Further steps in the execution of Kruskal's algorithm.

that (u, v) is a safe edge for C₁. Kruskal's algorithm qualifies as a greedy algorithm because at each step it adds to the forest an edge with the lowest possible weight.

Like the algorithm to compute connected components from Section 19.1, the procedure MST-KRUSKAL on the following page uses a disjoint-set data structure to maintain several disjoint sets of elements. Each set contains the vertices in one tree of the current forest. The operation FIND-SET(u) returns a representative element from the set that contains u. Thus, to determine whether two vertices u and v belong to the same tree, just test whether FIND-SET(u) equals FIND-SET(v). To combine trees, Kruskal's algorithm calls the UNION procedure.

Figure 21.4 shows how Kruskal's algorithm works. Lines 1–3 initialize the set A to the empty set and create |V| trees, one containing each vertex. The **for** loop in lines 6–9 examines edges in order of weight, from lowest to highest. The loop checks, for each edge (u, v), whether the endpoints u and v belong to the same tree. If they do, then the edge (u, v) cannot be added to the forest without creating a cycle, and the edge is ignored. Otherwise, the two vertices belong to different

```
MST-KRUSKAL(G, w)
1 A = ∅
2for each vertex v ∈ G:V 
3 MAKE-SET(v)
4 create a single list of the edges in G:E 
5 sort the list of edges into monotonically increasing order by weight w
6 for each edge (u, v) taken from the sorted list in order 
7 if FIND-SET(u) ≠ FIND-SET(v)
8 A = A ∪ {(u, v)}
9 UNION(u, v)
10 return A
```

trees. In this case, line 8 adds the edge (u, v) to A, and line 9 merges the vertices in the two trees.

The running time of Kruskal9s algorithm {or a }raph G = .V; E/ depends on the specific implementation of the disjoint-set data structure. Let9s assume that it uses the disjoint-set-forest implementation of Section 19.3 with the union-by-rank and path-compression heuristics, since that is the asymptotically fastest implementation known. Initializing the set A in line 1 takes O.1/ time, creating a single list of edges in line 4 takes O.V CE/ time (which is O.E/ because G is connected), and the time to sort the edges in line 5 is O.E lg E/. (We9ll account for the cost of the jV j MAKE-SET operations in the **for** loop of lines 233 in a moment.) The **for** loop of lines 639 performs O.E/ FIND-SET and UNION operations on the disjoint-set {orest. Along with the jV j MAKE-SET operations, these disjoint-set operations take a total of O..V C E/ ˛.V // time, where ˛ is the very slowly }rowing function defined in Section 19.4. Because we assume that G is connected, we have jEj jV j 1, and so the disjoint-set operations take O.E ˛.V // time. Moreover, since ˛.jV j/ D O.lg V / D O.lg E/, the total running time of Kruskal9s algorithm is O.E lg E/. Observing that jEj < jV j 2 , we have lg jEj D O.lg V /, and so we can restate the running time of Kruskal9s algorithm as O.E lg V /.

#### **Prim's algorithm**

Like Kruskal's algorithm, Prim's algorithm is a special case of the generic minimum-spanning-tree method from Section 21.1. Prim's algorithm operates much like Dijkstra's algorithm for finding shortest paths in a graph, which we'll see in Section 22.3. Prim's algorithm has the property that the edges in the set A always form a single tree. As Figure 21.5 shows, the tree starts from an arbitrary root vertex r and grows until it spans all the vertices in V . Each step adds to the tree A

**Figure 21.5** The execution of Prim's algorithm on the graph from Figure 21.1. The root vertex is a. Blue vertices and edges belong to the tree being grown, and tan vertices have yet to be added to the tree. At each step of the algorithm, the vertices in the tree determine a cut of the graph, and a light edge crossing the cut is added to the tree. The edge and vertex added to the tree are highlighted in orange. In the second step (part (c)), for example, the algorithm has a choice of adding either edge (b, c) or edge (a, h) to the tree since both are light edges crossing the cut.

a light edge that connects A to an isolated vertex—one on which no edge of A is incident. By Corollary 21.2, this rule adds only edges that are safe for A. Therefore, when the algorithm terminates, the edges in A form a minimum spanning tree. This strategy qualifies as greedy since at each step it adds to the tree an edge that contributes the minimum amount possible to the tree's weight.

In the procedure MST-PRIM below, the connected graph G and the root r of the minimum spanning tree to be grown are inputs to the algorithm. In order to efficiently select a new edge to add into tree A, the algorithm maintains a min-priority queue Q of all vertices that are *not* in the tree, based on a *key* attribute. For each vertex v, the attribute v:*key* is the minimum weight of any edge connecting v to a vertex in the tree, where by convention, v:*key* = ∞ if there is no such edge. The attribute v:π names the parent of v in the tree. The algorithm implicitly maintains the set A from GENERIC-MST as

```
A = {(v, v:π): v ∈ V − {r} − Q},
```

where we interpret the vertices in Q as forming a set. When the algorithm terminates, the min-priority queue Q is empty, and thus the minimum spanning tree A for G is

```
A = {(v, v:π): v ∈ V − {r}}.
```

```
MST-PRIM(G, w, r)
1 for each vertex u ∈ G:V 
2u:key = ∞
3 u:π = NIL 
4 r:key = 0
5 Q = ∅
6 for each vertex u ∈ G:V 
7 INSERT(Q, u)
8 while Q ≠ ∅
9u = EXTRACT-MIN(Q) // add u to the tree 
10 for each vertex v in G:Adj[u] // update keys of u's non-tree neighbors
11 if v ∈ Q and w(u, v) < v:key
12 v:π = u
13 v:key = w(u, v)
14 DECREASE-KEY(Q, v, w(u, v))
```

Figure 21.5 shows how Prim's algorithm works. Lines 1–7 set the key of each vertex to ∞ (except for the root r, whose key is set to 0 to make it the first vertex processed), set the parent of each vertex to NIL, and insert each vertex into the minpriority queue Q. The algorithm maintains the following three-part loop invariant:

Prior to each iteration of the **while** loop of lines 8–14,

- 1. A = {(v, v:π): v ∈ V − {r} − Q}.
- 2. The vertices already placed into the minimum spanning tree are those in V − Q.
- 3. For all vertices v ∈ Q, if v:π ≠ NIL, then v:*key* < ∞ and v:*key* is the weight of a light edge (v, v:π) connecting v to some vertex already placed into the minimum spanning tree.

Line 9 identifies a vertex u ∈ Q incident on a light edge that crosses the cut (V − Q, Q) (with the exception of the first iteration, in which u = r due to lines 4–7). Removing u from the set Q adds it to the set V − Q of vertices in the tree, thus adding the edge (u, u:π) to A. The **for** loop of lines 10–14 updates the *key* and π attributes of every vertex v adjacent to u but not in the tree, thereby maintaining the third part of the loop invariant. Whenever line 13 updates v:*key*, line 14 calls DECREASE-KEY to inform the min-priority queue that v's key has changed.

The running time of Prim's algorithm depends on the specific implementation of the min-priority queue Q. You can implement Q with a binary min-heap (see Chapter 6), including a way to map between vertices and their corresponding heap elements. The BUILD-MIN-HEAP procedure can perform lines 5–7 in O(V) time. In fact, there is no need to call BUILD-MIN-HEAP. You can just put the key of r at the root of the min-heap, and because all other keys are ∞, they can go anywhere else in the min-heap. The body of the **while** loop executes |V| times, and since each EXTRACT-MIN operation takes O(lg V) time, the total time for all calls to EXTRACT-MIN is O(V lg V). The **for** loop in lines 10–14 executes O(E) times altogether, since the sum of the lengths of all adjacency lists is 2|E|. Within the **for** loop, the test for membership in Q in line 11 can take constant time if you keep a bit for each vertex that indicates whether it belongs to Q and update the bit when the vertex is removed from Q. Each call to DECREASE-KEY in line 14 takes O(lg V) time. Thus, the total time for Prim's algorithm is O(V lg V + E lg V) = O(E lg V), which is asymptotically the same as for our implementation of Kruskal's algorithm.

You can further improve the asymptotic running time of Prim's algorithm by implementing the min-priority queue with a Fibonacci heap (see page 478). If a Fibonacci heap holds |V| elements, an EXTRACT-MIN operation takes O(lg V) amortized time and each INSERT and DECREASE-KEY operation takes only O(1) amortized time. Therefore, by using a Fibonacci heap to implement the minpriority queue Q, the running time of Prim's algorithm improves to O(E+V lg V).

#### **Exercises**

## *21.2-1*

Kruskal's algorithm can return different spanning trees for the same input graph G, depending on how it breaks ties when the edges are sorted. Show that for each minimum spanning tree T of G, there is a way to sort the edges of G in Kruskal's algorithm so that the algorithm returns T .

## *21.2-2*

Give a simple implementation of Prim's algorithm that runs in O(V²) time when the graph G = (V, E) is represented as an adjacency matrix.

## *21.2-3*

For a sparse graph G = (V, E), where |E| = Θ(V), is the implementation of Prim's algorithm with a Fibonacci heap asymptotically faster than the binary-heap implementation? What about for a dense graph, where |E| = Θ(V²)? How must the sizes |E| and |V| be related for the Fibonacci-heap implementation to be asymptotically faster than the binary-heap implementation?

#### *21.2-4*

Suppose that all edge weights in a graph are integers in the range from 1 to |V|. How fast can you make Kruskal's algorithm run? What if the edge weights are integers in the range from 1 to W for some constant W ?

## *21.2-5*

Suppose that all edge weights in a graph are integers in the range from 1 to |V|. How fast can you make Prim's algorithm run? What if the edge weights are integers in the range from 1 to W for some constant W ?

## *21.2-6*

Professor Borden proposes a new divide-and-conquer algorithm for computing minimum spanning trees, which goes as follows. Given a graph G = (V, E), partition the set V of vertices into two sets V₁ and V₂ such that |V₁| and |V₂| differ by at most 1. Let E₁ be the set of edges that are incident only on vertices in V₁, and let E₂ be the set of edges that are incident only on vertices in V₂. Recursively solve a minimum-spanning-tree problem on each of the two subgraphs G₁ = (V₁, E₁) and G₂ = (V₂, E₂). Finally, select the minimum-weight edge in E that crosses the cut (V₁, V₂), and use this edge to unite the resulting two minimum spanning trees into a single spanning tree.

Either argue that the algorithm correctly computes a minimum spanning tree of G, or provide an example for which the algorithm fails.

## ★ *21.2-7*

Suppose that the edge weights in a graph are uniformly distributed over the halfopen interval [0, 1). Which algorithm, Kruskal's or Prim's, can you make run faster?

## ★ *21.2-8*

Suppose that a graph G has a minimum spanning tree already computed. How quickly can you update the minimum spanning tree upon adding a new vertex and incident edges to G?

## **Problems**

## *21-1 Second-best minimum spanning tree*

Let G = (V, E) be an undirected, connected graph whose weight function is w: E → R, and suppose that |E| ≥ |V| and all edge weights are distinct.

We define a second-best minimum spanning tree as follows. Let T be the set of all spanning trees of G, and let T be a minimum spanning tree of G. Then a *second-best minimum spanning tree* is a spanning tree T' such that w(T') = min{w(T''): T'' ∈ T − {T}}.

- *a.* Show that the minimum spanning tree is unique, but that the second-best minimum spanning tree need not be unique.
- *b.* Let T be the minimum spanning tree of G. Prove that G contains some edge (u, v) ∈ T and some edge (x, y) ∉ T such that (T − {(u, v)}) ∪ {(x, y)} is a second-best minimum spanning tree of G.
- *c.* Now let T be any spanning tree of G and, for any two vertices u, v ∈ V, let *max*[u, v] denote an edge of maximum weight on the unique simple path between u and v in T. Describe an O(V²)-time algorithm that, given T, computes *max*[u, v] for all u, v ∈ V.
- *d.* Give an efficient algorithm to compute the second-best minimum spanning tree of G.

#### *21-2 Minimum spanning tree in sparse graphs*

For a very sparse connected graph G = (V, E), it is possible to further improve upon the O(E + V lg V) running time of Prim's algorithm with a Fibonacci heap by preprocessing G to decrease the number of vertices before running Prim's algorithm. In particular, for each vertex u, choose the minimum-weight edge (u, v)

incident on u, and put (u, v) into the minimum spanning tree under construction. Then, contract all chosen edges (see Section B.4). Rather than contracting these edges one at a time, first identify sets of vertices that are united into the same new vertex. Then create the graph that would have resulted from contracting these edges one at a time, but do so by "renaming" edges according to the sets into which their endpoints were placed. Several edges from the original graph might be renamed the same as each other. In such a case, only one edge results, and its weight is the minimum of the weights of the corresponding original edges.

Initially, set the minimum spanning tree T being constructed to be empty, and for each edge (u, v) ∈ E, initialize the two attributes (u, v):*orig* = (u, v) and (u, v):*c* = w(u, v). Use the *orig* attribute to reference the edge from the initial graph that is associated with an edge in the contracted graph. The c attribute holds the weight of an edge, and as edges are contracted, it is updated according to the above scheme for choosing edge weights. The procedure MST-REDUCE on the facing page takes inputs G and T, and it returns a contracted graph G' with updated attributes *orig*' and c'. The procedure also accumulates edges of G into the minimum spanning tree T.

- *a.* Let T be the set of edges returned by MST-REDUCE, and let A be the minimum spanning tree of the graph G' formed by the call MST-PRIM(G', c', r), where c' is the weight attribute on the edges of G':*E* and r is any vertex in G':*V*. Prove that T ∪ {(x, y):*orig*': (x, y) ∈ A} is a minimum spanning tree of G.
- *b.* Argue that |G':*V*| ≤ |V|/2.
- *c.* Show how to implement MST-REDUCE so that it runs in O(E) time. (*Hint:* Use simple data structures.)
- *d.* Suppose that you run k phases of MST-REDUCE, using the output G' produced by one phase as the input G to the next phase and accumulating edges in T. Argue that the overall running time of the k phases is O(kE).
- *e.* Suppose that after running k phases of MST-REDUCE, as in part (d), you run Prim's algorithm by calling MST-PRIM(G', c', r), where G', with weight attribute c', is returned by the last phase and r is any vertex in G':*V*. Show how to pick k so that the overall running time is O(E lg lg V). Argue that your choice of k minimizes the overall asymptotic running time.
- *f.* For what values of |E| (in terms of |V|) does Prim's algorithm with preprocessing asymptotically beat Prim's algorithm without preprocessing?

```
MST-REDUCE(G, T)
1 for each vertex v ∈ G:V 
2v:mark = FALSE 
3 MAKE-SET(v)
4 for each vertex u ∈ G:V 
5 if u:mark == FALSE 
6 choose v ∈ G:Adj[u] such that (u, v):c is minimized 
7 UNION(u, v)
8 T = T ∪ {(u, v):orig}
9u:mark = TRUE 
10 v:mark = TRUE 
11 G':V = {FIND-SET(v): v ∈ G:V}
12 G':E = ∅
13 for each edge (x, y) ∈ G:E 
14 u = FIND-SET(x)
15 v = FIND-SET(y)
16 if u ≠ v
17 if (u, v) ∉ G':E 
18 G':E = G':E ∪ {(u, v)}
19 (u, v):orig' = (x, y):orig 
20(u, v):c' = (x, y):c
21 elseif (x, y):c < (u, v):c'
22(u, v):orig' = (x, y):orig 
23 (u, v):c' = (x, y):c
24 construct adjacency lists G':Adj for G'
25 return G' and T
```

#### *21-3 Alternative minimum-spanning-tree algorithms*

Consider the three algorithms MAYBE-MST-A, MAYBE-MST-B, and MAYBE-MST-C on the next page. Each one takes a connected graph and a weight function as input and returns a set of edges T. For each algorithm, either prove that T is a minimum spanning tree or prove that T is not necessarily a minimum spanning tree. Also describe the most efficient implementation of each algorithm, regardless of whether it computes a minimum spanning tree.

#### *21-4 Bottleneck spanning tree*

A *bottleneck spanning tree* T of an undirected graph G is a spanning tree of G whose largest edge weight is minimum over all spanning trees of G. The value of the bottleneck spanning tree is the weight of the maximum-weight edge in T.

```
MAYBE-MST-A(G, w)
1 sort the edges into monotonically decreasing order of edge weights w
2T = E
3 for each edge e, taken in monotonically decreasing order by weight
4 if T − {e} is a connected graph 
5 T = T − {e}
6 return T
MAYBE-MST-B(G, w)
1 T = ∅
2 for each edge e, taken in arbitrary order 
3 if T ∪ {e} has no cycles 
4 T = T ∪ {e}
5 return T
MAYBE-MST-C(G, w)
1 T = ∅
2 for each edge e, taken in arbitrary order 
3 T = T ∪ {e}
4 if T has a cycle c
5 let e' be a maximum-weight edge on c
6 T = T − {e'}
7 return T
```

*a.* Argue that a minimum spanning tree is a bottleneck spanning tree.

Part (a) shows that finding a bottleneck spanning tree is no harder than finding a minimum spanning tree. In the remaining parts, you will show how to find a bottleneck spanning tree in linear time.

- *b.* Give a linear-time algorithm that, given a graph G and an integer b, determines whether the value of the bottleneck spanning tree is at most b.
- *c.* Use your algorithm for part (b) as a subroutine in a linear-time algorithm for the bottleneck-spanning-tree problem. (*Hint:* You might want to use a subroutine that contracts sets of edges, as in the MST-REDUCE procedure described in Problem 21-2.)

## **Chapter notes**

Tarjan [429] surveys the minimum-spanning-tree problem and provides excellent advanced material. Graham and Hell [198] compiled a history of the minimumspanning-tree problem.

Tarjan attributes the first minimum-spanning-tree algorithm to a 1926 paper by O. Borůvka. Borůvka's algorithm consists of running O(lg V) iterations of the procedure MST-REDUCE described in Problem 21-2. Kruskal's algorithm was reported by Kruskal [272] in 1956. The algorithm commonly known as Prim's algorithm was indeed invented by Prim [367], but it was also invented earlier by V. Jarník in 1930.

When |E| = Θ(V lg V), Prim's algorithm, implemented with a Fibonacci heap, runs in O(E) time. For sparser graphs, using a combination of the ideas from Prim's algorithm, Kruskal's algorithm, and Borůvka's algorithm, together with advanced data structures, Fredman and Tarjan [156] give an algorithm that runs in O(E lg V) time. Gabow, Galil, Spencer, and Tarjan [165] improved this algorithm to run in O(E lg lg V) time. Chazelle [83] gives an algorithm that runs in O(E α(E, V)) time, where α(E, V) is the functional inverse of Ackermann's function. (See the chapter notes for Chapter 19 for a brief discussion of Ackermann's function and its inverse.) Unlike previous minimum-spanning-tree algorithms, Chazelle's algorithm does not follow the greedy method. Pettie and Ramachandran [356] give an algorithm based on precomputed "MST decision trees" that also runs in O(E α(E, V)) time.

A related problem is *spanning-tree verification*: given a graph G = (V, E) and a tree T ⊆ E, determine whether T is a minimum spanning tree of G. King [254] gives a linear-time algorithm to verify a spanning tree, building on earlier work of Komlós [269] and Dixon, Rauch, and Tarjan [120].

The above algorithms are all deterministic and fall into the comparison-based model described in Chapter 8. Karger, Klein, and Tarjan [243] give a randomized minimum-spanning-tree algorithm that runs in O(V + E) expected time. This algorithm uses recursion in a manner similar to the linear-time selection algorithm in Section 9.3: a recursive call on an auxiliary problem identifies a subset of the edges E' that cannot be in any minimum spanning tree. Another recursive call on E − E' then finds the minimum spanning tree. The algorithm also uses ideas from Borůvka's algorithm and King's algorithm for spanning-tree verification.

Fredman and Willard [158] showed how to find a minimum spanning tree in O(V+E) time using a deterministic algorithm that is not comparison based. Their algorithm assumes that the data are b-bit integers and that the computer memory consists of addressable b-bit words.

Suppose that you need to drive from Oceanside, New York, to Oceanside, California, by the shortest possible route. Your GPS contains information about the entire road network of the United States, including the road distance between each pair of adjacent intersections. How can your GPS determine this shortest route?

One possible way is to enumerate all the routes from Oceanside, New York, to Oceanside, California, add up the distances on each route, and select the shortest. But even disallowing routes that contain cycles, your GPS would need to examine an enormous number of possibilities, most of which are simply not worth considering. For example, a route that passes through Miami, Florida, is a poor choice, because Miami is several hundred miles out of the way.

This chapter and Chapter 23 show how to solve such problems efficiently. The input to a *shortest-paths problem* is a weighted, directed graph G = (V, E), with a weight function w: E → R mapping edges to real-valued weights. The *weight* w(p) of path p = ⟨v₀, v₁, ..., vₖ⟩ is the sum of the weights of its constituent edges:

$$w(p) = \sum_{i=1}^{k} w(v_{i-1}, v_i).$$

We define the *shortest-path weight* δ(u, v) from u to v by

$$\delta(u,v) = \begin{cases} \min\{w(p) : u \stackrel{p}{\leadsto} v\} & \text{if there is a path from } u \text{ to } v \text{ ,} \\ \infty & \text{otherwise .} \end{cases}$$

A *shortest path* from vertex u to vertex v is then defined as any path p with weight w(p) = δ(u, v).

In the example of going from Oceanside, New York, to Oceanside, California, your GPS models the road network as a graph: vertices represent intersections, edges represent road segments between intersections, and edge weights represent road distances. The goal is to find a shortest path from a given intersection in