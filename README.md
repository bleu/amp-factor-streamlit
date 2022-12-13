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
b(x) = \cfrac{D}{A \cdot n^n}+S+x -D = C_1+x
$$

$$
c(x) = - \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot P \cdot x} = \frac{C_2}{x}
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
c'(x) = \cfrac{D^{n+1}}{A \cdot n^{2n}\cdot P \cdot x^2} = -x^{-1}c(x) = -\cfrac{C_2}{x^2}
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
y'(x) =  \frac{b(x)-2c'(x)}{2\sqrt{b(x)^2-4c(x)}} -\frac{1}{2}
$$

Now, in order to calculate the in ginen price function, we have to invert this function.

$$
y' + \frac{1}{2} = \cfrac{C_1+x+\cfrac{C_2}{x^2}}{2\sqrt{(C_1+x)^2-4\cfrac{C_2}{x}}}
$$

$$
2y' + 1 = \cfrac{\cfrac{C_1x^2+x^3+C_2}{x^2}}{\sqrt{(C_1+x)^2-4\cfrac{C_2}{x}}}
$$

$$
(2y' + 1)^2 = \cfrac{\cfrac{(C_1x^2+x^3+C_2)^2}{x^4}}{(C_1+x)^2-4\cfrac{C_2}{x}}
$$

$$
(2y' + 1)^2 = \cfrac{\cfrac{(C_1x^2+x^3+C_2)^2}{x^4}}{\cfrac{x(C_1+x)^2-4C_2}{x}}
$$

$$
(2y' + 1)^2 = \cfrac{(C_1x^2+x^3+C_2)^2}{x^3(x(C_1+x)^2-4C_2)}
$$

$$
(2y' + 1)^2(x^3(x(C_1+x)^2-4C_2)) = (C_1x^2+x^3+C_2)^2
$$

$$
(4y'^2 + 4y' + 1)(C_1^2x^4+2C_1x^5+x^6-4C_2x^3) = C_1^2x^4+2C_1x^5+2x^3C_2+2C_1x^2C_2+x^6+C_2^2
$$

Solving this equation, we get a polynominal equation can be writen as:

$$
f_6(y')x^6 + f_5(y')x^5 + f_4(y')x^4 + f_3(y')x^3 + f_2(y')x^4 + f_1(y')x^4 + f_0(y') = 0
$$

where:
$$
f_6(y')= 4 y^2 + 4
$$

$$
f_5(y')=8 C_1 y'^2 + 8 C_1 y'
$$

$$
f_4(y')=4 C_1^2 y^2 + 4 C_1^2 y
$$

$$
f_3(y')=- 16 C_2 y^2 - 16 C_2 y - 6 C_2
$$

$$
f_2(y') = -2C_1C_2
$$

$$
f_1(y') = 0
$$

$$
f_0(y') = -C_2^2
$$

Since this is a 6th order plinomial, does not exist an analytical solution. This means, that a numerical approach has to be used.