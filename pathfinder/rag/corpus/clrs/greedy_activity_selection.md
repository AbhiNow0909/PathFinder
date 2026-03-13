---
topic: greedy_activity_selection
pages: 440-447
---

#### **The optimal substructure of the activity-selection problem**

Let's verify that the activity-selection problem exhibits optimal substructure. Denote by S_ij the set of activities that start after activity a_i finishes and that finish before activity a_j starts. Suppose that you want to find a maximum set of mutually compatible activities in S_ij, and suppose further that such a maximum set is A_ij, which includes some activity a_k. By including a_k in an optimal solution, you are left with two subproblems: finding mutually compatible activities in the set S_ik (activities that start after activity a_i finishes and that finish before activity a_k starts) and finding mutually compatible activities in the set S_kj (activities that start after activity a_k finishes and that finish before activity a_j starts). Let A_ik = A_ij ∩ S_ik and A_kj = A_ij ∩ S_kj, so that A_ik contains the activities in A_ij that finish before a_k starts and A_kj contains the activities in A_ij that start after a_k finishes. Thus, we have A_ij = A_ik ∪ {a_k} ∪ A_kj, and so the maximum-size set A_ij of mutually compatible activities in S_ij consists of |A_ij| = |A_ik| + |A_kj| + 1 activities.

The usual cut-and-paste argument shows that an optimal solution A_ij must also include optimal solutions to the two subproblems for S_ik and S_kj. If you could find a set A'_kj of mutually compatible activities in S_kj where |A'_kj| > |A_kj|, then you could use A'_kj, rather than A_kj, in a solution to the subproblem for S_ij. You would have constructed a set of |A_ik| + |A'_kj| + 1 > |A_ik| + |A_kj| + 1 = |A_ij| mutually compatible activities, which contradicts the assumption that A_ij is an optimal solution. A symmetric argument applies to the activities in S_ik.

This way of characterizing optimal substructure suggests that you can solve the activity-selection problem by dynamic programming. Let's denote the size of an optimal solution for the set S_ij by c[i, j]. Then, the dynamic-programming approach gives the recurrence

$$c[i, j] = c[i, k] + c[k, j] + 1$$
.

Of course, if you do not know that an optimal solution for the set S_ij includes activity a_k, you must examine all activities in S_ij to find which one to choose, so that

$$c[i,j] = \begin{cases} 0 & \text{if } S_{ij} = \emptyset, \\ \max\{c[i,k] + c[k,j] + 1 : a_k \in S_{ij}\} & \text{if } S_{ij} \neq \emptyset. \end{cases}$$
 (15.2)

You can then develop a recursive algorithm and memoize it, or you can work bottom-up and fill in table entries as you go along. But you would be overlooking another important characteristic of the activity-selection problem that you can use to great advantage.

#### **Making the greedy choice**

What if you could choose an activity to add to an optimal solution without having to first solve all the subproblems? That could save you from having to consider all the choices inherent in recurrence (15.2). In fact, for the activity-selection problem, you need to consider only one choice: the greedy choice.

What is the greedy choice for the activity-selection problem? Intuition suggests that you should choose an activity that leaves the resource available for as many other activities as possible. Of the activities you end up choosing, one of them must be the first one to finish. Intuition says, therefore, choose the activity in S with the earliest finish time, since that leaves the resource available for as many of the activities that follow it as possible. (If more than one activity in S has the earliest finish time, then choose any such activity.) In other words, since the activities are sorted in monotonically increasing order by finish time, the greedy choice is activity a₁. Choosing the first activity to finish is not the only way to think of making a greedy choice for this problem. Exercise 15.1-3 asks you to explore other possibilities.

Once you make the greedy choice, you have only one remaining subproblem to solve: finding activities that start after a₁ finishes. Why don't you have to consider activities that finish before a₁ starts? Because s₁ < f₁, and because f₁ is the earliest finish time of any activity, no activity can have a finish time less than or equal to s₁. Thus, all activities that are compatible with activity a₁ must start after a₁ finishes.

Furthermore, we have already established that the activity-selection problem exhibits optimal substructure. Let S_k = {a_i ∈ S : s_i ≥ f_k} be the set of activities that start after activity a_k finishes. If you make the greedy choice of activity a₁, then S₁ remains as the only subproblem to solve.¹ Optimal substructure says that if a₁ belongs to an optimal solution, then an optimal solution to the original problem consists of activity a₁ and all the activities in an optimal solution to the subproblem S₁.

One big question remains: Is this intuition correct? Is the greedy choice—in which you choose the first activity to finish—always part of some optimal solution? The following theorem shows that it is.

¹ We sometimes refer to the sets S_k as subproblems rather than as just sets of activities. The context will make it clear whether we are referring to S_k as a set of activities or as a subproblem whose input is that set.

### *Theorem 15.1*

Consider any nonempty subproblem S_k, and let a_m be an activity in S_k with the earliest finish time. Then a_m is included in some maximum-size subset of mutually compatible activities of S_k.

*Proof* Let A_k be a maximum-size subset of mutually compatible activities in S_k, and let a_j be the activity in A_k with the earliest finish time. If a_j = a_m, we are done, since we have shown that a_m belongs to some maximum-size subset of mutually compatible activities of S_k. If a_j ≠ a_m, let the set A'_k = (A_k − {a_j}) ∪ {a_m} be A_k but substituting a_m for a_j. The activities in A'_k are compatible, which follows because the activities in A_k are compatible, a_j is the first activity in A_k to finish, and f_m ≤ f_j. Since |A'_k| = |A_k|, we conclude that A'_k is a maximum-size subset of mutually compatible activities of S_k, and it includes a_m.

Although you might be able to solve the activity-selection problem with dynamic programming, Theorem 15.1 says that you don't need to. Instead, you can repeatedly choose the activity that finishes first, keep only the activities compatible with this activity, and repeat until no activities remain. Moreover, because you always choose the activity with the earliest finish time, the finish times of the activities that you choose must strictly increase. You can consider each activity just once overall, in monotonically increasing order of finish times.

An algorithm to solve the activity-selection problem does not need to work bottom-up, like a table-based dynamic-programming algorithm. Instead, it can work top-down, choosing an activity to put into the optimal solution that it constructs and then solving the subproblem of choosing activities from those that are compatible with those already chosen. Greedy algorithms typically have this topdown design: make a choice and then solve a subproblem, rather than the bottomup technique of solving subproblems before making a choice.

#### **A recursive greedy algorithm**

Now that you know you can bypass the dynamic-programming approach and instead use a top-down, greedy algorithm, let's see a straightforward, recursive procedure to solve the activity-selection problem. The procedure RECURSIVE-ACTIVITY-SELECTOR on the following page takes the start and finish times of the activities, represented as arrays s and f,² the index k that defines the subproblem S_k it is to solve, and the size n of the original problem. It returns a maximum-

² Because the pseudocode takes s and f as arrays, it indexes into them with square brackets rather than with subscripts.

size set of mutually compatible activities in S_k. The procedure assumes that the n input activities are already ordered by monotonically increasing finish time, according to equation (15.1). If not, you can first sort them into this order in O(n lg n) time, breaking ties arbitrarily. In order to start, add the fictitious activity a₀ with f₀ = 0, so that subproblem S₀ is the entire set of activities S. The initial call, which solves the entire problem, is RECURSIVE-ACTIVITY-SELECTOR(s, f, 0, n).

```
RECURSIVE-ACTIVITY-SELECTOR(s, f, k, n)
1 m = k + 1
2 while m ≤ n and s[m] < f[k]  // find the first activity in S_k to finish
3    m = m + 1
4 if m ≤ n
5    return {a_m} ∪ RECURSIVE-ACTIVITY-SELECTOR(s, f, m, n)
6 else return ∅
```

Figure 15.2 shows how the algorithm operates on the activities in Figure 15.1. In a given recursive call RECURSIVE-ACTIVITY-SELECTOR(s, f, k, n), the **while** loop of lines 2–3 looks for the first activity in S_k to finish. The loop examines a_{k+1}, a_{k+2}, ..., a_n, until it finds the first activity a_m that is compatible with a_k, which means that s_m ≥ f_k. If the loop terminates because it finds such an activity, line 5 returns the union of {a_m} and the maximum-size subset of S_m returned by the recursive call RECURSIVE-ACTIVITY-SELECTOR(s, f, m, n). Alternatively, the loop may terminate because m > n, in which case the procedure has examined all activities in S_k without finding one that is compatible with a_k. In this case, S_k = ∅, and so line 6 returns ∅.

Assuming that the activities have already been sorted by finish times, the running time of the call RECURSIVE-ACTIVITY-SELECTOR(s, f, 0, n) is Θ(n). To see why, observe that over all recursive calls, each activity is examined exactly once in the **while** loop test of line 2. In particular, activity a_i is examined in the last call made in which k < i.

#### **An iterative greedy algorithm**

The recursive procedure can be converted to an iterative one because the procedure RECURSIVE-ACTIVITY-SELECTOR is almost "tail recursive" (see Problem 7-5): it ends with a recursive call to itself followed by a union operation. It is usually a straightforward task to transform a tail-recursive procedure to an iterative form. In fact, some compilers for certain programming languages perform this task automatically.

**Figure 15.2** The operation of RECURSIVE-ACTIVITY-SELECTOR on the 11 activities from Figure 15.1. Activities considered in each recursive call appear between horizontal lines. The fictitious activity a₀ finishes at time 0, and the initial call RECURSIVE-ACTIVITY-SELECTOR(s, f, 0, 11) selects activity a₁. In each recursive call, the activities that have already been selected are blue, and the activity shown in tan is being considered. If the starting time of an activity occurs before the finish time of the most recently added activity (the arrow between them points left), it is rejected. Otherwise (the arrow points directly up or to the right), it is selected. The last recursive call, RECURSIVE-ACTIVITY-SELECTOR(s, f, 11, 11), returns ∅. The resulting set of selected activities is {a₁, a₄, a₈, a₁₁}.

The procedure GREEDY-ACTIVITY-SELECTOR is an iterative version of the procedure RECURSIVE-ACTIVITY-SELECTOR. It, too, assumes that the input activities are ordered by monotonically increasing finish time. It collects selected activities into a set A and returns this set when it is done.

```
GREEDY-ACTIVITY-SELECTOR(s, f, n)
1 A = {a₁}
2 k = 1
3 for m = 2 to n
4    if s[m] ≥ f[k]  // is a_m in S_k?
5       A = A ∪ {a_m}  // yes, so choose it
6       k = m  // and continue from there
7 return A
```

The procedure works as follows. The variable k indexes the most recent addition to A, corresponding to the activity a_k in the recursive version. Since the procedure considers the activities in order of monotonically increasing finish time, f_k is always the maximum finish time of any activity in A. That is,

$$f_k = \max\{f_i : a_i \in A\} \ . \tag{15.3}$$

Lines 1–2 select activity a₁, initialize A to contain just this activity, and initialize k to index this activity. The **for** loop of lines 3–6 finds the earliest activity in S_k to finish. The loop considers each activity a_m in turn and adds a_m to A if it is compatible with all previously selected activities. Such an activity is the earliest in S_k to finish. To see whether activity a_m is compatible with every activity currently in A, it suffices by equation (15.3) to check (in line 4) that its start time s_m is not earlier than the finish time f_k of the activity most recently added to A. If activity a_m is compatible, then lines 5–6 add activity a_m to A and set k to m. The set A returned by the call GREEDY-ACTIVITY-SELECTOR(s, f) is precisely the set returned by the initial call RECURSIVE-ACTIVITY-SELECTOR(s, f, 0, n).

Like the recursive version, GREEDY-ACTIVITY-SELECTOR schedules a set of n activities in Θ(n) time, assuming that the activities were already sorted initially by their finish times.

#### **Exercises**

### *15.1-1*

Give a dynamic-programming algorithm for the activity-selection problem, based on recurrence (15.2). Have your algorithm compute the sizes c[i, j] as defined above and also produce the maximum-size subset of mutually compatible activities.

Assume that the inputs have been sorted as in equation (15.1). Compare the running time of your solution to the running time of GREEDY-ACTIVITY-SELECTOR.

### *15.1-2*

Suppose that instead of always selecting the first activity to finish, you instead select the last activity to start that is compatible with all previously selected activities. Describe how this approach is a greedy algorithm, and prove that it yields an optimal solution.

### *15.1-3*

Not just any greedy approach to the activity-selection problem produces a maximum-size set of mutually compatible activities. Give an example to show that the approach of selecting the activity of least duration from among those that are compatible with previously selected activities does not work. Do the same for the approaches of always selecting the compatible activity that overlaps the fewest other remaining activities and always selecting the compatible remaining activity with the earliest start time.

### *15.1-4*

You are given a set of activities to schedule among a large number of lecture halls, where any activity can take place in any lecture hall. You wish to schedule all the activities using as few lecture halls as possible. Give an efficient greedy algorithm to determine which activity should use which lecture hall.

(This problem is also known as the *interval-graph coloring problem*. It is modeled by an interval graph whose vertices are the given activities and whose edges connect incompatible activities. The smallest number of colors required to color every vertex so that no two adjacent vertices have the same color corresponds to finding the fewest lecture halls needed to schedule all of the given activities.)

#### *15.1-5*

Consider a modification to the activity-selection problem in which each activity a_i has, in addition to a start and finish time, a value v_i. The objective is no longer to maximize the number of activities scheduled, but instead to maximize the total value of the activities scheduled. That is, the goal is to choose a set A of compatible activities such that ∑_(a_k∈A) v_k is maximized. Give a polynomial-time algorithm for this problem.

### **15.2 Elements of the greedy strategy**

A greedy algorithm obtains an optimal solution to a problem by making a sequence of choices. At each decision point, the algorithm makes the choice that seems best at the moment. This heuristic strategy does not always produce an optimal solution, but as in the activity-selection problem, sometimes it does. This section discusses some of the general properties of greedy methods.

The process that we followed in Section 15.1 to develop a greedy algorithm was a bit more involved than is typical. It consisted of the following steps:

- 1. Determine the optimal substructure of the problem.
- 2. Develop a recursive solution. (For the activity-selection problem, we formulated recurrence (15.2), but bypassed developing a recursive algorithm based solely on this recurrence.)
- 3. Show that if you make the greedy choice, then only one subproblem remains.
- 4. Prove that it is always safe to make the greedy choice. (Steps 3 and 4 can occur in either order.)
- 5. Develop a recursive algorithm that implements the greedy strategy.
- 6. Convert the recursive algorithm to an iterative algorithm.

These steps highlighted in great detail the dynamic-programming underpinnings of a greedy algorithm. For example, the first cut at the activity-selection problem defined the subproblems S_ij, where both i and j varied. We then found that if you always make the greedy choice, you can restrict the subproblems to be of the form S_k.

An alternative approach is to fashion optimal substructure with a greedy choice in mind, so that the choice leaves just one subproblem to solve. In the activityselection problem, start by dropping the second subscript and defining subproblems of the form S_k. Then prove that a greedy choice (the first activity a_m to finish in S_k), combined with an optimal solution to the remaining set S_m of compatible activities, yields an optimal solution to S_k. More generally, you can design greedy algorithms according to the following sequence of steps:

- 1. Cast the optimization problem as one in which you make a choice and are left with one subproblem to solve.
- 2. Prove that there is always an optimal solution to the original problem that makes the greedy choice, so that the greedy choice is always safe.
- 3. Demonstrate optimal substructure by showing that, having made the greedy choice, what remains is a subproblem with the property that if you combine an