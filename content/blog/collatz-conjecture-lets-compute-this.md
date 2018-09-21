---
title: "Collatz Conjecture Lets Compute This"
date: 2017-08-17T12:51:48+12:00
draft: false
categories: ["Tutorial"]
tags: ["Maths"]
description: "Everything you wanted to know about Collatz conjecture."
---

Before we look into what a Collatz conjecture is, I highly recommend watching the (below) video by Numberphile.

{{< youtube 5mFpVDpKX70 >}}


Collatz conjecture also called as $3n+1$ problem, $3x+1$ mapping, Hasse's algorithm, Kakutani's problem, Syracuse algorithm, Syracuse problem, Thwaites conjecture, and Ulam's problem.

Basically, the problem states that all positive whole numbers should eventually compute to $1$, which is based on the following condition:

$$
a\_{n} =
\begin{cases}
\frac{1}{2}a\_{n-1},  & \text{if $a\_{n-1}$ is even} \\\
3n+1, & \text{if $a\_{n-1}$ is odd}
\end{cases}
$$

The above equation says, at every iteration, check if the input number is even or odd. If the number is even then divide it by $2$ i.e., $\frac{number}{2}$ else multiply $3$ and add $1$ to the number i.e., $3 \ast number+1$.

Programmatically, this can be written as

```python
def compute(number):

    while number != 1:
        print(number)
        if number % 2 == 0:
            number = (number / 2)
        else:
            number = int(3 * number + 1)
    else:
        print(number)

if __name__ == '__main__':
    compute(10)
```

<script type="text/javascript" async
  src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}
});
</script>