To run the server locally use this command with the environment active:

`streamlit run Home.py`

## Stable Swap Math

From the [Balancer documentation](https://dev.balancer.fi/resources/pool-math/stable-math) we know that the Stable Swap math is defined as:

$$
    A \cdot n^n \cdot \sum^{n} x_i + D = A \cdot D + \cfrac{D^{n+1}}{n^n \cdot \prod^{n} x_i}
$$

where:
- $A$: Amplification factor defined
- $n$: Number of tokens
- $x_i$: Amount of each token
- $D$: Pool invariant


### Out Given In

In the same documentation, is defined as:

$$
y^2+\big( \cfrac{D}{A \cdot n^n}+\sum_{j\neq out}^{n} x'_j -D\big)y - \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot \prod_{j\neq out}^{n}x'_j} = 0
$$
$$
a_{out} = x_{out} -  x'_{out} = x_{out} - y
$$

where:
- $x'_j$: ending amount of each token
- $a_{out}$: output token received
- $x_{out}$: starting amount of the output token
- $y=x'_{out}$: ending amount of the output token

Considering just one input token, we can redifine the $y$ function as:

$$
y^2+\big( \cfrac{D}{A \cdot n^n}+S+x -D\big)y - \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot P \cdot x} = 0
$$

where:
- $x$: Input token after trade
- $S$: Sum of the ammount of all tokens not involved in the trade
- $P$: Product of the ammount of all tokens not involved in the trade


Using Bhaskara and considering just the positive result, it is possible to define:

$$
y(x) = \cfrac{-b(x) + \sqrt{b(x)^2 + 4a(x)c(x)}}{2a(x)}
$$

where:

$$
a(x) = 1
$$

$$
b(x) = \cfrac{D}{A \cdot n^n}+S+x -D
$$

$$
c(x) = - \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot P \cdot x}
$$

Since $a(x)$ is constant, we can rewrite $y(x)$ as:

$$
y(x) = \cfrac{-b(x) + \sqrt{b(x)^2 + 4c(x)}}{2}
$$


### In given Price

In order to calculate the input token to change the price of a pair until a certain value, the $y'(x)$ will be calculated. First we will define the derivates $b'(x)$ and $c'(x)$.

$$
b'(x) = 1
$$

$$
c'(x) = \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot P \cdot x^2} = -x^{-1}c(x)
$$



Then, we can start calculating the derivative of the root square part:

$$
g(x) = \sqrt{b(x)^2 + 4c(x)}
$$

$$
g'(x) = \frac{b(x)b'(x)-2c'(x)}{\sqrt{b(x)^2-4c(x)}}
$$

Now, we can calculate $y'(x)$ as:

$$
y'(x) = \cfrac{-b'(x) + g'(x)}{2}
$$

$$
y'(x) = \cfrac{-b'(x) + \frac{b(x)b'(x)-2c'(x)}{\sqrt{b(x)^2-4c(x)}}}{2}
$$

Since $-b(x)$ is constant:

$$
y'(x) = \cfrac{-1 + \frac{b(x)-2c'(x)}{\sqrt{b(x)^2-4c(x)}}}{2}
$$

$$
y'(x) =  \frac{b(x)-2c'(x)}{2\sqrt{b(x)^2-4c(x)}} -0,5
$$

So, the final formula is:

