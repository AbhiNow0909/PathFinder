---
topic: difference_constraints
pages: 648-655
---

mediately have a polynomial-time algorithm to solve the problem. Second, faster algorithms exist for many special cases of linear programming. For example, the single-pair shortest-path problem (Exercise 22.4-4) and the maximum-flow problem (Exercise 24.1-5) are special cases of linear programming.

Sometimes the objective function does not matter: it's enough just to find any *feasible solution*, that is, any vector x that satisfies Ax ≤ b, or to determine that no feasible solution exists. This section focuses on one such *feasibility problem*.

#### **Systems of difference constraints**

In a *system of difference constraints*, each row of the linear-programming matrix A contains one 1 and one −1, and all other entries of A are 0. Thus, the constraints given by Ax ≤ b are a set of m *difference constraints* involving n unknowns, in which each constraint is a simple linear inequality of the form

$$x_j - x_i \le b_k ,$$

where 1 ≤ i, j ≤ n, i ≠ j, and 1 ≤ k ≤ m.

For example, consider the problem of finding a 5-vector x = (xᵢ) that satisfies

$$\begin{pmatrix} 1 & -1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 0 & -1 \\ 0 & 1 & 0 & 0 & -1 \\ -1 & 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 1 & 0 \\ 0 & 0 & -1 & 1 & 0 \\ 0 & 0 & 0 & -1 & 1 \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \\ x_5 \end{pmatrix} \le \begin{pmatrix} 0 \\ -1 \\ 1 \\ 5 \\ 4 \\ -1 \\ -3 \\ -3 \end{pmatrix}.$$

This problem is equivalent to finding values for the unknowns x₁, x₂, x₃, x₄, x₅, satisfying the following 8 difference constraints:

$$x_1 - x_2 \le 0 , (22.2)$$

$$x_1 - x_5 \le -1 \;, \tag{22.3}$$

$$x_2 - x_5 \le 1 , (22.4)$$

$$x_3 - x_1 \le 5 , (22.5)$$

$$x_4 - x_1 \le 4 \,, \tag{22.6}$$

$$x_4 - x_3 \le -1 \;, \tag{22.7}$$

$$x_5 - x_3 \le -3 , (22.8)$$

$$x_5 - x_4 \le -3. (22.9)$$

One solution to this problem is x = (−5, −3, 0, −1, −4), which you can verify directly by checking each inequality. In fact, this problem has more than one solution. 

Another is x' = (0, −2, −5, −4, −1). These two solutions are related: each component of x' is 5 larger than the corresponding component of x. This fact is not mere coincidence.

#### *Lemma 22.8*

Let x = (x₁, x₂, ..., xₙ) be a solution to a system Ax ≤ b of difference constraints, and let d be any constant. Then x + d = (x₁ + d, x₂ + d, ..., xₙ + d) is a solution to Ax ≤ b as well.

*Proof* For each xᵢ and xⱼ, we have (xⱼ + d) − (xᵢ + d) = xⱼ − xᵢ. Thus, if x satisfies Ax ≤ b, so does x + d.

Systems of difference constraints occur in various applications. For example, the unknowns xᵢ might be times at which events are to occur. Each constraint states that at least a certain amount of time, or at most a certain amount of time, must elapse between two events. Perhaps the events are jobs to be performed during the assembly of a product. If the manufacturer applies an adhesive that takes 2 hours to set at time x₁ and has to wait until it sets to install a part at time x₂, then there is a constraint that x₂ ≥ x₁ + 2 or, equivalently, that x₁ − x₂ ≤ −2. Alternatively, the manufacturer might require the part to be installed after the adhesive has been applied but no later than the time that the adhesive has set halfway. In this case, there is a pair of constraints x₂ ≥ x₁ and x₂ ≤ x₁ + 1 or, equivalently, x₁ − x₂ ≤ 0 and x₂ − x₁ ≤ 1.

If all the constraints have nonnegative numbers on the right-hand side—that is, if bᵢ ≥ 0 for i = 1, 2, ..., m—then finding a feasible solution is trivial: just set all the unknowns xᵢ equal to each other. Then all the differences are 0, and every constraint is satisfied. The problem of finding a feasible solution to a system of difference constraints is interesting only if at least one constraint has bᵢ < 0.

#### **Constraint graphs**

We can interpret systems of difference constraints from a graph-theoretic point of view. For a system Ax ≤ b of difference constraints, let's view the m × n linear-programming matrix A as the transpose of an incidence matrix (see Exercise 20.1-7) for a graph with n vertices and m edges. Each vertex vᵢ in the graph, for i = 1, 2, ..., n, corresponds to one of the n unknown variables xᵢ. Each directed edge in the graph corresponds to one of the m inequalities involving two unknowns.

More formally, given a system Ax ≤ b of difference constraints, the corresponding *constraint graph* is a weighted, directed graph G = (V, E), where

**Figure 22.8** The constraint graph corresponding to the system (22.2)–(22.9) of difference constraints. The value of δ(v₀, vᵢ) appears in each vertex vᵢ. One feasible solution to the system is x = (−5, −3, 0, −1, −4).

$$V = \{v_0, v_1, \dots, v_n\}$$

and

$$E = \{(v_i, v_j) : x_j - x_i \le b_k \text{ is a constraint}\}$$

$$\cup \{(v_0, v_1), (v_0, v_2), (v_0, v_3), \dots, (v_0, v_n)\}.$$

The constraint graph includes the additional vertex v₀, as we shall see shortly, to guarantee that the graph has some vertex that can reach all other vertices. Thus, the vertex set V consists of a vertex vᵢ for each unknown xᵢ, plus an additional vertex v₀. The edge set E contains an edge for each difference constraint, plus an edge (v₀, vᵢ) for each unknown xᵢ. If xⱼ − xᵢ ≤ bₖ is a difference constraint, then the weight of edge (vᵢ, vⱼ) is w(vᵢ, vⱼ) = bₖ. The weight of each edge leaving v₀ is 0. Figure 22.8 shows the constraint graph for the system (22.2)–(22.9) of difference constraints.

The following theorem shows how to solve a system of difference constraints by finding shortest-path weights in the corresponding constraint graph.

#### *Theorem 22.9*

Given a system Ax ≤ b of difference constraints, let G = (V, E) be the corresponding constraint graph. If G contains no negative-weight cycles, then

$$x = (\delta(v_0, v_1), \delta(v_0, v_2), \delta(v_0, v_3), \dots, \delta(v_0, v_n))$$
(22.10)

is a feasible solution for the system. If G contains a negative-weight cycle, then there is no feasible solution for the system.

*Proof* We first show that if the constraint graph contains no negative-weight cycles, then equation (22.10) gives a feasible solution. Consider any edge (vᵢ, vⱼ) ∈ E. The triangle inequality implies that δ(v₀, vⱼ) ≤ δ(v₀, vᵢ) + w(vᵢ, vⱼ), which is equivalent to δ(v₀, vⱼ) − δ(v₀, vᵢ) ≤ w(vᵢ, vⱼ). Thus, letting xᵢ = δ(v₀, vᵢ) and xⱼ = δ(v₀, vⱼ) satisfies the difference constraint xⱼ − xᵢ ≤ w(vᵢ, vⱼ) that corresponds to edge (vᵢ, vⱼ).

Now we show that if the constraint graph contains a negative-weight cycle, then the system of difference constraints has no feasible solution. Without loss of generality, let the negative-weight cycle be c = ⟨v₁, v₂, ..., vₖ⟩, where v₁ = vₖ. (The vertex v₀ cannot be on cycle c, because it has no entering edges.) Cycle c corresponds to the following difference constraints:

```
x₂ − x₁ ≤ w(v₁, v₂),
x₃ − x₂ ≤ w(v₂, v₃),
    .
    .
    .
xₖ₋₁ − xₖ₋₂ ≤ w(vₖ₋₂, vₖ₋₁),
xₖ − xₖ₋₁ ≤ w(vₖ₋₁, vₖ).
```

We'll assume that x has a solution satisfying each of these k inequalities and then derive a contradiction. The solution must also satisfy the inequality that results from summing the k inequalities together. In summing the left-hand sides, each unknown xᵢ is added in once and subtracted out once (remember that v₁ = vₖ implies x₁ = xₖ), so that the left-hand side sums to 0. The right-hand side sums to the weight w(c) of the cycle, giving 0 ≤ w(c). But since c is a negative-weight cycle, w(c) < 0, and we obtain the contradiction that 0 ≤ w(c) < 0.

#### **Solving systems of difference constraints**

Theorem 22.9 suggests how to use the Bellman-Ford algorithm to solve a system of difference constraints. Because the constraint graph contains edges from the source vertex v₀ to all other vertices, any negative-weight cycle in the constraint graph is reachable from v₀. If the Bellman-Ford algorithm returns TRUE, then the shortest-path weights give a feasible solution to the system. In Figure 22.8, for example, the shortest-path weights provide the feasible solution x = (−5, −3, 0, −1, −4), and by Lemma 22.8, x = (d − 5, d − 3, d, d − 1, d − 4) is also a feasible solution for any constant d. If the Bellman-Ford algorithm returns FALSE, there is no feasible solution to the system of difference constraints.

A system of difference constraints with m constraints on n unknowns produces a graph with n + 1 vertices and n + m edges. Thus, the Bellman-Ford algorithm provides a way to solve the system in O((n + 1)(n + m)) = O(n² + nm) time.

Exercise 22.4-5 asks you to modify the algorithm to run in O(nm) time, even if m is much less than n.

#### **Exercises**

## *22.4-1*

Find a feasible solution or determine that no feasible solution exists for the following system of difference constraints:

- x₁ − x₂ ≤ 1,
- x₁ − x₄ ≤ −4,
- x₂ − x₃ ≤ 2,
- x₂ − x₅ ≤ 7,
- x₂ − x₆ ≤ 5,
- x₃ − x₆ ≤ 10,
- x₄ − x₂ ≤ −2,
- x₅ − x₁ ≤ −1,
- x₅ − x₄ ≤ 3,
- x₆ − x₃ ≤ −8.

#### *22.4-2*

Find a feasible solution or determine that no feasible solution exists for the following system of difference constraints:

- x₁ − x₂ ≤ 4,
- x₁ − x₅ ≤ 5,
- x₂ − x₄ ≤ −6,
- x₃ − x₂ ≤ 1,
- x₄ − x₁ ≤ 3,
- x₄ − x₃ ≤ 5,
- x₄ − x₅ ≤ 10,
- x₅ − x₃ ≤ −4,
- x₅ − x₄ ≤ −8.

#### *22.4-3*

Can any shortest-path weight from the new vertex v₀ in a constraint graph be positive? Explain.

## *22.4-4*

Express the single-pair shortest-path problem as a linear program.

## *22.4-5*

Show how to modify the Bellman-Ford algorithm slightly so that when using it to solve a system of difference constraints with m inequalities on n unknowns, the running time is O(nm).

### *22.4-6*

Consider adding *equality constraints* of the form xᵢ = xⱼ + bₖ to a system of difference constraints. Show how to solve this variety of constraint system.

## *22.4-7*

Show how to solve a system of difference constraints by a Bellman-Ford-like algorithm that runs on a constraint graph without the extra vertex v₀.

## ? *22.4-8*

Let Ax ≤ b be a system of m difference constraints in n unknowns. Show that the Bellman-Ford algorithm, when run on the corresponding constraint graph, maximizes ∑ᵢ₌₁ⁿ xᵢ subject to Ax ≤ b and xᵢ ≤ 0 for all xᵢ.

## ? *22.4-9*

Show that the Bellman-Ford algorithm, when run on the constraint graph for a system Ax ≤ b of difference constraints, minimizes the quantity (max{xᵢ} − min{xᵢ}) subject to Ax ≤ b. Explain how this fact might come in handy if the algorithm is used to schedule construction jobs.

## *22.4-10*

Suppose that every row in the matrix A of a linear program Ax ≤ b corresponds to a difference constraint, a single-variable constraint of the form xᵢ ≥ bₖ, or a single-variable constraint of the form xᵢ ≤ bₖ. Show how to adapt the Bellman-Ford algorithm to solve this variety of constraint system.

## *22.4-11*

Give an efficient algorithm to solve a system Ax ≤ b of difference constraints when all of the elements of b are real-valued and all of the unknowns xᵢ must be integers.

## ? *22.4-12*

Give an efficient algorithm to solve a system Ax ≤ b of difference constraints when all of the elements of b are real-valued and a specified subset of some, but not necessarily all, of the unknowns xᵢ must be integers.

## **22.5 Proofs of shortest-paths properties**

Throughout this chapter, our correctness arguments have relied on the triangle inequality, upper-bound property, no-path property, convergence property, pathrelaxation property, and predecessor-subgraph property. We stated these properties without proof on page 611. In this section, we prove them.

## **The triangle inequality**

In studying breadth-first search (Section 20.2), we proved as Lemma 20.1 a simple property of shortest distances in unweighted graphs. The triangle inequality generalizes the property to weighted graphs.

#### *Lemma 22.10 (Triangle inequality)*

Let G = (V, E) be a weighted, directed graph with weight function w: E → ℝ and source vertex s. Then, for all edges (u, v) ∈ E,

$$\delta(s, v) \le \delta(s, u) + w(u, v)$$
.

*Proof* Suppose that p is a shortest path from source s to vertex v. Then p has no more weight than any other path from s to v. Specifically, path p has no more weight than the particular path that takes a shortest path from source s to vertex u and then takes edge (u, v).

Exercise 22.5-3 asks you to handle the case in which there is no shortest path from s to v.

#### **Effects of relaxation on shortest-path estimates**

The next group of lemmas describes how shortest-path estimates are affected by executing a sequence of relaxation steps on the edges of a weighted, directed graph that has been initialized by INITIALIZE-SINGLE-SOURCE.

#### *Lemma 22.11 (Upper-bound property)*

Let G = (V, E) be a weighted, directed graph with weight function w: E → ℝ. Let s ∈ V be the source vertex, and let the graph be initialized by INITIALIZE-SINGLE-SOURCE(G, s). Then, v.*d* ≥ δ(s, v) for all v ∈ V, and this invariant is maintained over any sequence of relaxation steps on the edges of G. Moreover, once v.*d* achieves its lower bound δ(s, v), it never changes.

*Proof* We prove the invariant v.*d* ≥ δ(s, v) for all vertices v ∈ V by induction over the number of relaxation steps.

For the base case, v.*d* ≥ δ(s, v) holds after initialization, since if v.*d* = ∞, then v.*d* ≥ δ(s, v) for all v ∈ V − {s}, and since s.*d* = 0 ≥ δ(s, s). (Note that δ(s, s) = −∞ if s is on a negative-weight cycle and that δ(s, s) = 0 otherwise.)

For the inductive step, consider the relaxation of an edge (u, v). By the inductive hypothesis, x.*d* ≥ δ(s, x) for all x ∈ V prior to the relaxation. The only d value that may change is v.*d*. If it changes, we have

```
v.d = u.d + w(u, v)
    ≥ δ(s, u) + w(u, v)  (by the inductive hypothesis)
    ≥ δ(s, v)  (by the triangle inequality),
```

and so the invariant is maintained.

The value of v.*d* never changes once v.*d* = δ(s, v) because, having achieved its lower bound, v.*d* cannot decrease since we have just shown that v.*d* ≥ δ(s, v), and it cannot increase because relaxation steps do not increase d values.

## *Corollary 22.12 (No-path property)*

Suppose that in a weighted, directed graph G = (V, E) with weight function w: E → ℝ, no path connects a source vertex s ∈ V to a given vertex v ∈ V. Then, after the graph is initialized by INITIALIZE-SINGLE-SOURCE(G, s), we have v.*d* = δ(s, v) = ∞, and this equation is maintained as an invariant over any sequence of relaxation steps on the edges of G.

*Proof* By the upper-bound property, we always have ∞ = δ(s, v) ≤ v.*d*, and thus v.*d* = ∞ = δ(s, v).

#### *Lemma 22.13*

Let G = (V, E) be a weighted, directed graph with weight function w: E → ℝ, and let (u, v) ∈ E. Then, immediately after edge (u, v) is relaxed by a call of RELAX(u, v, w), we have v.*d* ≤ u.*d* + w(u, v).

*Proof* If, just prior to relaxing edge (u, v), we have v.*d* > u.*d* + w(u, v), then v.*d* = u.*d* + w(u, v) afterward. If, instead, v.*d* ≤ u.*d* + w(u, v) just before the relaxation, then neither u.*d* nor v.*d* changes, and so v.*d* ≤ u.*d* + w(u, v) afterward.

#### *Lemma 22.14 (Convergence property)*

Let G = (V, E) be a weighted, directed graph with weight function w: E → ℝ, let s ∈ V be a source vertex, and let s ⤳ u → v be a shortest path in G for some vertices u, v ∈ V. Suppose that G is initialized by INITIALIZE-SINGLE-SOURCE(G, s) and then a sequence of relaxation steps that includes the call