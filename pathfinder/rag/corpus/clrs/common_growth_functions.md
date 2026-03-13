---
topic: common_growth_functions
pages: 85-97
---
# **3.3 Standard notations and common functions**

This section reviews some standard mathematical functions and notations and explores the relationships among them. It also illustrates the use of the asymptotic notations.

### **Monotonicity**

A function f(n) is *monotonically increasing* if m ≤ n implies f(m) ≤ f(n). Similarly, it is *monotonically decreasing* if m ≤ n implies f(m) ≥ f(n). A function f(n) is *strictly increasing* if m < n implies f(m) < f(n) and *strictly decreasing* if m < n implies f(m) > f(n).

#### **Floors and ceilings**

For any real number x, we denote the greatest integer less than or equal to x by ⌊x⌋ (read "the floor of x") and the least integer greater than or equal to x by ⌈x⌉ (read "the ceiling of x"). The floor function is monotonically increasing, as is the ceiling function.

Floors and ceilings obey the following properties. For any integer n, we have

$$\lfloor n \rfloor = n = \lceil n \rceil . \tag{3.1}$$

For all real x, we have

$$x - 1 < \lfloor x \rfloor \le x \le \lceil x \rceil < x + 1. \tag{3.2}$$

We also have

$$-\lfloor x \rfloor = \lceil -x \rceil , \qquad (3.3)$$

or equivalently,

$$-\lceil x \rceil = \lfloor -x \rfloor . \tag{3.4}$$

For any real number x ≥ 0 and integers a, b > 0, we have

$$\left\lceil \frac{\lceil x/a \rceil}{b} \right\rceil = \left\lceil \frac{x}{ab} \right\rceil, \tag{3.5}$$

$$\left\lfloor \frac{\lfloor x/a \rfloor}{b} \right\rfloor = \left\lfloor \frac{x}{ab} \right\rfloor, \tag{3.6}$$

$$\left\lceil \frac{a}{b} \right\rceil \le \frac{a + (b-1)}{b} \,, \tag{3.7}$$

$$\left\lfloor \frac{a}{b} \right\rfloor \ge \frac{a - (b - 1)}{b} \,. \tag{3.8}$$

For any integer n and real number x, we have

$$\lfloor n+x\rfloor = n+\lfloor x\rfloor , \qquad (3.9)$$

$$\lceil n+x \rceil = n + \lceil x \rceil . \tag{3.10}$$

## **Modular arithmetic**

For any integer a and any positive integer n, the value a mod n is the *remainder* (or *residue*) of the quotient a=n:

$$a \bmod n = a - n \lfloor a/n \rfloor . \tag{3.11}$$

It follows that

$$0 \le a \bmod n < n \;, \tag{3.12}$$

even when a is negative.

Given a well-defined notion of the remainder of one integer when divided by another, it is convenient to provide special notation to indicate equality of remainders. If (a mod n) = (b mod n), we write a ≡ b (mod n) and say that a is *equivalent* to b, modulo n. In other words, a ≡ b (mod n) if a and b have the same remainder when divided by n. Equivalently, a ≡ b (mod n) if and only if n is a divisor of b - a. We write a ≢ b (mod n) if a is not equivalent to b, modulo n.

## **Polynomials**

Given a nonnegative integer d, a *polynomial in* n *of degree* d is a function p(n) of the form

$$p(n) = \sum_{i=0}^d a_i n^i ,$$

where the constants a₀, a₁, ..., aₐ are the *coefficients* of the polynomial and aₐ ≠ 0. A polynomial is asymptotically positive if and only if aₐ > 0. For an asymptotically positive polynomial p(n) of degree d, we have p(n) = Θ(nᵈ). For any real constant a ≥ 0, the function nᵃ is monotonically increasing, and for any real constant a ≤ 0, the function nᵃ is monotonically decreasing. We say that a function f(n) is *polynomially bounded* if f(n) = O(nᵏ) for some constant k.

### **Exponentials**

For all real a > 0, m, and n, we have the following identities:

$$a^{0} = 1$$
,  
 $a^{1} = a$ ,  
 $a^{-1} = 1/a$ ,  
 $(a^{m})^{n} = a^{mn}$ ,  
 $(a^{m})^{n} = (a^{n})^{m}$ ,  
 $a^{m}a^{n} = a^{m+n}$ .

For all n and a ≥ 1, the function aⁿ is monotonically increasing in n. When convenient, we assume that 0⁰ = 1.

We can relate the rates of growth of polynomials and exponentials by the following fact. For all real constants a > 1 and b, we have

$$\lim_{n\to\infty}\frac{n^b}{a^n}=0\;,$$

from which we can conclude that

$$n^b = o(a^n) . (3.13)$$

Thus, any exponential function with a base strictly greater than 1 grows faster than any polynomial function.

Using e to denote 2.71828..., the base of the natural-logarithm function, we have for all real x,

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \dots = \sum_{i=0}^{\infty} \frac{x^i}{i!}$$

where "!" denotes the factorial function defined later in this section. For all real x, we have the inequality

$$1 + x \le e^x \,, \tag{3.14}$$

where equality holds only when x = 0. When jxj ≤ 1, we have the approximation

$$1 + x \le e^x \le 1 + x + x^2 \,. \tag{3.15}$$

When x → 0, the approximation of eˣ by 1 + x is quite good:

$$e^x = 1 + x + \Theta(x^2) .$$

(In this equation, the asymptotic notation is used to describe the limiting behavior as x → 0 rather than as x → ∞.) We have for all x,

$$\lim_{n \to \infty} \left( 1 + \frac{x}{n} \right)^n = e^x \,. \tag{3.16}$$

## **Logarithms**

We use the following notations:

lg n = log₂ n (binary logarithm) ,

ln n = logₑ n (natural logarithm) ,

lgᵏ n = (lg n)ᵏ (exponentiation) ,

lg lg n = lg(lg n) (composition) .

We adopt the following notational convention: in the absence of parentheses, *a logarithm function applies only to the next term in the formula*, so that lg n + 1 means (lg n) + 1 and not lg(n + 1).

For any constant b > 1, the function logᵇ n is undefined if n ≤ 0, strictly increasing if n > 0, negative if 0 < n < 1, positive if n > 1, and 0 if n = 1. For all real a > 0, b > 0, c > 0, and n, we have

$$a = b^{\log_b a}, (3.17)$$

$$\log_c(ab) = \log_c a + \log_c b , \qquad (3.18)$$

$$\log_b a^n = n \log_b a ,$$

$$\log_b a = \frac{\log_c a}{\log_c b} \,, \tag{3.19}$$

$$\log_b(1/a) = -\log_b a , \qquad (3.20)$$

$$\log_b a = \frac{1}{\log_a b} \,,$$

$$a^{\log_b c} = c^{\log_b a}, \tag{3.21}$$

where, in each equation above, logarithm bases are not 1.

By equation (3.19), changing the base of a logarithm from one constant to another changes the value of the logarithm by only a constant factor. Consequently, we often use the notation "lg n" when we don't care about constant factors, such as in O-notation. Computer scientists find 2 to be the most natural base for logarithms because so many algorithms and data structures involve splitting a problem into two parts.

There is a simple series expansion for ln(1 + x) when |x| < 1:

$$\ln(1+x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \frac{x^5}{5} - \dots$$
 (3.22)

We also have the following inequalities for x > -1:

$$\frac{x}{1+x} \le \ln(1+x) \le x \,, \tag{3.23}$$

where equality holds only for x = 0.

We say that a function f(n) is *polylogarithmically bounded* if f(n) = O(lgᵏ n) for some constant k. We can relate the growth of polynomials and polylogarithms by substituting lg n for n and 2ᵃ for a in equation (3.13). For all real constants a > 0 and b, we have

$$\lg^b n = o(n^a) . (3.24)$$

Thus, any positive polynomial function grows faster than any polylogarithmic function.

## **Factorials**

The notation n! (read "n factorial") is defined for integers n ≥ 0 as

$$n! = \begin{cases} 1 & \text{if } n = 0, \\ n \cdot (n-1)! & \text{if } n > 0. \end{cases}$$

Thus, n! = 1 · 2 · 3 · · · n.

A weak upper bound on the factorial function is n! ≤ nⁿ, since each of the n terms in the factorial product is at most n. *Stirling's approximation*,

$$n! = \sqrt{2\pi n} \left(\frac{n}{e}\right)^n \left(1 + \Theta\left(\frac{1}{n}\right)\right) , \qquad (3.25)$$

where e is the base of the natural logarithm, gives us a tighter upper bound, and a lower bound as well. Exercise 3.3-4 asks you to prove the three facts

$$n! = o(n^n), (3.26)$$

$$n! = \omega(2^n), \qquad (3.27)$$

$$\lg(n!) = \Theta(n \lg n) , \qquad (3.28)$$

where Stirling's approximation is helpful in proving equation (3.28). The following equation also holds for all n ≥ 1:

$$n! = \sqrt{2\pi n} \left(\frac{n}{e}\right)^n e^{\alpha_n} \tag{3.29}$$

where

$$\frac{1}{12n+1} < \alpha_n < \frac{1}{12n} .$$

## **Functional iteration**

We use the notation fᵢ(n) to denote the function f(n) iteratively applied i times to an initial value of n. Formally, let f(n) be a function over the reals. For nonnegative integers i, we recursively define

$$f^{(i)}(n) = \begin{cases} n & \text{if } i = 0, \\ f(f^{(i-1)}(n)) & \text{if } i > 0. \end{cases}$$
 (3.30)

For example, if f(n) = 2n, then fᵢ(n) = 2ⁱn.

## **The iterated logarithm function**

We use the notation lg* n (read "log star of n") to denote the iterated logarithm, defined as follows. Let lgᵢ n be as defined above, with f(n) = lg n. Because the logarithm of a nonpositive number is undefined, lgᵢ n is defined only if lgᵢ⁻¹ n > 0. Be sure to distinguish lgᵢ n (the logarithm function applied i times in succession, starting with argument n) from lgⁱ n (the logarithm of n raised to the ith power). Then we define the iterated logarithm function as

$$\lg^* n = \min \{ i \ge 0 : \lg^{(i)} n \le 1 \}$$
.

The iterated logarithm is a *very* slowly growing function:

$$lg^* 2 = 1,$$

$$lg^* 4 = 2,$$

$$lg^* 16 = 3,$$

$$lg^* 65536 = 4,$$

$$lg^* (2^{65536}) = 5.$$

Since the number of atoms in the observable universe is estimated to be about 10⁸⁰, which is much less than 2⁶⁵⁵³⁶ = 10⁶⁵⁵³⁶/lg 10 ≈ 10¹⁹⁸²⁸, we rarely encounter an input size n for which lg* n > 5.

## **Fibonacci numbers**

We define the *Fibonacci numbers* Fᵢ, for i ≥ 0, as follows:

$$F_{i} = \begin{cases} 0 & \text{if } i = 0, \\ 1 & \text{if } i = 1, \\ F_{i-1} + F_{i-2} & \text{if } i \ge 2. \end{cases}$$
(3.31)

Thus, after the first two, each Fibonacci number is the sum of the two previous ones, yielding the sequence

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

Fibonacci numbers are related to the *golden ratio* φ and its conjugate φ̂, which are the two roots of the equation

$$x^2 = x + 1.$$

As Exercise 3.3-7 asks you to prove, the golden ratio is given by

$$\phi = \frac{1 + \sqrt{5}}{2}$$
= 1.61803..., (3.32)

and its conjugate, by

$$\hat{\phi} = \frac{1 - \sqrt{5}}{2} = -.61803....$$
 (3.33)

Specifically, we have

$$F_i = \frac{\phi^i - \widehat{\phi}^i}{\sqrt{5}} ,$$

which can be proved by induction (Exercise 3.3-8). Since |φ̂| < 1, we have

$$\frac{\left|\hat{\phi}^{i}\right|}{\sqrt{5}} < \frac{1}{\sqrt{5}} < \frac{1}{2},$$

which implies that

$$F_i = \left\lfloor \frac{\phi^i}{\sqrt{5}} + \frac{1}{2} \right\rfloor \,, \tag{3.34}$$

which is to say that the ith Fibonacci number Fᵢ is equal to φⁱ/√5 rounded to the nearest integer. Thus, Fibonacci numbers grow exponentially.

## **Exercises**

## *3.3-1*

Show that if f(n) and g(n) are monotonically increasing functions, then so are the functions f(n) + g(n) and f(g(n)), and if f(n) and g(n) are in addition nonnegative, then f(n) · g(n) is monotonically increasing.

# *3.3-2*

Prove that ⌊αn⌋ + ⌈(1 - α)n⌉ = n for any integer n and real number α in the range 0 ≤ α ≤ 1.

# *3.3-3*

Use equation (3.14) or other means to show that (n + o(n))ᵏ = Θ(nᵏ) for any real constant k. Conclude that ⌈n⌉ᵏ = Θ(nᵏ) and ⌊n⌋ᵏ = Θ(nᵏ).

# *3.3-4*

Prove the following:

- *a.* Equation (3.21).
- *b.* Equations (3.26)-(3.28).
- *c.* lg(Θ(n)) = Θ(lg n).

# ★ *3.3-5*

Is the function ⌈lg n⌉! polynomially bounded? Is the function ⌈lg lg n⌉! polynomially bounded?

# ★ *3.3-6*

Which is asymptotically larger: lg(lg* n) or lg*(lg n)?

## *3.3-7*

Show that the golden ratio φ and its conjugate φ̂ both satisfy the equation x² = x + 1.

#### *3.3-8*

Prove by induction that the ith Fibonacci number satisfies the equation

$$F_i = (\phi^i - \hat{\phi}^i)/\sqrt{5} ,$$

where φ is the golden ratio and φ̂ is its conjugate.

## *3.3-9*

Show that k lg k = Θ(n) implies k = Θ(n/lg n).

# **Problems**

## *3-1 Asymptotic behavior of polynomials*

Let

$$p(n) = \sum_{i=0}^d a_i n^i ,$$

where aᵈ > 0, be a degree-d polynomial in n, and let k be a constant. Use the definitions of the asymptotic notations to prove the following properties.

**a.** If 
$$k \ge d$$
, then  $p(n) = O(n^k)$ .

**b.** If 
$$k \le d$$
, then  $p(n) = \Omega(n^k)$ .

c. If 
$$k = d$$
, then  $p(n) = \Theta(n^k)$ .

**d.** If 
$$k > d$$
, then  $p(n) = o(n^k)$ .

e. If 
$$k < d$$
, then  $p(n) = \omega(n^k)$ .

## *3-2 Relative asymptotic growths*

Indicate, for each pair of expressions (A, B) in the table below whether A is O, o, Ω, ω, or Θ of B. Assume that k ≥ 1, ε > 0, and c > 1 are constants. Write your answer in the form of the table with "yes" or "no" written in each box.

|    | A         | B          | O | o | Ω | ω | Θ |
|----|-----------|------------|---|---|----|----|----|---|
| a. | lgᵏ n | nᵋ         |   |   |    |    |    |
| b. | nᵏ    | cⁿ         |   |   |    |    |    |
| c. | √n    | n^sin n    |   |   |    |    |    |
| d. | 2ⁿ    | 2ⁿᐟ²     |   |   |    |    |    |
| e. | n^lg c | c^lg n     |   |   |    |    |    |
| f. | lg(n!)    | lg(nⁿ)     |   |   |    |    |    |

# *3-3 Ordering by asymptotic growth rates*

*a.* Rank the following functions by order of growth. That is, find an arrangement g₁, g₂, ..., g₃₀ of the functions satisfying g₁ = Ω(g₂), g₂ = Ω(g₃), ..., g₂₉ = Ω(g₃₀). Partition your list into equivalence classes such that functions f(n) and g(n) belong to the same class if and only if f(n) = Θ(g(n)).

$$\begin{array}{cccccccccccccccccccccccccccccccccccc$$

*b.* Give an example of a single nonnegative function f(n) such that for all functions gᵢ(n) in part (a), f(n) is neither O(gᵢ(n)) nor Ω(gᵢ(n)).

## *3-4 Asymptotic notation properties*

Let f(n) and g(n) be asymptotically positive functions. Prove or disprove each of the following conjectures.

a. 
$$f(n) = O(g(n))$$
 implies  $g(n) = O(f(n))$ .

**b.** 
$$f(n) + g(n) = \Theta(\min\{f(n), g(n)\}).$$

c. 
$$f(n) = O(g(n))$$
 implies  $\lg f(n) = O(\lg g(n))$ , where  $\lg g(n) \ge 1$  and  $f(n) \ge 1$  for all sufficiently large  $n$ .

**d.** 
$$f(n) = O(g(n))$$
 implies  $2^{f(n)} = O(2^{g(n)})$ .

**e.** 
$$f(n) = O((f(n))^2).$$

$$f.$$
  $f(n) = O(g(n))$  implies  $g(n) = \Omega(f(n))$ .

**g.** 
$$f(n) = \Theta(f(n/2)).$$

$$h. f(n) + o(f(n)) = \Theta(f(n)).$$

## *3-5 Manipulating asymptotic notation*

Let f(n) and g(n) be asymptotically positive functions. Prove the following identities:

$$a. \ \Theta(\Theta(f(n))) = \Theta(f(n)).$$

**b.** 
$$\Theta(f(n)) + O(f(n)) = \Theta(f(n)).$$

c. 
$$\Theta(f(n)) + \Theta(g(n)) = \Theta(f(n) + g(n)).$$

**d.** 
$$\Theta(f(n)) \cdot \Theta(g(n)) = \Theta(f(n) \cdot g(n)).$$

*e.* Argue that for any real constants a₁, b₁ > 0 and integer constants k₁, k₂, the following asymptotic bound holds:

$$(a_1 n)^{k_1} \lg^{k_2}(a_2 n) = \Theta(n^{k_1} \lg^{k_2} n).$$

★ *f.* Prove that for S ⊆ ℤ, we have

$$\sum_{k \in S} \Theta(f(k)) = \Theta\left(\sum_{k \in S} f(k)\right) ,$$

assuming that both sums converge.

★ *g.* Show that for S ⊆ ℤ, the following asymptotic bound does not necessarily hold, even assuming that both products converge, by giving a counterexample:

$$\prod_{k \in S} \Theta(f(k)) = \Theta\left(\prod_{k \in S} f(k)\right).$$

# *3-6 Variations on* O *and* Ω

Some authors define Ω-notation in a slightly different way than this textbook does. We'll use the nomenclature ∞Ω (read "omega infinity") for this alternative definition. We say that f(n) = ∞Ω(g(n)) if there exists a positive constant c such that f(n) ≥ cg(n) ≥ 0 for infinitely many integers n.

- *a.* Show that for any two asymptotically nonnegative functions f(n) and g(n), we have f(n) = O(g(n)) or f(n) = ∞Ω(g(n)) (or both).
- *b.* Show that there exist two asymptotically nonnegative functions f(n) and g(n) for which neither f(n) = O(g(n)) nor f(n) = Ω(g(n)) holds.
- *c.* Describe the potential advantages and disadvantages of using ∞Ω-notation instead of Ω-notation to characterize the running times of programs.

Some authors also define O in a slightly different manner. We'll use O' for the alternative definition: f(n) = O'(g(n)) if and only if |f(n)| = O(g(n)).

*d.* What happens to each direction of the "if and only if" in Theorem 3.1 on page 56 if we substitute O' for O but still use Ω?

Some authors define Õ (read "soft-oh") to mean O with logarithmic factors ignored:

$$\widetilde{O}(g(n)) = \{f(n) : \text{ there exist positive constants } c, k, \text{ and } n_0 \text{ such that } 0 \le f(n) \le cg(n) \lg^k(n) \text{ for all } n \ge n_0 \}$$
.

*e.* Define Õ(Ω) and Õ(Θ) in a similar manner. Prove the corresponding analog to Theorem 3.1.

# *3-7 Iterated functions*

We can apply the iteration operator used in the lg function to any monotonically increasing function f(n) over the reals. For a given constant c ∈ ℝ, we define the iterated function f*_c by

$$f_c^*(n) = \min \{ i \ge 0 : f^{(i)}(n) \le c \}$$
,

which need not be well defined in all cases. In other words, the quantity f*_c(n) is the minimum number of iterated applications of the function f required to reduce its argument down to c or less.

For each of the functions f(n) and constants c in the table below, give as tight a bound as possible on f*_c(n). If there is no i such that f^(i)(n) ≤ c, write <undefined> as your answer.

|    | f(n)    | c | f*_c(n) |
|----|---------|---|---------|
| a. | n - 1   | 0 |                    |
| b. | lg n    | 1 |                    |
| c. | n/2     | 1 |                    |
| d. | n/2     | 2 |                    |
| e. | √n      | 2 |                    |
| f. | √n      | 1 |                    |
| g. | n^(1/3) | 2 |                    |

# **Chapter notes**

Knuth [259] traces the origin of the O-notation to a number-theory text by P. Bachmann in 1892. The o-notation was invented by E. Landau in 1909 for his discussion of the distribution of prime numbers. The Ω and Θ notations were advocated by Knuth [265] to correct the popular, but technically sloppy, practice in the literature of using O-notation for both upper and lower bounds. As noted earlier in this chapter, many people continue to use the O-notation where the Θ-notation is more technically precise. The soft-oh notation Õ in Problem 3-6 was introduced by Babai, Luks, and Seress [31], although it was originally written as Õ. Some authors now define Õ(g(n)) as ignoring factors that are logarithmic in g(n), rather than in n. With this definition, we can say that n·2ⁿ = Õ(2ⁿ), but with the definition in Problem 3-6, this statement is not true. Further discussion of the history and development of asymptotic notations appears in works by Knuth [259, 265] and Brassard and Bratley [70].

Not all authors define the asymptotic notations in the same way, although the various definitions agree in most common situations. Some of the alternative definitions encompass functions that are not asymptotically nonnegative, as long as their absolute values are appropriately bounded.

Equation (3.29) is due to Robbins [381]. Other properties of elementary mathematical functions can be found in any good mathematical reference, such as Abramowitz and Stegun [1] or Zwillinger [468], or in a calculus book, such as Apostol [19] or Thomas et al. [433]. Knuth [259] and Graham, Knuth, and Patashnik [199] contain a wealth of material on discrete mathematics as used in computer science.

# **4 Divide-and-Conquer**

The divide-and-conquer method is a powerful strategy for designing asymptotically efficient algorithms. We saw an example of divide-and-conquer in Section 2.3.1 when learning about merge sort. In this chapter, we'll explore applications of the divide-and-conquer method and acquire valuable mathematical tools that you can use to solve the recurrences that arise when analyzing divide-and-conquer algorithms.

Recall that for divide-and-conquer, you solve a given problem (instance) recursively. If the problem is small enough—the *base case*—you just solve it directly without recursing. Otherwise—the *recursive case*—you perform three characteristic steps:

**Divide** the problem into one or more subproblems that are smaller instances of the same problem.

**Conquer** the subproblems by solving them recursively.

**Combine** the subproblem solutions to form a solution to the original problem.

A divide-and-conquer algorithm breaks down a large problem into smaller subproblems, which themselves may be broken down into even smaller subproblems, and so forth. The recursion *bottoms out* when it reaches a base case and the subproblem is small enough to solve directly without further recursing.

#### **Recurrences**

To analyze recursive divide-and-conquer algorithms, we'll need some mathematical tools. A *recurrence* is an equation that describes a function in terms of its value on other, typically smaller, arguments. Recurrences go hand in hand with the divide-and-conquer method because they give us a natural way to characterize the running times of recursive algorithms mathematically. You saw an example of a recurrence in Section 2.3.2 when we analyzed the worst-case running time of merge sort.