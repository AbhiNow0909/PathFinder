---
topic: recurrence_recursion_tree
pages: 117-122
---

**Figure 4.1** Constructing a recursion tree for the recurrence T(n) = 3T(n/4) + cn². Part **(a)** shows T(n), which progressively expands in **(b)–(d)** to form the recursion tree. The fully expanded tree in **(d)** has height log₄ n.

subproblems of size n/4. Part (c) shows this process carried one step further by expanding each node with cost T(n/4) from part (b). The cost for each of the three children of the root is c(n/4)². We continue expanding each node in the tree by breaking it into its constituent parts as determined by the recurrence.

Because subproblem sizes decrease by a factor of 4 every time we go down one level, the recursion must eventually bottom out in a base case where n < n₀. By convention, the base case is T(n) = Θ(1) for n < n₀, where n₀ > 0 is any threshold constant sufficiently large that the recurrence is well defined. For the purpose of intuition, however, let's simplify the math a little. Let's assume that n is an exact power of 4 and that the base case is T(1) = Θ(1). As it turns out, these assumptions don't affect the asymptotic solution.

What's the height of the recursion tree? The subproblem size for a node at depth i is n/4ⁱ. As we descend the tree from the root, the subproblem size hits n = 1 when n/4ⁱ = 1 or, equivalently, when i = log₄ n. Thus, the tree has internal nodes at depths 0, 1, 2, ..., log₄ n - 1 and leaves at depth log₄ n.

Part (d) of Figure 4.1 shows the cost at each level of the tree. Each level has three times as many nodes as the level above, and so the number of nodes at depth i is 3ⁱ. Because subproblem sizes reduce by a factor of 4 for each level further from the root, each internal node at depth i = 0, 1, 2, ..., log₄ n - 1 has a cost of c(n/4ⁱ)². Multiplying, we see that the total cost of all nodes at a given depth i is 3ⁱc(n/4ⁱ)² = (3/16)ⁱcn². The bottom level, at depth log₄ n, contains 3^(log₄ n) = n^(log₄ 3) leaves (using equation (3.21) on page 66). Each leaf contributes Θ(1), leading to a total leaf cost of Θ(n^(log₄ 3)).

Now we add up the costs over all levels to determine the cost for the entire tree:

$$T(n) = cn^{2} + \frac{3}{16}cn^{2} + \left(\frac{3}{16}\right)^{2}cn^{2} + \dots + \left(\frac{3}{16}\right)^{\log_{4}n}cn^{2} + \Theta(n^{\log_{4}3})$$

$$= \sum_{i=0}^{\log_{4}n} \left(\frac{3}{16}\right)^{i}cn^{2} + \Theta(n^{\log_{4}3})$$

$$< \sum_{i=0}^{\infty} \left(\frac{3}{16}\right)^{i}cn^{2} + \Theta(n^{\log_{4}3})$$

$$= \frac{1}{1 - (3/16)}cn^{2} + \Theta(n^{\log_{4}3}) \qquad \text{(by equation (A.7) on page 1142)}$$

$$= \frac{16}{13}cn^{2} + \Theta(n^{\log_{4}3})$$

$$= O(n^{2}) \qquad (\Theta(n^{\log_{4}3}) = O(n^{0.8}) = O(n^{2})).$$

We've derived the guess of T(n) = O(n²) for the original recurrence. In this example, the coefficients of cn² form a decreasing geometric series. By equation (A.7), the sum of these coefficients is bounded from above by the constant 16/13. Since 

the root's contribution to the total cost is cn², the cost of the root dominates the total cost of the tree.

In fact, if O(n²) is indeed an upper bound for the recurrence (as we'll verify in a moment), then it must be a tight bound. Why? The first recursive call contributes a cost of Θ(n²), and so Ω(n²) must be a lower bound for the recurrence.

Let's now use the substitution method to verify that our guess is correct, namely, that T(n) = O(n²) is an upper bound for the recurrence T(n) = 3T(n/4) + Θ(n²). We want to show that T(n) ≤ dn² for some constant d > 0. Using the same constant c > 0 as before, we have

$$T(n) \le 3T(n/4) + cn^2 \le 3d(n/4)^2 + cn^2 = \frac{3}{16} dn^2 + cn^2 \le dn^2,$$

where the last step holds if we choose d ≥ (16/13)c.

For the base case of the induction, let n₀ > 0 be a sufficiently large threshold constant that the recurrence is well defined when T(n) = Θ(1) for n < n₀. We can pick d large enough that d dominates the constant hidden by the Θ, in which case dn² ≥ T(n) for 1 ≤ n < n₀, completing the proof of the base case.

The substitution proof we just saw involves two named constants, c and d. We named c and used it to stand for the upper-bound constant hidden and guaranteed to exist by the Θ-notation. We cannot pick c arbitrarily—it's given to us—although, for any such c, any constant c′ ≥ c also suffices. We also named d, but we were free to choose any value for it that fit our needs. In this example, the value of d happened to depend on the value of c, which is fine, since d is constant if c is constant.

#### **An irregular example**

Let's find an asymptotic upper bound for another, more irregular, example. Figure 4.2 shows the recursion tree for the recurrence

$$T(n) = T(n/3) + T(2n/3) + \Theta(n).$$
(4.14)

This recursion tree is unbalanced, with different root-to-leaf paths having different lengths. Going left at any node produces a subproblem of one-third the size, and going right produces a subproblem of two-thirds the size. Let n₀ > 0 be the implicit threshold constant such that T(n) = Θ(1) for 0 < n < n₀, and let c represent the upper-bound constant hidden by the Θ(n) term for n ≥ n₀. There are actually two n₀ constants here—one for the threshold in the recurrence, and the other for the threshold in the Θ-notation, so we'll let n₀ be the larger of the two constants.

**Figure 4.2** A recursion tree for the recurrence T(n) = T(n/3) + T(2n/3) + cn.

The height of the tree runs down the right edge of the tree, corresponding to subproblems of sizes n, (2/3)n, (4/9)n, ..., Θ(1) with costs bounded by cn, c(2n/3), c(4n/9), ..., Θ(1), respectively. We hit the rightmost leaf when (2/3)ʰn < n₀ ≤ (2/3)^(h-1)n, which happens when h = ⌊log₃/₂(n/n₀)⌋ + 1 since, applying the floor bounds in equation (3.2) on page 64 with x = log₃/₂(n/n₀), we have (2/3)ʰn = (2/3)^(⌊x⌋+1)n < (2/3)ˣn = (n₀/n)n = n₀ and (2/3)^(h-1)n = (2/3)^⌊x⌋n > (2/3)ˣn = (n₀/n)n = n₀. Thus, the height of the tree is h = Θ(lg n).

We're now in a position to understand the upper bound. Let's postpone dealing with the leaves for a moment. Summing the costs of internal nodes across each level, we have at most cn per level times the Θ(lg n) tree height for a total cost of O(n lg n) for all internal nodes.

It remains to deal with the leaves of the recursion tree, which represent base cases, each costing Θ(1). How many leaves are there? It's tempting to upperbound their number by the number of leaves in a complete binary tree of height h = ⌊log₃/₂(n/n₀)⌋ + 1, since the recursion tree is contained within such a complete binary tree. But this approach turns out to give us a poor bound. The complete binary tree has 1 node at the root, 2 nodes at depth 1, and generally 2ᵏ nodes at depth k. Since the height is h = ⌊log₃/₂ n⌋ + 1, there are 

2ʰ = 2^(⌊log₃/₂ n⌋+1) ≤ 2n^(log₃/₂ 2) leaves in the complete binary tree, which is an upper bound on the number of leaves in the recursion tree. Because the cost of each leaf is Θ(1), this analysis says that the total cost of all leaves in the recursion tree is O(n^(log₃/₂ 2)) = O(n^1.71), which is an asymptotically greater bound than the O(n lg n) cost of all internal nodes. In fact, as we're about to see, this bound is not tight. The cost of all leaves in the recursion tree is O(n)—asymptotically *less*  than O(n lg n). In other words, the cost of the internal nodes dominates the cost of the leaves, not vice versa.

Rather than analyzing the leaves, we could quit right now and prove by substitution that T(n) = Θ(n lg n). This approach works (see Exercise 4.4-3), but it's instructive to understand how many leaves this recursion tree has. You may see recurrences for which the cost of leaves dominates the cost of internal nodes, and then you'll be in better shape if you've had some experience analyzing the number of leaves.

To figure out how many leaves there really are, let's write a recurrence L(n) for the number of leaves in the recursion tree for T(n). Since all the leaves in T(n) belong either to the left subtree or the right subtree of the root, we have

$$L(n) = \begin{cases} 1 & \text{if } n < n_0, \\ L(n/3) + L(2n/3) & \text{if } n \ge n_0. \end{cases}$$
 (4.15)

This recurrence is similar to recurrence (4.14), but it's missing the Θ(n) term, and it contains an explicit base case. Because this recurrence omits the Θ(n) term, it is much easier to solve. Let's apply the substitution method to show that it has solution L(n) = O(n). Using the inductive hypothesis L(n) ≤ dn for some constant d > 0, and assuming that the inductive hypothesis holds for all values less than n, we have

$$L(n) = L(n/3) + L(2n/3) \leq dn/3 + 2(dn)/3 \leq dn,$$

which holds for any d > 0. We can now choose d large enough to handle the base case L(n) = 1 for 0 < n < n₀, for which d = 1 suffices, thereby completing the substitution method for the upper bound on leaves. (Exercise 4.4-2 asks you to prove that L(n) = Ω(n).)

Returning to recurrence (4.14) for T(n), it now becomes apparent that the total cost of leaves over all levels must be L(n)Θ(1) = Θ(n). Since we have derived the bound of O(n lg n) on the cost of the internal nodes, it follows that the solution to recurrence (4.14) is T(n) = O(n lg n) + Θ(n) = O(n lg n). (Exercise 4.4-3 asks you to prove that T(n) = Ω(n lg n).)

It's wise to verify any bound obtained with a recursion tree by using the substitution method, especially if you've made simplifying assumptions. But another 

strategy altogether is to use more-powerful mathematics, typically in the form of the master method in the next section (which unfortunately doesn't apply to recurrence (4.14)) or the Akra-Bazzi method (which does, but requires calculus). Even if you use a powerful method, a recursion tree can improve your intuition for what's going on beneath the heavy math.

## **Exercises**

# *4.4-1*

For each of the following recurrences, sketch its recursion tree, and guess a good asymptotic upper bound on its solution. Then use the substitution method to verify your answer.

- *a.* T(n) = T(n/2) + n³.
- *b.* T(n) = 4T(n/3) + n.
- *c.* T(n) = 4T(n/2) + n.
- *d.* T(n) = 3T(n - 1) + 1.

# *4.4-2*

Use the substitution method to prove that recurrence (4.15) has the asymptotic lower bound L(n) = Ω(n). Conclude that L(n) = Θ(n).

## *4.4-3*

Use the substitution method to prove that recurrence (4.14) has the solution T(n) = Ω(n lg n). Conclude that T(n) = Θ(n lg n).

## *4.4-4*

Use a recursion tree to justify a good guess for the solution to the recurrence T(n) = T(αn) + T((1 - α)n) + Θ(n), where α is a constant in the range 0 < α < 1.

# **4.5 The master method for solving recurrences**

The master method provides a "cookbook" method for solving algorithmic recurrences of the form

$$T(n) = aT(n/b) + f(n),$$
 (4.16)

where a > 0 and b > 1 are constants. We call f(n) a *driving function*, and we call a recurrence of this general form a *master recurrence*. To use the master method, you need to memorize three cases, but then you'll be able to solve many master recurrences quite easily.