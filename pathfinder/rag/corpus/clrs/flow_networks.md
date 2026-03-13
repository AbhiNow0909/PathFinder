---
topic: flow_networks
pages: 693-697
---

We are now ready to define flows more formally. Let G = (V, E) be a flow network with a capacity function c. Let s be the source of the network, and let t be the sink. A *flow* in G is a real-valued function f : V × V → R that satisfies the following two properties:

**Capacity constraint:** For all u, v ∈ V, we require

$$0 \le f(u, v) \le c(u, v) .$$

The flow from one vertex to another must be nonnegative and must not exceed the given capacity.

**Flow conservation:** For all u ∈ V − {s, t}, we require

$$\sum_{v \in V} f(v, u) = \sum_{v \in V} f(u, v).$$

The total flow into a vertex other than the source or sink must equal the total flow out of that vertex—informally, "flow in equals flow out."

When (u, v) ∉ E, there can be no flow from u to v, and f(u, v) = 0.

We call the nonnegative quantity f(u, v) the flow from vertex u to vertex v. The *value* |f| of a flow f is defined as

$$|f| = \sum_{v \in V} f(s, v) - \sum_{v \in V} f(v, s) , \qquad (24.1)$$

that is, the total flow out of the source minus the flow into the source. (Here, the || notation denotes flow value, not absolute value or cardinality.) Typically, a flow network does not have any edges into the source, and the flow into the source, given by the summation ∑ᵥ₋ᵥ f(v, s), is 0. We include it, however, because when we introduce residual networks later in this chapter, the flow into the source can be positive. In the *maximum-flow problem*, the input is a flow network G with source s and sink t, and the goal is to find a flow of maximum value.

#### **An example of flow**

A flow network can model the trucking problem shown in Figure 24.1(a). The Lucky Puck Company has a factory (source s) in Vancouver that manufactures hockey pucks, and it has a warehouse (sink t) in Winnipeg that stocks them. Lucky Puck leases space on trucks from another firm to ship the pucks from the factory to the warehouse. Because the trucks travel over specified routes (edges) between cities (vertices) and have a limited capacity, Lucky Puck can ship at most c(u, v) crates per day between each pair of cities u and v in Figure 24.1(a). Lucky Puck

*24.1 Flow networks 673* 

**Figure 24.2** Converting a network with antiparallel edges to an equivalent one with no antiparallel edges. **(a)** A flow network containing both the edges (v₁, v₂) and (v₂, v₁). **(b)** An equivalent network with no antiparallel edges. A new vertex v' was added, and edge (v₁, v₂) was replaced by the pair of edges (v₁, v') and (v', v₂), both with the same capacity as (v₁, v₂).

has no control over these routes and capacities, and so the company cannot alter the flow network shown in Figure 24.1(a). They need to determine the largest number p of crates per day that they can ship and then to produce this amount, since there is no point in producing more pucks than they can ship to their warehouse. Lucky Puck is not concerned with how long it takes for a given puck to get from the factory to the warehouse. They care only that p crates per day leave the factory and p crates per day arrive at the warehouse.

A flow in this network models the "flow" of shipments because the number of crates shipped per day from one city to another is subject to a capacity constraint. Additionally, the model must obey flow conservation, for in a steady state, the rate at which pucks enter an intermediate city must equal the rate at which they leave. Otherwise, crates would accumulate at intermediate cities.

#### **Modeling problems with antiparallel edges**

Suppose that the trucking firm offers Lucky Puck the opportunity to lease space for 10 crates in trucks going from Edmonton to Calgary. It might seem natural to add this opportunity to our example and form the network shown in Figure 24.2(a). This network suffers from one problem, however: it violates the original assumption that if edge (v₁, v₂) ∈ E, then (v₂, v₁) ∉ E. We call the two edges (v₁, v₂) and (v₂, v₁) *antiparallel*. Thus, to model a flow problem with antiparallel edges, the network must be transformed into an equivalent one containing no antiparallel edges. Figure 24.2(b) displays this equivalent network. To transform the network, choose one of the two antiparallel edges, in this case (v₁, v₂), and split it by adding a new vertex v' and replacing edge (v₁, v₂) with the pair of edges (v₁, v') and (v', v₂). Also set the capacity of both new edges to the capacity of the original edge. The resulting network satisfies the property that if an edge belongs to

**Figure 24.3** Converting a multiple-source, multiple-sink maximum-flow problem into a problem with a single source and a single sink. **(a)** A flow network with three sources S = {s₁, s₂, s₃} and two sinks T = {t₁, t₂}. **(b)** An equivalent single-source, single-sink flow network. Add a supersource s and an edge with infinite capacity from s to each of the multiple sources. Also add a supersink t and an edge with infinite capacity from each of the multiple sinks to t.

the network, the reverse edge does not. As Exercise 24.1-1 asks you to prove, the resulting network is equivalent to the original one.

#### **Networks with multiple sources and sinks**

A maximum-flow problem may have several sources and sinks, rather than just one of each. The Lucky Puck Company, for example, might actually have a set of m factories {s₁, s₂, ..., sₘ} and a set of n warehouses {t₁, t₂, ..., tₙ}, as shown in Figure 24.3(a). Fortunately, this problem is no harder than ordinary maximum flow.

The problem of determining a maximum flow in a network with multiple sources and multiple sinks reduces to an ordinary maximum-flow problem. Figure 24.3(b) shows how to convert the network from (a) to an ordinary flow network with only a single source and a single sink. Add a *supersource* s and add a directed edge (s, sᵢ) with capacity c(s, sᵢ) = ∞ for each i = 1, 2, ..., m. Similarly, create a new *supersink* t and add a directed edge (tᵢ, t) with capacity c(tᵢ, t) = ∞ for each i = 1, 2, ..., n. Intuitively, any flow in the network in (a) corresponds to a flow in the network in (b), and vice versa. The single supersource s provides as much flow as desired for the multiple sources sᵢ, and the single supersink t likewise consumes as much flow as desired for the multiple sinks tᵢ. Exercise 24.1-2 asks you to prove formally that the two problems are equivalent.

*24.1 Flow networks 675* 

#### **Exercises**

## *24.1-1*

Show that splitting an edge in a flow network yields an equivalent network. More formally, suppose that flow network G contains edge (u, v), and define a new flow network G' by creating a new vertex x and replacing (u, v) by new edges (u, x) and (x, v) with c(u, x) = c(x, v) = c(u, v). Show that a maximum flow in G' has the same value as a maximum flow in G.

## *24.1-2*

Extend the flow properties and definitions to the multiple-source, multiple-sink problem. Show that any flow in a multiple-source, multiple-sink flow network corresponds to a flow of identical value in the single-source, single-sink network obtained by adding a supersource and a supersink, and vice versa.

## *24.1-3*

Suppose that a flow network G = (V, E) violates the assumption that the network contains a path s ↦ v ↦ t for all vertices v ∈ V. Let u be a vertex for which there is no path s ↦ u ↦ t. Show that there must exist a maximum flow f in G such that f(u, v) = f(v, u) = 0 for all vertices v ∈ V.

#### *24.1-4*

Let f be a flow in a network, and let α be a real number. The *scalar flow product*, denoted αf, is a function from V × V to R defined by

$$(\alpha f)(u,v) = \alpha \cdot f(u,v) .$$

Prove that the flows in a network form a *convex set*. That is, show that if f₁ and f₂ are flows, then so is αf₁ + (1 − α)f₂ for all α in the range 0 ≤ α ≤ 1.

### *24.1-5*

State the maximum-flow problem as a linear-programming problem.

## *24.1-6*

Professor Adam has two children who, unfortunately, dislike each other. The problem is so severe that not only do they refuse to walk to school together, but in fact each one refuses to walk on any block that the other child has stepped on that day. The children have no problem with their paths crossing at a corner. Fortunately both the professor's house and the school are on corners, but beyond that he is not sure if it is going to be possible to send both of his children to the same school. The professor has a map of his town. Show how to formulate the problem of determining whether both his children can go to the same school as a maximum-flow problem.

## *24.1-7*

Suppose that, in addition to edge capacities, a flow network has *vertex capacities*. That is each vertex v has a limit l(v) on how much flow can pass through v. Show how to transform a flow network G = (V, E) with vertex capacities into an equivalent flow network G' = (V', E') without vertex capacities, such that a maximum flow in G' has the same value as a maximum flow in G. How many vertices and edges does G' have?

## **24.2 The Ford-Fulkerson method**

This section presents the Ford-Fulkerson method for solving the maximum-flow problem. We call it a "method" rather than an "algorithm" because it encompasses several implementations with differing running times. The Ford-Fulkerson method depends on three important ideas that transcend the method and are relevant to many flow algorithms and problems: residual networks, augmenting paths, and cuts. These ideas are essential to the important max-flow min-cut theorem (Theorem 24.6), which characterizes the value of a maximum flow in terms of cuts of the flow network. We end this section by presenting one specific implementation of the Ford-Fulkerson method and analyzing its running time.

The Ford-Fulkerson method iteratively increases the value of the flow. It starts with f(u, v) = 0 for all u, v ∈ V, giving an initial flow of value 0. Each iteration increases the flow value in G by finding an "augmenting path" in an associated "residual network" G_f. The edges of the augmenting path in G_f indicate on which edges in G to update the flow in order to increase the flow value. Although each iteration of the Ford-Fulkerson method increases the value of the flow, we'll see that the flow on any particular edge of G may increase or decrease. Although it might seem counterintuitive to decrease the flow on an edge, doing so may enable flow to increase on other edges, allowing more flow to travel from the source to the sink. The Ford-Fulkerson method, given in the procedure FORD-FULKERSON-METHOD, repeatedly augments the flow until the residual network has no more augmenting paths. The max-flow min-cut theorem shows that upon termination, this process yields a maximum flow.

```
FORD-FULKERSON-METHOD(G, s, t)
1 initialize flow f to 0
2 while there exists an augmenting path p in the residual network G_f
3 augment flow f along p
4 return f
```