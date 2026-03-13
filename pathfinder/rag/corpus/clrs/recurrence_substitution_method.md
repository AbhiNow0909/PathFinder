---
topic: recurrence_substitution_method
pages: 112-116
---

constraints they need to obey. If we can establish this inductive hypothesis, we can conclude that T(n) = O(n lg n). It would be dangerous to use T(n) = O(n lg n) as the inductive hypothesis because the constants matter, as we'll see in a moment in our discussion of pitfalls.

Assume by induction that this bound holds for all numbers at least as big as n₀ and less than n. In particular, therefore, if n ≥ 2n₀, it holds for ⌊n/2⌋, yielding T(⌊n/2⌋) ≤ c⌊n/2⌋lg(⌊n/2⌋). Substituting into recurrence (4.11)—hence the name "substitution" method—yields

```
T(n) ≤ 2(c⌊n/2⌋lg(⌊n/2⌋)) + Θ(n)
     ≤ 2(c(n/2)lg(n/2)) + Θ(n)
     = cn lg(n/2) + Θ(n)
     = cn lg n - cn lg 2 + Θ(n)
     = cn lg n - cn + Θ(n)
     ≤ cn lg n ;
```

where the last step holds if we constrain the constants n₀ and c to be sufficiently large that for n ≥ 2n₀, the quantity cn dominates the anonymous function hidden by the Θ(n) term.

We've shown that the inductive hypothesis holds for the inductive case, but we also need to prove that the inductive hypothesis holds for the base cases of the induction, that is, that T(n) ≤ cn lg n when n₀ ≤ n < 2n₀. As long as n₀ > 1 (a new constraint on n₀), we have lg n > 0, which implies that n lg n > 0. So let's pick n₀ = 2. Since the base case of recurrence (4.11) is not stated explicitly, by our convention, T(n) is algorithmic, which means that T(2) and T(3) are constant (as they should be if they describe the worst-case running time of any real program on inputs of size 2 or 3). Picking c = max{T(2), T(3)} yields T(2) ≤ c < (2 lg 2)c and T(3) ≤ c < (3 lg 3)c, establishing the inductive hypothesis for the base cases.

Thus, we have T(n) ≤ cn lg n for all n ≥ 2, which implies that the solution to recurrence (4.11) is T(n) = O(n lg n).

In the algorithms literature, people rarely carry out their substitution proofs to this level of detail, especially in their treatment of base cases. The reason is that for most algorithmic divide-and-conquer recurrences, the base cases are all handled in pretty much the same way. You ground the induction on a range of values from a convenient positive constant n₀ up to some constant n′₀ > n₀ such that for n ≥ n′₀, the recurrence always bottoms out in a constant-sized base case between n₀ and n′₀. (This example used n′₀ = 2n₀.) Then, it's usually apparent, without spelling out the details, that with a suitably large choice of the leading constant (such as c for this example), the inductive hypothesis can be made to hold for all the values in the range from n₀ to n′₀.

## **Making a good guess**

Unfortunately, there is no general way to correctly guess the tightest asymptotic solution to an arbitrary recurrence. Making a good guess takes experience and, occasionally, creativity. Fortunately, learning some recurrence-solving heuristics, as well as playing around with recurrences to gain experience, can help you become a good guesser. You can also use recursion trees, which we'll see in Section 4.4, to help generate good guesses.

If a recurrence is similar to one you've seen before, then guessing a similar solution is reasonable. As an example, consider the recurrence

$$T(n) = 2T(n/2 + 17) + \Theta(n)$$
,

defined on the reals. This recurrence looks somewhat like the merge-sort recurrence (2.3), but it's more complicated because of the added "17" in the argument to T on the right-hand side. Intuitively, however, this additional term shouldn't substantially affect the solution to the recurrence. When n is large, the relative difference between n/2 and n/2 + 17 is not that large: both cut n nearly in half. Consequently, it makes sense to guess that T(n) = O(n lg n), which you can verify is correct using the substitution method (see Exercise 4.3-1).

Another way to make a good guess is to determine loose upper and lower bounds on the recurrence and then reduce your range of uncertainty. For example, you might start with a lower bound of T(n) = Ω(n) for recurrence (4.11), since the recurrence includes the term Θ(n), and you can prove an initial upper bound of T(n) = O(n²). Then split your time between trying to lower the upper bound and trying to raise the lower bound until you converge on the correct, asymptotically tight solution, which in this case is T(n) = Θ(n lg n).

#### **A trick of the trade: subtracting a low-order term**

Sometimes, you might correctly guess a tight asymptotic bound on the solution of a recurrence, but somehow the math fails to work out in the induction proof. The problem frequently turns out to be that the inductive assumption is not strong enough. The trick to resolving this problem is to revise your guess by *subtracting* a lower-order term when you hit such a snag. The math then often goes through.

Consider the recurrence

$$T(n) = 2T(n/2) + \Theta(1) \tag{4.12}$$

defined on the reals. Let's guess that the solution is T(n) = O(n) and try to show that T(n) ≤ cn for n ≥ n₀, where we choose the constants c, n₀ > 0 suitably. Substituting our guess into the recurrence, we obtain

$$T(n) \le 2(c(n/2)) + \Theta(1)$$
  
=  $cn + \Theta(1)$ ,

which, unfortunately, does not imply that T(n) ≤ cn for *any* choice of c. We might be tempted to try a larger guess, say T(n) = O(n²). Although this larger guess works, it provides only a loose upper bound. It turns out that our original guess of T(n) = O(n) is correct and tight. In order to show that it is correct, however, we must strengthen our inductive hypothesis.

Intuitively, our guess is nearly right: we are off only by Θ(1), a lower-order term. Nevertheless, mathematical induction requires us to prove the *exact* form of the inductive hypothesis. Let's try our trick of subtracting a lower-order term from our previous guess: T(n) ≤ cn - d, where d ≥ 0 is a constant. We now have

$$T(n) \leq 2(c(n/2) - d) + \Theta(1)$$

$$= cn - 2d + \Theta(1)$$

$$\leq cn - d - (d - \Theta(1))$$

$$\leq cn - d$$

as long as we choose d to be larger than the anonymous upper-bound constant hidden by the Θ-notation. Subtracting a lower-order term works! Of course, we must not forget to handle the base case, which is to choose the constant c large enough that cn - d dominates the implicit base cases.

You might find the idea of subtracting a lower-order term to be counterintuitive. After all, if the math doesn't work out, shouldn't you increase your guess? Not necessarily! When the recurrence contains more than one recursive invocation (recurrence (4.12) contains two), if you add a lower-order term to the guess, then you end up adding it once for each of the recursive invocations. Doing so takes you even further away from the inductive hypothesis. On the other hand, if you subtract a lower-order term from the guess, then you get to subtract it once for each of the recursive invocations. In the above example, we subtracted the constant d twice because the coefficient of T(n/2) is 2. We ended up with the inequality T(n) ≤ cn - d - (d - Θ(1)), and we readily found a suitable value for d.

## **Avoiding pitfalls**

Avoid using asymptotic notation in the inductive hypothesis for the substitution method because it's error prone. For example, for recurrence (4.11), we can falsely "prove" that T(n) = O(n) if we unwisely adopt T(n) = O(n) as our inductive hypothesis:

$$T(n) \leq 2 \cdot O(\lfloor n/2 \rfloor) + \Theta(n)$$

$$= 2 \cdot O(n) + \Theta(n)$$

$$= O(n) . \iff wrong!$$

The problem with this reasoning is that the constant hidden by the O-notation changes. We can expose the fallacy by repeating the "proof" using an explicit constant. For the inductive hypothesis, assume that T(n) ≤ cn for all n ≥ n₀, where c, n₀ > 0 are constants. Repeating the first two steps in the inequality chain yields

$$T(n) \le 2(c \lfloor n/2 \rfloor) + \Theta(n)$$
  
  $\le cn + \Theta(n)$ .

Now, indeed cn + Θ(n) = O(n), but the constant hidden by the O-notation must be larger than c because the anonymous function hidden by the Θ(n) is asymptotically positive. We cannot take the third step to conclude that cn + Θ(n) ≤ cn, thus exposing the fallacy.

When using the substitution method, or more generally mathematical induction, you must be careful that the constants hidden by any asymptotic notation are the same constants throughout the proof. Consequently, it's best to avoid asymptotic notation in your inductive hypothesis and to name constants explicitly.

Here's another {allacious use of the substitution method to show that the solution to recurrence (4.11) is T .n/ D O.n/. We }uess T .n/ ≤ cn and then argue

$$T(n) \leq 2(c \lfloor n/2 \rfloor) + \Theta(n)$$
  
$$\leq cn + \Theta(n)$$
  
$$= O(n), \qquad \longleftarrow wrong!$$

since c is a positive constant. The mistake stems from the difference between our goal—to prove that T(n) = O(n)—and our inductive hypothesis—to prove that T(n) ≤ cn. When using the substitution method, or in any inductive proof, you must prove the *exact* statement of the inductive hypothesis. In this case, we must explicitly prove that T(n) ≤ cn to show that T(n) = O(n).

#### **Exercises**

## *4.3-1*

Use the substitution method to show that each of the following recurrences defined on the reals has the asymptotic solution specified:

- *a.* T(n) = T(n - 1) + n has solution T(n) = O(n²).
- *b.* T(n) = T(n/2) + Θ(1) has solution T(n) = O(lg n).
- *c.* T(n) = 2T(n/2) + n has solution T(n) = Θ(n lg n).
- *d.* T(n) = 2T(n/2 + 17) + n has solution T(n) = O(n lg n).
- *e.* T(n) = 2T(n/3) + Θ(n) has solution T(n) = Θ(n).
- *f.* T(n) = 4T(n/2) + Θ(n) has solution T(n) = Θ(n²).

# *4.3-2*

The solution to the recurrence T(n) = 4T(n/2) + n turns out to be T(n) = Θ(n²). Show that a substitution proof with the assumption T(n) ≤ cn² fails. Then show how to subtract a lower-order term to make a substitution proof work.

## *4.3-3*

The recurrence T(n) = 2T(n - 1) + 1 has the solution T(n) = O(2ⁿ). Show that a substitution proof fails with the assumption T(n) ≤ c2ⁿ, where c > 0 is constant. Then show how to subtract a lower-order term to make a substitution proof work.

# **4.4 The recursion-tree method for solving recurrences**

Although you can use the substitution method to prove that a solution to a recurrence is correct, you might have trouble coming up with a good guess. Drawing out a recursion tree, as we did in our analysis of the merge-sort recurrence in Section 2.3.2, can help. In a *recursion tree*, each node represents the cost of a single subproblem somewhere in the set of recursive function invocations. You typically sum the costs within each level of the tree to obtain the per-level costs, and then you sum all the per-level costs to determine the total cost of all levels of the recursion. Sometimes, however, adding up the total cost takes more creativity.

A recursion tree is best used to generate intuition for a good guess, which you can then verify by the substitution method. If you are meticulous when drawing out a recursion tree and summing the costs, however, you can use a recursion tree as a direct proof of a solution to a recurrence. But if you use it only to generate a good guess, you can often tolerate a small amount of "sloppiness," which can simplify the math. When you verify your guess with the substitution method later on, your math should be precise. This section demonstrates how you can use recursion trees to solve recurrences, generate good guesses, and gain intuition for recurrences.

## **An illustrative example**

Let's see how a recursion tree can provide a good guess for an upper-bound solution to the recurrence

$$T(n) = 3T(n/4) + \Theta(n^2). \tag{4.13}$$

Figure 4.1 shows how to derive the recursion tree for T(n) = 3T(n/4) + cn², where the constant c > 0 is the upper-bound constant in the Θ(n²) term. Part (a) of the figure shows T(n), which part (b) expands into an equivalent tree representing the recurrence. The cn² term at the root represents the cost at the top level of recursion, and the three subtrees of the root represent the costs incurred by the