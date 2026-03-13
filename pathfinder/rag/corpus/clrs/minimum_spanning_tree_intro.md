---
topic: minimum_spanning_tree_intro
pages: 607-612
---

The two algorithms are greedy algorithms, as described in Chapter 15. Each step of a greedy algorithm must make one of several possible choices. The greedy strategy advocates making the choice that is the best at the moment. Such a strategy does not generally guarantee that it always finds globally optimal solutions to problems. For the minimum-spanning-tree problem, however, we can prove that certain greedy strategies do yield a spanning tree with minimum weight. Although you can read this chapter independently of Chapter 15, the greedy methods presented here are a classic application of the theoretical notions introduced there.

Section 21.1 introduces a "generic" minimum-spanning-tree method that grows a spanning tree by adding one edge at a time. Section 21.2 gives two algorithms that implement the generic method. The first algorithm, due to Kruskal, is similar to the connected-components algorithm from Section 19.1. The second, due to Prim, resembles Dijkstra's shortest-paths algorithm (Section 22.3).

Because a tree is a type of graph, in order to be precise we must define a tree in terms of not just its edges, but its vertices as well. Because this chapter focuses on trees in terms of their edges, we'll implicitly understand that the vertices of a tree T are those that some edge of T is incident on.

## **21.1 Growing a minimum spanning tree**

The input to the minumum-spanning-tree problem is a connected, undirected graph G = .V; E/ with a weight function w: E → R. The goal is to find a minimum spanning tree for G. The two algorithms considered in this chapter use a greedy approach to the problem, although they differ in how they apply this approach.

This greedy strategy is captured by the procedure GENERIC-MST on the facing page, which grows the minimum spanning tree one edge at a time. The generic method manages a set A of edges, maintaining the following loop invariant:

Prior to each iteration, A is a subset of some minimum spanning tree.

```
GENERIC-MST.G; w/
1 A = ;
2 while A does not form a spanning tree 
3 find an edge .u; v/ that is safe for A
4 A = A [ {.u; v/g
5 return A
```

Each step determines an edge .u; v/ that the procedure can add to A without violating this invariant, in the sense that A [ {.u; v/g is also a subset of a minimum spanning tree. We call such an edge a *safe edge* for A, since it can be added safely to A while maintaining the invariant.

This generic algorithm uses the loop invariant as follows:

**Initialization:** After line 1, the set A trivially satisfies the loop invariant.

**Maintenance:** The loop in lines 2–4 maintains the invariant by adding only safe edges.

**Termination:** All edges added to A belong to a minimum spanning tree, and the loop must terminate by the time it has considered all edges. Therefore, the set A returned in line 5 must be a minimum spanning tree.

The tricky part is, of course, finding a safe edge in line 3. One must exist, since when line 3 is executed, the invariant dictates that there is a spanning tree T such that A ⊆ T . Within the **while** loop body, A must be a proper subset of T , and therefore there must be an edge .u; v/ ∈ T such that .u; v/ ∉ A and .u; v/ is safe for A.

The remainder of this section provides a rule (Theorem 21.1) for recognizing safe edges. The next section describes two algorithms that use this rule to find safe edges efficiently.

We first need some definitions. A *cut* .S; V S / of an undirected graph G = .V; E/ is a partition of V . Figure 21.2 illustrates this notion. We say that an edge .u; v/ ∈ E *crosses* the cut .S; V S / if one of its endpoints belongs to S and the other belongs to V S. A cut *respects* a set A of edges if no edge in A crosses the cut. An edge is a *light edge* crossing a cut if its weight is the minimum of any edge crossing the cut. There can be more than one light edge crossing a cut in the case of ties. More generally, we say that an edge is a *light edge* satisfying a given property if its weight is the minimum of any edge satisfying the property.

The following theorem gives the rule for recognizing safe edges.

#### *Theorem 21.1*

Let G = .V; E/ be a connected, undirected graph with a real-valued weight function w defined on E. Let A be a subset of E that is included in some minimum spanning tree for G, let .S; V S / be any cut of G that respects A, and let .u; v/ be a light edge crossing .S; V S /. Then, edge .u; v/ is safe for A.

*Proof* Let T be a minimum spanning tree that includes A, and assume that T does not contain the light edge .u; v/, since if it does, we are done. We'll construct another minimum spanning tree T' that includes A ∪ {.u; v/g by using a cut-and-paste technique, thereby showing that .u; v/ is a safe edge for A.

The edge .u; v/ forms a cycle with the edges on the simple path p from u to v in T . Since u and v are on opposite sides of the cut .S; V S /, at least one edge in T lies on the simple path p and also crosses the cut. Let .x; y/ be any such edge. The edge .x; y/ is not in A, because the cut respects A. Since .x; y/ is on the unique simple path from u to v in T , removing .x; y/ breaks T into two components. Adding .u; v/ reconnects them to form a new spanning tree T' = .T \ {.x; y/g/ ∪ {.u; v/g.

We next show that T' is a minimum spanning tree. Since .u; v/ is a light edge crossing .S; V S / and .x; y/ also crosses this cut, w.u; v/ ≤ w.x; y/. Therefore,

$$w(T') = w(T) - w(x, y) + w(u, v)$$
  
 
$$\leq w(T).$$

But T is a minimum spanning tree, so that w.T/ ≤ w.T'/, and thus, T' must be a minimum spanning tree as well.

It remains to show that .u; v/ is actually a safe edge for A. We have A ⊆ T', since A ⊆ T and .x; y/ ∉ A, and thus, A ∪ {.u; v/g ⊆ T'. Consequently, since T' is a minimum spanning tree, .u; v/ is safe for A.

Theorem 21.1 provides insight into how the GENERIC-MST method works on a connected graph G = .V; E/. As the method proceeds, the set A is always acyclic, since it is a subset of a minimum spanning tree and a tree may not contain a cycle.

At any point in the execution, the graph GA = .V; A/ is a forest, and each of the connected components of GA is a tree. (Some of the trees may contain just one vertex, as is the case, for example, when the method begins: A is empty and the forest contains |V| trees, one for each vertex.) Moreover, any safe edge .u; v/ for A connects distinct components of GA, since A ∪ {.u; v/g must be acyclic.

The **while** loop in lines 2–4 of GENERIC-MST executes |V| - 1 times because it finds one of the |V| - 1 edges of a minimum spanning tree in each iteration. Initially, when A = ∅, there are |V| trees in GA, and each iteration reduces that number by 1. When the forest contains only a single tree, the method terminates.

The two algorithms in Section 21.2 use the following corollary to Theorem 21.1.

#### *Corollary 21.2*

Let G = .V; E/ be a connected, undirected graph with a real-valued weight function w defined on E. Let A be a subset of E that is included in some minimum spanning tree for G, and let C = .VC; EC/ be a connected component (tree) in the forest GA = .V; A/. If .u; v/ is a light edge connecting C to some other component in GA, then .u; v/ is safe for A.

*Proof* The cut .VC; V \ VC/ respects A, and .u; v/ is a light edge for this cut. Therefore, .u; v/ is safe for A.

#### **Exercises**

## *21.1-1*

Let .u; v/ be a minimum-weight edge in a connected graph G. Show that .u; v/ belongs to some minimum spanning tree of G.

## *21.1-2*

Professor Sabatier conjectures the following converse of Theorem 21.1. Let G = .V; E/ be a connected, undirected graph with a real-valued weight function w defined on E. Let A be a subset of E that is included in some minimum spanning tree for G, let .S; V S / be any cut of G that respects A, and let .u; v/ be a safe edge for A crossing .S; V S /. Then, .u; v/ is a light edge for the cut. Show that the professor's conjecture is incorrect by giving a counterexample.

#### *21.1-3*

Show that if an edge .u; v/ is contained in some minimum spanning tree, then it is a light edge crossing some cut of the graph.

#### *21.1-4*

Give a simple example of a connected graph such that the set of edges {.u; v/: there exists a cut .S; V \ S/ such that .u; v/ is a light edge crossing .S; V \ S/} does not form a minimum spanning tree.

#### *21.1-5*

Let e be a maximum-weight edge on some cycle of connected graph G = .V; E/. Prove that there is a minimum spanning tree of G' = .V; E \ eg/ that is also a minimum spanning tree of G. That is, there is a minimum spanning tree of G that does not include e.

## *21.1-6*

Show that a graph has a unique minimum spanning tree if, for every cut of the graph, there is a unique light edge crossing the cut. Show that the converse is not true by giving a counterexample.

#### *21.1-7*

Argue that if all edge weights of a graph are positive, then any subset of edges that connects all vertices and has minimum total weight must be a tree. Give an example to show that the same conclusion does not follow if we allow some weights to be nonpositive.

## *21.1-8*

Let T be a minimum spanning tree of a graph G, and let L be the sorted list of the edge weights of T . Show that for any other minimum spanning tree T' of G, the list L is also the sorted list of edge weights of T'.

### *21.1-9*

Let T be a minimum spanning tree of a graph G = .V; E/, and let V' be a subset of V . Let T' be the subgraph of T induced by V', and let G' be the subgraph of G induced by V'. Show that if T' is connected, then T' is a minimum spanning tree of G'.

## *21.1-10*

Given a graph G and a minimum spanning tree T , suppose that the weight of one of the edges in T decreases. Show that T is still a minimum spanning tree for G. More formally, let T be a minimum spanning tree for G with edge weights given by weight function w. Choose one edge .x; y/ ∈ T and a positive number k, and define the weight function w' by

$$w'(u,v) = \begin{cases} w(u,v) & \text{if } (u,v) \neq (x,y), \\ w(x,y) - k & \text{if } (u,v) = (x,y). \end{cases}$$

Show that T is a minimum spanning tree for G with edge weights given by w'.

## ? *21.1-11*

Given a graph G and a minimum spanning tree T , suppose that the weight of one of the edges *not* in T decreases. Give an algorithm for finding the minimum spanning tree in the modified graph.

## **21.2 The algorithms of Kruskal and Prim**

The two minimum-spanning-tree algorithms described in this section elaborate on the generic method. They each use a specific rule to determine a safe edge in line 3 of GENERIC-MST. In Kruskal's algorithm, the set A is a forest whose vertices are all those of the given graph. The safe edge added to A is always a lowest-weight edge in the graph that connects two distinct components. In Prim's algorithm, the set A forms a single tree. The safe edge added to A is always a lowest-weight edge connecting the tree to a vertex not in the tree. Both algorithms assume that the input graph is connected and represented by adjacency lists.