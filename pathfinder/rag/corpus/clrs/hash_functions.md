---
topic: hash_functions
pages: 304-314
---

hashing, universal hashing, works well. As we saw with quicksort in Chapter 7, randomization is a powerful algorithmic design tool.

#### **What makes a good hash function?**

A good hash function satisfies (approximately) the assumption of independent uniform hashing: each key is equally likely to hash to any of the m slots, independently of where any other keys have hashed to. What does "equally likely" mean here? If the hash function is fixed, any probabilities would have to be based on the probability distribution of the input keys.

Unfortunately, you typically have no way to check this condition, unless you happen to know the probability distribution from which the keys are drawn. Moreover, the keys might not be drawn independently.

Occasionally you might know the distribution. For example, if you know that the keys are random real numbers k independently and uniformly distributed in the range 0 ≤ k < 1, then the hash function

$$h(k) = \lfloor km \rfloor$$

satisfies the condition of independent uniform hashing.

A good static hashing approach derives the hash value in a way that you expect to be independent of any patterns that might exist in the data. For example, the "division method" (discussed in Section 11.3.1) computes the hash value as the remainder when the key is divided by a specified prime number. This method may give good results, if you (somehow) choose a prime number that is unrelated to any patterns in the distribution of keys.

Random hashing, described in Section 11.3.2, picks the hash function to be used at random from a suitable family of hashing functions. This approach removes any need to know anything about the probability distribution of the input keys, as the randomization necessary for good average-case behavior then comes from the (known) random process used to pick the hash function from the family of hash functions, rather than from the (unknown) process used to create the input keys. We recommend that you use random hashing.

#### **Keys are integers, vectors, or strings**

In practice, a hash function is designed to handle keys that are one of the following two types:

• A short nonnegative integer that fits in a w-bit machine word. Typical values for w would be 32 or 64.

• A short vector of nonnegative integers, each of bounded size. For example, each element might be an 8-bit byte, in which case the vector is often called a (byte) string. The vector might be of variable length.

To begin, we assume that keys are short nonnegative integers. Handling vector keys is more complicated and discussed in Sections 11.3.5 and 11.5.2.

### **11.3.1 Static hashing**

Static hashing uses a single, fixed hash function. The only randomization available is through the (usually unknown) distribution of input keys. This section discusses two standard approaches for static hashing: the division method and the multiplication method. Although static hashing is no longer recommended, the multiplication method also provides a good foundation for "nonstatic" hashing—better known as random hashing—where the hash function is chosen at random from a suitable family of hash functions.

#### **The division method**

The *division method* for creating hash functions maps a key k into one of m slots by taking the remainder of k divided by m. That is, the hash function is

$$h(k) = k \bmod m .$$

For example, if the hash table has size m = 12 and the key is k = 100, then h(k) = 4. Since it requires only a single division operation, hashing by division is quite fast.

The division method may work well when m is a prime not too close to an exact power of 2. There is no guarantee that this method provides good average-case performance, however, and it may complicate applications since it constrains the size of the hash tables to be prime.

#### **The multiplication method**

The general *multiplication method* for creating hash functions operates in two steps. First, multiply the key k by a constant A in the range 0 < A < 1 and extract the fractional part of kA. Then, multiply this value by m and take the floor of the result. That is, the hash function is

$$h(k) = \lfloor m (kA \bmod 1) \rfloor ,$$

where "kA mod 1" means the fractional part of kA, that is, kA−⌊kA⌋. The general multiplication method has the advantage that the value of m is not critical and you can choose it independently of how you choose the multiplicative constant A.

**Figure 11.4** The multiply-shift method to compute a hash function. The w-bit representation of the key k is multiplied by the w-bit value a = A·2^w. The ℓ highest-order bits of the lower w-bit half of the product form the desired hash value h_a(k).

### **The multiply-shift method**

In practice, the multiplication method is best in the special case where the number m of hash-table slots is an exact power of 2, so that m = 2^ℓ for some integer ℓ, where ℓ ≤ w and w is the number of bits in a machine word. If you choose a fixed w-bit positive integer a = A·2^w, where 0 < A < 1 as in the multiplication method so that a is in the range 0 < a < 2^w, you can implement the function on most computers as follows. We assume that a key k fits into a single w-bit word.

Referring to Figure 11.4, first multiply k by the w-bit integer a. The result is a 2w-bit value r₁·2^w + r₀, where r₁ is the high-order w-bit word of the product and r₀ is the low-order w-bit word of the product. The desired ℓ-bit hash value consists of the ℓ most significant bits of r₀. (Since r₁ is ignored, the hash function can be implemented on a computer that produces only a w-bit product given two w-bit inputs, that is, where the multiplication operation computes modulo 2^w.)

In other words, you define the hash function h = h_a, where

$$h_a(k) = (ka \mod 2^w) \ggg (w - \ell)$$
 (11.2)

for a fixed nonzero w-bit value a. Since the product ka of two w-bit words occupies 2w bits, taking this product modulo 2^w zeroes out the high-order w bits (r₁), leaving only the low-order w bits (r₀). The ≫ operator performs a logical right shift by w−ℓ bits, shifting zeros into the vacated positions on the left, so that the ℓ most significant bits of r₀ move into the ℓ rightmost positions. (It's the same as dividing by 2^(w−ℓ) and taking the floor of the result.) The resulting value equals the ℓ most significant bits of r₀. The hash function h_a can be implemented with three machine instructions: multiplication, subtraction, and logical right shift.

As an example, suppose that k = 123456, ℓ = 14, m = 2^14 = 16384, and w = 32. Suppose further that we choose a = 2654435769 (following a suggestion 

of Knuth [261]). Then ka = 327706022297664 = (76300·2^32) + 17612864, and so r₁ = 76300 and r₀ = 17612864. The 14 most significant bits of r₀ yield the value h_a(k) = 67.

Even though the multiply-shift method is fast, it doesn't provide any guarantee of good average-case performance. The universal hashing approach presented in the next section provides such a guarantee. A simple randomized variant of the multiply-shift method works well on the average, when the program begins by picking a as a randomly chosen odd integer.

### **11.3.2 Random hashing**

Suppose that a malicious adversary chooses the keys to be hashed by some fixed hash function. Then the adversary can choose n keys that all hash to the same slot, yielding an average retrieval time of Θ(n). Any static hash function is vulnerable to such terrible worst-case behavior. The only effective way to improve the situation is to choose the hash function *randomly* in a way that is *independent* of the keys that are actually going to be stored. This approach is called *random hashing*. A special case of this approach, called *universal hashing*, can yield provably good performance on average when collisions are handled by chaining, no matter which keys the adversary chooses.

To use random hashing, at the beginning of program execution you select the hash function at random from a suitable family of functions. As in the case of quicksort, randomization guarantees that no single input always evokes worst-case behavior. Because you randomly select the hash function, the algorithm can behave differently on each execution, even for the same set of keys to be hashed, guaranteeing good average-case performance.

Let H be a finite family of hash functions that map a given universe U of keys into the range {0, 1, ..., m−1}. Such a family is said to be *universal* if for each pair of distinct keys k₁, k₂ ∈ U, the number of hash functions h ∈ H for which h(k₁) = h(k₂) is at most |H|/m. In other words, with a hash function randomly chosen from H, the chance of a collision between distinct keys k₁ and k₂ is no more than the chance 1/m of a collision if h(k₁) and h(k₂) were randomly and independently chosen from the set {0, 1, ..., m−1}.

Independent uniform hashing is the same as picking a hash function uniformly at random from a family of m^n hash functions, each member of that family mapping the n keys to the m hash values in a different way.

Every independent uniform random family of hash function is universal, but the converse need not be true: consider the case where U = {0, 1, ..., m−1} and the only hash function in the family is the identity function. The probability that two distinct keys collide is zero, even though each key hashes to a fixed value.

The following corollary to Theorem 11.2 on page 279 says that universal hashing provides the desired payoff: it becomes impossible for an adversary to pick a sequence of operations that forces the worst-case running time.

### *Corollary 11.3*

Using universal hashing and collision resolution by chaining in an initially empty table with m slots, it takes Θ(s) expected time to handle any sequence of s INSERT, SEARCH, and DELETE operations containing n = O(m) INSERT operations.

*Proof* The INSERT and DELETE operations take constant time. Since the number n of insertions is O(m), we have that α = O(1). Furthermore, the expected time for each SEARCH operation is O(1), which can be seen by examining the proof of Theorem 11.2. That analysis depends only on collision probabilities, which are 1/m for any pair k₁, k₂ of keys by the choice of an independent uniform hash function in that theorem. Using a universal family of hash functions here instead of using independent uniform hashing changes the probability of collision from 1/m to at most 1/m. By linearity of expectation, therefore, the expected time for the entire sequence of s operations is O(s). Since each operation takes Ω(1) time, the Θ(s) bound follows.

#### **11.3.3 Achievable properties of random hashing**

There is a rich literature on the properties a family H of hash functions can have, and how they relate to the efficiency of hashing. We summarize a few of the most interesting ones here.

Let H be a family of hash functions, each with domain U and range {0, 1, ..., m−1}, and let h be any hash function that is picked uniformly at random from H. The probabilities mentioned are probabilities over the picks of h.

- The family H is *uniform* if for any key k in U and any slot q in the range {0, 1, ..., m−1}, the probability that h(k) = q is 1/m.
- The family H is *universal* if for any distinct keys k₁ and k₂ in U, the probability that h(k₁) = h(k₂) is at most 1/m.
- The family H of hash functions is *ε-universal* if for any distinct keys k₁ and k₂ in U, the probability that h(k₁) = h(k₂) is at most ε. Therefore, a universal family of hash functions is also 1/m-universal.²

² In the literature, a (c/m)-universal hash function is sometimes called c-universal or c-approximately universal. We'll stick with the notation (c/m)-universal.

• The family H is *d-independent* if for any distinct keys k₁, k₂, ..., k_d in U and any slots q₁, q₂, ..., q_d, not necessarily distinct, in {0, 1, ..., m−1}, the probability that h(k_i) = q_i for i = 1, 2, ..., d is 1/m^d.

Universal hash-function families are of particular interest, as they are the simplest type supporting provably efficient hash-table operations for any input data set. Many other interesting and desirable properties, such as those noted above, are also possible and allow for efficient specialized hash-table operations.

### **11.3.4 Designing a universal family of hash functions**

This section present two ways to design a universal (or ε-universal) family of hash functions: one based on number theory and another based on a randomized variant of the multiply-shift method presented in Section 11.3.1. The first method is a bit easier to prove universal, but the second method is newer and faster in practice.

#### **A universal family of hash functions based on number theory**

We can design a universal family of hash functions using a little number theory. You may wish to refer to Chapter 31 if you are unfamiliar with basic concepts in number theory.

Begin by choosing a prime number p large enough so that every possible key k lies in the range 0 to p−1, inclusive. We assume here that p has a "reasonable" length. (See Section 11.3.5 for a discussion of methods for handling long input keys, such as variable-length strings.) Let Z_p denote the set {0, 1, ..., p−1}, and let Z*_p denote the set {1, 2, ..., p−1}. Since p is prime, we can solve equations modulo p with the methods given in Chapter 31. Because the size of the universe of keys is greater than the number of slots in the hash table (otherwise, just use direct addressing), we have p > m.

Given any a ∈ Z*_p and any b ∈ Z_p, define the hash function h_ab as a linear transformation followed by reductions modulo p and then modulo m:

$$h_{ab}(k) = ((ak+b) \bmod p) \bmod m.$$
(11.3)

For example, with p = 17 and m = 6, we have

$$h_{3,4}(8) = ((3 \cdot 8 + 4) \mod 17) \mod 6$$
  
=  $(28 \mod 17) \mod 6$   
=  $11 \mod 6$   
=  $5$ .

Given p and m, the family of all such hash functions is

$$\mathcal{H}_{pm} = \left\{ h_{ab} : a \in \mathbb{Z}_p^* \text{ and } b \in \mathbb{Z}_p \right\} . \tag{11.4}$$

Each hash function h_ab maps Z_p to Z_m. This family of hash functions has the nice property that the size m of the output range (which is the size of the hash table) is arbitrary—it need not be prime. Since you can choose from among p−1 values for a and p values for b, the family H_pm contains p(p−1) hash functions.

### *Theorem 11.4*

The family H_pm of hash functions defined by equations (11.3) and (11.4) is universal.

*Proof* Consider two distinct keys k₁ and k₂ from Z_p, so that k₁ ≠ k₂. For a given hash function h_ab, let

$$r_1 = (ak_1 + b) \mod p,$$
  

$$r_2 = (ak_2 + b) \mod p.$$

We first note that r₁ ≠ r₂. Why? Since we have r₁−r₂ = a(k₁−k₂) (mod p), it follows that r₁ ≠ r₂ because p is prime and both a and (k₁−k₂) are nonzero modulo p. By Theorem 31.6 on page 908, their product must also be nonzero modulo p. Therefore, when computing any h_ab ∈ H_pm, distinct inputs k₁ and k₂ map to distinct values r₁ and r₂ modulo p, and there are no collisions yet at the "mod p level." Moreover, each of the possible p(p−1) choices for the pair (a, b) with a ≠ 0 yields a *different* resulting pair (r₁, r₂) with r₁ ≠ r₂, since we can solve for a and b given r₁ and r₂:

$$a = ((r_1 - r_2)((k_1 - k_2)^{-1} \mod p)) \mod p$$
,  
 $b = (r_1 - ak_1) \mod p$ ,

where ((k₁−k₂)^(−1) mod p) denotes the unique multiplicative inverse, modulo p, of k₁−k₂. For each of the p possible values of r₁, there are only p−1 possible values of r₂ that do not equal r₁, making only p(p−1) possible pairs (r₁, r₂) with r₁ ≠ r₂. Therefore, there is a one-to-one correspondence between pairs (a, b) with a ≠ 0 and pairs (r₁, r₂) with r₁ ≠ r₂. Thus, for any given pair of distinct inputs k₁ and k₂, if we pick (a, b) uniformly at random from Z*_p × Z_p, the resulting pair (r₁, r₂) is equally likely to be any pair of distinct values modulo p.

Therefore, the probability that distinct keys k₁ and k₂ collide is equal to the probability that r₁ = r₂ (mod m) when r₁ and r₂ are randomly chosen as distinct values modulo p. For a given value of r₁, of the p−1 possible remaining values for r₂, the number of values r₂ such that r₂ ≠ r₁ and r₂ = r₁ (mod m) is at most

$$\left\lceil \frac{p}{m} \right\rceil - 1 \le \frac{p + m - 1}{m} - 1 \quad \text{(by inequality (3.7) on page 64)}$$

$$= \frac{p - 1}{m}.$$

The probability that r₂ collides with r₁ when reduced modulo m is at most ((p−1)/m)/(p−1) = 1/m, since r₂ is equally likely to be any of the p−1 values in Z_p that are different from r₁, but at most (p−1)/m of those values are equivalent to r₁ modulo m.

Therefore, for any pair of distinct values k₁, k₂ ∈ Z_p,

$$\Pr\{h_{ab}(k_1) = h_{ab}(k_2)\} \le 1/m ,$$

so that H_pm is indeed universal.

### **A 2/m-universal family of hash functions based on the multiply-shift method**

We recommend that in practice you use the following hash-function family based on the multiply-shift method. It is exceptionally efficient and (although we omit the proof) provably 2/m-universal. Define H to be the family of multiply-shift hash functions with odd constants a:

$$\mathcal{H} = \{h_a : a \text{ is odd}, 1 \le a < m, \text{ and } h_a \text{ is defined by equation (11.2)} \}$$
 . (11.5)

### *Theorem 11.5*

The family of hash functions H given by equation (11.5) is 2/m-universal.

That is, the probability that any two distinct keys collide is at most 2/m. In many practical situations, the speed of computing the hash function more than compensates for the higher upper bound on the probability that two distinct keys collide when compared with a universal hash function.

### **11.3.5 Hashing long inputs such as vectors or strings**

Sometimes hash function inputs are so long that they cannot be easily encoded modulo a reasonably sized prime number p or encoded within a single word of, say, 64 bits. As an example, consider the class of vectors, such as vectors of 8-bit bytes (which is how strings in many programming languages are stored). A vector might have an arbitrary nonnegative length, in which case the length of the input to the hash function may vary from input to input.

### **Number-theoretic approaches**

One way to design good hash functions for variable-length inputs is to extend the ideas used in Section 11.3.4 to design universal hash functions. Exercise 11.3-6 explores one such approach.

### **Cryptographic hashing**

Another way to design a good hash function for variable-length inputs is to use a hash function designed for cryptographic applications. *Cryptographic hash functions* are complex pseudorandom functions, designed for applications requiring properties beyond those needed here, but are robust, widely implemented, and usable as hash functions for hash tables.

A cryptographic hash function takes as input an arbitrary byte string and returns a fixed-length output. For example, the NIST standard deterministic cryptographic hash function SHA-256 [346] produces a 256-bit (32-byte) output for any input.

Some chip manufacturers include instructions in their CPU architectures to provide fast implementations of some cryptographic functions. Of particular interest are instructions that efficiently implement rounds of the Advanced Encryption Standard (AES), the "AES-NI" instructions. These instructions execute in a few tens of nanoseconds, which is generally fast enough for use with hash tables. A message authentication code such as CBC-MAC based on AES and the use of the AES-NI instructions could be a useful and efficient hash function. We don't pursue the potential use of specialized instruction sets further here.

Cryptographic hash functions are useful because they provide a way of implementing an approximate version of a random oracle. As noted earlier, a random oracle is equivalent to an independent uniform hash function family. From a theoretical point of view, a random oracle is an unachievable ideal: a deterministic function that provides a randomly selected output for each input. Because it is deterministic, it provides the same output if queried again for the same input. From a practical point of view, constructions of hash function families based on cryptographic hash functions are sensible substitutes for random oracles.

There are many ways to use a cryptographic hash function as a hash function. For example, we could define

$$h(k) = SHA-256(k) \bmod m.$$

To define a family of such hash functions one may prepend a "salt" string a to the input before hashing it, as in

$$h_a(k) = SHA-256(a \parallel k) \bmod m ,$$

where a∥k denotes the string formed by concatenating the strings a and k. The literature on message authentication codes (MACs) provides additional approaches.

Cryptographic approaches to hash-function design are becoming more practical as computers arrange their memories in hierarchies of differing capacities and speeds. Section 11.5 discusses one hash-function design based on the RC6 encryption method.

### **Exercises**

### *11.3-1*

You wish to search a linked list of length n, where each element contains a key k along with a hash value h(k). Each key is a long character string. How might you take advantage of the hash values when searching the list for an element with a given key?

### *11.3-2*

You hash a string of r characters into m slots by treating it as a radix-128 number and then using the division method. You can represent the number m as a 32-bit computer word, but the string of r characters, treated as a radix-128 number, takes many words. How can you apply the division method to compute the hash value of the character string without using more than a constant number of words of storage outside the string itself?

### *11.3-3*

Consider a version of the division method in which h(k) = k mod m, where m = 2^p − 1 and k is a character string interpreted in radix 2^p. Show that if string x can be converted to string y by permuting its characters, then x and y hash to the same value. Give an example of an application in which this property would be undesirable in a hash function.

#### *11.3-4*

Consider a hash table of size m = 1000 and a corresponding hash function h(k) = ⌊m(kA mod 1)⌋ for A = (√5−1)/2. Compute the locations to which the keys 61, 62, 63, 64, and 65 are mapped.

# ? *11.3-5*

Show that any ε-universal family H of hash functions from a finite set U to a finite set Q has ε ≥ 1/|Q|−1/|U|.

# ? *11.3-6*

Let U be the set of d-tuples of values drawn from Z_p, and let Q = Z_p, where p is prime. Define the hash function h_b : U → Q for b ∈ Z_p on an input d-tuple ⟨a₀, a₁, ..., a_{d−1}⟩ from U as

$$h_b(\langle a_0, a_1, \dots, a_{d-1} \rangle) = \left(\sum_{j=0}^{d-1} a_j b^j\right) \bmod p$$
,

and let H = {h_b : b ∈ Z_p}. Argue that H is ε-universal for ε = (d−1)/p. (*Hint:* See Exercise 31.4-4).

### **11.4 Open addressing**

This section describes open addressing, a method for collision resolution that, unlike chaining, does not make use of storage outside of the hash table itself. In *open addressing*, all elements occupy the hash table itself. That is, each table entry contains either an element of the dynamic set or NIL. No lists or elements are stored outside the table, unlike in chaining. Thus, in open addressing, the hash table can "fill up" so that no further insertions can be made. One consequence is that the load factor α can never exceed 1.

Collisions are handled as follows: when a new element is to be inserted into the table, it is placed in its "first-choice" location if possible. If that location is already occupied, the new element is placed in its "second-choice" location. The process continues until an empty slot is found in which to place the new element. Different elements have different preference orders for the locations.

To search for an element, systematically examine the preferred table slots for that element, in order of decreasing preference, until either you find the desired element or you find an empty slot and thus verify that the element is not in the table.

Of course, you could use chaining and store the linked lists inside the hash table, in the otherwise unused hash-table slots (see Exercise 11.2-4), but the advantage of open addressing is that it avoids pointers altogether. Instead of following pointers, you compute the sequence of slots to be examined. The memory freed by not storing pointers provides the hash table with a larger number of slots in the same amount of memory, potentially yielding fewer collisions and faster retrieval.

To perform insertion using open addressing, successively examine, or *probe*, the hash table until you find an empty slot in which to put the key. Instead of being fixed in the order 0, 1, ..., m−1 (which implies a Θ(n) search time), the sequence of positions probed depends upon the key being inserted. To determine which slots to probe, the hash function includes the probe number (starting from 0) as a second input. Thus, the hash function becomes

$$h: U \times \{0, 1, \dots, m-1\} \to \{0, 1, \dots, m-1\}$$
.

Open addressing requires that for every key k, the *probe sequence* ⟨h(k, 0), h(k, 1), ..., h(k, m−1)⟩ be a permutation of ⟨0, 1, ..., m−1⟩, so that every hash-table position is eventually considered as a slot for a new key as the table fills up. The HASH-INSERT procedure on the following page assumes that the elements in the hash table T are keys with no satellite information: the key k is identical to the element containing key k. Each slot contains either a key or NIL (if the slot is empty). The HASH-INSERT procedure takes as input a hash table T and a key k