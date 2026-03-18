Next we're going to look at how to use the **chain** rule for differentiating more complex functions.

---

## Composite functions

$f(x)$ is a composite function if it is a function of a function, i.e.:

$$y = g\Big(h(x)\Big)$$

We can refer to $g$ as the outer function and $h$ as the inner function.

We now look at some examples to help to identify what a composite function is.

**Examples of composite functions**

1. $\cos(x^2)$
   * $g(x) = \cos(x)$
   * $h(x) = x^2$
2. $e^{3x}$
   * $g(x) = e^x$
   * $h(x) = 3x$
3. $(1+x)^{-1}$
   * $g(x) = x^{-1}$
   * $h(x) = 1+x$

A good thing to look out for in a composite function is to see if there is something attached to the $x$ within the traditional function we recognise. It's important to be able to distinguish between a product of functions of $x$ (like $x^2 \cos(x)$) and a function of a function of $x$ (a double transformation of $x$).

---

## Chain rule

The **chain rule** is used to compute the gradient of composite functions. The chain part refers to the fact that we make the substitution $t = h(x)$ for the inner part of the function.

$$y = g\Big(h(x)\Big) = g(t)$$

We then find the derivative $\frac{dy}{dx}$ by treating $t$ as the new $x$. We then have to remember to differentiate $t$ with respect to $x$, by finding $h'(x)$ and then multiply these together.

$$\implies \frac{dy}{dx} = \frac{dy}{dt} \frac{dt}{dx} = g'(t) h'(x) = g' \Big( h(x) \Big) h'(x)$$

Look at the following example to familiarise yourself with this function:

**Worked example:** $y = \sin(3x)$

* $t = 3x \implies y = \sin(t)$
* $\frac{dt}{dx} = 3 \text{ and } \frac{dy}{dt} = \cos(t)$
* $\frac{dy}{dx} = 3\cos(t) = 3\cos(3x)$