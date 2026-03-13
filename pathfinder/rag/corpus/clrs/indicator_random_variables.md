---
topic: indicator_random_variables
pages: 162-178
---

$$= \sum_{r=1}^{n} \frac{1}{n^2}$$

$$= \frac{1}{n}.$$
(5.7)

More intuitively, once bᵢ is chosen, the probability that bⱼ is chosen to be the same day is 1/n. As long as the birthdays are independent, the probability that i and j have the same birthday is the same as the probability that the birthday of one of them falls on a given day.

We can analyze the probability of at least 2 out of k people having matching birthdays by looking at the complementary event. The probability that at least two of the birthdays match is 1 minus the probability that all the birthdays are different. The event Bₖ that k people have distinct birthdays is

$$B_k = \bigcap_{i=1}^k A_i ,$$

where Aᵢ is the event that person i's birthday is different from person j's for all j < i. Since we can write Bₖ = Aₖ ∩ Bₖ₋₁, we obtain from equation (C.18) on page 1189 the recurrence

$$\Pr\{B_k\} = \Pr\{B_{k-1}\} \Pr\{A_k \mid B_{k-1}\}, \qquad (5.8)$$

where we take Pr{B₁} = Pr{A₁} = 1 as an initial condition. In other words, the probability that b₁, b₂, ..., bₖ are distinct birthdays equals the probability that b₁, b₂, ..., bₖ₋₁ are distinct birthdays multiplied by the probability that bₖ ≠ bᵢ for i = 1, 2, ..., k−1, given that b₁, b₂, ..., bₖ₋₁ are distinct.

If b₁, b₂, ..., bₖ₋₁ are distinct, the conditional probability that bₖ ≠ bᵢ for i = 1, 2, ..., k−1 is Pr{Aₖ | Bₖ₋₁} = (n−k+1)/n, since out of the n days, n−(k−1) days are not taken. We iteratively apply the recurrence (5.8) to obtain

$$\Pr\{B_{k}\} = \Pr\{B_{k-1}\} \Pr\{A_{k} \mid B_{k-1}\}$$

$$= \Pr\{B_{k-2}\} \Pr\{A_{k-1} \mid B_{k-2}\} \Pr\{A_{k} \mid B_{k-1}\}$$

$$\vdots$$

$$= \Pr\{B_{1}\} \Pr\{A_{2} \mid B_{1}\} \Pr\{A_{3} \mid B_{2}\} \cdots \Pr\{A_{k} \mid B_{k-1}\}$$

$$= 1 \cdot \left(\frac{n-1}{n}\right) \left(\frac{n-2}{n}\right) \cdots \left(\frac{n-k+1}{n}\right)$$

$$= 1 \cdot \left(1 - \frac{1}{n}\right) \left(1 - \frac{2}{n}\right) \cdots \left(1 - \frac{k-1}{n}\right).$$

Inequality (3.14) on page 66, 1 + x ≤ e^x, gives us

$$\Pr\{B_k\} \le e^{-1/n} e^{-2/n} \cdots e^{-(k-1)/n}$$

$$= e^{-\sum_{i=1}^{k-1} i/n}$$

$$= e^{-k(k-1)/2n}$$

$$\le \frac{1}{2}$$

when k(k−1)/2n ≥ ln(1/2). The probability that all k birthdays are distinct is at most 1/2 when k(k−1) ≥ 2n ln 2 or, solving the quadratic equation, when k ≥ (1 + √(1 + (8 ln 2)n))/2. For n = 365, we must have k ≥ 23. Thus, if at least 23 people are in a room, the probability is at least 1/2 that at least two people have the same birthday. Since a year on Mars is 669 Martian days long, it takes 31 Martians to get the same effect.

### **An analysis using indicator random variables**

Indicator random variables afford a simpler but approximate analysis of the birthday paradox. For each pair (i, j) of the k people in the room, define the indicator random variable X_{ij}, for 1 ≤ i < j ≤ k, by

$$X_{ij} = I \{ \text{person } i \text{ and person } j \text{ have the same birthday} \}$$

$$= \begin{cases} 1 & \text{if person } i \text{ and person } j \text{ have the same birthday}, \\ 0 & \text{otherwise}. \end{cases}$$

By equation (5.7), the probability that two people have matching birthdays is 1/n, and thus by Lemma 5.1 on page 130, we have

$$E[X_{ij}] = \Pr\{\text{person } i \text{ and person } j \text{ have the same birthday}\}$$
  
= 1/n.

Letting X be the random variable that counts the number of pairs of individuals having the same birthday, we have

$$X = \sum_{i=1}^{k-1} \sum_{j=i+1}^{k} X_{ij} .$$

Taking expectations of both sides and applying linearity of expectation, we obtain

$$E[X] = E\left[\sum_{i=1}^{k-1} \sum_{j=i+1}^{k} X_{ij}\right]$$
$$= \sum_{i=1}^{k-1} \sum_{j=i+1}^{k} E[X_{ij}]$$

$$= \binom{k}{2} \frac{1}{n}$$
$$= \frac{k(k-1)}{2n}.$$

When k(k−1) ≥ 2n, therefore, the expected number of pairs of people with the same birthday is at least 1. Thus, if we have at least √(2n)+1 individuals in a room, we can expect at least two to have the same birthday. For n = 365, if k = 28, the expected number of pairs with the same birthday is (28·27)/(2·365) ≈ 1.0356. Thus, with at least 28 people, we expect to find at least one matching pair of birthdays. On Mars, with 669 days per year, we need at least 38 Martians.

The first analysis, which used only probabilities, determined the number of people required for the probability to exceed 1/2 that a matching pair of birthdays exists, and the second analysis, which used indicator random variables, determined the number such that the expected number of matching birthdays is 1. Although the exact numbers of people differ for the two situations, they are the same asymptotically: Θ(√n).

## **5.4.2 Balls and bins**

Consider a process in which you randomly toss identical balls into b bins, numbered 1, 2, ..., b. The tosses are independent, and on each toss the ball is equally likely to end up in any bin. The probability that a tossed ball lands in any given bin is 1/b. If we view the ball-tossing process as a sequence of Bernoulli trials (see Appendix C.4), where success means that the ball falls in the given bin, then each trial has a probability 1/b of success. This model is particularly useful for analyzing hashing (see Chapter 11), and we can answer a variety of interesting questions about the ball-tossing process. (Problem C-2 asks additional questions about balls and bins.)

- *How many balls fall in a given bin?* The number of balls that fall in a given bin follows the binomial distribution b(k; n, 1/b). If you toss n balls, equation (C.41) on page 1199 tells us that the expected number of balls that fall in the given bin is n/b.
- *How many balls must you toss, on the average, until a given bin contains a ball?* The number of tosses until the given bin receives a ball follows the geometric distribution with probability 1/b and, by equation (C.36) on page 1197, the expected number of tosses until success is 1/(1/b) = b.
- *How many balls must you toss until every bin contains at least one ball?* Let us call a toss in which a ball falls into an empty bin a "hit." We want to know the expected number n of tosses required to get b hits.

Using the hits, we can partition the n tosses into stages. The ith stage consists of the tosses after the (i−1)st hit up to and including the ith hit. The first stage consists of the first toss, since you are guaranteed to have a hit when all bins are empty. For each toss during the ith stage, i−1 bins contain balls and b−i+1 bins are empty. Thus, for each toss in the ith stage, the probability of obtaining a hit is (b−i+1)/b.

Let nᵢ denote the number of tosses in the ith stage. The number of tosses required to get b hits is n = ∑ᵢ₌₁ᵇ nᵢ. Each random variable nᵢ has a geometric distribution with probability of success (b−i+1)/b and thus, by equation (C.36), we have

$$\mathrm{E}\left[n_i\right] = \frac{b}{b-i+1} \; .$$

By linearity of expectation, we have

$$E[n] = E\left[\sum_{i=1}^{b} n_i\right]$$

$$= \sum_{i=1}^{b} E[n_i]$$

$$= \sum_{i=1}^{b} \frac{b}{b-i+1}$$

$$= b\sum_{i=1}^{b} \frac{1}{i} \qquad \text{(by equation (A.14) on page 1144)}$$

$$= b(\ln b + O(1)) \quad \text{(by equation (A.9) on page 1142)}.$$

It therefore takes approximately b ln b tosses before we can expect that every bin has a ball. This problem is also known as the *coupon collector's problem*, which says that if you are trying to collect each of b different coupons, then you should expect to acquire approximately b ln b randomly obtained coupons in order to succeed.

### **5.4.3 Streaks**

Suppose that you flip a fair coin n times. What is the longest streak of consecutive heads that you expect to see? We'll prove upper and lower bounds separately to show that the answer is Θ(lg n).

We first prove that the expected length of the longest streak of heads is O(lg n). The probability that each coin flip is a head is 1/2. Let Aᵢₖ be the event that a streak of heads of length at least k begins with the ith coin flip or, more precisely, the event that the k consecutive coin flips i, i+1, ..., i+k−1 yield only heads, where 1 ≤ k ≤ n and 1 ≤ i ≤ n−k+1. Since coin flips are mutually independent, for any given event Aᵢₖ, the probability that all k flips are heads is

$$\Pr\{A_{ik}\} = \frac{1}{2^k}.$$

$$\operatorname{For} k = 2 \lceil \lg n \rceil,$$

$$\operatorname{Pr}\{A_{i,2\lceil \lg n \rceil}\} = \frac{1}{2^{2\lceil \lg n \rceil}}$$

$$\leq \frac{1}{2^{2 \lg n}}$$

$$= \frac{1}{n^2},$$
(5.9)

and thus the probability that a streak of heads of length at least 2 ceil(lg n) begins in position i is quite small. There are at most n 2 ceil(lg n) C 1 positions where such a streak can begin. The probability that a streak of heads of length at least 2 ceil(lg n) begins anywhere is therefore

$$\Pr\left\{ \bigcup_{i=1}^{n-2\lceil \lg n\rceil+1} A_{i,2\lceil \lg n\rceil} \right\}$$

$$\leq \sum_{i=1}^{n-2\lceil \lg n\rceil+1} \Pr\left\{ A_{i,2\lceil \lg n\rceil} \right\} \quad \text{(by Boole's inequality (C.21) on page 1190)}$$

$$\leq \sum_{i=1}^{n-2\lceil \lg n\rceil+1} \frac{1}{n^2}$$

$$< \sum_{i=1}^{n} \frac{1}{n^2}$$

$$= \frac{1}{n}. \quad (5.10)$$

We can use inequality (5.10) to bound the length of the longest streak. For j = 0, 1, 2, ..., n, let L_j be the event that the longest streak of heads has length exactly j, and let L be the length of the longest streak. By the definition of expected value, we have

$$E[L] = \sum_{j=0}^{n} j \Pr\{L_j\}.$$
 (5.11)

We could try to evaluate this sum using upper bounds on each Pr{L_j} similar to those computed in inequality (5.10). Unfortunately, this method yields weak bounds. We can use some intuition gained by the above analysis to obtain a good bound, however. For no individual term in the summation in equation (5.11) are both the factors j and Pr{L_j} large. Why? When j ≥ 2⌈lg n⌉, then Pr{L_j} is very small, and when j < 2⌈lg n⌉, then j is fairly small. More precisely, since the events L_j for j = 0, 1, ..., n are disjoint, the probability that a streak of heads of length at least 2⌈lg n⌉ begins anywhere is ∑ⁿ_{j=2⌈lg n⌉} Pr{L_j}. Inequality (5.10) tells us that the probability that a streak of heads of length at least 2⌈lg n⌉ begins anywhere is less than 1/n, which means that ∑ⁿ_{j=2⌈lg n⌉} Pr{L_j} < 1/n. Also, noting that ∑ⁿ_{j=0} Pr{L_j} = 1, we have that ∑^{2⌈lg n⌉-1}_{j=0} Pr{L_j} ≤ 1. Thus, we obtain

$$\begin{split} \mathbf{E}\left[L\right] &= \sum_{j=0}^{n} j \, \Pr\{L_{j}\} \\ &= \sum_{j=0}^{2\lceil \lg n \rceil - 1} j \, \Pr\{L_{j}\} + \sum_{j=2\lceil \lg n \rceil}^{n} j \, \Pr\{L_{j}\} \\ &< \sum_{j=0}^{2\lceil \lg n \rceil - 1} (2\lceil \lg n \rceil) \Pr\{L_{j}\} + \sum_{j=2\lceil \lg n \rceil}^{n} n \, \Pr\{L_{j}\} \\ &= 2\lceil \lg n \rceil \sum_{j=0}^{2\lceil \lg n \rceil - 1} \Pr\{L_{j}\} + n \sum_{j=2\lceil \lg n \rceil}^{n} \Pr\{L_{j}\} \\ &< 2\lceil \lg n \rceil \cdot 1 + n \cdot \frac{1}{n} \\ &= O(\lg n) \; . \end{split}$$

The probability that a streak of heads exceeds r⌈lg n⌉ flips diminishes quickly with r. Let's get a rough bound on the probability that a streak of at least r⌈lg n⌉ heads occurs, for r ≥ 1. The probability that a streak of at least r⌈lg n⌉ heads starts in position i is

$$\Pr\{A_{i,r\lceil \lg n \rceil}\} = \frac{1}{2^{r\lceil \lg n \rceil}} \\ \leq \frac{1}{n^r}.$$

A streak of at least r⌈lg n⌉ heads cannot start in the last n − r⌈lg n⌉ + 1 flips, but let's overestimate the probability of such a streak by allowing it to start anywhere within the n coin flips. Then the probability that a streak of at least r⌈lg n⌉ heads 

occurs is at most

$$\Pr\left\{\bigcup_{i=1}^{n} A_{i,r\lceil \lg n \rceil}\right\} \leq \sum_{i=1}^{n} \Pr\left\{A_{i,r\lceil \lg n \rceil}\right\}$$
 (by Boole's inequality (C.21))
$$\leq \sum_{i=1}^{n} \frac{1}{n^{r}}$$

$$= \frac{1}{n^{r-1}}.$$

Equivalently, the probability is at least 1−1/n^{r−1} that the longest streak has length less than r⌈lg n⌉.

As an example, during n = 1000 coin flips, the probability of encountering a streak of at least 2⌈lg n⌉ = 20 heads is at most 1/n = 1/1000. The chance of a streak of at least 3⌈lg n⌉ = 30 heads is at most 1/n² = 1/1,000,000.

Let's now prove a complementary lower bound: the expected length of the longest streak of heads in n coin flips is Ω(lg n). To prove this bound, we look for streaks of length s by partitioning the n flips into approximately n/s groups of s flips each. If we choose s = ⌊(lg n)/2⌋, we'll see that it is likely that at least one of these groups comes up all heads, which means that it's likely that the longest streak has length at least s = Ω(lg n). We'll then show that the longest streak has expected length Ω(lg n).

Let's partition the n coin flips into at least ⌊n/⌊(lg n)/2⌋⌋ groups of ⌊(lg n)/2⌋ consecutive flips and bound the probability that no group comes up all heads. By equation (5.9), the probability that the group starting in position i comes up all heads is

$$\Pr\{A_{i,\lfloor(\lg n)/2\rfloor}\} = \frac{1}{2^{\lfloor(\lg n)/2\rfloor}}$$

$$\geq \frac{1}{\sqrt{n}}.$$

The probability that a streak of heads of length at least ⌊(lg n)/2⌋ does not begin in position i is therefore at most 1 − 1/√n. Since the ⌊n/⌊(lg n)/2⌋⌋ groups are formed from mutually exclusive, independent coin flips, the probability that every one of these groups *fails* to be a streak of length ⌊(lg n)/2⌋ is at most

$$(1 - 1/\sqrt{n})^{\lfloor n/\lfloor (\lg n)/2 \rfloor \rfloor} \leq (1 - 1/\sqrt{n})^{n/\lfloor (\lg n)/2 \rfloor - 1}$$

$$\leq (1 - 1/\sqrt{n})^{2n/\lg n - 1}$$

$$\leq e^{-(2n/\lg n - 1)/\sqrt{n}}$$

$$= O(e^{-\ln n})$$

$$= O(1/n). \tag{5.12}$$

For this argument, we used inequality (3.14), 1 + x ≤ e^x, on page 66 and the fact, which you may verify, that (2n/lg n − 1)/√n ≥ ln n for sufficiently large n.

We want to bound the probability that the longest streak equals or exceeds ⌊(lg n)/2⌋. To do so, let L be the event that the longest streak of heads equals or exceeds s = ⌊(lg n)/2⌋. Let L̄ be the complementary event, that the longest streak of heads is strictly less than s, so that Pr{L} + Pr{L̄} = 1. Let F be the event that every group of s flips fails to be a streak of s heads. By inequality (5.12), we have Pr{F} = O(1/n). If the longest streak of heads is less than s, then certainly every group of s flips fails to be a streak of s heads, which means that event L̄ implies event F. Of course, event F could occur even if event L̄ does not (for example, if a streak of s or more heads crosses over the boundary between two groups), and so we have Pr{L̄} ≤ Pr{F} = O(1/n). Since Pr{L} + Pr{L̄} = 1, we have that

$$Pr \{L\} = 1 - Pr \{\overline{L}\}$$

$$\geq 1 - Pr \{F\}$$

$$= 1 - O(1/n).$$

That is, the probability that the longest streak equals or exceeds ⌊(lg n)/2⌋ is

$$\sum_{j=\lfloor (\lg n)/2 \rfloor}^{n} \Pr\{L_{j}\} \ge 1 - O(1/n) . \tag{5.13}$$

We can now calculate a lower bound on the expected length of the longest streak, beginning with equation (5.11) and proceeding in a manner similar to our analysis of the upper bound:

$$E[L] = \sum_{j=0}^{n} j \Pr\{L_{j}\}\$$

$$= \sum_{j=0}^{\lfloor (\lg n)/2 \rfloor - 1} j \Pr\{L_{j}\} + \sum_{j=\lfloor (\lg n)/2 \rfloor}^{n} j \Pr\{L_{j}\}\$$

$$\geq \sum_{j=0}^{\lfloor (\lg n)/2 \rfloor - 1} 0 \cdot \Pr\{L_{j}\} + \sum_{j=\lfloor (\lg n)/2 \rfloor}^{n} \lfloor (\lg n)/2 \rfloor \Pr\{L_{j}\}\$$

$$= 0 \cdot \sum_{j=0}^{\lfloor (\lg n)/2 \rfloor - 1} \Pr\{L_{j}\} + \lfloor (\lg n)/2 \rfloor \sum_{j=\lfloor (\lg n)/2 \rfloor}^{n} \Pr\{L_{j}\}\$$

$$\geq 0 + \lfloor (\lg n)/2 \rfloor (1 - O(1/n)) \qquad \text{(by inequality (5.13))}\$$

$$= \Omega(\lg n) .$$

As with the birthday paradox, we can obtain a simpler, but approximate, analysis using indicator random variables. Instead of determining the expected length of the longest streak, we'll find the expected number of streaks with at least a given length. Let X_{ik} = I{A_{ik}} be the indicator random variable associated with a streak of heads of length at least k beginning with the ith coin flip. To count the total number of such streaks, define

$$X_k = \sum_{i=1}^{n-k+1} X_{ik} \ .$$

Taking expectations and using linearity of expectation, we have

$$E[X_k] = E\left[\sum_{i=1}^{n-k+1} X_{ik}\right]$$

$$= \sum_{i=1}^{n-k+1} E[X_{ik}]$$

$$= \sum_{i=1}^{n-k+1} \Pr\{A_{ik}\}$$

$$= \sum_{i=1}^{n-k+1} \frac{1}{2^k}$$

$$= \frac{n-k+1}{2^k}.$$

By plugging in various values for k, we can calculate the expected number of streaks of length at least k. If this expected number is large (much greater than 1), then we expect many streaks of length k to occur, and the probability that one occurs is high. If this expected number is small (much less than 1), then we expect to see few streaks of length k, and the probability that one occurs is low. If k = c lg n, for some positive constant c, we obtain

$$E[X_{c \lg n}] = \frac{n - c \lg n + 1}{2^{c \lg n}}$$

$$= \frac{n - c \lg n + 1}{n^c}$$

$$= \frac{1}{n^{c-1}} - \frac{(c \lg n - 1)/n}{n^{c-1}}$$

$$= \Theta(1/n^{c-1}).$$

If c is large, the expected number of streaks of length c lg n is small, and we conclude that they are unlikely to occur. On the other hand, if c = 1/2, then we 

obtain E[X_{(1/2)lg n}] = Θ(1/n^{1/2−1}) = Θ(n^{1/2}), and we expect there to be numerous streaks of length (1/2)lg n. Therefore, one streak of such a length is likely to occur. We can conclude that the expected length of the longest streak is Θ(lg n).

### **5.4.4 The online hiring problem**

As a final example, let's consider a variant of the hiring problem. Suppose now that you do not wish to interview all the candidates in order to find the best one. You also want to avoid hiring and firing as you find better and better applicants. Instead, you are willing to settle for a candidate who is close to the best, in exchange for hiring exactly once. You must obey one company requirement: after each interview you must either immediately offer the position to the applicant or immediately reject the applicant. What is the trade-off between minimizing the amount of interviewing and maximizing the quality of the candidate hired?

We can model this problem in the following way. After meeting an applicant, you are able to give each one a score. Let *score*(i) denote the score you give to the ith applicant, and assume that no two applicants receive the same score. After you have seen j applicants, you know which of the j has the highest score, but you do not know whether any of the remaining n − j applicants will receive a higher score. You decide to adopt the strategy of selecting a positive integer k < n, interviewing and then rejecting the first k applicants, and hiring the first applicant thereafter who has a higher score than all preceding applicants. If it turns out that the best-qualified applicant was among the first k interviewed, then you hire the nth applicant—the last one interviewed. We formalize this strategy in the procedure ONLINE-MAXIMUM(k, n), which returns the index of the candidate you wish to hire.

```
ONLINE-MAXIMUM(k, n)
1 best-score = −∞
2for i = 1 to k
3 if score(i) > best-score
4 best-score = score(i)
5 for i = k + 1 to n
6 if score(i) > best-score
7 return i
8 return n
```

If we determine, for each possible value of k, the probability that you hire the most qualified applicant, then you can choose the best possible k and implement the strategy with that value. For the moment, assume that k is fixed. Let

M(j) = max{*score*(i): 1 ≤ i ≤ j} denote the maximum score among applicants 1 through j. Let S be the event that you succeed in choosing the best-qualified applicant, and let S_i be the event that you succeed when the best-qualified applicant is the ith one interviewed. Since the various S_i are disjoint, we have that Pr{S} = ∑ⁿ_{i=1} Pr{S_i}. Noting that you never succeed when the best-qualified applicant is one of the first k, we have that Pr{S_i} = 0 for i = 1, 2, ..., k. Thus, we obtain

$$\Pr\{S\} = \sum_{i=k+1}^{n} \Pr\{S_i\} . \tag{5.14}$$

We now compute Pr{S_i}. In order to succeed when the best-qualified applicant is the ith one, two things must happen. First, the best-qualified applicant must be in position i, an event which we denote by B_i. Second, the algorithm must not select any of the applicants in positions k + 1 through i − 1, which happens only if, for each j such that k + 1 ≤ j ≤ i − 1, line 6 finds that *score*(j) < *best-score*. (Because scores are unique, we can ignore the possibility of *score*(j) = *best-score*.) In other words, all of the values *score*(k + 1) through *score*(i − 1) must be less than M(k). If any are greater than M(k), the algorithm instead returns the index of the first one that is greater. We use O_i to denote the event that none of the applicants in position k + 1 through i − 1 are chosen. Fortunately, the two events B_i and O_i are independent. The event O_i depends only on the relative ordering of the values in positions 1 through i − 1, whereas B_i depends only on whether the value in position i is greater than the values in all other positions. The ordering of the values in positions 1 through i − 1 does not affect whether the value in position i is greater than all of them, and the value in position i does not affect the ordering of the values in positions 1 through i − 1. Thus, we can apply equation (C.17) on page 1188 to obtain

$$\Pr\{S_i\} = \Pr\{B_i \cap O_i\} = \Pr\{B_i\} \Pr\{O_i\}.$$

We have Pr{B_i} = 1/n since the maximum is equally likely to be in any one of the n positions. For event O_i to occur, the maximum value in positions 1 through i − 1, which is equally likely to be in any of these i − 1 positions, must be in one of the first k positions. Consequently, Pr{O_i} = k/(i − 1) and Pr{S_i} = k/(n(i − 1)). Using equation (5.14), we have

$$\Pr\{S\} = \sum_{i=k+1}^{n} \Pr\{S_i\}$$
$$= \sum_{i=k+1}^{n} \frac{k}{n(i-1)}$$

$$= \frac{k}{n} \sum_{i=k+1}^{n} \frac{1}{i-1}$$
$$= \frac{k}{n} \sum_{i=k}^{n-1} \frac{1}{i}.$$

We approximate by integrals to bound this summation from above and below. By the inequalities (A.19) on page 1150, we have

$$\int_{k}^{n} \frac{1}{x} dx \le \sum_{i=k}^{n-1} \frac{1}{i} \le \int_{k-1}^{n-1} \frac{1}{x} dx.$$

Evaluating these definite integrals gives us the bounds

$$\frac{k}{n}(\ln n - \ln k) \le \Pr\{S\} \le \frac{k}{n}(\ln(n-1) - \ln(k-1)),$$

which provide a rather tight bound for Pr{S}. Because you wish to maximize your probability of success, let us focus on choosing the value of k that maximizes the lower bound on Pr{S}. (Besides, the lower-bound expression is easier to maximize than the upper-bound expression.) Differentiating the expression (k/n)(ln n − ln k) with respect to k, we obtain

$$\frac{1}{n}(\ln n - \ln k - 1) \ .$$

Setting this derivative equal to 0, we see that you maximize the lower bound on the probability when ln k = ln n − 1 = ln(n/e) or, equivalently, when k = n/e. Thus, if you implement our strategy with k = n/e, you succeed in hiring the best-qualified applicant with probability at least 1/e.

### **Exercises**

### *5.4-1*

How many people must there be in a room before the probability that someone has the same birthday as you do is at least 1/2? How many people must there be before the probability that at least two people have a birthday on July 4 is greater than 1/2?

### *5.4-2*

How many people must there be in a room before the probability that two people have the same birthday is at least 0.99? For that many people, what is the expected number of pairs of people who have the same birthday?

## *5.4-3*

You toss balls into b bins until some bin contains two balls. Each toss is independent, and each ball is equally likely to end up in any bin. What is the expected number of ball tosses?

# ⋆ *5.4-4*

For the analysis of the birthday paradox, is it important that the birthdays be mutually independent, or is pairwise independence sufficient? Justify your answer.

# ⋆ *5.4-5*

How many people should be invited to a party in order to make it likely that there are *three* people with the same birthday?

# ⋆ *5.4-6*

What is the probability that a k-string (defined on page 1179) over a set of size n forms a k-permutation? How does this question relate to the birthday paradox?

# ⋆ *5.4-7*

You toss n balls into n bins, where each toss is independent and the ball is equally likely to end up in any bin. What is the expected number of empty bins? What is the expected number of bins with exactly one ball?

# ⋆ *5.4-8*

Sharpen the lower bound on streak length by showing that in n flips of a fair coin, the probability is at least 1 − 1/n that a streak of length lg n − 2 lg lg n consecutive heads occurs.

## **Problems**

### *5-1 Probabilistic counting*

With a b-bit counter, we can ordinarily only count up to 2^b − 1. With R. Morris's *probabilistic counting*, we can count up to a much larger value at the expense of some loss of precision.

We let a counter value of i represent a count of n_i for i = 0, 1, ..., 2^b − 1, where the n_i form an increasing sequence of nonnegative values. We assume that the initial value of the counter is 0, representing a count of n₀ = 0. The INCREMENT operation works on a counter containing the value i in a probabilistic manner. If i = 2^b − 1, then the operation reports an overflow error. Otherwise, the INCREMENT operation increases the counter by 1 with probability 1/(n_{i+1} − n_i), and it leaves the counter unchanged with probability 1 − 1/(n_{i+1} − n_i).

If we select n_i = i for all i ≥ 0, then the counter is an ordinary one. More interesting situations arise if we select, say, n_i = 2^{i−1} for i > 0 or n_i = F_i (the ith Fibonacci number—see equation (3.31) on page 69).

For this problem, assume that n_{2^b−1} is large enough that the probability of an overflow error is negligible.

- *a.* Show that the expected value represented by the counter after n INCREMENT operations have been performed is exactly n.
- *b.* The analysis of the variance of the count represented by the counter depends on the sequence of the n_i. Let us consider a simple case: n_i = 100i for all i ≥ 0. Estimate the variance in the value represented by the register after n INCREMENT operations have been performed.

## *5-2 Searching an unsorted array*

This problem examines three algorithms for searching for a value x in an unsorted array A consisting of n elements.

Consider the following randomized strategy: pick a random index i into A. If A[i] = x, then terminate; otherwise, continue the search by picking a new random index into A. Continue picking random indices into A until you find an index j such that A[j] = x or until every element of A has been checked. This strategy may examine a given element more than once, because it picks from the whole set of indices each time.

- *a.* Write pseudocode for a procedure RANDOM-SEARCH to implement the strategy above. Be sure that your algorithm terminates when all indices into A have been picked.
- *b.* Suppose that there is exactly one index i such that A[i] = x. What is the expected number of indices into A that must be picked before x is found and RANDOM-SEARCH terminates?
- *c.* Generalizing your solution to part (b), suppose that there are k ≥ 1 indices i such that A[i] = x. What is the expected number of indices into A that must be picked before x is found and RANDOM-SEARCH terminates? Your answer should be a function of n and k.
- *d.* Suppose that there are no indices i such that A[i] = x. What is the expected number of indices into A that must be picked before all elements of A have been checked and RANDOM-SEARCH terminates?

Now consider a deterministic linear search algorithm. The algorithm, which we call DETERMINISTIC-SEARCH, searches A for x in order, considering A[1], A[2],

A[3], ..., A[n] until either it finds A[i] = x or it reaches the end of the array. Assume that all possible permutations of the input array are equally likely.

- *e.* Suppose that there is exactly one index i such that A[i] = x. What is the average-case running time of DETERMINISTIC-SEARCH? What is the worstcase running time of DETERMINISTIC-SEARCH?
- *f.* Generalizing your solution to part (e), suppose that there are k ≥ 1 indices i such that A[i] = x. What isthe average-case running time of DETERMINISTIC-SEARCH? What is the worst-case running time of DETERMINISTIC-SEARCH? Your answer should be a function of n and k.
- *g.* Suppose that there are no indices i such that A[i] = x. What is the average-case running time of DETERMINISTIC-SEARCH? What is the worst-case running time of DETERMINISTIC-SEARCH?

Finally, consider a randomized algorithm SCRAMBLE-SEARCH that first randomly permutes the input array and then runs the deterministic linear search given above on the resulting permuted array.

- *h.* Letting k be the number of indices i such that A[i] = x, give the worst-case and expected running times of SCRAMBLE-SEARCH for the cases in which k = 0 and k = 1. Generalize your solution to handle the case in which k ≥ 1.
- *i.* Which of the three searching algorithms would you use? Explain your answer.

## **Chapter notes**

Bollobás [65], Hofri [223], and Spencer [420] contain a wealth of advanced probabilistic techniques. The advantages of randomized algorithms are discussed and surveyed by Karp [249] and Rabin [372]. The textbook by Motwani and Raghavan [336] gives an extensive treatment of randomized algorithms.

The RANDOMLY-PERMUTE procedure is by Durstenfeld [128], based on an earlier procedure by Fisher and Yates [143, p. 34].

Several variants of the hiring problem have been widely studied. These problems are more commonly referred to as "secretary problems." Examples of work in this area are the paper by Ajtai, Meggido, and Waarts [11] and another by Kleinberg [258], which ties the secretary problem to online ad auctions.

## **Introduction**

This part presents several algorithms that solve the following *sorting problem*:

**Input:** A sequence of n numbers ⟨a₁, a₂, ..., aₙ⟩.

**Output:** A permutation (reordering) ⟨a'₁, a'₂, ..., a'ₙ⟩ of the input sequence such that a'₁ ≤ a'₂ ≤ ... ≤ a'ₙ.

The input sequence is usually an n-element array, although it may be represented in some other fashion, such as a linked list.

### **The structure of the data**

In practice, the numbers to be sorted are rarely isolated values. Each is usually part of a collection of data called a *record*. Each record contains a *key*, which is the value to be sorted. The remainder of the record consists of *satellite data*, which are usually carried around with the key. In practice, when a sorting algorithm permutes the keys, it must permute the satellite data as well. If each record includes a large amount of satellite data, it often pays to permute an array of pointers to the records rather than the records themselves in order to minimize data movement.

In a sense, it is these implementation details that distinguish an algorithm from a full-blown program. A sorting algorithm describes the *method* to determine the sorted order, regardless of whether what's being sorted are individual numbers or large records containing many bytes of satellite data. Thus, when focusing on the problem of sorting, we typically assume that the input consists only of numbers. Translating an algorithm for sorting numbers into a program for sorting records is conceptually straightforward, although in a given engineering situation other subtleties may make the actual programming task a challenge.