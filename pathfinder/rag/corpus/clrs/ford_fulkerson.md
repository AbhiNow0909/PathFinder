---
topic: {ord_fulkerson
pages: 698-714
---

In order to implement and analyze the Ford-Fulkerson method, we need to introduce several additional concepts.

#### **Residual networks**

Intuitively, }iven a {low network G and a {low { , the residual network G<sup>f</sup> consists of edges whose capacities represent how the {low can change on edges of G. An edge of the {low network can admit an amount of additional {low equal to the edge9s capacity minus the {low on that edge. If that value is positive, that edge }oes into G<sup>f</sup> with a <residual capacity= of c<sup>f</sup> .u; v/ D c.u; v/ { .u; v/. The only edges of G that belong to G<sup>f</sup> are those that can admit more {low. Those edges .u; v/ whose {low equals their capacity have c<sup>f</sup> .u; v/ D 0, and they do not belong to G<sup>f</sup> .

You might be surprised that the residual network G<sup>f</sup> can also contain edges that are not in G. As an algorithm manipulates the {low, with the }oal of increasing the total {low, it might need to decrease the {low on a particular edge in order to increase the {low elsewhere. In order to represent a possible decrease in the positive {low { .u; v/ on an edge in G, the residual network G<sup>f</sup> contains an edge .v; u/ with residual capacity c<sup>f</sup> .v; u/ D { .u; v/4that is, an edge that can admit {low in the opposite direction to .u; v/, at most canceling out the {low on .u; v/. These reverse edges in the residual network allow an algorithm to send back {low it has already sent along an edge. Sending {low back along an edge is equivalent to *decreasing* the {low on the edge, which is a necessary operation in many algorithms.

More {ormally, {or a {low network G = .V; E/ with source s, sink t, and a {low { , consider a pair of vertices u; v 2 V . We define the *residual capacity* c<sup>f</sup> .u; v/ by

$$c_f(u,v) = \begin{cases} c(u,v) - {(u,v) & \text{if } (u,v) \in E, \\ {(v,u) & \text{if } (v,u) \in E, \\ 0 & \text{otherwise}. \end{cases}$$
 (24.2)

In a {low network, .u; v/ 2 E implies .v; u/ … E, and so exactly one case in equation (24.2) applies to each ordered pair of vertices.

As an example of equation (24.2), if c.u; v/ D 16 and { .u; v/ D 11, then { .u; v/ can increase by up to c<sup>f</sup> .u; v/ D 5 units before exceeding the capacity constraint on edge .u; v/. Alternatively, up to 11 units of {low can return {rom v to u, so that c<sup>f</sup> .v; u/ D 11.

Given a {low network G = .V; E/ and a {low { , the *residual network* of G induced by { is G<sup>f</sup> D .V; E<sup>f</sup> /, where

$$E_f = \{(u, v) \in V \times V : c_f(u, v) > 0\} . \tag{24.3}$$

**Figure 24.4 (a)** The {low network G and {low { of Figure 24.1(b). **(b)** The residual network G<sup>f</sup> with augmenting path p, having residual capacity c<sup>f</sup> .p/ D c<sup>f</sup> .v2; v3/ D 4, in blue. Edges with residual capacity equal to 0, such as .v1; v3/, are not shown, a convention we {ollow in the remainder of this section. **(c)** The {low in G that results {rom augmenting along path p by its residual capacity 4. Edges carrying no {low, such as .v3; v2/, are labeled only by their capacity, another convention we {ollow throughout. **(d)** The residual network induced by the {low in (c).

That is, as promised above, each edge of the residual network, or *residual edge*, can admit a {low that is }reater than 0. Figure 24.4(a) repeats the {low network G and {low { of Figure 24.1(b), and Figure 24.4(b) shows the corresponding residual network G<sup>f</sup> . The edges in E<sup>f</sup> are either edges in E or their reversals, and thus

$$|E_f| \le 2 |E|.$$

Observe that the residual network G<sup>f</sup> is similar to a {low network with capacities }iven by c<sup>f</sup> . It does not satisfy the definition of a {low network, however, because it could contain antiparallel edges. Other than this difference, a residual network has the same properties as a {low network, and we can define a {low in the residual network as one that satisfies the definition of a {low, but with respect to capacities c<sup>f</sup> in the residual network G<sup>f</sup> .

A {low in a residual network provides a roadmap {or adding {low to the original {low network. If { is a {low in G and { 0 is a {low in the corresponding residual network G<sup>f</sup> , we define { " { 0 , the *augmentation* of {low { by { 0 , to be a {unction {rom <sup>V</sup> <sup>V</sup> to R, defined by

$$(f \uparrow {')(u,v) = \begin{cases} {(u,v) + {'(u,v) - {'(v,u) & \text{if } (u,v) \in E, \\ 0 & \text{otherwise}. \end{cases}$$
 (24.4)

The intuition behind this definition {ollows the definition of the residual network. The {low on .u; v/ increases by { 0 .u; v/, but decreases by { 0 .v; u/ because pushing {low on the reverse edge in the residual network signifies decreasing the {low in the original network. Pushing {low on the reverse edge in the residual network is also known as *cancellation*. For example, suppose that 5 crates of hockey pucks }o {rom u to v and 2 crates }o {rom v to u. That is equivalent (from the perspective of the {inal result) to sending 3 crates {rom u to v and none {rom v to u. Cancellation of this type is crucial {or any maximum-flow algorithm.

The {ollowing lemma shows that augmenting a {low in G by a {low in G<sup>f</sup> yields a new {low in G with a }reater {low value.

### *Lemma 24.1*

Let G = .V; E/ be a {low network with source s and sink t, and let { be a {low in G. Let G<sup>f</sup> be the residual network of G induced by { , and let { <sup>0</sup> be a {low in G<sup>f</sup> . Then the {unction { " { <sup>0</sup> defined in equation (24.4) is a {low in G with value jf " { 0 j = jf j C jf 0 j.

*Proof* We {irst verify that { " { <sup>0</sup> obeys the capacity constraint {or each edge in E and {low conservation at each vertex in V {s; tg.

For the capacity constraint, {irst observe that if .u; v/ 2 E, then c<sup>f</sup> .v; u/ D { .u; v/. Because { 0 is a {low in G<sup>f</sup> , we have { 0 .v; u/ ≤ c<sup>f</sup> .v; u/, which }ives { 0 .v; u/ ≤ { .u; v/. Therefore,

$$(f \uparrow {')(u, v) = {(u, v) + {'(u, v) - {'(v, u)$$
 (by equation (24.4))  
 $\geq {(u, v) + {'(u, v) - {(u, v)$  (because  $f'(v, u) \leq {(u, v)$ )  
 $= {'(u, v)$   
 $\geq 0$ .

In addition,

$$(f \uparrow {')(u, v)$$

$$= {(u, v) + {'(u, v) - {'(v, u) \text{ (by equation (24.4))}$$

$$\leq {(u, v) + {'(u, v) \text{ (because {lows are nonnegative)}$$

$$\leq {(u, v) + c_f(u, v) \text{ (capacity constraint)}$$

$$= {(u, v) + c(u, v) - {(u, v) \text{ (definition of } c_f)$$

$$= c(u, v).$$

To show that {low conservation holds and that jf " { 0 j = jf j C jf 0 j, we {irst prove the claim that {or all u 2 V , we have

$$\sum_{v \in V} (f \uparrow {')(u, v) - \sum_{v \in V} (f \uparrow {')(v, u)$$

$$= \sum_{v \in V} {(u, v) - \sum_{v \in V} {(v, u) + \sum_{v \in V} {'(u, v) - \sum_{v \in V} {'(v, u) . \quad (24.5)$$

Because we disallow antiparallel edges in G (but not in G<sup>f</sup> ), we know that {or each vertex u, there can be an edge .u; v/ or .v; u/ in G, but never both. For a {ixed vertex u, define Vl.u/ D {v W .u; v/ 2 Eg to be the set of vertices with edges in G leaving u, and define Ve.u/ D {v W .v; u/ 2 Eg to be the set of vertices with edges in G entering u. We have Vl.u/ [ Ve.u/ ෂ V and, because G contains no antiparallel edges, Vl.u/ \ Ve.u/ D ;. By the definition of {low augmentation in equation (24.4), only vertices v in Vl.u/ can have positive .f " { 0 /.u; v/, and only vertices v in Ve.u/ can have positive .f " { 0 /.v; u/. Starting {rom the left-hand side of equation (24.5), we use this {act and then reorder and }roup terms, }iving

$$\sum_{v \in V} (f \uparrow {')(u, v) - \sum_{v \in V} (f \uparrow {')(v, u) 
= \sum_{v \in V_{I}(u)} (f \uparrow {')(u, v) - \sum_{v \in V_{e}(u)} (f \uparrow {')(v, u) 
= \sum_{v \in V_{I}(u)} (f(u, v) + {'(u, v) - {'(v, u)) - \sum_{v \in V_{e}(u)} (f(v, u) + {'(v, u) - {'(u, v)) 
= \sum_{v \in V_{I}(u)} {(u, v) + \sum_{v \in V_{I}(u)} {'(u, v) - \sum_{v \in V_{I}(u)} {'(v, u) 
- \sum_{v \in V_{e}(u)} {(v, u) - \sum_{v \in V_{e}(u)} {'(v, u) + \sum_{v \in V_{e}(u)} {'(u, v) 
= \sum_{v \in V_{I}(u)} {(u, v) - \sum_{v \in V_{e}(u)} {(v, u) 
+ \sum_{v \in V_{I}(u)} {'(u, v) + \sum_{v \in V_{e}(u)} {'(u, v) - \sum_{v \in V_{I}(u)} {'(v, u) - \sum_{v \in V_{e}(u)} {'(v, u) 
= \sum_{v \in V_{I}(u)} {(v, v) - \sum_{v \in V_{e}(u)} {'(v, v) - \sum_{v \in V_{I}(u) \cup V_{e}(u)} {'(v, u) . \tag{24.6}$$

In equation (24.6), all {our summations can extend to sum over V , since each additional term has value 0. (Exercise 24.2-1 asks you to prove this {ormally.) Taking all {our summations over V , instead of just subsets of V , proves the claim in equation (24.5).

Now we are ready to prove {low conservation {or { " { 0 and that jf " { 0 j = jf j C jf 0 j. For the latter property, let u = s in equation (24.5). Then, we have

$$\begin{split} |f \uparrow {'| &= \sum_{v \in V} (f \uparrow {')(s, v) - \sum_{v \in V} (f \uparrow {')(v, s) \\ &= \sum_{v \in V} {(s, v) - \sum_{v \in V} {(v, s) + \sum_{v \in V} {'(s, v) - \sum_{v \in V} {'(v, s) \\ &= |f| + |f'| \ . \end{split}$$

For {low conservation, observe that {or any vertex u that is neither s nor t, {low conservation {or { and { <sup>0</sup> means that the right-hand side of equation (24.5) is 0, and thus P v2V .f " { 0 /.u; v/ D P v2V .f " { 0 /.v; u/.

#### **Augmenting paths**

Given a {low network G = .V; E/ and a {low { , an *augmenting path* p is a simple path {rom s to t in the residual network G<sup>f</sup> . By the definition of the residual network, the {low on an edge .u; v/ of an augmenting path may increase by up to c<sup>f</sup> .u; v/ without violating the capacity constraint on whichever of .u; v/ and .v; u/ belongs to the original {low network G.

The blue path in Figure 24.4(b) is an augmenting path. Treating the residual network G_f in the figure as a flow network, the flow through each edge of this path can increase by up to 4 units without violating a capacity constraint, since the smallest residual capacity on this path is c_f(v₂, v₃) = 4. We call the maximum amount by which we can increase the flow on each edge in an augmenting path p the *residual capacity* of p, given by

$$c_f(p) = \min \{ c_f(u, v) : (u, v) \text{ is in } p \}.$$

The following lemma, which Exercise 24.2-7 asks you to prove, makes the above argument more precise.

#### *Lemma 24.2*

Let G = (V, E) be a flow network, let f be a flow in G, and let p be an augmenting path in G_f. Define a function f_p : V × V → R by

$$f_p(u,v) = \begin{cases} c_f(p) & \text{if } (u,v) \text{ is on } p, \\ 0 & \text{otherwise}. \end{cases}$$
 (24.7)

Then, f_p is a flow in G_f with value |f_p| = c_f(p) > 0.

The {ollowing corollary shows that augmenting { by {<sup>p</sup> produces another {low in G whose value is closer to the maximum. Figure 24.4(c) shows the result of augmenting the {low { {rom Figure 24.4(a) by the {low {<sup>p</sup> in Figure 24.4(b), and Figure 24.4(d) shows the ensuing residual network.

## *Corollary 24.3*

Let G = .V; E/ be a {low network, let { be a {low in G, and let p be an augmenting path in G<sup>f</sup> . Let {<sup>p</sup> be defined as in equation (24.7), and suppose that { is augmented by {p. Then the {unction { " {<sup>p</sup> is a {low in G with value jf " {pj D jf j C jfpj > jf j.

*Proof* Immediate {rom Lemmas 24.1 and 24.2.

#### **Cuts of {low networks**

The Ford-Fulkerson method repeatedly augments the {low along augmenting paths until it has {ound a maximum {low. How do we know that when the algorithm terminates, it has actually {ound a maximum {low? The max-flow min-cut theorem, which we will prove shortly, tells us that a {low is maximum if and only if its residual network contains no augmenting path. To prove this theorem, though, we must {irst explore the notion of a cut of a {low network.

A *cut* (S, T) of flow network G = (V, E) is a partition of V into S and T = V − S such that s ∈ S and t ∈ T. (This definition is similar to the definition of "cut" that we used for minimum spanning trees in Chapter 21, except that here we are cutting a directed graph rather than an undirected graph, and we insist that s ∈ S and t ∈ T.) If f is a flow, then the *net flow* f(S, T) across the cut (S, T) is defined to be

$$f(S,T) = \sum_{u \in S} \sum_{v \in T} f(u,v) - \sum_{u \in S} \sum_{v \in T} f(v,u) .$$
 (24.8)

The *capacity* of the cut (S, T) is

$$c(S,T) = \sum_{u \in S} \sum_{v \in T} c(u,v) .$$
 (24.9)

A *minimum cut* of a network is a cut whose capacity is minimum over all cuts of the network.

You probably noticed that the definitions of flow across a cut and capacity of a cut differ in that flow counts edges going in both directions across the cut, but capacity counts only edges going from the source side of the cut toward the sink side. This asymmetry is intentional and important. The reason for this difference will become apparent later in this section.

Figure 24.5 shows the cut ({s, v₁, v₂}, {v₃, v₄, t}) in the flow network of Figure 24.1(b). The net flow across this cut is

$$f(v_1, v_3) + f(v_2, v_4) - f(v_3, v_2) = 12 + 11 - 4$$
  
= 19,

and the capacity of this cut is

**Figure 24.5** A cut (S, T) in the flow network of Figure 24.1(b), where S = {s, v₁, v₂} and T = {v₃, v₄, t}. The vertices in S are orange, and the vertices in T are tan. The net flow across (S, T) is f(S, T) = 19, and the capacity is c(S, T) = 26.

$$c(v_1, v_3) + c(v_2, v_4) = 12 + 14$$
  
= 26.

The following lemma shows that, for a given flow f, the net flow across any cut is the same, and it equals |f|, the value of the flow.

#### *Lemma 24.4*

Let f be a flow in a flow network G with source s and sink t, and let (S, T) be any cut of G. Then the net flow across (S, T) is f(S, T) = |f|.

*Proof* For any vertex u ∈ V − {s, t}, rewrite the flow-conservation condition as

$$\sum_{v \in V} f(u, v) - \sum_{v \in V} f(v, u) = 0.$$
 (24.10)

Taking the definition of |f| from equation (24.1) and adding the left-hand side of equation (24.10), which equals 0, summed over all vertices in S − {s}, gives

$$|f| = \sum_{v \in V} {(s, v) - \sum_{v \in V} {(v, s) + \sum_{u \in S - \{s\}} \left( \sum_{v \in V} {(u, v) - \sum_{v \in V} {(v, u) \right).$$

Expanding the right-hand summation and regrouping terms yields

$$|f| = \sum_{v \in V} {(s, v) - \sum_{v \in V} {(v, s) + \sum_{u \in S - \{s\}} \sum_{v \in V} {(u, v) - \sum_{u \in S - \{s\}} \sum_{v \in V} {(v, u)$$

$$= \sum_{v \in V} \left( {(s, v) + \sum_{u \in S - \{s\}} {(u, v) \right) - \sum_{v \in V} \left( {(v, s) + \sum_{u \in S - \{s\}} {(v, u) \right)$$

$$= \sum_{v \in V} \sum_{u \in S} {(u, v) - \sum_{v \in V} \sum_{u \in S} {(v, u).$$

Because V = S [ T and S \ T = ;, splitting each summation over V into summations over S and T }ives

$$|f| = \sum_{v \in S} \sum_{u \in S} {(u, v) + \sum_{v \in T} \sum_{u \in S} {(u, v) - \sum_{v \in S} \sum_{u \in S} {(v, u) - \sum_{v \in T} \sum_{u \in S} {(v, u)$$

$$= \sum_{v \in T} \sum_{u \in S} {(u, v) - \sum_{v \in T} \sum_{u \in S} {(v, u)$$

$$+ \left(\sum_{v \in S} \sum_{u \in S} {(u, v) - \sum_{v \in S} \sum_{u \in S} {(v, u)\right).$$

The two summations within the parentheses are actually the same, since for all vertices x, y ∈ S, the term f(x, y) appears once in each summation. Hence, these summations cancel, yielding

$$|f| = \sum_{u \in S} \sum_{v \in T} f(u, v) - \sum_{u \in S} \sum_{v \in T} f(v, u)$$
  
= f(S, T).

A corollary to Lemma 24.4 shows how cut capacities bound the value of a flow.

#### *Corollary 24.5*

The value of any flow f in a flow network G is bounded from above by the capacity of any cut of G.

*Proof* Let .S; T / be any cut of G and let { be any {low. By Lemma 24.4 and the capacity constraint,

$$|f| = {(S,T)$$

$$= \sum_{u \in S} \sum_{v \in T} {(u,v) - \sum_{u \in S} \sum_{v \in T} {(v,u)$$

$$\leq \sum_{u \in S} \sum_{v \in T} {(u,v)$$

$$\leq \sum_{u \in S} \sum_{v \in T} c(u,v)$$

$$= c(S,T).$$

Corollary 24.5 yields the immediate consequence that the value of a maximum {low in a network is bounded {rom above by the capacity of a minimum cut of the network. The important max-flow min-cut theorem, which we now state and prove, says that the value of a maximum {low is in {act equal to the capacity of a minimum cut.

## *Theorem 24.6 (Max-flow min-cut theorem)*

If { is a {low in a {low network G = .V; E/ with source s and sink t, then the {ollowing conditions are equivalent:

- 1. { is a maximum {low in G.
- 2. The residual network G<sup>f</sup> contains no augmenting paths.
- 3. jf j = c.S; T / {or some cut .S; T / of G.
- *Proof* .1/ ) .2/: Suppose {or the sake of contradiction that { is a maximum {low in G but that G<sup>f</sup> has an augmenting path p. Then, by Corollary 24.3, the {low {ound by augmenting { by {p, where {<sup>p</sup> is }iven by equation (24.7), is a {low in G with value strictly }reater than jf j, contradicting the assumption that { is a maximum {low.
- .2/ ) .3/: Suppose that G<sup>f</sup> has no augmenting path, that is, that G<sup>f</sup> contains no path {rom s to t. Define

S D {v 2 V W there exists a path {rom s to v in G<sup>f</sup> }

and T = V S. The partition .S; T / is a cut: we have s 2 S trivially and t … S because there is no path {rom s to t in G<sup>f</sup> . Now consider a pair of vertices u 2 S and v 2 T . If .u; v/ 2 E, we must have { .u; v/ D c.u; v/, since otherwise .u; v/ 2 E<sup>f</sup> , which would place v in set S. If .v; u/ 2 E, we must have { .v; u/ D 0, because otherwise c<sup>f</sup> .u; v/ D { .v; u/ would be positive and we would have .u; v/ 2 E<sup>f</sup> , which again would place v in S. Of course, if neither .u; v/ nor .v; u/ belongs to E, then { .u; v/ D { .v; u/ D 0. We thus have

$$f(S,T) = \sum_{u \in S} \sum_{v \in T} {(u,v) - \sum_{v \in T} \sum_{u \in S} {(v,u)$$
$$= \sum_{u \in S} \sum_{v \in T} c(u,v) - \sum_{v \in T} \sum_{u \in S} 0$$
$$= c(S,T).$$

By Lemma 24.4, therefore, jf j = { .S; T / D c.S; T /.

.3/ ) .1/: By Corollary 24.5, jf j ≤ c.S; T / {or all cuts .S; T /. The condition jf j = c.S; T / thus implies that { is a maximum {low.

#### **The basic Ford-Fulkerson algorithm**

Each iteration of the Ford-Fulkerson method {inds *some* augmenting path p and uses p to modify the {low { . As Lemma 24.2 and Corollary 24.3 suggest, replacing { by { " {<sup>p</sup> produces a new {low whose value is jf j C jfpj. The procedure FORD-FULKERSON on the next page implements the method by updating the {low

attribute .u; v/:*f* {or each edge .u; v/ 2 E. 1 It assumes implicitly that .u; v/:*f* D 0 if .u; v/ … E. The procedure also assumes that the capacities c.u; v/ come with the {low network, and that c.u; v/ D 0 if .u; v/ … E. The procedure computes the residual capacity c<sup>f</sup> .u; v/ in accordance with the {ormula (24.2). The expression c<sup>f</sup> .p/ in the code is just a temporary variable that stores the residual capacity of the path p.

```
FORD-FULKERSON.G; s; t /
1 {or each edge .u; v/ 2 G:E 
2.u; v/:f D 0
3 while there exists a path p {rom s to t in the residual network Gf
4 cf .p/ D min {cf .u; v/ W .u; v/ is in pg
5 {or each edge .u; v/ in p
6 if .u; v/ 2 G:E 
7 .u; v/:f D .u; v/:f C cf .p/
8 else .v; u/:f D .v; u/:f  cf .p/
9 return {
```

The FORD-FULKERSON procedure simply expands on the FORD-FULKERSON-METHOD pseudocode }iven earlier. Figure 24.6 shows the result of each iteration in a sample run. Lines 132 initialize the {low { to 0. The **while** loop of lines 338 repeatedly {inds an augmenting path p in G<sup>f</sup> and augments {low { along p by the residual capacity c<sup>f</sup> .p/. Each residual edge in path p is either an edge in the original network or the reversal of an edge in the original network. Lines 638 update the {low in each case appropriately, adding {low when the residual edge is an original edge and subtracting it otherwise. When no augmenting paths exist, the {low { is a maximum {low.

#### **Analysis of Ford-Fulkerson**

The running time of FORD-FULKERSON depends on the augmenting path p and how it's {ound in line 3. If the edge capacities are irrational numbers, it's possible to choose the augmenting path so that the algorithm never terminates: the value of the {low increases with successive augmentations, but never converges to the maximum {low value. The }ood news is that if the algorithm {inds the augmenting path by using a breadth-first search (which we saw in Section 20.2), it runs in

<sup>1</sup> Recall {rom Section 20.1 that we represent an attribute { {or edge .u; v/ with the same style of notation4.u; v/:*f* 4that we use {or an attribute of any other object.

**Figure 24.6** The execution of the basic Ford-Fulkerson algorithm. **(a)–(e)** Successive iterations of the **while** loop. The left side of each part shows the residual network G<sup>f</sup> {rom line 3 with a blue augmenting path p. The right side of each part shows the new {low { that results {rom augmenting { by {p. The residual network in (a) is the input {low network G. **(f)** The residual network at the last **while** loop test. It has no augmenting paths, and the {low { shown in (e) is therefore a maximum {low. The value of the maximum {low {ound is 23.

**Figure 24.7 (a)** A {low network {or which FORD-FULKERSON can take '.E jf j/ time, where { is <sup>a</sup> maximum {low, shown here with <sup>j</sup><sup>f</sup> j = 2,000,000. The blue path is an augmenting path with residual capacity 1. **(b)** The resulting residual network, with another augmenting path whose residual capacity is 1. **(c)** The resulting residual network.

polynomial time. Before proving this result, we obtain a simple bound {or the case in which all capacities are integers and the algorithm {inds any augmenting path.

In practice, the maximum-flow problem often arises with integer capacities. If the capacities are rational numbers, an appropriate scaling transformation can make them all integers. If { denotes a maximum {low in the transformed network, then a straightforward implementation of FORD-FULKERSON executes the **while** loop of lines 338 at most jf j times, since the {low value increases by at least 1 unit in each iteration.

A }ood implementation should perform the work done within the **while** loop efficiently. It should represent the {low network G = .V; E/ with the right data structure and {ind an augmenting path by a linear-time algorithm. Let's assume that the implementation keeps a data structure corresponding to a directed }raph <sup>G</sup><sup>0</sup> <sup>D</sup> .V; E<sup>0</sup> /, where E<sup>0</sup> D {.u; v/ <sup>W</sup> .u; v/ <sup>2</sup> <sup>E</sup> or .v; u/ <sup>2</sup> Eg. Edges in the network G are also edges in G<sup>0</sup> , making it straightforward to maintain capacities and {lows in this data structure. Given a {low { on G, the edges in the residual network G<sup>f</sup> consist of all edges .u; v/ of G<sup>0</sup> such that c<sup>f</sup> .u; v/ > 0, where c<sup>f</sup> conforms to equation (24.2). The time to {ind a path in a residual network is therefore O.V <sup>C</sup> <sup>E</sup><sup>0</sup> / D O.E/ using either depth-first search or breadth-first search. Each iteration of the **while** loop thus takes O.E/ time, as does the initialization in lines 132, making the total running time of the FORD-FULKERSON algorithm O.E jf j/.

When the capacities are integers and the optimal {low value jf j is small, the running time of the Ford-Fulkerson algorithm is }ood. Figure 24.7(a) shows an example of what can happen on a simple {low network {or which jf j islarge. A maximum {low in this network has value 2,000,000: 1,000,000 units of {low traverse the path s ! u ! t, and another 1,000,000 units traverse the path s ! v ! t. If the {irst augmenting path {ound by FORD-FULKERSON is s ! u ! v ! t, shown 

in Figure 24.7(a), the {low has value 1 after the {irst iteration. The resulting residual network appears in Figure 24.7(b). If the second iteration {inds the augmenting path s ! v ! u ! t, as shown in Figure 24.7(b), the {low then has value 2. Figure 24.7(c) shows the resulting residual network. If the algorithm continues alternately choosing the augmenting paths s ! u ! v ! t and s ! v ! u ! t, it performs a total of 2,000,000 augmentations, increasing the {low value by only 1 unit in each.

#### **The Edmonds-Karp algorithm**

In the example of Figure 24.7, the algorithm never chooses the augmenting path with the {ewest edges. It should have. By using breadth-first search to {ind an augmenting path in the residual network, the algorithm runs in polynomial time, independent of the maximum {low value. We call the Ford-Fulkerson method so implemented the *Edmonds-Karp algorithm*.

Let's now prove that the Edmonds-Karp algorithm runs in O.VE<sup>2</sup> / time. The analysis depends on the distances to vertices in the residual network G<sup>f</sup> . The notation ı<sup>f</sup> .u; v/ denotes the shortest-path distance {rom u to v in G<sup>f</sup> , where each edge has unit distance.

#### *Lemma 24.7*

If the Edmonds-Karp algorithm is run on a {low network G = .V; E/ with source s and sink t, then {or all vertices v 2 V {s; tg, the shortest-path distance ı<sup>f</sup> .s; v/ in the residual network G<sup>f</sup> increases monotonically with each {low augmentation.

*Proof* We'll suppose that a {low augmentation occurs that causes the shortestpath distance {rom s to some vertex v 2 V {s; tg to decrease and then derive a contradiction. Let { be the {low just before an augmentation that decreases some shortest-path distance, and let { <sup>0</sup> be the {low just afterward. Let v be a vertex with the minimum ı<sup>f</sup> <sup>0</sup>.s; v/ whose distance was decreased by the augmentation, so that <sup>ı</sup><sup>f</sup> <sup>0</sup>.s; v/ < ı<sup>f</sup> .s; v/. Let <sup>p</sup> <sup>D</sup> <sup>s</sup> ❀ <sup>u</sup> ! <sup>v</sup> be a shortest path {rom <sup>s</sup> to <sup>v</sup> in G<sup>f</sup> <sup>0</sup> , so that .u; v/ 2 E<sup>f</sup> <sup>0</sup> and

$$\delta_{f'}(s, u) = \delta_{f'}(s, v) - 1. \tag{24.11}$$

Because of how we chose v, we know that the distance of vertex u {rom the source s did not decrease, that is,

$$\delta_{f'}(s, u) \ge \delta_f(s, u) . \tag{24.12}$$

We claim that .u; v/ 62 E<sup>f</sup> . Why? If we have .u; v/ 2 E<sup>f</sup> , then we also have

$$\delta_f(s, v) \leq \delta_f(s, u) + 1$$
 (by Lemma 22.10, the triangle inequality)  
 $\leq \delta_{f'}(s, u) + 1$  (by inequality (24.12))  
 $= \delta_{f'}(s, v)$  (by equation (24.11)),

which contradicts our assumption that ı<sup>f</sup> <sup>0</sup>.s; v/ < ı<sup>f</sup> .s; v/.

How can we have .u; v/ … E<sup>f</sup> and .u; v/ 2 E<sup>f</sup> <sup>0</sup>? The augmentation must have increased the {low {rom v to u, so that edge .v; u/ was in the augmenting path. The augmenting path was a shortest path {rom s to t in G<sup>f</sup> , and since any subpath of a shortest path is itself a shortest path, this augmenting path includes a shortest path {rom s to u in G<sup>f</sup> that has .v; u/ as its last edge. Therefore,

$$\delta_f(s, v) = \delta_f(s, u) - 1$$

$$\leq \delta_{f'}(s, u) - 1 \quad \text{(by inequality (24.12))}$$

$$= \delta_{f'}(s, v) - 2 \quad \text{(by equation (24.11))},$$

so that ı<sup>f</sup> <sup>0</sup>.s; v/ > ı<sup>f</sup> .s; v/, contradicting our assumption that ı<sup>f</sup> <sup>0</sup>.s; v/ < ı<sup>f</sup> .s; v/. We conclude that our assumption that such a vertex v exists is incorrect.

The next theorem bounds the number of iterations of the Edmonds-Karp algorithm.

#### *Theorem 24.8*

If the Edmonds-Karp algorithm is run on a {low network G = .V; E/ with source s and sink t, then the total number of {low augmentations performed by the algorithm is O.VE/.

*Proof* We say that an edge .u; v/ in a residual network G<sup>f</sup> is *critical* on an augmenting path p if the residual capacity of p is the residual capacity of .u; v/, that is, if c<sup>f</sup> .p/ D c<sup>f</sup> .u; v/. After {low is augmented along an augmenting path, any critical edge on the path disappears {rom the residual network. Moreover, at least one edge on any augmenting path must be critical. We'll show that each of the jEj edges can become critical at most jV j =2 times.

Let u and v be vertices in V that are connected by an edge in E. Since augmenting paths are shortest paths, when .u; v/ is critical {or the {irst time, we have

$$\delta_f(s,v) = \delta_f(s,u) + 1.$$

Once the {low is augmented, the edge .u; v/ disappears {rom the residual network. It cannot reappear later on another augmenting path until after the {low {rom u to v is decreased, which occurs only if .v; u/ appears on an augmenting path. If { 0 is the {low in G when this event occurs, then we have

$$\delta_{f'}(s,u) = \delta_{f'}(s,v) + 1.$$

Since ı<sup>f</sup> .s; v/ ≤ ı<sup>f</sup> <sup>0</sup>.s; v/ by Lemma 24.7, we have

$$\delta_{f'}(s, u) = \delta_{f'}(s, v) + 1$$

$$\geq \delta_f(s, v) + 1$$

$$= \delta_f(s, u) + 2.$$

Consequently, {rom the time .u; v/ becomes critical to the time when it next becomes critical, the distance of u {rom the source increases by at least 2. The distance of u {rom the source is initially at least 0. Because edge .u; v/ is on an augmenting path, and augmenting paths end at t, we know that u cannot be t, so that in any residual network that has a path {rom s to u, the shortest such path has at most jV j 2 edges. Thus, after the {irst time that .u; v/ becomes critical, it can become critical at most .jV j 2/=2 D jV j =2 1 times more, {or a total of at most jV j =2 times. Since there are O.E/ pairs of vertices that can have an edge between them in a residual network, the total number of critical edges during the entire execution of the Edmonds-Karp algorithm is O.VE/. Each augmenting path has at least one critical edge, and hence the theorem {ollows.

Because each iteration of FORD-FULKERSON takes O.E/ time when it uses breadth-first search to {ind the augmenting path, the total running time of the Edmonds-Karp algorithm is O.VE<sup>2</sup> /.

#### **Exercises**

#### *24.2-1*

Prove that the summations in equation (24.6) equal the summations on the righthand side of equation (24.5).

#### *24.2-2*

In Figure 24.1(b), what is the net {low across the cut .fs; v2; v4g ; {v1; v3; tg/? What is the capacity of this cut?

#### *24.2-3*

Show the execution of the Edmonds-Karp algorithm on the {low network of Figure 24.1(a).

#### *24.2-4*

In the example of Figure 24.6, what is the minimum cut corresponding to the maximum {low shown? Of the augmenting paths appearing in the example, which one cancels {low?

## *24.2-5*

The construction in Section 24.1 to convert a {low network with multiple sources and sinks into a single-source, single-sink network adds edges with infinite capacity. Prove that any {low in the resulting network has a {inite value if the edges of the original network with multiple sources and sinks have {inite capacity.

### *24.2-6*

Suppose that each source s<sup>i</sup> in a {low network with multiple sources and sinks produces exactly p<sup>i</sup> units of {low, so that P v2V { .s<sup>i</sup> ; v/ D p<sup>i</sup> . Suppose also that each sink t<sup>j</sup> consumes exactly q<sup>j</sup> units, so that P v2V P { .v; t<sup>j</sup> / D q<sup>j</sup> , where <sup>i</sup> p<sup>i</sup> D P j q<sup>j</sup> . Show how to convert the problem of {inding a {low { that obeys these additional constraints into the problem of {inding a maximum {low in a singlesource, single-sink {low network.

#### *24.2-7*

Prove Lemma 24.2.

#### *24.2-8*

Suppose that we redefine the residual network to disallow edges into s. Argue that the procedure FORD-FULKERSON still correctly computes a maximum {low.

#### *24.2-9*

Suppose that both { and { 0 are {lows in a {low network. Does the augmented {low { " { 0 satisfy the {low conservation property? Does it satisfy the capacity constraint?

#### *24.2-10*

Show how to {ind a maximum {low in a {low network G = .V; E/ by a sequence of at most jEj augmenting paths. (*Hint:* Determine the paths *after* {inding the maximum {low.)

#### *24.2-11*

The *edge connectivity* of an undirected }raph is the minimum number k of edges that must be removed to disconnect the }raph. For example, the edge connectivity of a tree is 1, and the edge connectivity of a cyclic chain of vertices is 2. Show how to determine the edge connectivity of an undirected }raph G = .V; E/ by running a maximum-flow algorithm on at most jV j {low networks, each having O.V C E/ vertices and O.E/ edges.

#### *24.2-12*

You are }iven a {low network G, where G contains edges entering the source s. Let { be a {low in G with jf j 0 in which one of the edges .v; s/ entering 

the source has { .v; s/ D 1. Prove that there must exist another {low { <sup>0</sup> with { 0 .v; s/ D 0 such that jf j = jf 0 j. Give an O.E/-time algorithm to compute { 0 , }iven { and assuming that all edge capacities are integers.

## *24.2-13*

Suppose that you wish to {ind, among all minimum cuts in a {low network G with integer capacities, one that contains the smallest number of edges. Show how to modify the capacities of G to create a new {low network G<sup>0</sup> in which any minimum cut in G<sup>0</sup> is a minimum cut with the smallest number of edges in G.

## **24.3 Maximum bipartite matching**

Some combinatorial problems can be cast as maximum-flow problems, such as the multiple-source, multiple-sink maximum-flow problem {rom Section 24.1. Other combinatorial problems seem on the surface to have little to do with {low networks, but they can in {act be reduced to maximum-flow problems. This section presents one such problem: {inding a maximum matching in a bipartite }raph. In order to solve this problem, we'll take advantage of an integrality property provided by the Ford-Fulkerson method. We'll also see how to use the Ford-Fulkerson method to solve the maximum-bipartite-matching problem on a }raph G = .V; E/ in O.VE/ time. Section 25.1 will present an algorithm specifically designed to solve this problem.

#### **The maximum-bipartite-matching problem**

Given an undirected }raph G = .V; E/, a *matching* is a subset of edges M ෂ E such that {or all vertices v 2 V , at most one edge of M is incident on v. We say that a vertex v 2 V is *matched* by the matching M if some edge in M is incident on v, and otherwise, v is *unmatched*. A *maximum matching* is a matching of maximum cardinality, that is, a matching M such that {or any matching M<sup>0</sup> , we have jMj jM<sup>0</sup> j. In this section, we restrict our attention to {inding maximum matchings in bipartite }raphs: }raphs in which the vertex set can be partitioned into V = L [ R, where L and R are disjoint and all edges in E }o between L and R. We {urther assume that every vertex in V has at least one incident edge. Figure 24.8 illustrates the notion of a matching in a bipartite }raph.

The problem of {inding a maximum matching in a bipartite }raph has many practical applications. As an example, consider matching a set L of machines with a set R of tasks to be performed simultaneously. An edge .u; v/ in E signifies that