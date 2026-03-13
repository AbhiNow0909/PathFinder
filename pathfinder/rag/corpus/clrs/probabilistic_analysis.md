---
topic: probabilistic_analysis
pages: 148-161
---

```
HIRE-ASSISTANT(n)
1 best = 0 // candidate 0 is a least-qualified dummy candidate
2 for i = 1 to n
3     interview candidate i
4     if candidate i is better than candidate best 
5         best = i
6         hire candidate i
```

may seem very different from analyzing the running time of, say, merge sort. The analytical techniques used, however, are identical whether we are analyzing cost or running time. In either case, we are counting the number of times certain basic operations are executed.

Interviewing has a low cost, say c_i, whereas hiring is expensive, costing c_h. Letting m be the number of people hired, the total cost associated with this algorithm is O(c_i·n + c_h·m). No matter how many people you hire, you always interview n candidates and thus always incur the cost c_i·n associated with interviewing. We therefore concentrate on analyzing c_h·m, the hiring cost. This quantity depends on the order in which you interview candidates.

This scenario serves as a model for a common computational paradigm. Algorithms often need to find the maximum or minimum value in a sequence by examining each element of the sequence and maintaining a current "winner." The hiring problem models how often a procedure updates its notion of which element is currently winning.

### **Worst-case analysis**

In the worst case, you actually hire every candidate that you interview. This situation occurs if the candidates come in strictly increasing order of quality, in which case you hire n times, for a total hiring cost of O(c_h·n).

Of course, the candidates do not always come in increasing order of quality. In fact, you have no idea about the order in which they arrive, nor do you have any control over this order. Therefore, it is natural to ask what we expect to happen in a typical or average case.

#### **Probabilistic analysis**

*Probabilistic analysis* is the use of probability in the analysis of problems. Most commonly, we use probabilistic analysis to analyze the running time of an algorithm. Sometimes we use it to analyze other quantities, such as the hiring cost in 

procedure HIRE-ASSISTANT. In order to perform a probabilistic analysis, we must use knowledge of, or make assumptions about, the distribution of the inputs. Then we analyze our algorithm, computing an average-case running time, where we take the average, or expected value, over the distribution of the possible inputs. When reporting such a running time, we refer to it as the *average-case running time*.

You must be careful in deciding on the distribution of inputs. For some problems, you may reasonably assume something about the set of all possible inputs, and then you can use probabilistic analysis as a technique {or designing an efficient algorithm and as a means {or }aining insight into a problem. For other problems, you cannot characterize a reasonable input distribution, and in these cases you cannot use probabilistic analysis.

For the hiring problem, we can assume that the applicants come in a random order. What does that mean for this problem? We assume that you can compare any two candidates and decide which one is better qualified, which is to say that there is a total order on the candidates. (See Section B.2 for the definition of a total order.) Thus, you can rank each candidate with a unique number from 1 through n, using *rank*(i) to denote the rank of applicant i, and adopt the convention that a higher rank corresponds to a better qualified applicant. The ordered list ⟨*rank*(1), *rank*(2), ..., *rank*(n)⟩ is a permutation of the list ⟨1, 2, ..., n⟩. Saying that the applicants come in a random order is equivalent to saying that this list of ranks is equally likely to be any one of the n! permutations of the numbers 1 through n. Alternatively, we say that the ranks form a *uniform random permutation*, that is, each of the possible n! permutations appears with equal probability.

Section 5.2 contains a probabilistic analysis of the hiring problem.

#### **Randomized algorithms**

In order to use probabilistic analysis, you need to know something about the distribution of the inputs. In many cases, you know little about the input distribution. Even if you do know something about the distribution, you might not be able to model this knowledge computationally. Yet, probability and randomness often serve as tools {or algorithm design and analysis, by making part of the algorithm behave randomly.

In the hiring problem, it may seem as if the candidates are being presented to you in a random order, but you have no way of knowing whether they really are. Thus, in order to develop a randomized algorithm for the hiring problem, you need greater control over the order in which you'll interview the candidates. We will, therefore, change the model slightly. The employment agency sends you a list of the n candidates in advance. On each day, you choose, randomly, which candidate to interview. Although you know nothing about the candidates (besides their names), we have made a significant change. Instead of accepting the order given 

to you by the employment agency and hoping that it's random, you have instead gained control of the process and enforced a random order.

More generally, we call an algorithm *randomized* if its behavior is determined not only by its input but also by values produced by a *random-number generator*. We assume that we have at our disposal a random-number generator RANDOM. A call to RANDOM(a, b) returns an integer between a and b, inclusive, with each such integer being equally likely. For example, RANDOM(0, 1) produces 0 with probability 1/2, and it produces 1 with probability 1/2. A call to RANDOM(3, 7) returns any one of 3, 4, 5, 6, or 7, each with probability 1/5. Each integer returned by RANDOM is independent of the integers returned on previous calls. You may imagine RANDOM as rolling a (b - a + 1)-sided die to obtain its output. (In practice, most programming environments offer a *pseudorandom-number generator*: a deterministic algorithm returning numbers that "look" statistically random.)

When analyzing the running time of a randomized algorithm, we take the expectation of the running time over the distribution of values returned by the random number generator. We distinguish these algorithms from those in which the input is random by referring to the running time of a randomized algorithm as an *expected running time*. In general, we discuss the average-case running time when the probability distribution is over the inputs to the algorithm, and we discuss the expected running time when the algorithm itself makes random choices.

## **Exercises**

## *5.1-1*

Show that the assumption that you are always able to determine which candidate is best, in line 4 of procedure HIRE-ASSISTANT, implies that you know a total order on the ranks of the candidates.

# ⋆ *5.1-2*

Describe an implementation of the procedure RANDOM(a, b) that makes calls only to RANDOM(0, 1). What is the expected running time of your procedure, as a function of a and b?

# ⋆ *5.1-3*

You wish to implement a program that outputs 0 with probability 1/2 and 1 with probability 1/2. At your disposal is a procedure BIASED-RANDOM that outputs either 0 or 1, but it outputs 1 with some probability p and 0 with probability 1 - p, where 0 < p < 1. You do not know what p is. Give an algorithm that uses BIASED-RANDOM as a subroutine, and returns an unbiased answer, returning 0 with probability 1/2 and 1 with probability 1/2. What is the expected running time of your algorithm as a function of p?

==================================================

## **5.2 Indicator random variables**

In order to analyze many algorithms, including the hiring problem, we use indicator random variables. Indicator random variables provide a convenient method for converting between probabilities and expectations. Given a sample space S and an event A, the *indicator random variable* I{A} associated with event A is defined as

$$I\{A\} = \begin{cases} 1 & \text{if } A \text{ occurs }, \\ 0 & \text{if } A \text{ does not occur }. \end{cases}$$
 (5.1)

As a simple example, let us determine the expected number of heads obtained when flipping a fair coin. The sample space for a single coin flip is S = {H, T}, with Pr{H} = Pr{T} = 1/2. We can then define an indicator random variable X_H, associated with the coin coming up heads, which is the event H. This variable counts the number of heads obtained in this flip, and it is 1 if the coin comes up heads and 0 otherwise. We write

$$X_H = I\{H\}$$

$$= \begin{cases} 1 & \text{if } H \text{ occurs }, \\ 0 & \text{if } T \text{ occurs }. \end{cases}$$

The expected number of heads obtained in one flip of the coin is simply the expected value of our indicator variable X_H:

$$E[X_H] = E[I\{H\}]$$
= 1 \cdot Pr\{H\} + 0 \cdot Pr\{T\}
= 1 \cdot (1/2) + 0 \cdot (1/2)
= 1/2.

Thus the expected number of heads obtained by one flip of a fair coin is 1/2. As the following lemma shows, the expected value of an indicator random variable associated with an event A is equal to the probability that A occurs.

### *Lemma 5.1*

Given a sample space S and an event A in the sample space S, let X_A = I{A}. Then E[X_A] = Pr{A}.

*Proof* By the definition of an indicator random variable from equation (5.1) and the definition of expected value, we have

$$E[X_A] = E[I\{A\}]$$

$$= 1 \cdot \Pr\{A\} + 0 \cdot \Pr\{\overline{A}\}$$

$$= \Pr\{A\},$$

where Ā denotes S - A, the complement of A.

Although indicator random variables may seem cumbersome for an application such as counting the expected number of heads on a flip of a single coin, they are useful for analyzing situations that perform repeated random trials. In Appendix C, for example, indicator random variables provide a simple way to determine the expected number of heads in n coin flips. One option is to consider separately the probability of obtaining 0 heads, 1 head, 2 heads, etc. to arrive at the result of equation (C.41) on page 1199. Alternatively, we can employ the simpler method proposed in equation (C.42), which uses indicator random variables implicitly. Making this argument more explicit, let X_i be the indicator random variable associated with the event in which the ith flip comes up heads: X_i = I{the ith flip results in the event H}. Let X be the random variable denoting the total number of heads in the n coin flips, so that

$$X = \sum_{i=1}^{n} X_i .$$

In order to compute the expected number of heads, take the expectation of both sides of the above equation to obtain

$$E[X] = E\left[\sum_{i=1}^{n} X_i\right]. \tag{5.2}$$

By Lemma 5.1, the expectation of each of the random variables is E[X_i] = 1/2 for i = 1, 2, ..., n. Then we can compute the sum of the expectations: ∑ⁿᵢ₌₁ E[X_i] = n/2. But equation (5.2) calls for the expectation of the sum, not the sum of the expectations. How can we resolve this conundrum? Linearity of expectation, equation (C.24) on page 1192, to the rescue: *the expectation of the sum always equals the sum of the expectations*. Linearity of expectation applies even when there is dependence among the random variables. Combining indicator random variables with linearity of expectation gives us a powerful technique to compute expected values when multiple events occur. We now can compute the expected number of heads:

$$E[X] = E\left[\sum_{i=1}^{n} X_i\right]$$
$$= \sum_{i=1}^{n} E[X_i]$$
$$= \sum_{i=1}^{n} 1/2$$
$$= n/2.$$

Thus, compared with the method used in equation (C.41), indicator random variables greatly simplify the calculation. We use indicator random variables throughout this book.

## **Analysis of the hiring problem using indicator random variables**

Returning to the hiring problem, we now wish to compute the expected number of times that you hire a new office assistant. In order to use a probabilistic analysis, let's assume that the candidates arrive in a random order, as discussed in Section 5.1. (We'll see in Section 5.3 how to remove this assumption.) Let X be the random variable whose value equals the number of times you hire a new office assistant. We could then apply the definition of expected value from equation (C.23) on page 1192 to obtain

$$E[X] = \sum_{x=1}^{n} x \Pr{X = x},$$

but this calculation would be cumbersome. Instead, let's simplify the calculation by using indicator random variables.

To use indicator random variables, instead of computing E[X] by defining just one variable denoting the number of times you hire a new office assistant, think of the process of hiring as repeated random trials and define n variables indicating whether each particular candidate is hired. In particular, let X_i be the indicator random variable associated with the event in which the ith candidate is hired. Thus,

$$X_i = I\{\text{candidate } i \text{ is hired}\}$$

$$= \begin{cases} 1 & \text{if candidate } i \text{ is hired }, \\ 0 & \text{if candidate } i \text{ is not hired }, \end{cases}$$

and

$$X = X_1 + X_2 + \dots + X_n \,. \tag{5.3}$$

Lemma 5.1 gives

E[X_i] = Pr{candidate i is hired};

and we must therefore compute the probability that lines 5–6 of HIRE-ASSISTANT are executed.

Candidate i is hired, in line 6, exactly when candidate i is better than each of candidates 1 through i - 1. Because we have assumed that the candidates arrive in a random order, the first i candidates have appeared in a random order. Any one of these first i candidates is equally likely to be the best qualified so far. Candidate i has a probability of 1/i of being better qualified than candidates 1 through i - 1 and thus a probability of 1/i of being hired. By Lemma 5.1, we conclude that

$$\mathrm{E}\left[X_{i}\right] = 1/i \ . \tag{5.4}$$

Now we can compute E[X]:

$$E[X] = E\left[\sum_{i=1}^{n} X_{i}\right]$$
 (by equation (5.3))
$$= \sum_{i=1}^{n} E[X_{i}]$$
 (by equation (C.24), linearity of expectation)
$$= \sum_{i=1}^{n} \frac{1}{i}$$
 (by equation (5.4))
$$= \ln n + O(1)$$
 (by equation (A.9), the harmonic series). (5.6)

Even though you interview n people, you actually hire only approximately ln n of them, on average. We summarize this result in the following lemma.

## *Lemma 5.2*

Assuming that the candidates are presented in a random order, algorithm HIRE-ASSISTANT has an average-case total hiring cost of O(c_h ln n).

*Proof* The bound follows immediately from our definition of the hiring cost and equation (5.6), which shows that the expected number of hires is approximately ln n.

The average-case hiring cost is a significant improvement over the worst-case hiring cost of O(c_h·n).

### **Exercises**

### *5.2-1*

In HIRE-ASSISTANT, assuming that the candidates are presented in a random order, what is the probability that you hire exactly one time? What is the probability that you hire exactly n times?

### *5.2-2*

In HIRE-ASSISTANT, assuming that the candidates are presented in a random order, what is the probability that you hire exactly twice?

### *5.2-3*

Use indicator random variables to compute the expected value of the sum of n dice.

## *5.2-4*

This exercise asks you to (partly) verify that linearity of expectation holds even if the random variables are not independent. Consider two 6-sided dice that are rolled independently. What is the expected value of the sum? Now consider the case where the {irst die is rolled normally and then the second die is set equal to the value shown on the {irst die. What is the expected value of the sum? Now consider the case where the {irst die is rolled normally and the second die is set equal to 7 minus the value of the {irst die. What is the expected value of the sum?

## *5.2-5*

Use indicator random variables to solve the following problem, which is known as the *hat-check problem*. Each of n customers gives a hat to a hat-check person at a restaurant. The hat-check person gives the hats back to the customers in a random order. What is the expected number of customers who get back their own hat?

## *5.2-6*

Let A[1:n] be an array of n distinct numbers. If i < j and A[i] > A[j], then the pair (i, j) is called an *inversion* of A. (See Problem 2-4 on page 47 for more on inversions.) Suppose that the elements of A form a uniform random permutation of ⟨1, 2, ..., n⟩. Use indicator random variables to compute the expected number of inversions.

## **5.3 Randomized algorithms**

In the previous section, we showed how knowing a distribution on the inputs can help us to analyze the average-case behavior of an algorithm. What if you do not know the distribution? Then you cannot perform an average-case analysis. As mentioned in Section 5.1, however, you might be able to use a randomized algorithm.

For a problem such as the hiring problem, in which it is helpful to assume that all permutations of the input are equally likely, a probabilistic analysis can guide us when developing a randomized algorithm. Instead of *assuming* a distribution of inputs, we *impose* a distribution. In particular, before running the algorithm, let's randomly permute the candidates in order to enforce the property that every permutation is equally likely. Although we have modified the algorithm, we still expect to hire a new office assistant approximately ln n times. But now we expect this to be the case for *any* input, rather than for inputs drawn from a particular distribution.

Let us further explore the distinction between probabilistic analysis and randomized algorithms. In Section 5.2, we claimed that, assuming that the candidates 

arrive in a random order, the expected number of times you hire a new office assistant is about ln n. This algorithm is deterministic: for any particular input, the number of times a new office assistant is hired is always the same. Furthermore, the number of times you hire a new office assistant differs for different inputs, and it depends on the ranks of the various candidates. Since this number depends only on the ranks of the candidates, to represent a particular input, we can just list, in order, the ranks ⟨*rank*(1), *rank*(2), ..., *rank*(n)⟩ of the candidates. Given the rank list A₁ = ⟨1, 2, 3, 4, 5, 6, 7, 8, 9, 10⟩, a new office assistant is always hired 10 times, since each successive candidate is better than the previous one, and lines 5–6 of HIRE-ASSISTANT are executed in each iteration. Given the list of ranks A₂ = ⟨10, 9, 8, 7, 6, 5, 4, 3, 2, 1⟩, a new office assistant is hired only once, in the first iteration. Given a list of ranks A₃ = ⟨5, 2, 1, 8, 4, 7, 10, 9, 3, 6⟩, a new office assistant is hired three times, upon interviewing the candidates with ranks 5, 8, and 10. Recalling that the cost of our algorithm depends on how many times you hire a new office assistant, we see that there are expensive inputs such as A₁, inexpensive inputs such as A₂, and moderately expensive inputs such as A₃.

Consider, on the other hand, the randomized algorithm that first permutes the list of candidates and then determines the best candidate. In this case, we randomize in the algorithm, not in the input distribution. Given a particular input, say A₃ above, we cannot say how many times the maximum is updated, because this quantity differs with each run of the algorithm. The first time you run the algorithm on A₃, it might produce the permutation A₁ and perform 10 updates. But the second time you run the algorithm, it might produce the permutation A₂ and perform only one update. The third time you run the algorithm, it might perform some other number of updates. Each time you run the algorithm, its execution depends on the random choices made and is likely to differ from the previous execution of the algorithm. For this algorithm and many other randomized algorithms, *no particular input elicits its worst-case behavior*. Even your worst enemy cannot produce a bad input array, since the random permutation makes the input order irrelevant. The randomized algorithm performs badly only if the random-number generator produces an "unlucky" permutation.

For the hiring problem, the only change needed in the code is to randomly permute the array, as done in the RANDOMIZED-HIRE-ASSISTANT procedure. This simple change creates a randomized algorithm whose performance matches that obtained by assuming that the candidates were presented in a random order.

### RANDOMIZED-HIRE-ASSISTANT(n)

- 1 randomly permute the list of candidates
- 2 HIRE-ASSISTANT(n)

## *Lemma 5.3*

The expected hiring cost of the procedure RANDOMIZED-HIRE-ASSISTANT is O(c_h ln n).

*Proof* Permuting the input array achieves a situation identical to that of the probabilistic analysis of HIRE-ASSISTANT in Section 5.2.

By carefully comparing Lemmas 5.2 and 5.3, you can see the difference between probabilistic analysis and randomized algorithms. Lemma 5.2 makes an assumption about the input. Lemma 5.3 makes no such assumption, although randomizing the input takes some additional time. To remain consistent with our terminology, we couched Lemma 5.2 in terms of the average-case hiring cost and Lemma 5.3 in terms of the expected hiring cost. In the remainder of this section, we discuss some issues involved in randomly permuting inputs.

## **Randomly permuting arrays**

Many randomized algorithms randomize the input by permuting a given input array. We'll see elsewhere in this book other ways to randomize an algorithm, but now, let's see how we can randomly permute an array of n elements. The goal is to produce a *uniform random permutation*, that is, a permutation that is as likely as any other permutation. Since there are n! possible permutations, we want the probability that any particular permutation is produced to be 1/n!.

You might think that to prove that a permutation is a uniform random permutation, it suffices to show that, for each element A[i], the probability that the element winds up in position j is 1/n. Exercise 5.3-4 shows that this weaker condition is, in fact, insufficient.

Our method to generate a random permutation permutes the array *in place*: at most a constant number of elements of the input array are ever stored outside the array. The procedure RANDOMLY-PERMUTE permutes an array A[1:n] in place in Θ(n) time. In its ith iteration, it chooses the element A[i] randomly from among elements A[i] through A[n]. After the ith iteration, A[i] is never altered.

```
RANDOMLY-PERMUTE(A, n)
1 for i = 1 to n
2     swap A[i] with A[RANDOM(i, n)]
```

We use a loop invariant to show that procedure RANDOMLY-PERMUTE produces a uniform random permutation. A k*-permutation* on a set of n elements is a se

quence containing k of the n elements, with no repetitions. (See page 1180 in Appendix C.) There are n!/(n - k)! such possible k-permutations.

## *Lemma 5.4*

Procedure RANDOMLY-PERMUTE computes a uniform random permutation.

*Proof* We use the following loop invariant:

Just prior to the ith iteration of the **for** loop of lines 1–2, for each possible (i - 1)-permutation of the n elements, the subarray A[1:i - 1] contains this (i - 1)-permutation with probability (n - i + 1)!/n!.

We need to show that this invariant is true prior to the first loop iteration, that each iteration of the loop maintains the invariant, that the loop terminates, and that the invariant provides a useful property to show correctness when the loop terminates.

**Initialization:** Consider the situation just before the first loop iteration, so that i = 1. The loop invariant says that for each possible 0-permutation, the subarray A[1:0] contains this 0-permutation with probability (n - i + 1)!/n! = n!/n! = 1. The subarray A[1:0] is an empty subarray, and a 0-permutation has no elements. Thus, A[1:0] contains any 0-permutation with probability 1, and the loop invariant holds prior to the first iteration.

**Maintenance:** By the loop invariant, we assume that just before the ith iteration, each possible (i - 1)-permutation appears in the subarray A[1:i - 1] with probability (n - i + 1)!/n!. We shall show that after the ith iteration, each possible i-permutation appears in the subarray A[1:i] with probability (n - i)!/n!. Incrementing i for the next iteration then maintains the loop invariant.

Let us examine the ith iteration. Consider a particular i-permutation, and denote the elements in it by ⟨x₁, x₂, ..., xᵢ⟩. This permutation consists of an (i - 1)-permutation ⟨x₁, ..., xᵢ₋₁⟩ followed by the value xᵢ that the algorithm places in A[i]. Let E₁ denote the event in which the first i - 1 iterations have created the particular (i - 1)-permutation ⟨x₁, ..., xᵢ₋₁⟩ in A[1:i - 1]. By the loop invariant, Pr{E₁} = (n - i + 1)!/n!. Let E₂ be the event that the ith iteration puts xᵢ in position A[i]. The i-permutation ⟨x₁, ..., xᵢ⟩ appears in A[1:i] precisely when both E₁ and E₂ occur, and so we wish to compute Pr{E₂ ∩ E₁}. Using equation (C.16) on page 1187, we have

$$\Pr\{E_2 \cap E_1\} = \Pr\{E_2 \mid E_1\} \Pr\{E_1\} \ .$$

The probability Pr{E₂ | E₁} equals 1/(n - i + 1) because in line 2 the algorithm chooses xᵢ randomly from the n - i + 1 values in positions A[i:n]. Thus, we have

$$\Pr\{E_2 \cap E_1\} = \Pr\{E_2 \mid E_1\} \Pr\{E_1\}$$

$$= \frac{1}{n-i+1} \cdot \frac{(n-i+1)!}{n!}$$

$$= \frac{(n-i)!}{n!}.$$

**Termination:** The loop terminates, since it is a **for** loop iterating n times. At termination, i = n + 1, and we have that the subarray A[1:n] is a given n-permutation with probability (n - (n + 1) + 1)!/n! = 0!/n! = 1/n!.

Thus, RANDOMLY-PERMUTE produces a uniform random permutation.

A randomized algorithm is often the simplest and most efficient way to solve a problem.

### **Exercises**

## *5.3-1*

Professor Marceau objects to the loop invariant used in the proof of Lemma 5.4. He questions whether it holds prior to the first iteration. He reasons that we could just as easily declare that an empty subarray contains no 0-permutations. Therefore, the probability that an empty subarray contains a 0-permutation should be 0, thus invalidating the loop invariant prior to the first iteration. Rewrite the procedure RANDOMLY-PERMUTE so that its associated loop invariant applies to a nonempty subarray prior to the first iteration, and modify the proof of Lemma 5.4 for your procedure.

## *5.3-2*

Professor Kelp decides to write a procedure that produces at random any permutation except the *identity permutation*, in which every element ends up where it started. He proposes the procedure PERMUTE-WITHOUT-IDENTITY. Does this procedure do what Professor Kelp intends?

```
PERMUTE-WITHOUT-IDENTITY(A, n)
1 for i = 1 to n - 1
2     swap A[i] with A[RANDOM(i + 1, n)]
```

### *5.3-3*

Consider the PERMUTE-WITH-ALL procedure on the facing page, which instead of swapping element A[i] with a random element from the subarray A[i:n], swaps it with a random element from anywhere in the array. Does PERMUTE-WITH-ALL produce a uniform random permutation? Why or why not?

```
PERMUTE-WITH-ALL(A, n)
1 for i = 1 to n
2     swap A[i] with A[RANDOM(1, n)]
```

## *5.3-4*

Professor Knievel suggests the procedure PERMUTE-BY-CYCLE to generate a uniform random permutation. Show that each element A[i] has a 1/n probability of winding up in any particular position in B. Then show that Professor Knievel is mistaken by showing that the resulting permutation is not uniformly random.

```
PERMUTE-BY-CYCLE(A, n)
1 let B[1:n] be a new array 
2 offset = RANDOM(1, n)
3 for i = 1 to n
4     dest = i + offset 
5     if dest > n
6         dest = dest - n
7     B[dest] = A[i]
8 return B
```

## *5.3-5*

Professor Gallup wants to create a *random sample* of the set {1, 2, 3, ..., n}, that is, an m-element subset S, where 0 ≤ m ≤ n, such that each m-subset is equally likely to be created. One way is to set A[i] = i, for i = 1, 2, 3, ..., n, call RANDOMLY-PERMUTE(A), and then take just the first m array elements. This method makes n calls to the RANDOM procedure. In Professor Gallup's application, n is much larger than m, and so the professor wants to create a random sample with fewer calls to RANDOM.

```
RANDOM-SAMPLE(m, n)
1 S = ∅
2 for k = n - m + 1 to n // iterates m times 
3     i = RANDOM(1, k)
4     if i ∈ S
5         S = S ∪ {k}
6     else S = S ∪ {i}
7 return S
```

Show that the procedure RANDOM-SAMPLE on the previous page returns a random m-subset S of {1, 2, 3, ..., n}, in which each m-subset is equally likely, while making only m calls to RANDOM.

## ⋆ **5.4 Probabilistic analysis and further uses of indicator random variables**

This advanced section further illustrates probabilistic analysis by way of four examples. The first determines the probability that in a room of k people, two of them share the same birthday. The second example examines what happens when randomly tossing balls into bins. The third investigates "streaks" of consecutive heads when flipping coins. The final example analyzes a variant of the hiring problem in which you have to make decisions without actually interviewing all the candidates.

## **5.4.1 The birthday paradox**

Our first example is the *birthday paradox*. How many people must there be in a room before there is a 50% chance that two of them were born on the same day of the year? The answer is surprisingly few. The paradox is that it is in fact far fewer than the number of days in a year, or even half the number of days in a year, as we shall see.

To answer this question, we index the people in the room with the integers 1, 2, ..., k, where k is the number of people in the room. We ignore the issue of leap years and assume that all years have n = 365 days. For i = 1, 2, ..., k, let bᵢ be the day of the year on which person i's birthday falls, where 1 ≤ bᵢ ≤ n. We also assume that birthdays are uniformly distributed across the n days of the year, so that Pr{bᵢ = r} = 1/n for i = 1, 2, ..., k and r = 1, 2, ..., n.

The probability that two given people, say i and j, have matching birthdays depends on whether the random selection of birthdays is independent. We assume from now on that birthdays are independent, so that the probability that i's birthday and j's birthday both fall on day r is

$$\Pr\{b_i = r \text{ and } b_j = r\} = \Pr\{b_i = r\} \Pr\{b_j = r\}$$
  
=  $\frac{1}{n^2}$ .

Thus, the probability that they both fall on the same day is

$$\Pr\{b_i = b_j\} = \sum_{r=1}^n \Pr\{b_i = r \text{ and } b_j = r\}$$