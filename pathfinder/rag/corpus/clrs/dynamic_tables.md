---
topic: dynamic_tables
pages: 482-498
---

It is convenient to use a concept introduced in Section 11.2, where we analyzed hashing. The *load factor* α(T) of a nonempty table T is defined as the number of items stored in the table divided by the size (number of slots) of the table. An empty table (one with no slots) has size 0, and its load factor is defined to be 1. If the load factor of a dynamic table is bounded below by a constant, the unused space in the table is never more than a constant fraction of the total amount of space.

We start by analyzing a dynamic table that allows only insertion and then move on to the more general case that supports both insertion and deletion.

#### **16.4.1 Table expansion**

Let's assume that storage for a table is allocated as an array of slots. A table fills up when all slots have been used or, equivalently, when its load factor is 1. 1 In some software environments, upon an attempt to insert an item into a full table, the only alternative is to abort with an error. The scenario in this section assumes, however, that the software environment, like many modern ones, provides a memorymanagement system that can allocate and free blocks of storage on request. Thus, upon inserting an item into a full table, the system can *expand* the table by allocating a new table with more slots than the old table had. Because the table must always reside in contiguous memory, the system must allocate a new array for the larger table and then copy items from the old table into the new table.

A common heuristic allocates a new table with twice as many slots as the old one. If the only table operations are insertions, then the load factor of the table is always at least 1/2, and thus the amount of wasted space never exceeds half the total space in the table.

The TABLE-INSERT procedure on the following page assumes that T is an object representing the table. The attribute T:*table* contains a pointer to the block of storage representing the table, T:*num* contains the number of items in the table, and T:*size* gives the total number of slots in the table. Initially, the table is empty: T:*num* = T:*size* = 0.

There are two types of insertion here: the TABLE-INSERT procedure itself and the *elementary insertion* into a table in lines 6 and 10. We can analyze the running time of TABLE-INSERT in terms of the number of elementary insertions by assigning a cost of 1 to each elementary insertion. In most computing environments, the overhead for allocating an initial table in line 2 is constant and the overhead for allocating and freeing storage in lines 5 and 7 is dominated by the cost of transfer-

<sup>1</sup> In some situations, such as an open-address hash table, it's better to consider a table to be full if its load factor equals some constant strictly less than 1. (See Exercise 16.4-2.)

```
TABLE-INSERT(T, x)
1 if T.size == 0
2 allocate T.table with 1 slot 
3 T.size = 1
4 if T.num == T.size
5 allocate new-table with 2 · T.size slots 
6 insert all items in T.table into new-table 
7 free T.table 
8 T.table = new-table 
9 T.size = 2 · T.size
10 insert x into T.table 
11 T.num = T.num + 1
```

ring items in line 6. Thus, the actual running time of TABLE-INSERT is linear in the number of elementary insertions. An *expansion* occurs when lines 5–9 execute.

Now, we'll use all three amortized analysis techniques to analyze a sequence of n TABLE-INSERT operations on an initially empty table. First, we need to determine the actual cost cᵢ of the ith operation. If the current table has room for the new item (or if this is the first operation), then cᵢ = 1, since the only elementary insertion performed is the one in line 10. If the current table is full, however, and an expansion occurs, then cᵢ = i: the cost is 1 for the elementary insertion in line 10 plus i − 1 for the items copied from the old table to the new table in line 6. For n operations, the worst-case cost of an operation is O(n), which leads to an upper bound of O(n²) on the total running time for n operations.

This bound is not tight, because the table rarely expands in the course of n TABLE-INSERT operations. Specifically, the ith operation causes an expansion only when i − 1 is an exact power of 2. The amortized cost of an operation is in fact O(1), as an aggregate analysis shows. The cost of the ith operation is

$$c_i = \begin{cases} i & \text{if } i - 1 \text{ is an exact power of } 2, \\ 1 & \text{otherwise}. \end{cases}$$

The total cost of n TABLE-INSERT operations is therefore

$$\sum_{i=1}^{n} c_i \leq n + \sum_{j=0}^{\lfloor \lg n \rfloor} 2^j$$

$$< n + 2n \qquad \text{(by equation (A.6) on page 1142)}$$

$$= 3n,$$

**Figure 16.3** Analysis of table expansion by the accounting method. Each call of TABLE-INSERT charges \$3 as follows: \$1 to pay for the elementary insertion, \$1 on the item inserted as prepayment for it to be reinserted later, and \$1 on an item that was already in the table, also as prepayment for reinsertion. **(a)** The table immediately after an expansion, with 8 slots, 4 items (tan slots), and no stored credit. **(b)–(e)** After each of 4 calls to TABLE-INSERT, the table has one more item, with \$1 stored on the new item and \$1 stored on one of the 4 items that were present immediately after the expansion. Slots with these new items are blue. **(f)** Upon the next call to TABLE-INSERT, the table is full, and so it expands again. Each item had \$1 to pay for it to be reinserted. Now the table looks as it did in part (a), with no stored credit but 16 slots and 8 items.

because at most n operations cost 1 each and the costs of the remaining operations form a geometric series. Since the total cost of n TABLE-INSERT operations is bounded by 3n, the amortized cost of a single operation is at most 3.

The accounting method can provide some intuition for why the amortized cost of a TABLE-INSERT operation should be 3. You can think of each item paying for three elementary insertions: inserting itself into the current table, moving itself the next time that the table expands, and moving some other item that was already in the table the next time that the table expands. For example, suppose that the size of the table is m immediately after an expansion, as shown in Figure 16.3 for m = 8. Then the table holds m/2 items, and it contains no credit. Each call of TABLE-INSERT charges \$3. The elementary insertion that occurs immediately costs \$1. Another \$1 resides on the item inserted as credit. The third \$1 resides as credit on one of the m/2 items already in the table. The table will not fill again until another m/2 − 1 items have been inserted, and thus, by the time the table contains m items and is full, each item has \$1 on it to pay for it to be reinserted it during the expansion.

Now, let's see how to use the potential method. We'll use it again in Section 16.4.2 to design a TABLE-DELETE operation that has an O(1) amortized cost 

as well. Just as the accounting method had no stored credit immediately after an expansion—that is, when T:*num* = T:*size*/2—let's define the potential to be 0 when T:*num* = T:*size*/2. As elementary insertions occur, the potential needs to increase enough to pay for all the reinsertions that will happen when the table next expands. The table fills after another T:*size*/2 calls of TABLE-INSERT, when T:*num* = T:*size*. The next call of TABLE-INSERT after these T:*size*/2 calls triggers an expansion with a cost of T:*size* to reinsert all the items. Therefore, over the course of T:*size*/2 calls of TABLE-INSERT, the potential must increase from 0 to T:*size*. To achieve this increase, let's design the potential so that each call of TABLE-INSERT increases it by

$$\frac{T.size}{T.size/2} = 2 ,$$

until the table expands. You can see that the potential function

$$\Phi(T) = 2(T.num - T.size/2) \tag{16.4}$$

equals 0 immediately after the table expands, when T:*num* = T:*size*/2, and it increases by 2 upon each insertion until the table fills. Once the table fills, that is, when T:*num* = T:*size*, the potential Φ(T) equals T:*size*. The initial value of the potential is 0, and since the table is always at least half full, T:*num* ≥ T:*size*/2, which implies that Φ(T) is always nonnegative. Thus, the sum of the amortized costs of n TABLE-INSERT operations gives an upper bound on the sum of the actual costs.

To analyze the amortized costs of table operations, it is convenient to think in terms of the change in potential due to each operation. Letting Φᵢ denote the potential after the ith operation, we can rewrite equation (16.2) as

$$\hat{c}_i = c_i + \Phi_i - \Phi_{i-1}$$
$$= c_i + \Delta \Phi_i ,$$

where ΔΦᵢ is the change in potential due to the ith operation. First, consider the case when the ith insertion does not cause the table to expand. In this case, ΔΦᵢ is 2. Since the actual cost cᵢ is 1, the amortized cost is

$$\hat{c}_i = c_i + \Delta \Phi_i 
= 1 + 2 
= 3.$$

Now, consider the change in potential when the table does expand during the ith insertion because it was full immediately before the insertion. Let *num*ᵢ denote the number of items stored in the table after the ith operation and *size*ᵢ denote the total size of the table after the ith operation, so that *size*ᵢ₋₁ = *num*ᵢ₋₁ = i − 1

**Figure 16.4** The effect of a sequence of n TABLE-INSERT operations on the number *num*ᵢ of items in the table (the brown line), the number *size*ᵢ of slots in the table (the blue line), and the potential Φᵢ = 2(*num*ᵢ − *size*ᵢ/2) (the red line), each being measured after the ith operation. Immediately before an expansion, the potential has built up to the number of items in the table, and therefore it can pay for moving all the items to the new table. Afterward, the potential drops to 0, but it immediately increases by 2 upon insertion of the item that caused the expansion.

and therefore Φᵢ₋₁ = 2(*size*ᵢ₋₁ − *size*ᵢ₋₁/2) = *size*ᵢ₋₁ = i − 1. Immediately after the expansion, the potential goes down to 0, and then the new item is inserted, causing the potential to increase to Φᵢ = 2. Thus, when the ith insertion triggers an expansion, ΔΦᵢ = 2 − (i − 1) = 3 − i. When the table expands in the ith TABLE-INSERT operation, the actual cost cᵢ equals i (to reinsert i − 1 items and insert the ith item), giving an amortized cost of

$$\hat{c}_i = c_i + \Delta \Phi_i$$
  
=  $i + (3 - i)$   
= 3.

Figure 16.4 plots the values of *num*ᵢ, *size*ᵢ, and Φᵢ against i. Notice how the potential builds to pay for expanding the table.

#### **16.4.2 Table expansion and contraction**

To implement a TABLE-DELETE operation, it is simple enough to remove the specified item from the table. In order to limit the amount of wasted space, however, you might want to *contract* the table when the load factor becomes too small. Table contraction is analogous to table expansion: when the number of items in the table drops too low, allocate a new, smaller table and then copy the items from the old table into the new one. You can then free the storage for the old table by returning it to the memory-management system. In order to not waste space, yet keep the amortized costs low, the insertion and deletion procedures should preserve two properties:

- the load factor of the dynamic table is bounded below by a positive constant, as well as above by 1, and
- the amortized cost of a table operation is bounded above by a constant.

The actual cost of each operation equals the number of elementary insertions or deletions.

You might think that if you double the table size upon inserting an item into a full table, then you should halve the size when deleting an item that would cause the table to become less than half full. This strategy does indeed guarantee that the load factor of the table never drops below 1/2. Unfortunately, it can also cause the amortized cost of an operation to be quite large. Consider the following scenario. Perform n operations on a table T of size n/2, where n is an exact power of 2. The first n/2 operations are insertions, which by our previous analysis cost a total of Θ(n). At the end of this sequence of insertions, T:*num* = T:*size* = n/2. For the second n/2 operations, perform the following sequence:

insert, delete, delete, insert, insert, delete, delete, insert, insert, . . . .

The first insertion causes the table to expand to size n. The two deletions that follow cause the table to contract back to size n/2. Two further insertions cause another expansion, and so forth. The cost of each expansion and contraction is Θ(n), and there are Θ(n) of them. Thus, the total cost of the n operations is Θ(n²), making the amortized cost of an operation Θ(n).

The problem with this strategy is that after the table expands, not enough deletions occur to pay for a contraction. Likewise, after the table contracts, not enough insertions take place to pay for an expansion.

How can we solve this problem? Allow the load factor of the table to drop below 1/2. Specifically, continue to double the table size upon inserting an item into a full table, but halve the table size when deleting an item causes the table to become less than 1/4 full, rather than 1/2 full as before. The load factor of the table is therefore bounded below by the constant 1/4, and the load factor is 1/2 immediately after a contraction.

An expansion or contraction should exhaust all the built-up potential, so that immediately after expansion or contraction, when the load factor is 1/2, the table's potential is 0. Figure 16.5 shows the idea. As the load factor deviates from 1/2, the

**Figure 16.5** How to think about the potential function Φ for table insertion and deletion. When the load factor α is 1/2, the potential is 0. In order to accumulate sufficient potential to pay for reinserting all T:*size* items when the table fills, the potential needs to increase by 2 upon each insertion when α ≥ 1/2. Correspondingly, the potential decreases by 2 upon each deletion that leaves α ≥ 1/2. In order to accrue enough potential to cover the cost of reinserting all T:*size*/4 items when the table contracts, the potential needs to increase by 1 upon each deletion when α < 1/2, and correspondingly the potential decreases by 1 upon each insertion that leaves α < 1/2. The red area represents load factors less than 1/4, which are not allowed.

potential increases so that by the time an expansion or contraction occurs, the table has garnered sufficient potential to pay for copying all the items into the newly allocated table. Thus, the potential function should grow to T:*num* by the time that the load factor has either increased to 1 or decreased to 1/4. Immediately after either expanding or contracting the table, the load factor goes back to 1/2 and the table's potential reduces back to 0.

We omit the code for TABLE-DELETE, since it is analogous to TABLE-INSERT. We assume that if a contraction occurs during TABLE-DELETE, it occurs after the item is deleted from the table. The analysis assumes that whenever the number of items in the table drops to 0, the table occupies no storage. That is, if T:*num* = 0, then T:*size* = 0.

How do we design a potential function that gives constant amortized time for both insertion and deletion? When the load factor is at least 1/2, the same potential function, Φ(T) = 2(T:*num* − T:*size*/2), that we used for insertion still works. When the table is at least half full, each insertion increases the potential by 2 if the table does not expand, and each deletion reduces the potential by 2 if it does not cause the load factor to drop below 1/2.

What about when the load factor is less than 1/2, that is, when 1/4 ≤ α(T) < 1/2? As before, when α(T) = 1/2, so that T:*num* = T:*size*/2, the potential Φ(T) should be 0. To get the load factor from 1/2 down to 1/4, T:*size*/4 deletions need 

to occur, at which time T:*num* = T:*size*/4. To pay for all the reinsertions, the potential must increase from 0 to T:*size*/4 over these T:*size*/4 deletions. Therefore, for each call of TABLE-DELETE until the table contracts, the potential should increase by

$$\frac{T.size/4}{T.size/4} = 1.$$

Likewise, when α < 1/2, each call of TABLE-INSERT should decrease the potential by 1. When 1/4 ≤ α(T) < 1/2, the potential function

$$\Phi(T) = T.size/2 - T.num$$

produces this desired behavior.

Putting the two cases together, we get the potential function

$$\Phi(T) = \begin{cases} 2(T.num - T.size/2) & \text{if } \alpha(T) \ge 1/2, \\ T.size/2 - T.num & \text{if } \alpha(T) < 1/2. \end{cases}$$
(16.5)

The potential of an empty table is 0 and the potential is never negative. Thus, the total amortized cost of a sequence of operations with respect to Φ provides an upper bound on the actual cost of the sequence. Figure 16.6 illustrates how the potential function behaves over a sequence of insertions and deletions.

Now, let's determine the amortized costs of each operation. As before, let *num*ᵢ denote the number of items stored in the table after the ith operation, *size*ᵢ denote the total size of the table after the ith operation, αᵢ = *num*ᵢ/*size*ᵢ denote the load factor after the ith operation, Φᵢ denote the potential after the ith operation, and ΔΦᵢ denote the change in potential due to the ith operation. Initially, *num*₀ = 0, *size*₀ = 0, and Φ₀ = 0.

The cases in which the table does not expand or contract and the load factor does not cross α = 1/2 are straightforward. As we have seen, if αᵢ₋₁ ≥ 1/2 and the ith operation is an insertion that does not cause the table to expand, then ΔΦᵢ = 2. Likewise, if the ith operation is a deletion and αᵢ ≥ 1/2, then ΔΦᵢ = −2. Furthermore, if αᵢ₋₁ < 1/2 and the ith operation is a deletion that does not trigger a contraction, then ΔΦᵢ = 1, and if the ith operation is an insertion and αᵢ < 1/2, then ΔΦᵢ = −1. In other words, if no expansion or contraction occurs and the load factor does not cross α = 1/2, then

- if the load factor stays at or above 1/2, then the potential increases by 2 for an insertion and decreases by 2 for a deletion, and
- if the load factor stays below 1/2, then the potential increases by 1 for a deletion and decreases by 1 for an insertion.

In each of these cases, the actual cost cᵢ of the ith operation is just 1, and so

**Figure 16.6** The effect of a sequence of n TABLE-INSERT and TABLE-DELETE operations on the number *num*ᵢ of items in the table (the brown line), the number *size*ᵢ of slots in the table (the blue line), and the potential (the red line)

$$\Phi_i = \begin{cases} 2(num_i - size_i/2) & \text{if } \alpha_i \ge 1/2, \\ size_i/2 - num_i & \text{if } \alpha_i < 1/2, \end{cases}$$

where αᵢ = *num*ᵢ/*size*ᵢ, each measured after the ith operation. Immediately before an expansion or contraction, the potential has built up to the number of items in the table, and therefore it can pay for moving all the items to the new table.

- if the ith operation is an insertion, its amortized cost ĉᵢ is cᵢ + ΔΦᵢ, which is 1 + 2 = 3 if the load factor stays at or above 1/2, and 1 + (−1) = 0 if the load factor stays below 1/2, and
- if the ith operation is a deletion, its amortized cost ĉᵢ is cᵢ + ΔΦᵢ, which is 1 + (−2) = −1 if the load factor stays at or above 1/2, and 1 + 1 = 2 if the load factor stays below 1/2.

Four cases remain: an insertion that takes the load factor from below 1/2 to 1/2, a deletion that takes the load factor from 1/2 to below 1/2, a deletion that causes the table to contract, and an insertion that causes the table to expand. We analyzed that last case at the end of Section 16.4.1 to show that its amortized cost is 3.

When the ith operation is a deletion that causes the table to contract, we have *num*ᵢ₋₁ = *size*ᵢ₋₁/4 before the contraction, then the item is deleted, and finally *num*ᵢ = *size*ᵢ/2 − 1 after the contraction. Thus, by equation (16.5) we have

$$\Phi_{i-1} = size_{i-1}/2 - num_{i-1}$$
  
=  $size_{i-1}/2 - size_{i-1}/4$   
=  $size_{i-1}/4$ ,

which also equals the actual cost cᵢ of deleting one item and copying *size*ᵢ₋₁/4 − 1 items into the new, smaller table. Since *num*ᵢ = *size*ᵢ/2 − 1 after the operation has completed, αᵢ < 1/2, and so

$$\Phi_i = size_i/2 - num_i$$
$$= 1,$$

giving ΔΦᵢ = 1 − *size*ᵢ₋₁/4. Therefore, when the ith operation is a deletion that triggers a contraction, its amortized cost is

$$\widehat{c}_i = c_i + \Delta \Phi_i$$
  
=  $size_{i-1}/4 + (1 - size_{i-1}/4)$   
= 1.

Finally, we handle the cases where the load factor fits one case of equation (16.5) before the operation and the other case afterward. We start with deletion, where we have *num*ᵢ₋₁ = *size*ᵢ₋₁/2, so that αᵢ₋₁ = 1/2, beforehand, and *num*ᵢ = *size*ᵢ/2−1, so that αᵢ < 1/2 afterward. Because αᵢ₋₁ = 1/2, we have Φᵢ₋₁ = 0, and because αᵢ < 1/2, we have Φᵢ = *size*ᵢ/2 − *num*ᵢ = 1. Thus we get that ΔΦᵢ = 1 − 0 = 1. Since the ith operation is a deletion that does not cause a contraction, the actual cost cᵢ equals 1, and the amortized cost ĉᵢ is cᵢ + ΔΦᵢ = 1 + 1 = 2.

Conversely, if the ith operation is an insertion that takes the load factor from below 1/2 to equaling 1/2, the change in potential ΔΦᵢ equals −1. Again, the actual cost cᵢ is 1, and now the amortized cost ĉᵢ is cᵢ + ΔΦᵢ = 1 + (−1) = 0.

In summary, since the amortized cost of each operation is bounded above by a constant, the actual time for any sequence of n operations on a dynamic table is O(n).

#### **Exercises**

#### *16.4-1*

Using the potential method, analyze the amortized cost of the first table insertion.

#### *16.4-2*

You wish to implement a dynamic, open-address hash table. Why might you consider the table to be full when its load factor reaches some value α that is strictly less than 1? Describe briefly how to make insertion into a dynamic, open-address hash table run in such a way that the expected value of the amortized cost per 

insertion is O(1). Why is the expected value of the actual cost per insertion not necessarily O(1) for all insertions?

# *16.4-3*

Discuss how to use the accounting method to analyze both the insertion and deletion operations, assuming that the table doubles in size when its load factor exceeds 1 and the table halves in size when its load factor goes below 1/4.

# *16.4-4*

Suppose that instead of contracting a table by halving its size when its load factor drops below 1/4, you contract the table by multiplying its size by 2/3 when its load factor drops below 1/3. Using the potential function

$$\Phi(T) = |2(T.num - T.size/2)|,$$

show that the amortized cost of a TABLE-DELETE that uses this strategy is bounded above by a constant.

# **Problems**

# *16-1 Binary reflected Gray code*

A *binary Gray code* represents a sequence of nonnegative integers in binary such that to go from one integer to the next, exactly one bit flips every time. The *binary reflected Gray code* represents a sequence of the integers 0 to 2^k − 1 for some positive integer k according to the following recursive method:

- For k = 1, the binary reflected Gray code is ⟨0, 1⟩.
- For k ≥ 2, first form the binary reflected Gray code for k − 1, giving the 2^(k−1) integers 0 to 2^(k−1) − 1. Then form the reflection of this sequence, which is just the sequence in reverse. (That is, the jth integer in the sequence becomes the (2^(k−1) − j − 1)st integer in the reflection). Next, add 2^(k−1) to each of the 2^(k−1) integers in the reflected sequence. Finally, concatenate the two sequences.

For example, for k = 2, first form the binary reflected Gray code ⟨0, 1⟩ for k = 1. Its reflection is the sequence ⟨1, 0⟩. Adding 2^(k−1) = 2 to each integer in the reflection gives the sequence ⟨3, 2⟩. Concatenating the two sequences gives ⟨0, 1, 3, 2⟩ or, in binary, ⟨00, 01, 11, 10⟩, so that each integer differs from its predecessor by exactly one bit. For k = 3, the reflection of the binary reflected Gray code for k = 2 is ⟨2, 3, 1, 0⟩ and adding 2^(k−1) = 4 gives ⟨6, 7, 5, 4⟩. Concatenating produces the sequence ⟨0, 1, 3, 2, 6, 7, 5, 4⟩, which in binary is ⟨000, 001, 011, 010, 110, 111, 101, 100⟩. In the binary reflected Gray code, only one bit flips even when wrapping around from the last integer to the first.

- *a.* Index the integers in a binary reflected Gray code from 0 to 2^k − 1, and consider the ith integer in the binary reflected Gray code. To go from the (i − 1)st integer to the ith integer in the binary reflected Gray code, exactly one bit flips. Show how to determine which bit flips, given the index i.
- *b.* Assuming that given a bit number j, you can flip bit j of an integer in constant time, show how to compute the entire binary reflected Gray code sequence of 2^k numbers in Θ(2^k) time.

#### *16-2 Making binary search dynamic*

Binary search of a sorted array takes logarithmic search time, but the time to insert a new element is linear in the size of the array. You can improve the time for insertion by keeping several sorted arrays.

Specifically, suppose that you wish to support SEARCH and INSERT on a set of n elements. Let k = ⌈lg(n + 1)⌉, and let the binary representation of n be ⟨n_(k−1), n_(k−2), ..., n₀⟩. Maintain k sorted arrays A₀, A₁, ..., A_(k−1), where for i = 0, 1, ..., k − 1, the length of array Aᵢ is 2^i. Each array is either full or empty, depending on whether nᵢ = 1 or nᵢ = 0, respectively. The total number of elements held in all k arrays is therefore ∑ᵢ₌₀^(k−1) nᵢ · 2^i = n. Although each individual array is sorted, elements in different arrays bear no particular relationship to each other.

- *a.* Describe how to perform the SEARCH operation for this data structure. Analyze its worst-case running time.
- *b.* Describe how to perform the INSERT operation. Analyze its worst-case and amortized running times, assuming that the only operations are INSERT and SEARCH.
- *c.* Describe how to implement DELETE. Analyze its worst-case and amortized running times, assuming that there can be DELETE, INSERT, and SEARCH operations.

#### *16-3 Amortized weight-balanced trees*

Consider an ordinary binary search tree augmented by adding to each node x the attribute x:*size*, which gives the number of keys stored in the subtree rooted at x. Let α be a constant in the range 1/2 ≤ α < 1. We say that a given node x is α*-balanced* if x:*left*:*size* ≤ α · x:*size* and x:*right*:*size* ≤ α · x:*size*. The tree as a whole is α*-balanced* if every node in the tree is α-balanced. The following amortized approach to maintaining weight-balanced trees was suggested by G. Varghese.

- *a.* A 1/2-balanced tree is, in a sense, as balanced as it can be. Given a node x in an arbitrary binary search tree, show how to rebuild the subtree rooted at x so that it becomes 1/2-balanced. Your algorithm should run in Θ(x:*size*) time, and it can use O(x:*size*) auxiliary storage.
- *b.* Show that performing a search in an n-node α-balanced binary search tree takes O(lg n) worst-case time.

For the remainder of this problem, assume that the constant α is strictly greater than 1/2. Suppose that you implement INSERT and DELETE as usual for an n-node binary search tree, except that after every such operation, if any node in the tree is no longer α-balanced, then you "rebuild" the subtree rooted at the highest such node in the tree so that it becomes 1/2-balanced.

We'll analyze this rebuilding scheme using the potential method. For a node x in a binary search tree T, define

$$\Delta(x) = |x.left.size - x.right.size|.$$

Define the potential of T as

$$\Phi(T) = c \sum_{x \in T: \Delta(x) \ge 2} \Delta(x),$$

where c is a sufficiently large constant that depends on α.

- *c.* Argue that any binary search tree has nonnegative potential and also that a 1/2-balanced tree has potential 0.
- *d.* Suppose that m units of potential can pay for rebuilding an m-node subtree. How large must c be in terms of α in order for it to take O(1) amortized time to rebuild a subtree that is not α-balanced?
- *e.* Show that inserting a node into or deleting a node from an n-node α-balanced tree costs O(lg n) amortized time.

#### *16-4 The cost of restructuring red-black trees*

There are four basic operations on red-black trees that perform *structural modifications*: node insertions, node deletions, rotations, and color changes. We have seen that RB-INSERT and RB-DELETE use only O(1) rotations, node insertions, and node deletions to maintain the red-black properties, but they may make many more color changes.

*a.* Describe a legal red-black tree with n nodes such that calling RB-INSERT to add the (n + 1)st node causes Ω(lg n) color changes. Then describe a legal 

red-black tree with n nodes for which calling RB-DELETE on a particular node causes Ω(lg n) color changes.

Although the worst-case number of color changes per operation can be logarithmic, you will prove that any sequence of m RB-INSERT and RB-DELETE operations on an initially empty red-black tree causes O(m) structural modifications in the worst case.

*b.* Some of the cases handled by the main loop of the code of both RB-INSERT-FIXUP and RB-DELETE-FIXUP are *terminating*: once encountered, they cause the loop to terminate after a constant number of additional operations. For each of the cases of RB-INSERT-FIXUP and RB-DELETE-FIXUP, specify which are terminating and which are not. (*Hint:* Look at Figures 13.5, 13.6, and 13.7 in Sections 13.3 and 13.4.)

You will first analyze the structural modifications when only insertions are performed. Let T be a red-black tree, and define Φ(T) to be the number of red nodes in T. Assume that one unit of potential can pay for the structural modifications performed by any of the three cases of RB-INSERT-FIXUP.

- *c.* Let T₀ be the result of applying Case 1 of RB-INSERT-FIXUP to T. Argue that Φ(T₀) = Φ(T) − 1.
- *d.* We can break the operation of the RB-INSERT procedure into three parts. List the structural modifications and potential changes resulting from lines 13–16 of RB-INSERT, from nonterminating cases of RB-INSERT-FIXUP, and from terminating cases of RB-INSERT-FIXUP.
- *e.* Using part (d), argue that the amortized number of structural modifications performed by any call of RB-INSERT is O(1).

Next you will prove that there are O(m) structural modifications when both insertions and deletions occur. Define, for each node x,

$$w(x) = \begin{cases} 0 & \text{if } x \text{ is red }, \\ 1 & \text{if } x \text{ is black and has no red children }, \\ 0 & \text{if } x \text{ is black and has one red child }, \\ 2 & \text{if } x \text{ is black and has two red children }. \end{cases}$$

Now redefine the potential of a red-black tree T as

$$\Phi(T) = \sum_{x \in T} w(x) ,$$

and let T₀ be the tree that results from applying any nonterminating case of RB-INSERT-FIXUP or RB-DELETE-FIXUP to T.

- *f.* Show that Φ(T₀) ≤ Φ(T) − 1 for all nonterminating cases of RB-INSERT-FIXUP. Argue that the amortized number of structural modifications performed by any call of RB-INSERT-FIXUP is O(1).
- *g.* Show that Φ(T₀) ≤ Φ(T) − 1 for all nonterminating cases of RB-DELETE-FIXUP. Argue that the amortized number of structural modifications performed by any call of RB-DELETE-FIXUP is O(1).
- *h.* Complete the proof that in the worst case, any sequence of m RB-INSERT and RB-DELETE operations performs O(m) structural modifications.

# **Chapter notes**

Aho, Hopcroft, and Ullman [5] used aggregate analysis to determine the running time of operations on a disjoint-set forest. We'll analyze this data structure using the potential method in Chapter 19. Tarjan [430] surveys the accounting and potential methods of amortized analysis and presents several applications. He attributes the accounting method to several authors, including M. R. Brown, R. E. Tarjan, S. Huddleston, and K. Mehlhorn. He attributes the potential method to D. D. Sleator. The term "amortized" is due to D. D. Sleator and R. E. Tarjan.

Potential functions are also useful for proving lower bounds for certain types of problems. For each configuration of the problem, define a potential function that maps the configuration to a real number. Then determine the potential Φ_init of the initial configuration, the potential Φ_final of the final configuration, and the maximum change in potential ΔΦ_max due to any step. The number of steps must therefore be at least |Φ_final − Φ_init| / |ΔΦ_max|. Examples of potential functions to prove lower bounds in I/O complexity appear in works by Cormen, Sundquist, and Wisniewski [105], Floyd [146], and Aggarwal and Vitter [3]. Krumme, Cybenko, and Venkataraman [271] applied potential functions to prove lower bounds on *gossiping*: communicating a unique item from each vertex in a graph to every other vertex.

# **Introduction**

This part returns to studying data structures that support operations on dynamic sets, but at a more advanced level than Part III. One of the chapters, for example, makes extensive use of the amortized analysis techniques from Chapter 16.

Chapter 17 shows how to augment red-black trees—adding additional information in each node—to support dynamic-set operations in addition to those covered in Chapters 12 and 13. The first example augments red-black trees to dynamically maintain order statistics for a set of keys. Another example augments them in a different way to maintain intervals of real numbers. Chapter 17 includes a theorem giving sufficient conditions for when a red-black tree can be augmented while maintaining the O(lg n) running times for insertion and deletion.

Chapter 18 presents B-trees, which are balanced search trees specifically designed to be stored on disks. Since disks operate much more slowly than randomaccess memory, B-tree performance depends not only on how much computing time the dynamic-set operations consume but also on how many disk accesses they perform. For each B-tree operation, the number of disk accesses increases with the height of the B-tree, but B-tree operations keep the height low.

Chapter 19 examines data structures for disjoint sets. Starting with a universe of n elements, each initially in its own singleton set, the operation UNION unites two sets. At all times, the n elements are partitioned into disjoint sets, even as calls to the UNION operation change the members of a set dynamically. The query FIND-SET identifies the unique set that contains a given element at the moment. Representing each set as a simple rooted tree yields surprisingly fast operations: a sequence of m operations runs in O(m · α(n)) time, where α(n) is an incredibly slowly growing function—α(n) is at most 4 in any conceivable application. The amortized analysis that proves this time bound is as complex as the data structure is simple.