---
topic: path_compression_analysis
pages: 553-568
---

$$A_k(j) = \begin{cases} j+1 & \text{if } k = 0, \\ A_{k-1}^{(j+1)}(j) & \text{if } k \ge 1, \end{cases}$$
 (19.1)

where the expression A^(j+1)_(k-1)(j) uses the functional-iteration notation defined in equation (3.30) on page 68. Specifically, equation (3.30) gives A^(0)_(k-1)(j) = j and A^(i)_(k-1)(j) = A_(k-1)(A^(i-1)_(k-1)(j)) for i ≥ 1. We call the parameter k the *level* of the function A.

The function A_k(j) strictly increases with both j and k. To see just how quickly this function grows, we first obtain closed-form expressions for A₁(j) and A₂(j).

# *Lemma 19.2*

For any integer j ≥ 1, we have A₁(j) = 2j + 1.

*Proof* We first use induction on i to show that A^(i)_0(j) = j + i. For the base case, A^(0)_0(j) = j = j + 0. For the inductive step, assume that A^(i-1)_0(j) = j + (i - 1). Then A^(i)_0(j) = A₀(A^(i-1)_0(j)) = (j + (i - 1)) + 1 = j + i. Finally, we note that A₁(j) = A^(j+1)_0(j) = j + (j + 1) = 2j + 1.

# *Lemma 19.3*

For any integer j ≥ 1, we have A₂(j) = 2^(j+1)(j + 1) - 1.

*Proof* We first use induction on i to show that A^(i)_1(j) = 2^i(j + 1) - 1. For the base case, we have A^(0)_1(j) = j = 2^0(j + 1) - 1. For the inductive step, assume that A^(i-1)_1(j) = 2^(i-1)(j + 1) - 1. Then A^(i)_1(j) = A₁(A^(i-1)_1(j)) = A₁(2^(i-1)(j + 1) - 1) = 2(2^(i-1)(j + 1) - 1) + 1 = 2^i(j + 1) - 2 + 1 = 2^i(j + 1) - 1. Finally, we note that A₂(j) = A^(j+1)_1(j) = 2^(j+1)(j + 1) - 1.

Now we can see how quickly A_k(j) grows by simply examining A_k(1) for levels k = 0, 1, 2, 3, 4. From the definition of A₀(j) and the above lemmas, we have A₀(1) = 1 + 1 = 2, A₁(1) = 2 · 1 + 1 = 3, and A₂(1) = 2^(1+1)(1 + 1) - 1 = 7. We also have

$$A_3(1) = A_2^{(2)}(1)$$

$$= A_2(A_2(1))$$

$$= A_2(7)$$

$$= 2^8 \cdot 8 - 1$$

$$= 2^{11} - 1$$

$$= 2047$$

and

$$A_4(1) = A_3^{(2)}(1)$$

$$= A_3(A_3(1))$$

$$= A_2(2047)$$

$$= A_2^{(2048)}(2047)$$

$$\Rightarrow A_2(2047)$$

$$= 2^{2048} \cdot 2048 - 1$$

$$= 2^{2059} - 1$$

$$> 2^{2056}$$

$$= (2^4)^{514}$$

$$= 16^{514}$$

$$\Rightarrow 10^{80}$$

which is the estimated number of atoms in the observable universe. (The symbol ⇒ denotes the "much-greater-than" relation.)

We define the inverse of the function A_k(n), for integer n ≥ 0, by

$$\alpha(n) = \min\{k : A_k(1) \ge n\} \ . \tag{19.2}$$

In words, α(n) is the lowest level k for which A_k(1) is at least n. From the above values of A_k(1), we see that

$$\alpha(n) = \begin{cases} 0 & \text{for } 0 \le n \le 2, \\ 1 & \text{for } n = 3, \\ 2 & \text{for } 4 \le n \le 7, \\ 3 & \text{for } 8 \le n \le 2047, \\ 4 & \text{for } 2048 \le n \le A_4(1). \end{cases}$$

It is only for values of n so large that the term "astronomical" understates them (greater than A₄(1), a huge number) that α(n) > 4, and so α(n) ≤ 4 for all practical purposes.

### **Properties of ranks**

In the remainder of this section, we prove an O(m·α(n)) bound on the running time of the disjoint-set operations with union by rank and path compression. In order to prove this bound, we first prove some simple properties of ranks.

#### *Lemma 19.4*

For all nodes x, we have x:*rank* ≤ x:*p*:*rank*, with strict inequality if x ≠ x:*p* (x is not a root). The value of x:*rank* is initially 0, increases through time until x ≠ x:*p*, 

and from then on, x:*rank* does not change. The value of x:*p*:*rank* monotonically increases over time.

*Proof* The proof is a straightforward induction on the number of operations, using the implementations of MAKE-SET, UNION, and FIND-SET that appear on page 530, and is left as Exercise 19.4-1.

# *Corollary 19.5*

On the simple path from any node going up toward a root, node ranks strictly increase.

# *Lemma 19.6*

Every node has rank at most n - 1.

*Proof* Each node's rank starts at 0, and it increases only upon LINK operations. Because there are at most n - 1 UNION operations, there are also at most n - 1 LINK operations. Because each LINK operation either leaves all ranks alone or increases some node's rank by 1, all ranks are at most n - 1.

Lemma 19.6 provides a weak bound on ranks. In fact, every node has rank at most ⌊lg n⌋ (see Exercise 19.4-2). The looser bound of Lemma 19.6 suffices for our purposes, however.

#### **Proving the time bound**

In order to prove the O(m·α(n)) time bound, we'll use the potential method of amortized analysis from Section 16.3. In performing the amortized analysis, it will be convenient to assume that we invoke the LINK operation rather than the UNION operation. That is, since the parameters of the LINK procedure are pointers to two roots, we act as though we perform the appropriate FIND-SET operations separately. The following lemma shows that even if we count the extra FIND-SET operations induced by UNION calls, the asymptotic running time remains unchanged.

#### *Lemma 19.7*

Suppose that we convert a sequence S′ of m′ MAKE-SET, UNION, and FIND-SET operations into a sequence S of m MAKE-SET, LINK, and FIND-SET operations by turning each UNION into two FIND-SET operations followed by one LINK. Then, if sequence S runs in O(m·α(n)) time, sequence S′ runs in O(m′·α(n)) time.

*Proof* Since each UNION operation in sequence S′ is converted into three operations in S, we have m′ ≤ m ≤ 3m′, so that m = Θ(m′). Thus, an O(m·α(n)) 

time bound for the converted sequence S implies an O(m′·α(n)) time bound for the original sequence S′.

From now on, we assume that the initial sequence of m′ MAKE-SET, UNION, and FIND-SET operations has been converted to a sequence of m MAKE-SET, LINK, and FIND-SET operations. We now prove an O(m·α(n)) time bound for the converted sequence and appeal to Lemma 19.7 to prove the O(m′·α(n)) running time of the original sequence of m′ operations.

### **Potential function**

The potential function we use assigns a potential φ_q(x) to each node x in the disjoint-set forest after q operations. For the potential Φ^q of the entire forest after q operations, sum the individual node potentials: Φ^q = ∑_x φ_q(x). Because the forest is empty before the first operation, the sum is taken over an empty set, and so Φ^0 = 0. No potential Φ^q is ever negative.

The value of φ_q(x) depends on whether x is a tree root after the qth operation. If it is, or if x:*rank* = 0, then φ_q(x) = α(n) · x:*rank*.

Now suppose that after the qth operation, x is not a root and that x:*rank* ≥ 1. We need to define two auxiliary functions on x before we can define φ_q(x). First we define

$$level(x) = \max\{k : x.p.rank \ge A_k(x.rank)\}.$$
(19.3)

That is, level(x) is the greatest level k for which A_k, applied to x's rank, is no greater than x's parent's rank.

We claim that

$$0 \le \operatorname{level}(x) < \alpha(n) , \tag{19.4}$$

which we see as follows. We have

$$x.p.rank \ge x.rank + 1$$
 (by Lemma 19.4 because  $x$  is not a root)  
=  $A_0(x.rank)$  (by the definition (19.1) of  $A_0(j)$ ),

which implies that level(x) ≥ 0, and

$$A_{\alpha(n)}(x.rank) \ge A_{\alpha(n)}(1)$$
 (because  $A_k(j)$  is strictly increasing)  
 $\ge n$  (by the definition (19.2) of  $\alpha(n)$ )  
 $> x. \ p.rank$  (by Lemma 19.6),

which implies that level(x) < α(n).

For a given nonroot node x, the value of level(x) monotonically increases over time. Why? Because x is not a root, its rank does not change. The rank of x:*p*  

monotonically increases over time, since if x:*p* is not a root then its rank does not change, and if x:*p* is a root then its rank can never decrease. Thus, the difference between x:*rank* and x:*p*:*rank* monotonically increases over time. Therefore, the value of k needed for A_k(x:*rank*) to overtake x:*p*:*rank* monotonically increases over time as well.

The second auxiliary function applies when x:*rank* ≥ 1:

$$iter(x) = \max \left\{ i : x.p.rank \ge A_{level(x)}^{(i)}(x.rank) \right\}.$$
(19.5)

That is, iter(x) is the largest number of times we can iteratively apply A_level(x), applied initially to x's rank, before exceeding x's parent's rank.

We claim that when x:*rank* ≥ 1, we have

$$1 \le iter(x) \le x.rank, \tag{19.6}$$

which we see as follows. We have

$$x.p.rank \ge A_{\text{level}(x)}(x.rank)$$
 (by the definition (19.3) of level(x))  
=  $A_{\text{level}(x)}^{(1)}(x.rank)$  (by the definition (3.30) of functional iteration),

which implies that iter(x) ≥ 1. We also have

$$A_{\text{level}(x)}^{(x.rank+1)}(x.rank) = A_{\text{level}(x)+1}(x.rank)$$
 (by the definition (19.1) of  $A_k(j)$ )  
>  $x.p.rank$  (by the definition (19.3) of level( $x$ )),

which implies that iter(x) ≤ x:*rank*. Note that because x:*p*:*rank* monotonically increases over time, in order for iter(x) to decrease, level(x) must increase. As long as level(x) remains unchanged, iter(x) must either increase or remain unchanged.

With these auxiliary functions in place, we are ready to define the potential of node x after q operations:

$$\phi_q(x) = \begin{cases} \alpha(n) \cdot x. rank & \text{if } x \text{ is a root or } x. rank = 0, \\ (\alpha(n) - \text{level}(x)) \cdot x. rank - \text{iter}(x) & \text{if } x \text{ is not a root and } x. rank \ge 1. \end{cases}$$
(19.7)

We next investigate some useful properties of node potentials.

#### *Lemma 19.8*

For every node x, and for all operation counts q, we have

$$0 \le \phi_q(x) \le \alpha(n) \cdot x.rank$$
.

*Proof* If x is a root or x:*rank* = 0, then φ_q(x) = α(n) · x:*rank* by definition. Now suppose that x is not a root and that x:*rank* ≥ 1. We can obtain a lower bound on φ_q(x) by maximizing level(x) and iter(x). The bounds (19.4) and (19.6) give α(n) - level(x) ≥ 1 and iter(x) ≤ x:*rank*. Thus, we have

$$\phi_q(x) = (\alpha(n) - \text{level}(x)) \cdot x.rank - \text{iter}(x)$$

$$\geq x.rank - x.rank$$

$$= 0.$$

Similarly, minimizing level(x) and iter(x) provides an upper bound on φ_q(x). By the bound (19.4), level(x) ≥ 0, and by the bound (19.6), iter(x) ≥ 1. Thus, we have

$$\phi_q(x) \le (\alpha(n) - 0) \cdot x. rank - 1$$

$$= \alpha(n) \cdot x. rank - 1$$

$$< \alpha(n) \cdot x. rank.$$

# *Corollary 19.9*

If node x is not a root and x:*rank* > 0, then φ_q(x) < α(n) · x:*rank*.

#### **Potential changes and amortized costs of operations**

We are now ready to examine how the disjoint-set operations affect node potentials. Once we understand how each operation can change the potential, we can determine the amortized costs.

#### *Lemma 19.10*

Let x be a node that is not a root, and suppose that the qth operation is either a LINK or a FIND-SET. Then after the qth operation, φ_q(x) ≤ φ_(q-1)(x). Moreover, if x:*rank* ≥ 1 and either level(x) or iter(x) changes due to the qth operation, then φ_q(x) ≤ φ_(q-1)(x) - 1. That is, x's potential cannot increase, and if it has positive rank and either level(x) or iter(x) changes, then x's potential drops by at least 1.

*Proof* Because x is not a root, the qth operation does not change x:*rank*, and because n does not change after the initial n MAKE-SET operations, α(n) remains unchanged as well. Hence, these components of the formula for x's potential remain the same after the qth operation. If x:*rank* = 0, then φ_q(x) = φ_(q-1)(x) = 0.

Now assume that x:*rank* ≥ 1. Recall that level(x) monotonically increases over time. If the qth operation leaves level(x) unchanged, then iter(x) either increases or remains unchanged. If both level(x) and iter(x) are unchanged, then φ_q(x) = φ_(q-1)(x). If level(x) is unchanged and iter(x) increases, then it increases by at least 1, and so φ_q(x) ≤ φ_(q-1)(x) - 1.

Finally, if the qth operation increases level(x), it increases by at least 1, so that the value of the term (α(n) - level(x)) · x:*rank* drops by at least x:*rank*. Because level(x) increased, the value of iter(x) might drop, but according to the bound (19.6), the drop is by at most x:*rank* - 1. Thus, the increase in poten

tial due to the change in iter(x) is less than the decrease in potential due to the change in level(x), yielding φ_q(x) ≤ φ_(q-1)(x) - 1.

Our final three lemmas show that the amortized cost of each MAKE-SET, LINK, and FIND-SET operation is O(α(n)). Recall from equation (16.2) on page 456 that the amortized cost of each operation is its actual cost plus the change in potential due to the operation.

# *Lemma 19.11*

The amortized cost of each MAKE-SET operation is O(1).

*Proof* Suppose that the qth operation is MAKE-SET(x). This operation creates node x with rank 0, so that φ_q(x) = 0. No other ranks or potentials change, and so Φ^q = Φ^(q-1). Noting that the actual cost of the MAKE-SET operation is O(1) completes the proof.

# *Lemma 19.12*

The amortized cost of each LINK operation is O(α(n)).

*Proof* Suppose that the qth operation is LINK(x, y). The actual cost of the LINK operation is O(1). Without loss of generality, suppose that the LINK makes y the parent of x.

To determine the change in potential due to the LINK, note that the only nodes whose potentials may change are x, y, and the children of y just prior to the operation. We'll show that the only node whose potential can increase due to the LINK is y, and that its increase is at most α(n):

- By Lemma 19.10, any node that is y's child just before the LINK cannot have its potential increase due to the LINK.
- From the definition (19.7) of φ_q(x), note that, since x was a root just before the qth operation, φ_(q-1)(x) = α(n) · x:*rank* at that time. If x:*rank* = 0, then φ_q(x) = φ_(q-1)(x) = 0. Otherwise,

$$\phi_q(x) < \alpha(n)$$
 · x.rank (by Corollary 19.9)  
=  $\phi_{q-1}(x)$ ,

and so x's potential decreases.

 Because y is a root prior to the LINK, φ_(q-1)(y) = α(n) · y:*rank*. After the LINK operation, y remains a root, so that y's potential still equals α(n) times its rank after the operation. The LINK operation either leaves y's rank alone or increases y's rank by 1. Therefore, either φ_q(y) = φ_(q-1)(y) or φ_q(y) = φ_(q-1)(y) + α(n).

The increase in potential due to the LINK operation, therefore, is at most α(n). The amortized cost of the LINK operation is O(1) + α(n) = O(α(n)).

# *Lemma 19.13*

The amortized cost of each FIND-SET operation is O(α(n)).

*Proof* Suppose that the qth operation is a FIND-SET and that the find path contains s nodes. The actual cost of the FIND-SET operation is O(s). We will show that no node's potential increases due to the FIND-SET and that at least max{0, s - (α(n) + 2)} nodes on the find path have their potential decrease by at least 1.

We first show that no node's potential increases. Lemma 19.10 takes care of all nodes other than the root. If x is the root, then its potential is α(n) · x:*rank*, which does not change due to the FIND-SET operation.

Now we show that at least max{0, s - (α(n) + 2)} nodes have their potential decrease by at least 1. Let x be a node on the find path such that x:*rank* > 0 and x is followed somewhere on the find path by another node y that is not a root, where level(y) = level(x) just before the FIND-SET operation. (Node y need not *immediately* follow x on the find path.) All but at most α(n) + 2 nodes on the find path satisfy these constraints on x. Those that do not satisfy them are the first node on the find path (if it has rank 0), the last node on the path (i.e., the root), and the last node w on the path for which level(w) = k, for each k = 0, 1, 2, ..., α(n) - 1.

Consider such a node x. It has positive rank and is followed somewhere on the find path by nonroot node y such that level(y) = level(x) before the path compression occurs. We claim that the path compression decreases x's potential by at least 1. To prove this claim, let k = level(x) = level(y) and i = iter(x) before the path compression occurs. Just prior to the path compression caused by the FIND-SET, we have

```
x:p:rank ≥ A^(i)_k(x:rank) (by the definition (19.5) of iter(x)), 
y:p:rank ≥ A_k(y:rank) (by the definition (19.3) of level(y)), 
  y:rank ≥ x:p:rank (by Corollary 19.5 and because
                               y follows x on the find path).
```

Putting these inequalities together gives

```
y:p:rank ≥ A_k(y:rank)
         ≥ A_k(x:p:rank) (because A_k(j) is strictly increasing) 
         ≥ A_k(A^(i)_k(x:rank))
         = A^(i+1)_k(x:rank) (by the definition (3.30) of functional iteration).
```

Because path compression makes x and y have the same parent, after path compression we have x:*p*:*rank* = y:*p*:*rank*. The parent of y might change due to the path compression, but if it does, the rank of y's new parent compared with the rank of y's parent before path compression is either the same or greater. Since x:*rank* does not change, x:*p*:*rank* = y:*p*:*rank* ≥ A^(i+1)_k(x:*rank*) after path compression. By the definition (19.5) of the iter function, the value of iter(x) increases from i to at least i + 1. By Lemma 19.10, φ_q(x) ≤ φ_(q-1)(x) - 1, so that x's potential decreases by at least 1.

The amortized cost of the FIND-SET operation is the actual cost plus the change in potential. The actual cost is O(s), and we have shown that the total potential decreases by at least max{0, s - (α(n) + 2)}. The amortized cost, therefore, is at most O(s) - (s - (α(n) + 2)) = O(s) - s + O(α(n)) = O(α(n)), since we can scale up the units of potential to dominate the constant hidden in O(s). (See Exercise 19.4-6.)

Putting the preceding lemmas together yields the following theorem.

#### *Theorem 19.14*

A sequence of m MAKE-SET, UNION, and FIND-SET operations, n of which are MAKE-SET operations, can be performed on a disjoint-set forest with union by rank and path compression in O(m·α(n)) time.

*Proof* Immediate from Lemmas 19.7, 19.11, 19.12, and 19.13.

#### **Exercises**

#### *19.4-1*

Prove Lemma 19.4.

# *19.4-2*

Prove that every node has rank at most ⌊lg n⌋.

#### *19.4-3*

In light of Exercise 19.4-2, how many bits are necessary to store x:*rank* for each node x?

# *19.4-4*

Using Exercise 19.4-2, give a simple proof that operations on a disjoint-set forest with union by rank but without path compression run in O(m lg n) time.

# *19.4-5*

Professor Dante reasons that because node ranks increase strictly along a simple path to the root, node levels must monotonically increase along the path. In other words, if x:*rank* > 0 and x:*p* is not a root, then level(x) ≤ level(x:*p*). Is the professor correct?

# *19.4-6*

The proof of Lemma 19.13 ends with scaling the units of potential to dominate the constant hidden in the O(s) term. To be more precise in the proof, you need to change the definition (19.7) of the potential function to multiply each of the two cases by a constant, say c, that dominates the constant in the O(s) term. How must the rest of the analysis change to accommodate this updated potential function?

# ⋆ *19.4-7*

Consider the function α′(n) = min{k : A_k(1) ≥ lg(n + 1)}. Show that α′(n) ≤ 3 for all practical values of n and, using Exercise 19.4-2, show how to modify the potential-function argument to prove that performing a sequence of m MAKE-SET, UNION, and FIND-SET operations, n of which are MAKE-SET operations, on a disjoint-set forest with union by rank and path compression takes O(m·α′(n)) time.

# **Problems**

#### *19-1 Offline minimum*

In the *offline minimum problem*, you maintain a dynamic set T of elements from the domain {1, 2, ..., n} under the operations INSERT and EXTRACT-MIN. The input is a sequence S of n INSERT and m EXTRACT-MIN calls, where each key in {1, 2, ..., n} is inserted exactly once. Your goal is to determine which key is returned by each EXTRACT-MIN call. Specifically, you must fill in an array *extracted*[1:m], where for i = 1, 2, ..., m, *extracted*[i] is the key returned by the ith EXTRACT-MIN call. The problem is "offline" in the sense that you are allowed to process the entire sequence S before determining any of the returned keys.

*a.* Consider the following instance of the offline minimum problem, in which each operation INSERT(i) is represented by the value of i and each EXTRACT-MIN is represented by the letter E:

```
4, 8, E, 3, E, 9, 2, 6, E, E, E, 1, 7, E, 5.
```

Fill in the correct values in the *extracted* array.

To develop an algorithm for this problem, break the sequence S into homogeneous subsequences. That is, represent S by

```
I₁, E, I₂, E, I₃, ..., Iₘ, E, I_(m+1),
```

where each E represents a single EXTRACT-MIN call and each Iⱼ represents a (possibly empty) sequence of INSERT calls. For each subsequence Iⱼ, initially place the keys inserted by these operations into a set Kⱼ, which is empty if Iⱼ is empty. Then execute the OFFLINE-MINIMUM procedure.

```
OFFLINE-MINIMUM(m, n)
1 for i = 1 to n
2     determine j such that i ∈ Kⱼ
3     if j ≠ m + 1
4         extracted[j] = i
5         let l be the smallest value greater than j for which set K_l exists 
6         K_l = Kⱼ ∪ K_l, destroying Kⱼ
7 return extracted
```

- *b.* Argue that the array *extracted* returned by OFFLINE-MINIMUM is correct.
- *c.* Describe how to implement OFFLINE-MINIMUM efficiently with a disjoint-set data structure. Give as tight a bound as you can on the worst-case running time of your implementation.

#### *19-2 Depth determination*

In the *depth-determination problem*, you maintain a forest F = {Tᵢ} of rooted trees under three operations:

MAKE-TREE(v) creates a tree whose only node is v.

FIND-DEPTH(v) returns the depth of node v within its tree.

GRAFT(r, v) makes node r, which is assumed to be the root of a tree, become the child of node v, which is assumed to be in a different tree from r but may or may not itself be a root.

*a.* Suppose that you use a tree representation similar to a disjoint-set forest: v:*p* is the parent of node v, except that v:*p* = v if v is a root. Suppose further that you implement GRAFT(r, v) by setting r:*p* = v and FIND-DEPTH(v) by following the find path from v up to the root, returning a count of all nodes other than v encountered. Show that the worst-case running time of a sequence of m MAKE-TREE, FIND-DEPTH, and GRAFT operations is Θ(m²).

By using the union-by-rank and path-compression heuristics, you can reduce the worst-case running time. Use the disjoint-set forest S = {Sᵢ}, where each set Sᵢ (which is itself a tree) corresponds to a tree Tᵢ in the forest F. The tree structure within a set Sᵢ, however, does not necessarily correspond to that of Tᵢ. In fact, the implementation of Sᵢ does not record the exact parent-child relationships but nevertheless allows you to determine any node's depth in Tᵢ.

The key idea is to maintain in each node v a "pseudodistance" v:*d*, which is defined so that the sum of the pseudodistances along the simple path from v to the root of its set Sᵢ equals the depth of v in Tᵢ. That is, if the simple path from v to its root in Sᵢ is v₀, v₁, ..., v_k, where v₀ = v and v_k is Sᵢ's root, then the depth of v in Tᵢ is ∑ᵏⱼ₌₀ vⱼ:*d*.

- *b.* Give an implementation of MAKE-TREE.
- *c.* Show how to modify FIND-SET to implement FIND-DEPTH. Your implementation should perform path compression, and its running time should be linear in the length of the find path. Make sure that your implementation updates pseudodistances correctly.
- *d.* Show how to implement GRAFT(r, v), which combines the sets containing r and v, by modifying the UNION and LINK procedures. Make sure that your implementation updates pseudodistances correctly. Note that the root of a set Sᵢ is not necessarily the root of the corresponding tree Tᵢ.
- *e.* Give a tight bound on the worst-case running time of a sequence of m MAKE-TREE, FIND-DEPTH, and GRAFT operations, n of which are MAKE-TREE operations.

#### *19-3 Tarjan's offline lowest-common-ancestors algorithm*

The *lowest common ancestor* of two nodes u and v in a rooted tree T is the node w that is an ancestor of both u and v and that has the greatest depth in T. In the *offline lowest-common-ancestors problem*, you are given a rooted tree T and an arbitrary set P = {{u, v}} of unordered pairs of nodes in T, and you wish to determine the lowest common ancestor of each pair in P.

To solve the offline lowest-common-ancestors problem, the LCA procedure on the following page performs a tree walk of T with the initial call LCA(T:*root*). Assume that each node is colored WHITE prior to the walk.

- *a.* Argue that line 10 executes exactly once for each pair {u, v} ∈ P.
- *b.* Argue that at the time of the call LCA(u), the number of sets in the disjoint-set data structure equals the depth of u in T.

```
LCA(u)
1 MAKE-SET(u)
2 FIND-SET(u):ancestor = u
3 for each child v of u in T
4     LCA(v)
5     UNION(u, v)
6     FIND-SET(u):ancestor = u
7 u:color = BLACK
8 for each node v such that {u, v} ∈ P
9     if v:color == BLACK
10         print "The lowest common ancestor of" 
              u "and" v "is" FIND-SET(v):ancestor
```

- *c.* Prove that LCA correctly prints the lowest common ancestor of u and v for each pair {u, v} ∈ P.
- *d.* Analyze the running time of LCA, assuming that you use the implementation of the disjoint-set data structure in Section 19.3.

# **Chapter notes**

Many of the important results for disjoint-set data structures are due at least in part to R. E. Tarjan. Using aggregate analysis, Tarjan [427, 429] gave the first tight upper bound in terms of the very slowly growing inverse α(m, n) of Ackermann's function. (The function A_k(j) given in Section 19.4 is similar to Ackermann's function, and the function α(n) is similar to α(m, n). Both α(n) and α(m, n) are at most 4 for all conceivable values of m and n.) An upper bound of O(m lg n) was proven earlier by Hopcroft and Ullman [5, 227]. The treatment in Section 19.4 is adapted from a later analysis by Tarjan [431], which is based on an analysis by Kozen [270]. Harfst and Reingold [209] give a potential-based version of Tarjan's earlier bound.

Tarjan and van Leeuwen [432] discuss variants on the path-compression heuristic, including "one-pass methods," which sometimes offer better constant factors in their performance than do two-pass methods. As with Tarjan's earlier analyses of the basic path-compression heuristic, the analyses by Tarjan and van Leeuwen are aggregate. Harfst and Reingold [209] later showed how to make a small change to the potential function to adapt their path-compression analysis to these one-pass variants. Goel et al. [182] prove that linking disjoint-set trees randomly yields the 

same asymptotic running time as union by rank. Gabow and Tarjan [166] show that in certain applications, the disjoint-set operations can be made to run in O(m) time.

Tarjan [428] showed that a lower bound of Ω(m·α(m, n)) time is required for operations on any disjoint-set data structure satisfying certain technical conditions. This lower bound was later generalized by Fredman and Saks [155], who showed that in the worst case, Ω(m·α(m, n) / lg n)-bit words of memory must be accessed.

# **Introduction**

Graph problems pervade computer science, and algorithms for working with them are fundamental to the field. Hundreds of interesting computational problems are couched in terms of graphs. This part touches on a few of the more significant ones.

Chapter 20 shows how to represent a graph in a computer and then discusses algorithms based on searching a graph using either breadth-first search or depthfirst search. The chapter gives two applications of depth-first search: topologically sorting a directed acyclic graph and decomposing a directed graph into its strongly connected components.

Chapter 21 describes how to compute a minimum-weight spanning tree of a graph: the least-weight way of connecting all of the vertices together when each edge has an associated weight. The algorithms for computing minimum spanning trees serve as good examples of greedy algorithms (see Chapter 15).

Chapters 22 and 23 consider how to compute shortest paths between vertices when each edge has an associated length or "weight." Chapter 22 shows how to find shortest paths from a given source vertex to all other vertices, and Chapter 23 examines methods to compute shortest paths between every pair of vertices.

Chapter 24 shows how to compute a maximum flow of material in a flow network, which is a directed graph having a specified source vertex of material, a specified sink vertex, and specified capacities for the amount of material that can traverse each directed edge. This general problem arises in many forms, and a good algorithm for computing maximum flows can help solve a variety of related problems efficiently.

Finally, Chapter 25 explores matchings in bipartite graphs: methods for pairing up vertices that are partitioned into two sets by selecting edges that go between the sets. Bipartite-matching problems model several situations that arise in the real world. The chapter examines how to find a matching of maximum cardinality; the