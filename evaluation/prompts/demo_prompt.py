# nondimensionalization symbolic (1 shot)

# pid = 0

demo_prompt = "Example question: Nondimensionalize the polynomial\\[a_{1} x^{7} + a_{2} x^{2} + a_{3}\\]\
    into one of the form $\\\\epsilon y^{7} + y^{2} + 1.$Express $\\\\epsilon$ as a function of $a_1$, \
    $a_2$, and $a_3.$\nExample solution: We begin with the substitution $ x=y \\sqrt{\\frac{a_{3}}{a_{2}}}$  \
    \nThis gives the expression $ a_{1} y^{7} \\left(\\frac{a_{3}}{a_{2}}\\right)^{\\frac{7}{2}} + a_{3} y^{2} + a_{3}$  \
    \nDivide by the coefficient remaining in front of the constant, leaving us with the nondimensionalized \
    polynomial with coefficients in terms of $ a_1$ , $ a_2$ , and $ a_3$ : \
    $  \\boxed{\\frac{a_{1} y^{7} \\left(\\frac{a_{3}}{a_{2}}\\right)^{\\frac{7}{2}}}{a_{3}} + y^{2} + 1}.$ \
    By inspection, we can see that $  \\boxed{\\epsilon=\\frac{a_{1} \\left(\\frac{a_{3}}{a_{2}}\\right)^{\\frac{7}{2}}}{a_{3}}}.$"


# nondimensionalization numeric (1 shot)

# pid = 100

demo_prompt = "Example question: Nondimensionalize the polynomial \\[P(x) = 2 x^{7} + 8 x^{2} + 5\\] \
into a polynomial of the form $\\epsilon y^{7} \\pm y^{2} \\pm 1$. Solve for $\\epsilon$.\nExample \
solution: For now, we ignore the numeric values of the coefficients and instead call them $ a_1, a_2, \
a_3$ . Our polynomial is then: $ a_{1} x^{7} + a_{2} x^{2} + a_{3}.$   Use the substitution \
$ x=y \\sqrt{\\frac{a_{3}}{a_{2}}},$  \nwhich gives the expression \
$ a_{1} y^{7} \\left(\\frac{a_{3}}{a_{2}}\\right)^{\\frac{7}{2}} + a_{3} y^{2} + a_{3}.$  \
\nDivide all terms by the coefficient remaining in front of the constant term, giving us the \
nondimensionalized polynomial with coefficients in terms of $ a_1, a_2, a_3$ :   \
$ frac{a_{1} y^{7} \\left(\\frac{a_{3}}{a_{2}}\\right)^{\\frac{7}{2}}}{a_{3}} + y^{2} + 1$  \
\nSubstituting in the known numeric values for $ a_1, a_2, a_3$  (using their absolute values as \
we have already accounted for sign), we get:   $ frac{25 \\sqrt{10} y^{7}}{1024} + y^{2} + 1$  \
\nFrom inspection of this nondimensionalized equation, we can now identify  $ epsilon$ :  \
$  \\epsilon=\\frac{25 \\sqrt{10}}{1024}\\implies \\boxed{\\epsilon \\approx0.08}.$"

# polynomial roots finding (1 shot)

# pid = 199

demo_prompt = "Example question: Consider the polynomial\\[P(x) =\\epsilon x^{9} + x^{4} - 1.\\] \
\nFind approximate expressions for all roots of the polynomials in the limit of small positive \
$\\epsilon$ and large positive $\\epsilon$. Only a single term approximation to the root is required. \
\nExample solution: Consider the problem to be of form $ A+B+C=0$ , with $ A$ , $ B$ , and $ C$  \
corresponding to the three terms in $ P(x)$  :$ A=\\epsilon x^{9};$  $ B=x^{4};$  $ C=-1.$ \nWe now \
consider the three possible dominant balances, solving for the roots in each case and evaluating whether \
each balance holds for large or for small  $ epsilon$ .\\vspace{1em}\n\nWe start with the balance \
$ A+B=0$ , assuming that $ |C|$  is negligible when compared to $ |A|$  and $ |B|$ . Solving this for \
$ x$  in terms of  $ epsilon$  then gives us 5 non-zero roots: \n  $ epsilon x^{9} + x^{4}=0 $  \
$  \\implies \\boxed{ x=\\left[ \\sqrt[5]{- \\frac{1}{\\epsilon}}, \\  \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(-1 + \\sqrt{5} - \\sqrt{2} \\sqrt{-5 - \\sqrt{5}}\\right)}{4}, \\ \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(-1 + \\sqrt{5} + \\sqrt{2} \\sqrt{-5 - \\sqrt{5}}\\right)}{4}, \\  \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(- \\sqrt{5} - 1 - \\sqrt{2} \\sqrt{-5 + \\sqrt{5}}\\right)}{4}, \\  \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(- \\sqrt{5} - 1 + \\sqrt{2} \\sqrt{-5 + \\sqrt{5}}\\right)}{4}\\right]}.$  \
\nTo verify the roots found for consistency with our initial assumption, we check that $ |A|,|B|>>|C|$  \
holds for this root by substituting our found root expression for $ x$  back into $ A$ , $ B$ , and $ C$  \
and comparing their magnitudes. Using this method, we find that validity for small  $ epsilon$  is True and \
validity for large  $ epsilon$  is False.\n\n\\underline{Therefore, these roots are valid in the limit of \
small positive  $ epsilon$  only.}\\vspace{1em}\n\nNext we examine the balance $ B+C=0$ , assuming that \
$ |A|$  is negligible when compared to $ |B|$  and $ |C|$ . Solving this for $ x$  in terms of  \
$ epsilon$  gives us 4 non-zero roots:  $ x^{4} - 1=0$   $  \\implies\\boxed{ x=\\left[ -1, \\  1, \
\\  - i, \\  i\\right]}.$  \nTo verify the roots found for consistency with our initial assumption, \
we check that $ |B|,|C|>>|A|$  holds for this root by substituting our found root expression for $ x$  \
back into $ A$ , $ B$ , and $ C$  and comparing their magnitudes. Using this method, we find that\
validity for small  $ epsilon$  is True and validity for large  $ epsilon$  is False.\
\n\n\\underline{Therefore, these roots are valid in the limit of small positive  $ epsilon$  only.}\\vspace{1em}\n\n\
Finally, we examine the balance $ A+C=0$ , assuming that $ |B|$  is negligible when compared to $ |A|$  \
and $ |C|$ . Solving this for $ x$  in terms of  $ epsilon$  gives us 9 non-zero roots:  \
$ epsilon x^{9} - 1=0$   $  \\implies\\boxed{ x=\\left[ - \\sqrt[9]{\\frac{1}{\\epsilon}} e^{\\frac{i \\pi}{9}}, \\ \
- \\sqrt[9]{\\frac{1}{\\epsilon}} e^{- \\frac{i \\pi}{9}}, \\  \\sqrt[9]{\\frac{1}{\\epsilon}} e^{- \\frac{2 i \\pi}{9}}, \\ \
\\sqrt[9]{\\frac{1}{\\epsilon}} e^{\\frac{2 i \\pi}{9}}, \\ \
\\left(\\sin{\\left(\\frac{\\pi}{18} \\right)} - i \\cos{\\left(\\frac{\\pi}{18} \\right)}\\right) \
\\sqrt[9]{\\frac{1}{\\epsilon}}, \\  \\left(\\sin{\\left(\\frac{\\pi}{18} \\right)} + \
i \\cos{\\left(\\frac{\\pi}{18} \\right)}\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}, \\ \
\\frac{\\left(-1 - \\sqrt{3} i\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}}{2}, \\ \
\\frac{\\left(-1 + \\sqrt{3} i\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}}{2}, \\ \
\\sqrt[9]{\\frac{1}{\\epsilon}}\\right]}.$  \nTo verify the roots found for consistency with our \
initial assumption, we check that $ |A|,|C|>>|B|$  holds for this root by substituting our found \
root expression for $ x$  back into $ A$ , $ B$ , and $ C$  and comparing their magnitudes. \
Using this method, we find that validity for small  $ epsilon$  is False and validity for large \
$ epsilon$  is True.\n\n\\underline{Therefore, these roots are valid in the limit of large positive \
$ epsilon$  only.}\\vspace{1em}\n\nWe expect that, in each  $ epsilon$  regime, we have the same number \
of roots as the degree of the polynomial $ P(x)$ . We have found a total of 18 roots, half of which are \
valid in the limit of small positive  $ epsilon$  and the other half of which are valid in the limit of \
large positive  $ epsilon$ . This is expected given the degree of the polynomial. So, the roots of \
$ P(x)$  for large positive  $ epsilon$  are $  \\boxed{ \\left[ - \\sqrt[9]{\\frac{1}{\\epsilon}} e^{\\frac{i \\pi}{9}}, \\ \
- \\sqrt[9]{\\frac{1}{\\epsilon}} e^{- \\frac{i \\pi}{9}}, \\  \\sqrt[9]{\\frac{1}{\\epsilon}} e^{- \\frac{2 i \\pi}{9}}, \\ \
\\sqrt[9]{\\frac{1}{\\epsilon}} e^{\\frac{2 i \\pi}{9}}, \\  \\left(\\sin{\\left(\\frac{\\pi}{18} \\right)} - \
i \\cos{\\left(\\frac{\\pi}{18} \\right)}\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}, \\ \
\\left(\\sin{\\left(\\frac{\\pi}{18} \\right)} + i \\cos{\\left(\\frac{\\pi}{18} \\right)}\\right)\
\\sqrt[9]{\\frac{1}{\\epsilon}}, \\  \\frac{\\left(-1 - \\sqrt{3} i\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}}{2}, \\ \
\\frac{\\left(-1 + \\sqrt{3} i\\right) \\sqrt[9]{\\frac{1}{\\epsilon}}}{2}, \\  \\sqrt[9]{\\frac{1}{\\epsilon}}\\right]} $ \
and the roots of $ P(x)$  for small positive  $ epsilon$  are $  \\boxed{ \\left[ \\sqrt[5]{- \\frac{1}{\\epsilon}}, \\ \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(-1 + \\sqrt{5} - \\sqrt{2} \\sqrt{-5 - \\sqrt{5}}\\right)}{4}, \\ \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(-1 + \\sqrt{5} + \\sqrt{2} \\sqrt{-5 - \\sqrt{5}}\\right)}{4}, \\ \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(- \\sqrt{5} - 1 - \\sqrt{2} \\sqrt{-5 + \\sqrt{5}}\\right)}{4}, \\ \
\\frac{\\sqrt[5]{- \\frac{1}{\\epsilon}} \\left(- \\sqrt{5} - 1 + \\sqrt{2} \\sqrt{-5 + \\sqrt{5}}\\right)}{4}, \\ \
-1, \\  1, \\  - i, \\  i\\right]} $."


# ode (1 shot)

# pid = 262

demo_prompt = "Example question: Consider the following third-order ordinary differential equation: \
$$y''' = - \\frac{y}{24 x^{4} + 6 x^{2} + 3} + y'^{2} - \\frac{y''}{5 x^{3} - 2 x^{2} - x + 2} - \
\\frac{1}{12 x^{2} - \\cos{\\left(x \\right)} + 11}$$\n\n\\text{with initial conditions at } x = 0:\n\
\\begin{align*}\ny(0) &= 1.00 \\\\\ny'(0) &= 0.00 \\\\\ny''(0) &= 0.00\n\\end{align*}\n\nFind analytical \
expressions that approximate the solution of $y(x)$ in the small $x$ and large $x$ regimes.\n\n\nExample \
solution: The dominant balance in the small x regime is given by $  $ frac{d^{3}}{d x^{3}} y \
= - \\frac{y}{24 x^{4} + 6 x^{2} + 3},$ $  and the dominant balance in the large x regime is given by \
$  $ frac{d^{3}}{d x^{3}} y = \\left(\\frac{d}{d x} y\\right)^{2}$ $ \nUsing the dominant balance in the \
small x regime, the solution can be derived by setting $ x=0$ , analytically solving the dominant \
balance equation for y, and plugging in the initial conditions. The solution is thus $ $ y{\\left(x \
\\right)} = 1 - \\frac{x^{3}}{18}$ $  in the small x regime.\n\nThe solution for the large  $  x  $  \
regime uses an ansatz of the form \n$ $  y = \\alpha (x - x^*)^p, $ $  \nwhere  $  x^*  $  is the \
divergence point. Plugging in the ansatz and solving for the terms yields \n$ $ \n\\alpha p \
\\left(p - 2\\right) \\left(p - 1\\right) \\left(x - 11.4511451145115\\right)^{p - 3} = \\alpha^{2} p^{2} \
\\left(x - 11.4511451145115\\right)^{2 p - 2}\n$ $ \n\nAfter substituting the derivatives, the equation \
is reorganized to collect terms with respect to  $  (x - x^*)  $ . This leads to an equation where the \
coefficients and powers of  $  (x - x^*)  $  are equated on both sides. Simplifying the equation gives \
us two separate equations, one for the coefficients and another for the powers of  $  (x - x^*)  \
$ .\n\nThe coefficients' equation is:\n$ $ \n\\alpha p \\left(p - 2\\right) \\left(p - 1\\right) = \
\\alpha^{2} p^{2}\n$ $ \n\nThe powers' equation is:\n$ $ \np - 3 = 2 p - 2\n$ $ \n\nSolving this system \
of equations provides the values of  $  \\alpha  $  and  $  p  $ . \nA valid solution is identified if  \
$  \\alpha  $  and  $  p  $  are both nonzero. \nIn such a case, the solution for  $  \\alpha  $  and \
$  p  $  is found to be:\n$ $ \n\\alpha = -6, \\quad p = -1\n$ $ \n\nWith these values, the integration \
constant  $  C  $  is determined by substituting \na known point from the numerical solution into the \
ansatz. This yields the following equation for  $  C  $ :\n$ $ \n63.9257998942671 = C + 66.6600000000007\
\n$ $ \n\nSolving this equation, we find the value of  $  C  $  to be:\n$ $ \nC = -2.7342001057336,\n$ $ \
\n\nso, the analytical approximation for the solution at large $ x$  (near the divergence point) is \
given by\n$ $ \ny = -6 (x - 11.4511451145115)^{-1} + (-2.7342001057336),\n$ $ \n\nand the analytical \
approximation for the solution at small $ x$  is given by\n$ $ \ny = 1 - \\frac{x^{3}}{18}.\n$ $ \n\n\
Thus, the solution is given by \n$  $ boxed{[y = 1 - \\frac{x^{3}}{18}, \
y = -6 (x - 11.4511451145115)^{-1} + (-2.7342001057336)]}$ $"

# laplace integral (1 shot)

# pid = 316

demo_prompt = "Example question: Consider the integral \\par \\begin{equation} I(x) = \\int_{-1.0}^{0.3} \
(- 2.6 t^{2} + 1.5 t) e^{- x (- 0.7 \\sin{\\left(t \\right)})} \\, dt \\end{equation} \\par Develop an \
analytical formula for $I(x)$ that is accurate as $x \\to \\infty$.\nExample solution: The integral is \
of the form \\begin{equation} I(x) = \\int_{a}^{b} g(t) e^{- x f(t)} \\, dt \\end{equation} \\par where \
$ a=-1.0$ , $ b=0.3$ , $ g(t) = - 2.6 t^{2} + 1.5 t$ , and $ f(t) = - 0.7 \\sin{\\left(t \\right)}$ . \
This means we can use Laplace's method to develop an analytical approximation in the limit that \
$ x \\to \\infty$ . \\par In this limit, the integral will be dominated by the integrand near the \
minimum of $ f(t)$  within the bounds $ [-1.0, 0.3]$ . So, to simplify the integral, we will expand the \
integrand around this minimum. \\par In this case, we can find the minimum of \
$ f(t) = - 0.7 \\sin{\\left(t \\right)}$  on the interval analytically. We begin by looking for critical \
point(s) $ t_{crit}$  of $ f(t)$  by solving $ f'(t) = - 0.7 \\cos{\\left(t \\right)} = 0$  for $ t$ . \
We find that there are no critical points of $ f(t) \\in (-1.0, 0.3)$ . This means that its minimum must \
be on the bounds. Comparing the values of $ f(t)$  on the bounds, we find that its minimum occurs at \
$ t_0 = b = 0.3$ . \\par Since the integral is dominated by the value of the integrand near b, we Taylor \
expand the integrand around this point. \\begin{equation} I(x) =  \\int_{a}^{b} (g(b) + (t-b)g'(b)+...) \
e^{- x (f(b) + (t-b) f'(b) + ...)} \\, dt \\end{equation} We can then approximate \\begin{equation} I(x) \
\\approx \\int_{a}^{b} g(b) e^{- x (f(b) + (t-b) f'(b))} \\, dt \\end{equation} Pulling out the constant \
in the integral gives \\begin{equation} I(x) \\approx g(b) e^{- x f(b)} \\int_{a}^{b} e^{- x (t-b) f'(b)} \
\\, dt \\end{equation} \\par Since $ x$  is large, we perform the change of variables $ u = x (t-b) |f'(b)|$ . \
Note $ f'(b) < 0$  since it is a minimum. So, rewriting the integral, we get \\begin{equation} I(x) \\approx \
g(b) e^{- x f(b)} \\int_{x (a-b) |f'(b)|}^{0} \\frac{1}{x |f'(b)|} e^{u} \\, dt \\end{equation} Since \
$ x \\to \\infty$ , we approximate this with new bounds as \\begin{equation} I(x) \\approx g(b) \
e^{- x f(b)} \\frac{1}{x |f'(b)|} \\int_{-\\infty}^{0} e^{u} \\, dt \\end{equation} \\par \
Solving the integral and evaluating, we find that \\par \\begin{equation} \\boxed{I(x) \\approx \
\\frac{0.322997637046038 e^{0.206864144662938 x}}{x}} \\end{equation}\n"

# simple integral (1 shot)

# pid = 376

demo_prompt = "Example question: Consider the integral $I(\\epsilon) = \\int_0^{43.00} \
\\frac{1}{\\epsilon + 2.0 x^{6.0} + 16.0 x^{12.0} + 11.0 x^{18.0} + 6.0 x^{19.0}} dx$. Develop an \
analytical formula for $I(\\epsilon)$.\nExample solution: The integral is of the form $ I(\\epsilon) = \
\\int_0^{43} \\frac{1}{\\epsilon + P(x)} dx$  where $ P(x)$  is a polynomial.\n    The integrand is \
maximum at $ x = 0$ , with a height of  $ frac{1}{\\epsilon}$ .\n\n    For small  $ epsilon$ ,\n    \
We define the width as the point where the integrand becomes half of its maximum height.\n    This \
corresponds to solving $ P(x) = \\epsilon$ .\n    Applying dominant balance, considering the term in \
$ P(x)$  with the smallest degree, the width is approximated as $  \\left( \\frac{1}{2.0*\\epsilon} \
\\right)^{1/6.0} $ .\n    Therefore, the solution for the integral for small  $ epsilon$  is  \
$ boxed{I(\\epsilon) = \\frac{0.890898718140339}{\\epsilon^{0.833333333333333}}}$ .\n\n    \
For large $ epsilon$ ,\n    We also define the width based on the term with the largest degree.\n    \
The width is approximated as  $  \\left( \\frac{1}{6.0*\\epsilon} \\right)^{1/19.0}  $ .\n    \
Therefore, the solution for the integral for large  $ epsilon$  is  $ boxed{I(\\epsilon) = \
\\frac{0.910006870081735}{\\epsilon^{0.947368421052632}}}$ .\n\n    Altogether, the solutions at \
small  $ epsilon$  and large  $ epsilon$  are  $ boxed{\\frac{0.890898718140339}{\\epsilon^{0.833333333333333}}, \
\\frac{0.910006870081735}{\\epsilon^{0.947368421052632}}}$ ."