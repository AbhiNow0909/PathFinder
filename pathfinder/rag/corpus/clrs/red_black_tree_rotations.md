---
topic: red_black_tree_rotations
pages: 357-359
---

**Figure 13.2** The rotation operations on a binary search tree. The operation LEFT-ROTATE(T, x) transforms the configuration of the two nodes on the right into the configuration on the left by changing a constant number of pointers. The inverse operation RIGHT-ROTATE(T, y) transforms the configuration on the left into the configuration on the right. The letters α, β, and γ represent arbitrary subtrees. A rotation operation preserves the binary-search-tree property: the keys in α precede x:*key*, which precedes the keys in β, which precede y:*key*, which precedes the keys in γ.

example of how LEFT-ROTATE modifies a binary search tree. The code for RIGHT-ROTATE is symmetric. Both LEFT-ROTATE and RIGHT-ROTATE run in O(1) time. Only pointers are changed by a rotation, and all other attributes in a node remain the same.

```
LEFT-ROTATE(T, x)
1 y = x:right 
2 x:right = y:left // turn y's left subtree into x's right subtree
3 if y:left ≠ T:nil // if y's left subtree is not empty . . .
4     y:left:p = x // . . . then x becomes the parent of the subtree's root
5 y:p = x:p // x's parent becomes y's parent
6 if x:p == T:nil // if x was the root . . . 
7     T:root = y // . . . then y becomes the root 
8 elseif x == x:p:left // otherwise, if x was a left child . . . 
9     x:p:left = y // . . . then y becomes a left child 
10 else x:p:right = y // otherwise, x was a right child, and now y is 
11 y:left = x // make x become y's left child
12 x:p = y
```

#### **Exercises**

#### *13.2-1*

Write pseudocode for RIGHT-ROTATE.

*13.2 Rotations 337* 

**Figure 13.3** An example of how the procedure LEFT-ROTATE.T; x/ modifies a binary search tree. Inorder tree walks of the input tree and the modified tree produce the same listing of key values.

### *13.2-2*

Argue that in every n-node binary search tree, there are exactly n - 1 possible rotations.

### *13.2-3*

Let a, b, and c be arbitrary nodes in subtrees α, β, and γ, respectively, in the right tree of Figure 13.2. How do the depths of a, b, and c change when a left rotation is performed on node x in the figure?

### *13.2-4*

Show that any arbitrary n-node binary search tree can be transformed into any other arbitrary n-node binary search tree using O(n) rotations. (*Hint:* First show that at most n - 1 right rotations suffice to transform the tree into a right-going chain.)

# ⋆ *13.2-5*

We say that a binary search tree T₁ can be *right-converted* to binary search tree T₂ if it is possible to obtain T₂ from T₁ via a series of calls to RIGHT-ROTATE. Give an example of two trees T₁ and T₂ such that T₁ cannot be right-converted to T₂. Then, show that if a tree T₁ can be right-converted to T₂, it can be right-converted using O(n²) calls to RIGHT-ROTATE.

### **13.3 Insertion**

In order to insert a node into a red-black tree with n internal nodes in O(lg n) time and maintain the red-black properties, we'll need to slightly modify the TREE-INSERT procedure on page 321. The procedure RB-INSERT starts by inserting node z into the tree T as if it were an ordinary binary search tree, and then it colors z red. (Exercise 13.3-1 asks you to explain why to make node z red rather than black.) To guarantee that the red-black properties are preserved, an auxiliary procedure RB-INSERT-FIXUP on the facing page recolors nodes and performs rotations. The call RB-INSERT(T, z) inserts node z, whose *key* is assumed to have already been filled in, into the red-black tree T.

```
RB-INSERT(T, z)
1 x = T:root // node being compared with z
2 y = T:nil // y will be parent of z
3 while x ≠ T:nil // descend until reaching the sentinel 
4     y = x
5     if z:key < x:key
6         x = x:left 
7     else x = x:right 
8 z:p = y // found the location—insert z with parent y
9 if y == T:nil 
10     T:root = z // tree T was empty 
11 elseif z:key < y:key
12     y:left = z
13 else y:right = z
14 z:left = T:nil // both of z's children are the sentinel
15 z:right = T:nil 
16 z:color = RED // the new node starts out red 
17 RB-INSERT-FIXUP(T, z) // correct any violations of red-black properties
```

The procedures TREE-INSERT and RB-INSERT differ in four ways. First, all instances of NIL in TREE-INSERT are replaced by T:*nil*. Second, lines 14–15 of RB-INSERT set z:*left* and z:*right* to T:*nil*, in order to maintain the proper tree structure. (TREE-INSERT assumed that z's children were already NIL.) Third, line 16 colors z red. Fourth, because coloring z red may cause a violation of one of the red-black properties, line 17 of RB-INSERT calls RB-INSERT-FIXUP(T, z) in order to restore the red-black properties.