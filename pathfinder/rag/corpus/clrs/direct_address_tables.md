---
topic: direct_address_tables
pages: 295-296
---

```
DIRECT-ADDRESS-SEARCH .T; k/
1 return T [k�
DIRECT-ADDRESS-INSERT .T; x/
1 T [x:key� D x
DIRECT-ADDRESS-DELETE .T; x/
1 T [x:key� D NIL
```

### **Exercises**

## *11.1-1*

A dynamic set S is represented by a direct-address table T of length m. Describe a procedure that finds the maximum element of S. What is the worst-case performance of your procedure?

## *11.1-2*

A *bit vector* is simply an array of bits (each either 0 or 1). A bit vector of length m takes much less space than an array of m pointers. Describe how to use a bit vector to represent a dynamic set of distinct elements drawn from the set {0, 1, ..., m − 1} and with no satellite data. Dictionary operations should run in O(1) time.

## *11.1-3*

Suggest how to implement a direct-address table in which the keys of stored elements do not need to be distinct and the elements can have satellite data. All three dictionary operations (INSERT, DELETE, and SEARCH) should run in O(1) time. (Don't forget that DELETE takes as an argument a pointer to an object to be deleted, not a key.)

# ? *11.1-4*

Suppose that you want to implement a dictionary by using direct addressing on a *huge* array. That is, if the array size is m and the dictionary contains at most n elements at any one time, then m ≫ n. At the start, the array entries may contain garbage, and initializing the entire array is impractical because of its size. Describe a scheme for implementing a direct-address dictionary on a huge array. Each stored object should use O(1) space; the operations SEARCH, INSERT, and DELETE should take O(1) time each; and initializing the data structure should take O(1) time. (*Hint:* Use an additional array, treated somewhat like a stack whose size is the number of keys actually stored in the dictionary, to help determine whether a given entry in the huge array is valid or not.)

*11.2 Hash tables 275* 

## **11.2 Hash tables**

The downside of direct addressing is apparent: if the universe U is large or infinite, storing a table T of size |U| may be impractical, or even impossible, given the memory available on a typical computer. Furthermore, the set K of keys *actually stored* may be so small relative to U that most of the space allocated for T would be wasted.

When the set K of keys stored in a dictionary is much smaller than the universe U of all possible keys, a hash table requires much less storage than a direct-address table. Specifically, the storage requirement reduces to Θ(|K|) while maintaining the benefit that searching for an element in the hash table still requires only O(1) time. The catch is that this bound is for the *average-case time*, ¹ whereas for direct addressing it holds for the *worst-case time*.

With direct addressing, an element with key k is stored in slot k, but with hashing, we use a *hash function* h to compute the slot number from the key k, so that the element goes into slot h(k). The hash function h maps the universe U of keys into the slots of a *hash table* T[0 : m − 1]:

$$h: U \to \{0, 1, \dots, m-1\}$$
,

where the size m of the hash table is typically much less than |U|. We say that an element with key k *hashes* to slot h(k), and we also say that h(k) is the *hash value* of key k. Figure 11.2 illustrates the basic idea. The hash function reduces the range of array indices and hence the size of the array. Instead of a size of |U|, the array can have size m. An example of a simple, but not particularly good, hash function is h(k) = k mod m.

There is one hitch, namely that two keys may hash to the same slot. We call this situation a *collision*. Fortunately, there are effective techniques for resolving the conflict created by collisions.

Of course, the ideal solution is to avoid collisions altogether. We might try to achieve this goal by choosing a suitable hash function h. One idea is to make h appear to be "random," thus avoiding collisions or at least minimizing their number. The very term "to hash," evoking images of random mixing and chopping, captures the spirit of this approach. (Of course, a hash function h must be deterministic in that a given input k must always produce the same output h(k).) Because |U| > m, however, there must be at least two keys that have the same hash value,

<sup>1</sup> The definition of "average-case" requires care—are we assuming an input distribution over the keys, or are we randomizing the choice of hash function itself? We'll consider both approaches, but with an emphasis on the use of a randomly chosen hash function.