# Imports
import random
import pandas as pd
from sympy import *
from deduplication import *
from deduplication import CustomLatexPrinter

custom_printer = CustomLatexPrinter()
init_printing(latex_printer=custom_printer)


# Generates nondimensionalized polynomial of the form described above
def generate_nondimensionalized(max_n1):
    """
    Inputs:
    max_n1 (int): Maximum power in polynomial

    Outputs:
    polynomial (sympy expression): Nondimensionalized random polynomial of the given format
    """
    # Ensure max_n1 is at least 2
    if max_n1 < 2:
        raise ValueError("max_n1 must be at least 2")

    # Randomly choose n1 and n2
    n1 = random.randint(2, max_n1)
    n2 = random.randint(1, n1 - 1)
    # Randomly choose signs
    signs = random.choices([-1, 1], k=2)

    # Construct polynomial, let first term always be + since same as negating if negative
    x = symbols('x')
    epsilon = symbols('epsilon')
    polynomial = epsilon * x**n1 + signs[0] * x**n2 + signs[1]

    # Return
    return polynomial


# Function to solve for roots of nondimensionalized polynomial
def solve_roots(polynomial):
    """
    Inputs:
    polynomial (sympy expression): nondimensionalized polynomial

    Outputs:
    question (string): Latex for problem
    answer (string): Latex for answer
    """
    # Extract terms and solve
    x, epsilon = symbols('x epsilon')
    terms = list(polynomial.expand().args)[::-1]
    A, B, C = terms[0], terms[1], terms[2]
    sol_ab = [simplify(sol) for sol in solve(A + B, x)]
    sol_bc = [simplify(sol) for sol in solve(B + C, x)]
    sol_ac = [simplify(sol) for sol in solve(A + C, x)]

    # Remove extraneous root 0 that shows up - bc it never occurs in this problem formulation
    def remove_zeros(sol_list):
        # Helper function to remove zeros
        while 0 in sol_list:
            sol_list.remove(0)
    remove_zeros(sol_ab)
    remove_zeros(sol_bc)
    remove_zeros(sol_ac)

    # Check dominant balances to see if roots belong to small or large epsilon regimes
    AB_valid_small_eps = (abs(A.subs(x, sol_ab[0]).subs(epsilon, 0.0001)) > abs(C.subs(x, sol_ab[0]).subs(epsilon, 0.001))) # A,B >> C small eps
    AB_valid_large_eps = (abs(A.subs(x, sol_ab[0]).subs(epsilon, 10000)) > abs(C.subs(x, sol_ab[0]).subs(epsilon, 1000))) # A,B >> C large eps
    AB_validity = "small" if AB_valid_small_eps else "large"

    BC_valid_small_eps = (abs(B.subs(x, sol_bc[0]).subs(epsilon, 0.0001)) > abs(A.subs(x, sol_bc[0]).subs(epsilon, 0.001))) # B,C >> A small eps
    BC_valid_large_eps = (abs(B.subs(x, sol_bc[0]).subs(epsilon, 10000)) > abs(A.subs(x, sol_bc[0]).subs(epsilon, 1000))) # B,C >> A large eps
    BC_validity = "small" if BC_valid_small_eps else "large"

    AC_valid_small_eps = (abs(A.subs(x, sol_ac[0]).subs(epsilon, 0.0001)) > abs(B.subs(x, sol_ac[0]).subs(epsilon, 0.001))) # A,C >> B small eps
    AC_valid_large_eps = (abs(A.subs(x, sol_ac[0]).subs(epsilon, 10000)) > abs(B.subs(x, sol_ac[0]).subs(epsilon, 1000))) # A,C >> B large eps
    AC_validity = "small" if AC_valid_small_eps else "large"

    # Return answers
    question = ""
    answer = ""
    question_type = "polynomial_roots"
    answer_type = "math_expression_lst"

    question += "Consider the polynomial"
    question += "\[P(x) =" + latex(polynomial) + ".\] \n"
    question += "Find first order approximations for all roots of the polynomial in the limit of small positive $\\epsilon$ and large positive $\\epsilon$. "

    answer += "We begin by equating the polynomial to zero to solve for the roots: $P(x) = 0.$ "
    answer += "This problem can be rewritten in the form $A+B+C=0$, where: "
    answer += "$A=" + latex(A) + ";$ "
    answer += "$B=" + latex(B) + ";$ "
    answer += "$C=" + latex(C) + ".$"

    answer += "\n\nWe find approximate solutions to the roots by considering the three possible dominant balances. "
    answer += "For each dominant balance, we find the roots of the resulting equation and evaluate whether each balance is self-consistent for small or large positive $\epsilon$. "
    answer += "\\vspace{1em}"

    answer += "\n\nWe start with the balance $A+B=0$, assuming that $|C|$ is negligible when compared to $|A|$ and $|B|$. "
    answer += "Solving this for $x$ in terms of $\\epsilon$ then gives us "
    answer += f"{len(sol_ab)} non-zero {'root' if len(sol_ab) == 1 else 'roots'}: "
    answer += "\n\[" + latex(A+B) + "=0 \]"
    answer += "\[ \implies \\boxed{ x=" + latex(sol_ab) + ".}\]"
    answer += "\nTo verify that these roots are consistent with the assumption that $|A|, |B| \gg |C|,$ we substitute these found roots back into the terms $A$, $B$, and $C$ and compare their magnitudes. "
    answer += "Using this method, we find that "
    answer += f"it is {str(AB_valid_small_eps).lower()} that these roots are valid for small $\\epsilon$, "
    answer += f"while validity for large $\\epsilon$ is {str(AB_valid_large_eps).lower()}."
    answer += f"\n\n\\underline{{Therefore, these roots are valid in the limit of {AB_validity} positive $\\epsilon$ only.}}"
    answer += "\\vspace{1em}"

    answer += "\n\nNext we examine the balance $B+C=0$, assuming that $|A|$ is negligible when compared to $|B|$ and $|C|$. "
    answer += "Solving this for $x$ in terms of $\\epsilon$ gives us "
    answer += f"{len(sol_bc)} non-zero {'root' if len(sol_bc) == 1 else 'roots'}: "
    answer += "\[" + latex(B+C) + "=0\]"
    answer += "\[ \implies\\boxed{ x=" + latex(sol_bc) + ".}\]"
    answer += "\nTo verify that these roots are consistent with the assumption that $|B|, |C| \gg |A|,$ we substitute these found roots back into $A$, $B$, and $C$ and compare their magnitudes. "
    answer += "Using this method, we find that "
    answer += f"it is {str(BC_valid_small_eps).lower()} that these roots are valid for small $\\epsilon$, "
    answer += f"while validity for large $\\epsilon$ is {str(BC_valid_large_eps).lower()}."
    answer += f"\n\n\\underline{{Therefore, these roots are valid in the limit of {BC_validity} positive $\\epsilon$ only.}}"
    answer += "\\vspace{1em}"

    answer += "\n\nFinally, we examine the balance $A+C=0$, assuming that $|B|$ is negligible when compared to $|A|$ and $|C|$. "
    answer += "Solving this for $x$ in terms of $\\epsilon$ gives us "
    answer += f"{len(sol_ac)} non-zero {'root' if len(sol_ac) == 1 else 'roots'}: "
    answer += "\[" + latex(A+C) + "=0\]"
    answer += "\[ \implies\\boxed{ x=" + latex(sol_ac) + ".}\]"
    answer += "\nTo verify that these roots are consistent with the assumption that $|A|, |C| \gg |B|,$ we substitute these found roots back into $A$, $B$, and $C$ and compare their magnitudes. "
    answer += "Using this method, we find that "
    answer += f"it is {str(AC_valid_small_eps).lower()} that these roots are valid for small $\\epsilon$, "
    answer += f"while validity for large $\\epsilon$ is {str(AC_valid_large_eps).lower()}."
    answer += f"\n\n\\underline{{Therefore, these roots are valid in the limit of {AC_validity} positive $\\epsilon$ only.}}"
    answer += "\\vspace{1em}"

    deg = (len(sol_ab) + len(sol_bc) + len(sol_ac))/2

    answer += f"\n\nBy the Fundamental Theorem of Algebra, a polynomial of degree {int(deg)} has exactly {int(deg)} roots."
    answer += f" We have found {int(deg)} roots that are valid in the limit of small positive $\\epsilon$ "
    answer += f"and {int(deg)} roots valid in the limit of large positive $\\epsilon$. "
    answer += "Our method therefore provides a complete solution to the problem, finding the correct number of roots in each $\\epsilon$ regime. \n\n"

    if len(sol_ab) == deg:
        answer += "The roots of $P(x)$ for " + AB_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_ab) + "} \]"
        answer += "and the roots of $P(x)$ for " + AC_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_bc+sol_bc) + "} \]"
        extracted_answer = "$$\\boxed{" + latex(sol_ab) + ", " + latex(sol_bc+sol_bc) + "}\]$$"
    elif len(sol_bc) == deg:
        answer += "The roots of $P(x)$ for " + BC_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_bc) + "} \]"
        answer += "and the roots of $P(x)$ for " + AC_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_ab+sol_ac) + "} \]"
        extracted_answer = "$$\\boxed{" + latex(sol_bc) + ", " + latex(sol_ab+sol_ac) + "}\]$$"
    elif len(sol_ac) == deg:
        answer += "The roots of $P(x)$ for " + AC_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_ac) + "} \]"
        answer += "and the roots of $P(x)$ for " + AB_validity + " positive $\\epsilon$ are"
        answer += "\[ \\boxed{ " + latex(sol_ab+sol_bc) + "} \]"
        extracted_answer = "$$\\boxed{" + latex(sol_ac) + ", " + latex(sol_ab+sol_bc) + "}\]$$"

    return [[AB_validity, sol_ab], [BC_validity, sol_bc], [AC_validity, sol_ac]], question, answer, question_type, answer_type, extracted_answer


# # Sample Usage:

# # check against existing set:
# eval_path = 'data/train/small_batch_examples/polynomial_type_3_100.xlsx'
# data = pd.read_excel(eval_path)

# while True:
#     polynomial = generate_nondimensionalized(10) # generates a random polynomial of max degree 10

#     if q_exists(latex(polynomial), data):
#         print('Question already exists in eval set. Generating again.')
#         continue
    
#     x, eps = symbols('x epsilon')
#     soln_info, q, a, q_type, a_type, extracted_answer = solve_roots(polynomial)
#     break

# # soln_info contains (validity, [analytic root expressions])
# print(extracted_answer)