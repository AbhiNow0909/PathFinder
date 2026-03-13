---
topic: hashing_practical_considerations
pages: 323-333
---

**Advanced instruction sets:** Modern CPUs may have sophisticated instruction sets that implement advanced primitives useful for encryption or other forms of cryptography. These instructions may be useful in the design of exceptionally efficient hash functions.

Section 11.5.1 discusses linear probing, which becomes the collision-resolution method of choice in the presence of a memory hierarchy. Section 11.5.2 suggests how to construct "advanced" hash functions based on cryptographic primitives, suitable for use on computers with hierarchical memory models.

### **11.5.1 Linear probing**

Linear probing is often disparaged because of its poor performance in the standard RAM model. But linear probing excels for hierarchical memory models, because successive probes are usually to the same cache block of memory.

#### **Deletion with linear probing**

Another reason why linear probing is often not used in practice is that deletion seems complicated or impossible without using the special DELETED value. Yet we'll now see that deletion from a hash table based on linear probing is not all that difficult, even without the DELETED marker. The deletion procedure works for linear probing, but not for open-address probing in general, because with linear probing keys all follow the same simple cyclic probing sequence (albeit with different starting points).

The deletion procedure relies on an "inverse" function to the linear-probing hash function h(k, i) = (h₁(k) + i) mod m, which maps a key k and a probe number i to a slot number in the hash table. The inverse function g maps a key k and a slot number q, where 0 ≤ q < m, to the probe number that reaches slot q:

$$g(k,q) = (q - h_1(k)) \bmod m.$$

If 
$$h(k,i) = q$$
, then  $g(k,q) = i$ , and so  $h(k,g(k,q)) = q$ .

The procedure LINEAR-PROBING-HASH-DELETE on the facing page deletes the key stored in position q from hash table T. Figure 11.6 shows how it works. The procedure first deletes the key in position q by setting T[q] to NIL in line 2. It then searches for a slot q' (if any) that contains a key that should be moved to the slot q just vacated by key k. Line 9 asks the critical question: does the key k' in slot q' need to be moved to the vacated slot q in order to preserve the accessibility of k'? If g(k', q) < g(k', q'), then during the insertion of k' into the table, slot q was examined but found to be already occupied. But now slot q, where a search will look for k', is empty. In this case, key k' moves to slot q in line 10, and the

**Figure 11.6** Deletion in a hash table that uses linear probing. The hash table has size 10 with h₁(k) = k mod 10. **(a)** The hash table after inserting keys in the order 74, 43, 93, 18, 82, 38, 92. **(b)** The hash table after deleting the key 43 from slot 3. Key 93 moves up to slot 3 to keep it accessible, and then key 92 moves up to slot 5 just vacated by key 93. No other keys need to be moved.

search continues, to see whether any later key also needs to be moved to the slot q that was just freed up when k moved.

```
LINEAR-PROBING-HASH-DELETE(T, q)
1 while TRUE 
2    T[q] = NIL // make slot q empty 
3    q' = q // starting point for search 
4    repeat
5       q' = (q' + 1) mod m // next slot number with linear probing 
6       k' = T[q'] // next key to try to move 
7       if k' == NIL 
8          return // return when an empty slot is found 
9    until g(k', q) < g(k', q') // was empty slot q probed before q'?
10    T[q] = k' // move k' into slot q
11    q = q' // free up slot q'
```

#### **Analysis of linear probing**

Linear probing is popular to implement, but it exhibits a phenomenon known as *primary clustering*. Long runs of occupied slots build up, increasing the average 

search time. Clusters arise because an empty slot preceded by i full slots gets filled next with probability (i+1)/m. Long runs of occupied slots tend to get longer, and the average search time increases.

In the standard RAM model, primary clustering is a problem, and general double hashing usually performs better than linear probing. By contrast, in a hierarchical memory model, primary clustering is a beneficial property, as elements are often stored together in the same cache block. Searching proceeds through one cache block before advancing to search the next cache block. With linear probing, the running time for a key k of HASH-INSERT, HASH-SEARCH, or LINEAR-PROBING-HASH-DELETE is at most proportional to the distance from h₁(k) to the next empty slot.

The following theorem is due to Pagh et al. [351]. A more recent proof is given by Thorup [438]. We omit the proof here. The need for 5-independence is by no means obvious; see the cited proofs.

#### *Theorem 11.9*

If h₁ is 5-independent and α ≤ 2/3, then it takes expected constant time to search for, insert, or delete a key in a hash table using linear probing.

(Indeed, the expected operation time is O(1/ε²) for α = 1−ε.)

# ? **11.5.2 Hash functions for hierarchical memory models**

This section illustrates an approach for designing efficient hash tables in a modern computer system having a memory hierarchy.

Because of the memory hierarchy, linear probing is a good choice for resolving collisions, as probe sequences are sequential and tend to stay within cache blocks. But linear probing is most efficient when the hash function is complex (for example, 5-independent as in Theorem 11.9). Fortunately, having a memory hierarchy means that complex hash functions can be implemented efficiently.

As noted in Section 11.3.5, one approach is to use a cryptographic hash function such as SHA-256. Such functions are complex and sufficiently random for hash table applications. On machines with specialized instructions, cryptographic functions can be quite efficient.

Instead, we present here a simple hash function based only on addition, multiplication, and swapping the halves of a word. This function can be implemented entirely within the fast registers, and on a machine with a memory hierarchy, its latency is small compared with the time taken to access a random slot of the hash table. It is related to the RC6 encryption algorithm and can for practical purposes be considered a "random oracle."

### **The wee hash function**

Let w denote the word size of the machine (e.g., w = 64), assumed to be even, and let a and b be w-bit unsigned (nonnegative) integers such that a is odd. Let swap(x) denote the w-bit result of swapping the two w/2-bit halves of w-bit input x. That is,

$$swap(x) = (x \gg (w/2)) + (x \ll (w/2))$$

where "≫" is "logical right shift" (as in equation (11.2)) and "≪" is "left shift." Define

$$f_a(k) = \operatorname{swap}((2k^2 + ak) \bmod 2^w).$$

Thus, to compute f_a(k), evaluate the quadratic function 2k² + ak modulo 2^w and then swap the left and right halves of the result.

Let r denote a desired number of "rounds" for the computation of the hash function. We'll use r = 4, but the hash function is well defined for any nonnegative r. Denote by f^(r)_a(k) the result of iterating f_a a total of r times (that is, r rounds) starting with input value k. For any odd a and any r ≥ 0, the function f^(r)_a, although complicated, is one-to-one (see Exercise 11.5-1). A cryptographer would view f^(r)_a as a simple block cipher operating on w-bit input blocks, with r rounds and key a.

We first define the wee hash function h for short inputs, where by "short" we mean "whose length t is at most w bits," so that the input fits within one computer word. We would like inputs of different lengths to be hashed differently. The *wee hash function* h_{a,b,t,r}(k) for parameters a, b, and r on t-bit input k is defined as

$$h_{a,b,t,r}(k) = \left(f_{a+2t}^{(r)}(k+b)\right) \bmod m \ .$$
 (11.7)

That is, the hash value for t-bit input k is obtained by applying f^(r)_{a+2t} to k+b, then taking the final result modulo m. Adding the value b provides hash-dependent randomization of the input, in a way that ensures that for variable-length inputs the 0-length input does not have a fixed hash value. Adding the value 2t to a ensures that the hash function acts differently for inputs of different lengths. (We use 2t rather than t to ensure that the key a+2t is odd if a is odd.) We call this hash function "wee" because it uses a tiny amount of memory—more precisely, it can be implemented efficiently using only the computer's fast registers. (This hash function does not have a name in the literature; it is a variant we developed for this textbook.)

#### **Speed of the wee hash function**

It is surprising how much efficiency can be bought with locality. Experiments (unpublished, by the authors) suggest that evaluating the wee hash function takes less 

time than probing a *single* randomly chosen slot in a hash table. These experiments were run on a laptop (2019 MacBook Pro) with w = 64 and a = 123. For large hash tables, evaluating the wee hash function was 2 to 10 times faster than performing a single probe of the hash table.

#### **The wee hash function for variable-length inputs**

Sometimes inputs are long—more than one w-bit word in length—or have variable length, as discussed in Section 11.3.5. We can extend the wee hash function, defined above for inputs that are at most single w-bit word in length, to handle long or variable-length inputs. Here is one method for doing so.

Suppose that an input k has length t (measured in bits). Break k into a sequence ⟨k₁, k₂, ..., k_u⟩ of w-bit words, where u = ⌈t/w⌉, k₁ contains the least-significant w bits of k, and k_u contains the most significant bits. If t is not a multiple of w, then k_u contains fewer than w bits, in which case, pad out the unused high-order bits of k_u with 0-bits. Define the function chop to return a sequence of the w-bit words in k:

$$chop(k) = \langle k_1, k_2, \dots, k_u \rangle .$$

The most important property of the chop operation is that it is one-to-one, given t: for any two t-bit keys k and k', if k ≠ k' then chop(k) ≠ chop(k'), and k can be derived from chop(k) and t. The chop operation also has the useful property that a single-word input key yields a single-word output sequence: chop(k) = ⟨k⟩.

With the chop function in hand, we specify the wee hash function h_{a,b,t,r}(k) for an input k of length t bits as follows:

$$h_{a,b,t,r}(k) = \text{WEE}(k,a,b,t,r,m)$$
,

where the procedure WEE defined on the facing page iterates through the elements of the w-bit words returned by chop(k), applying f^(r)_a to the sum of the current word k_i and the previously computed hash value so far, finally returning the result obtained modulo m. This definition for variable-length and long (multiple-word) inputs is a consistent extension of the definition in equation (11.7) for short (singleword) inputs. For practical use, we recommend that a be a randomly chosen odd w-bit word, b be a randomly chosen w-bit word, and that r = 4.

Note that the wee hash function is really a hash function family, with individual hash functions determined by parameters a, b, t, r, and m. The (approximate) 5-independence of the wee hash function family for variable-length inputs can be argued based on the assumption that the 1-word wee hash function is a random oracle and on the security of the cipher-block-chaining message authentication code (CBC-MAC), as studied by Bellare et al. [42]. The case here is actually simpler than that studied in the literature, since if two messages have different lengths t and t' , then their "keys" are different: a + 2t ≠ a + 2t'. We omit the details.

```
WEE(k, a, b, t, r, m)
1 u = ⌈t/w⌉
2 ⟨k₁, k₂, ..., k_u⟩ = chop(k)
3 q = b
4 for i = 1 to u
5    q = f^(r)_{a+2t}(k_i + q)
6 return q mod m
```

This definition of a cryptographically inspired hash-function family is meant to be realistic, yet only illustrative, and many variations and improvements are possible. See the chapter notes for suggestions.

In summary, we see that when the memory system is hierarchical, it becomes advantageous to use linear probing (a special case of double hashing), since successive probes tend to stay in the same cache block. Furthermore, hash functions that can be implemented using only the computer's fast registers are exceptionally efficient, so they can be quite complex and even cryptographically inspired, providing the high degree of independence needed for linear probing to work most efficiently.

#### **Exercises**

# ? *11.5-1*

Complete the argument that for any odd positive integer a and any integer r ≥ 0, the function f^(r)_a is one-to-one. Use a proof by contradiction and make use of the fact that the function f_a works modulo 2^w.

# ? *11.5-2*

Argue that a random oracle is 5-independent.

# ? *11.5-3*

Consider what happens to the value f^(r)_a(k) as we flip a single bit k_i of the input value k, for various values of r. Let k = Σ^(w-1)_{i=0} k_i·2^i and g_a(k) = Σ^(w-1)_{j=0} b_j·2^j define the bit values k_i in the input (with k_0 the least-significant bit) and the bit values b_j in g_a(k) = (2k² + ak) mod 2^w (where g_a(k) is the value that, when its halves are swapped, becomes f_a(k)). Suppose that flipping a single bit k_i of the input k may cause any bit b_j of g_a(k) to flip, for j ≥ i. What is the least value of r for which flipping the value of any single bit k_i may cause *any* bit of the output f^(r)_a(k) to flip? Explain.

### **Problems**

#### *11-1 Longest-probe bound for hashing*

Suppose you are using an open-addressed hash table of size m to store n ≤ m/2 items.

- *a.* Assuming independent uniform permutation hashing, show that for i = 1, 2, ..., n, the probability is at most 2^(-p) that the ith insertion requires strictly more than p probes.
- *b.* Show that for i = 1, 2, ..., n, the probability is O(1/n²) that the ith insertion requires more than 2 lg n probes.

Let the random variable X_i denote the number of probes required by the ith insertion. You have shown in part (b) that Pr{X_i > 2 lg n} = O(1/n²). Let the random variable X = max{X_i : 1 ≤ i ≤ n} denote the maximum number of probes required by any of the n insertions.

- *c.* Show that Pr{X > 2 lg n} = O(1/n).
- *d.* Show that the expected length E[X] of the longest probe sequence is O(lg n).

#### *11-2 Searching a static set*

You are asked to implement a searchable set of n elements in which the keys are numbers. The set is static (no INSERT or DELETE operations), and the only operation required is SEARCH. You are given an arbitrary amount of time to preprocess the n elements so that SEARCH operations run quickly.

- *a.* Show how to implement SEARCH in O(lg n) worst-case time using no extra storage beyond what is needed to store the elements of the set themselves.
- *b.* Consider implementing the set by open-address hashing on m slots, and assume independent uniform permutation hashing. What is the minimum amount of extra storage m − n required to make the average performance of an unsuccessful SEARCH operation be at least as good as the bound in part (a)? Your answer should be an asymptotic bound on m − n in terms of n.

#### *11-3 Slot-size bound for chaining*

Given a hash table with n slots, with collisions resolved by chaining, suppose that n keys are inserted into the table. Each key is equally likely to be hashed to each slot. Let M be the maximum number of keys in any slot after all the keys have 

been inserted. Your mission is to prove an O(lg n / lg lg n) upper bound on E[M], the expected value of M.

*a.* Argue that the probability Q_k that exactly k keys hash to a particular slot is given by

$$Q_k = \left(\frac{1}{n}\right)^k \left(1 - \frac{1}{n}\right)^{n-k} \binom{n}{k}.$$

- *b.* Let P_k be the probability that M = k, that is, the probability that the slot containing the most keys contains k keys. Show that P_k ≤ nQ_k.
- *c.* Show that Q_k < e^k/k^k. *Hint:* Use Stirling's approximation, equation (3.25) on page 67.
- *d.* Show that there exists a constant c > 1 such that Q_{k_0} < 1/n³ for k_0 = c lg n / lg lg n. Conclude that P_k < 1/n² for k ≥ k_0 = c lg n / lg lg n.
- *e.* Argue that

$$\mathrm{E}\left[M\right] \leq \Pr\left\{M > \frac{c \lg n}{\lg \lg n}\right\} \cdot n + \Pr\left\{M \leq \frac{c \lg n}{\lg \lg n}\right\} \cdot \frac{c \lg n}{\lg \lg n} \; .$$

Conclude that E[M] = O(lg n / lg lg n).

#### *11-4 Hashing and authentication*

Let H be a family of hash functions in which each hash function h ∈ H maps the universe U of keys to {0, 1, ..., m−1}.

- *a.* Show that if the family H of hash functions is 2-independent, then it is universal.
- *b.* Suppose that the universe U is the set of n-tuples of values drawn from Z_p = {0, 1, ..., p−1}, where p is prime. Consider an element x = ⟨x₀, x₁, ..., x_{n-1}⟩ ∈ U. For any n-tuple a = ⟨a₀, a₁, ..., a_{n-1}⟩ ∈ U, define the hash function h_a by

$$h_a(x) = \left(\sum_{j=0}^{n-1} a_j x_j\right) \bmod p.$$

Let H = {h_a : a ∈ U}. Show that H is universal, but not 2-independent. (*Hint:* Find a key for which all hash functions in H produce the same value.)

*c.* Suppose that we modify H slightly from part (b): for any a ∈ U and for any b ∈ Z_p, define

$$h'_{ab}(x) = \left(\sum_{j=0}^{n-1} a_j x_j + b\right) \bmod p$$

and H' = {h'_{ab} : a ∈ U and b ∈ Z_p}. Argue that H' is 2-independent. (*Hint:* Consider fixed n-tuples x ∈ U and y ∈ U, with x_i ≠ y_i for some i. What happens to h'_{ab}(x) and h'_{ab}(y) as a_i and b range over Z_p?)

*d.* Alice and Bob secretly agree on a hash function h from a 2-independent family H of hash functions. Each h ∈ H maps from a universe of keys U to Z_p, where p is prime. Later, Alice sends a message m to Bob over the internet, where m ∈ U. She authenticates this message to Bob by also sending an authentication tag t = h(m), and Bob checks that the pair (m, t) he receives indeed satisfies t = h(m). Suppose that an adversary intercepts (m, t) en route and tries to fool Bob by replacing the pair (m, t) with a different pair (m', t'). Argue that the probability that the adversary succeeds in fooling Bob into accepting (m', t') is at most 1/p, no matter how much computing power the adversary has, even if the adversary knows the family H of hash functions used.

## **Chapter notes**

The books by Knuth [261] and Gonnet and Baeza-Yates [193] are excellent references for the analysis of hashing algorithms. Knuth credits H. P. Luhn (1953) for inventing hash tables, along with the chaining method for resolving collisions. At about the same time, G. M. Amdahl originated the idea of open addressing. The notion of a random oracle was introduced by Bellare et al. [43]. Carter and Wegman [80] introduced the notion of universal families of hash functions in 1979.

Dietzfelbinger et al. [113] invented the multiply-shift hash function and gave a proof of Theorem 11.5. Thorup [437] provides extensions and additional analysis. Thorup [438] gives a simple proof that linear probing with 5-independent hashing takes constant expected time per operation. Thorup also describes the method for deletion in a hash table using linear probing.

Fredman, Komlós, and Szemerédi [154] developed a perfect hashing scheme for static sets—"perfect" because all collisions are avoided. An extension of their method to dynamic sets, handling insertions and deletions in amortized expected time O(1), has been given by Dietzfelbinger et al. [114].

The wee hash function is based on the RC6 encryption algorithm [379]. Leiserson et al. [292] propose an "RC6MIX" function that is essentially the same as the 

wee hash function. They give experimental evidence that it has good randomness, and they also give a "DOTMIX" function for dealing with variable-length inputs. Bellare et al. [42] provide an analysis of the security of the cipher-block-chaining message authentication code. This analysis implies that the wee hash function has the desired pseudorandomness properties.

# **12 Binary Search Trees**

The search tree data structure supports each of the dynamic-set operations listed on page 250: SEARCH, MINIMUM, MAXIMUM, PREDECESSOR, SUCCESSOR, INSERT, and DELETE. Thus, you can use a search tree both as a dictionary and as a priority queue.

Basic operations on a binary search tree take time proportional to the height of the tree. For a complete binary tree with n nodes, such operations run in Θ(lg n) worst-case time. If the tree is a linear chain of n nodes, however, the same operations take Θ(n) worst-case time. In Chapter 13, we'll see a variation of binary search trees, red-black trees, whose operations guarantee a height of O(lg n). We won't prove it here, but if you build a binary search tree on a random set of n keys, its expected height is O(lg n) even if you don't try to limit its height.

After presenting the basic properties of binary search trees, the following sections show how to walk a binary search tree to print its values in sorted order, how to search for a value in a binary search tree, how to find the minimum or maximum element, how to find the predecessor or successor of an element, and how to insert into or delete from a binary search tree. The basic mathematical properties of trees appear in Appendix B.

## **12.1 What is a binary search tree?**

A binary search tree is organized, as the name suggests, in a binary tree, as shown in Figure 12.1. You can represent such a tree with a linked data structure, as in Section 10.3. In addition to a *key* and satellite data, each node object contains attributes *left* , *right* , and p that point to the nodes corresponding to its left child, its right child, and its parent, respectively. If a child or the parent is missing, the appropriate attribute contains the value NIL. The tree itself has an attribute *root*