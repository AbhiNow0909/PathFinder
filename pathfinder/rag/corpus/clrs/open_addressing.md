---
topic: open_addressing
pages: 315-322
---

that is assumed to be not already present in the hash table. It either returns the slot number where it stores key k or flags an error because the hash table is already full.

```
HASH-INSERT(T, k)
1 i = 0
2 repeat
3 q = h(k, i)
4 if T[q] == NIL 
5 T[q] = k
6 return q
7 else i = i + 1
8 until i == m
9 error "hash table overflow"
HASH-SEARCH(T, k)
1 i = 0
2 repeat
3 q = h(k, i)
4 if T[q] == k
5 return q
6 i = i + 1
7 until T[q] == NIL or i == m
8 return NIL
```

The algorithm for searching for key k probes the same sequence of slots that the insertion algorithm examined when key k was inserted. Therefore, the search can terminate (unsuccessfully) when it finds an empty slot, since k would have been inserted there and not later in its probe sequence. The procedure HASH-SEARCH takes as input a hash table T and a key k, returning q if it finds that slot q contains key k, or NIL if key k is not present in table T.

Deletion from an open-address hash table is tricky. When you delete a key from slot q, it would be a mistake to mark that slot as empty by simply storing NIL in it. If you did, you might be unable to retrieve any key k for which slot q was probed and found occupied when k was inserted. One way to solve this problem is by marking the slot, storing in it the special value DELETED instead of NIL. The HASH-INSERT procedure then has to treat such a slot as empty so that it can insert a new key there. The HASH-SEARCH procedure passes over DELETED values while searching, since slots containing DELETED were filled when the key being searched for was inserted. Using the special value DELETED, however, means that search times no longer depend on the load factor α, and for this reason chaining is frequently selected as a collision resolution technique when keys must be deleted. There is a simple special case of open addressing, linear probing, that avoids the need to mark slots with DELETED. Section 11.5.1 shows how to delete from a hash table when using linear probing.

In our analysis, we assume *independent uniform permutation hashing* (also confusingly known as *uniform hashing* in the literature): the probe sequence of each key is equally likely to be any of the m! permutations of {0, 1, ..., m - 1}. Independent uniform permutation hashing generalizes the notion of independent uniform hashing defined earlier to a hash function that produces not just a single slot number, but a whole probe sequence. True independent uniform permutation hashing is difficult to implement, however, and in practice suitable approximations (such as double hashing, defined below) are used.

We'll examine both double hashing and its special case, linear probing. These techniques guarantee that {h(k, 0), h(k, 1), ..., h(k, m - 1)} is a permutation of {0, 1, ..., m - 1} for each key k. (Recall that the second parameter to the hash function h is the probe number.) Neither double hashing nor linear probing meets the assumption of independent uniform permutation hashing, however. Double hashing cannot generate more than m² different probe sequences (instead of the m! that independent uniform permutation hashing requires). Nonetheless, double hashing has a large number of possible probe sequences and, as you might expect, seems to give good results. Linear probing is even more restricted, capable of generating only m different probe sequences.

Double hashing offers one of the best methods available for open addressing because the permutations produced have many of the characteristics of randomly chosen permutations. *Double hashing* uses a hash function of the form

$$h(k,i) = (h_1(k) + ih_2(k)) \mod m$$
,

where both h₁ and h₂ are *auxiliary hash functions*. The initial probe goes to position T[h₁(k)], and successive probe positions are offset from previous positions by the amount h₂(k), modulo m. Thus, the probe sequence here depends in two ways upon the key k, since the initial probe position h₁(k), the step size h₂(k), or both, may vary. Figure 11.5 gives an example of insertion by double hashing.

In order for the entire hash table to be searched, the value h₂(k) must be relatively prime to the hash-table size m. (See Exercise 11.4-5.) A convenient way to ensure this condition is to let m be an exact power of 2 and to design h₂ so that it always produces an odd number. Another way is to let m be prime and to design h₂ so that it always returns a positive integer less than m. For example, you

**Figure 11.5** Insertion by double hashing. The hash table has size 13 with h₁(k) = k mod 13 and h₂(k) = 1 + (k mod 11). Since 14 ≡ 1 (mod 13) and 14 ≡ 3 (mod 11), the key 14 goes into empty slot 9, after slots 1 and 5 are examined and found to be occupied.

could choose m prime and let

$$h_1(k) = k \mod m$$
,  
 $h_2(k) = 1 + (k \mod m')$ ,

where m' is chosen to be slightly less than m (say, m - 1). For example, if k = 123456, m = 701, and m' = 700, then h₁(k) = 80 and h₂(k) = 257, so that the first probe goes to position 80, and successive probes examine every 257th slot (modulo m) until the key has been found or every slot has been examined.

Although values of m other than primes or exact powers of 2 can in principle be used with double hashing, in practice it becomes more difficult to efficiently generate h₂(k) (other than choosing h₂(k) = 1, which gives linear probing) in a way that ensures that it is relatively prime to m, in part because the relative density φ(m)/m of such numbers for general m may be small (see equation (31.25) on page 921).

When m is prime or an exact power of 2, double hashing produces Θ(m²) probe sequences, since each possible (h₁(k), h₂(k)) pair yields a distinct probe sequence. As a result, for such values of m, double hashing appears to perform close to the "ideal" scheme of independent uniform permutation hashing.

#### **Linear probing**

*Linear probing*, a special case of double hashing, is the simplest open-addressing approach to resolving collisions. As with double hashing, an auxiliary hash function h₁ determines the first probe position h₁(k) for inserting an element. If slot T[h₁(k)] is already occupied, probe the next position T[h₁(k) + 1]. Keep going as necessary, on up to slot T[m - 1], and then wrap around to slots T[0], T[1], and so on, but never going past slot T[h₁(k) - 1]. To view linear probing as a special case of double hashing, just set the double-hashing step function h₂ to be fixed at 1: h₂(k) = 1 for all k. That is, the hash function is

$$h(k,i) = (h_1(k) + i) \bmod m$$
 (11.6)

for i = 0, 1, ..., m - 1. The value of h₁(k) determines the entire probe sequence, and so assuming that h₁(k) can take on any value in {0, 1, ..., m - 1}, linear probing allows only m distinct probe sequences.

We'll revisit linear probing in Section 11.5.1.

### **Analysis of open-address hashing**

As in our analysis of chaining in Section 11.2, we analyze open addressing in terms of the load factor α = n/m of the hash table. With open addressing, at most one element occupies each slot, and thus n ≤ m, which implies α ≤ 1. The analysis below requires α to be strictly less than 1, and so we assume that at least one slot is empty. Because deleting from an open-address hash table does not really free up a slot, we assume as well that no deletions occur.

For the hash function, we assume independent uniform permutation hashing. In this idealized scheme, the probe sequence ⟨h(k, 0), h(k, 1), ..., h(k, m - 1)⟩ used to insert or search for each key k is equally likely to be any permutation of ⟨0, 1, ..., m-1⟩. Of course, any given key has a unique fixed probe sequence associated with it. What we mean here is that, considering the probability distribution on the space of keys and the operation of the hash function on the keys, each possible probe sequence is equally likely.

We now analyze the expected number of probes for hashing with open addressing under the assumption of independent uniform permutation hashing, beginning with the expected number of probes made in an unsuccessful search (assuming, as stated above, that α < 1).

The bound proven, of 1/(1 - α) = 1 + α + α² + α³ + ..., has an intuitive interpretation. The first probe always occurs. With probability approximately α, the first probe finds an occupied slot, so that a second probe happens. With probability approximately α², the first two slots are occupied so that a third probe ensues, and so on.

### *Theorem 11.6*

Given an open-address hash table with load factor α = n/m < 1, the expected number of probes in an unsuccessful search is at most 1/(1 - α), assuming independent uniform permutation hashing and no deletions.

*Proof* In an unsuccessful search, every probe but the last accesses an occupied slot that does not contain the desired key, and the last slot probed is empty. Let the random variable X denote the number of probes made in an unsuccessful search, and define the event A_i, for i = 1, 2, ..., as the event that an ith probe occurs and it is to an occupied slot. Then the event {X ≥ i} is the intersection of events A₁ ∩ A₂ ∩ ... ∩ Aᵢ₋₁. We bound Pr{X ≥ i} by bounding Pr{A₁ ∩ A₂ ∩ ... ∩ Aᵢ₋₁}. By Exercise C.2-5 on page 1190,

$$\Pr\{A_{1} \cap A_{2} \cap \dots \cap A_{i-1}\} = \Pr\{A_{1}\} \cdot \Pr\{A_{2} \mid A_{1}\} \cdot \Pr\{A_{3} \mid A_{1} \cap A_{2}\} \cdots$$

$$\Pr\{A_{i-1} \mid A_{1} \cap A_{2} \cap \dots \cap A_{i-2}\}.$$

Since there are n elements and m slots, Pr{A₁} = n/m. For j > 1, the probability that there is a jth probe and it is to an occupied slot, given that the first j - 1 probes were to occupied slots, is (n - j + 1)/(m - j + 1). This probability follows because the jth probe would be finding one of the remaining (n - (j - 1)) elements in one of the (m - (j - 1)) unexamined slots, and by the assumption of independent uniform permutation hashing, the probability is the ratio of these quantities. Since n < m implies that (n - j)/(m - j) ≤ n/m for all j in the range 0 ≤ j < m, it follows that for all i in the range 1 ≤ i ≤ m, we have

$$\Pr\{X \ge i\} = \frac{n}{m} \cdot \frac{n-1}{m-1} \cdot \frac{n-2}{m-2} \cdots \frac{n-i+2}{m-i+2}$$

$$\le \left(\frac{n}{m}\right)^{i-1}$$

$$= \alpha^{i-1}.$$

The product in the first line has i - 1 factors. When i = 1, the product is 1, the identity for multiplication, and we get Pr{X ≥ 1} = 1, which makes sense, since there must always be at least 1 probe. If each of the first n probes is to an occupied slot, then all occupied slots have been probed. Then, the (n + 1)st probe must be to an empty slot, which gives Pr{X ≥ i} = 0 for i > n + 1. Now, we use equation (C.28) on page 1193 to bound the expected number of probes:

$$E[X] = \sum_{i=1}^{\infty} \Pr\{X \ge i\}$$

$$= \sum_{i=1}^{n+1} \Pr\{X \ge i\} + \sum_{i>n+1} \Pr\{X \ge i\}$$

$$\leq \sum_{i=1}^{\infty} \alpha^{i-1} + 0$$

$$= \sum_{i=0}^{\infty} \alpha^{i}$$

$$= \frac{1}{1-\alpha} \quad \text{(by equation (A.7) on page 1142 because } 0 \leq \alpha < 1) . \quad \blacksquare$$

If α is a constant, Theorem 11.6 predicts that an unsuccessful search runs in O(1) time. For example, if the hash table is half full, the average number of probes in an unsuccessful search is at most 1/(1 - 0.5) = 2. If it is 90% full, the average number of probes is at most 1/(1 - 0.9) = 10.

Theorem 11.6 yields almost immediately how well the HASH-INSERT procedure performs.

#### *Corollary 11.7*

Inserting an element into an open-address hash table with load factor α, where α < 1, requires at most 1/(1 - α) probes on average, assuming independent uniform permutation hashing and no deletions.

*Proof* An element is inserted only if there is room in the table, and thus α < 1. Inserting a key requires an unsuccessful search followed by placing the key into the first empty slot found. Thus, the expected number of probes is at most 1/(1 - α).

It takes a little more work to compute the expected number of probes for a successful search.

#### *Theorem 11.8*

Given an open-address hash table with load factor α < 1, the expected number of probes in a successful search is at most

$$\frac{1}{\alpha} \ln \frac{1}{1-\alpha} \;,$$

assuming independent uniform permutation hashing with no deletions and assuming that each key in the table is equally likely to be searched for.

*Proof* A search for a key k reproduces the same probe sequence as when the element with key k was inserted. If k was the (i + 1)st key inserted into the hash table, then the load factor at the time it was inserted was i/m, and so by Corollary 11.7, the expected number of probes made in a search for k is at most 1/(1 - i/m) = m/(m - i). Averaging over all n keys in the hash table gives us the expected number of probes in a successful search:

$$\frac{1}{n} \sum_{i=0}^{n-1} \frac{m}{m-i} = \frac{m}{n} \sum_{i=0}^{n-1} \frac{1}{m-i}$$

$$= \frac{1}{\alpha} \sum_{k=m-n+1}^{m} \frac{1}{k}$$

$$\leq \frac{1}{\alpha} \int_{m-n}^{m} \frac{1}{x} dx \qquad \text{(by inequality (A.19) on page 1150)}$$

$$= \frac{1}{\alpha} (\ln m - \ln(m-n))$$

$$= \frac{1}{\alpha} \ln \frac{m}{m-n}$$

$$= \frac{1}{\alpha} \ln \frac{1}{1-\alpha}.$$

If the hash table is half full, the expected number of probes in a successful search is less than 1.387. If the hash table is 90% full, the expected number of probes is less than 2.559. If α = 1, then in an unsuccessful search, all m slots must be probed. Exercise 11.4-4 asks you to analyze a successful search when α = 1.

### **Exercises**

### *11.4-1*

Consider inserting the keys 10, 22, 31, 4, 15, 28, 17, 88, 59 into a hash table of length m = 11 using open addressing. Illustrate the result of inserting these keys using linear probing with h(k, i) = (k + i) mod m and using double hashing with h₁(k) = k and h₂(k) = 1 + (k mod (m - 1)).

### *11.4-2*

Write pseudocode for HASH-DELETE that fills the deleted key's slot with the special value DELETED, and modify HASH-SEARCH and HASH-INSERT as needed to handle DELETED.

### *11.4-3*

Consider an open-address hash table with independent uniform permutation hashing and no deletions. Give upper bounds on the expected number of probes in an unsuccessful search and on the expected number of probes in a successful search when the load factor is 3/4 and when it is 7/8.

### *11.4-4*

Show that the expected number of probes required for a successful search when α = 1 (that is, when n = m), is H_m, the mth harmonic number.

# ⋆ *11.4-5*

Show that, with double hashing, if m and h₂(k) have greatest common divisor d ≥ 1 for some key k, then an unsuccessful search for key k examines (1/d)th of the hash table before returning to slot h₁(k). Thus, when d = 1, so that m and h₂(k) are relatively prime, the search may examine the entire hash table. (*Hint:* See Chapter 31.)

# ⋆ *11.4-6*

Consider an open-address hash table with a load factor α. Approximate the nonzero value α for which the expected number of probes in an unsuccessful search equals twice the expected number of probes in a successful search. Use the upper bounds given by Theorems 11.6 and 11.8 for these expected numbers of probes.

## **11.5 Practical considerations**

Efficient hash table algorithms are not only of theoretical interest, but also of immense practical importance. Constant factors can matter. For this reason, this section discusses two aspects of modern CPUs that are not included in the standard RAM model presented in Section 2.2:

**Memory hierarchies:** The memory of modern CPUs has a number of levels, from the fast registers, through one or more levels of *cache memory*, to the main-memory level. Each successive level stores more data than the previous level, but access is slower. As a consequence, a complex computation (such as a complicated hash function) that works entirely within the fast registers can take less time than a single read operation from main memory. Furthermore, cache memory is organized in *cache blocks* of (say) 64 bytes each, which are always fetched together from main memory. There is a substantial benefit for ensuring that memory usage is local: reusing the same cache block is much more efficient than fetching a different cache block from main memory.

The standard RAM model measures efficiency of a hash-table operation by counting the number of hash-table slots probed. In practice, this metric is only a crude approximation to the truth, since once a cache block is in the cache, successive probes to that cache block are much faster than probes that must access main memory.