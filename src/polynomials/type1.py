# Imports
import random
import pandas as pd
from sympy import *
from deduplication import *


# Generates two numbers n1, n2 < max_degree where n1 < n2
def generate_n1n2(max_degree):
    """
    Inputs:
    max_degree (int): Maximum possible degree of polynomial

    Outputs:
    n1 (int): Degree of polynomial
    n2 (int): Second largest power of polynomial
    """
    n2 = random.randint(1, max_degree - 1)
    n1 = random.randint(n2 + 1, max_degree)
    return n1, n2


# Solves nondimensionalization problem given n1, n2
def nondimensionalize_polynomial1(n1, n2, eval=False, existing_col_name='Question'):
    """
    Inputs:
    n1 (int): Degree of polynomial
    n2 (int): Second largest power of polynomial

    Outputs:
    question (string): Latex for problem
    answer (string): Latex for answer
    question_type (string) = type of problem (question)
    answer_type (string) = type of solution (answer)
    """
    # Define sympy symbols
    x, y, a1, a2, a3, epsilon = symbols('x y a_1 a_2 a_3 epsilon')

    # Generate sympy polynomial a1*x^n1 + a2*x^n2 + a3
    n1r, n2r = Rational(n1), Rational(n2)
    polynomial_x = a1 * x**n1r + a2 * x**n2r + a3

    # Check whether we already have this question
    if eval is not False:
        data = pd.read_excel(eval)
        if q_exists(latex(polynomial_x), data, existing_col_name):
            return
    
    # Define x = (a/b)y
    x_sub = ((a3/a2)**Rational(1/n2r)) * y

    # Substitute
    polynomial_y = polynomial_x.subs(x, x_sub).expand()
    # polynomial_y = polynomial_y.subs(x, y).expand()

    # Simplify before dividing by a3
    simplified_polynomial = polynomial_y / a3

    # Further simplify the expression
    final_simplified_polynomial = simplify(simplified_polynomial)

    # Get epsilon
    epsilon_value = list(final_simplified_polynomial.expand().args)[::-1][0] / (y**n1r)

    # Return question and answer
    question = ""
    answer = ""
    question_type = "nondimensionalization_symbolic"
    answer_type = "math_expression"

    question += "Nondimensionalize the polynomial"
    question += "\[" + latex(polynomial_x) + "\]"
    question += f"into one of the form $\\epsilon y^{{{n1}}} + y^{{{n2}}} + 1. $"
    question += "Express $\\epsilon$ as a function of $a_1$, $a_2$, and $a_3.$"

    answer += "We begin with the substitution"
    answer += "\[" + "x=" + latex(x_sub) + ".\]"

    answer += "\nThis gives the expression"
    answer += "\[" + latex(polynomial_y) + ".\]"

    answer += "\nDividing by the constant $a_3$ leaves us with the nondimensionalized polynomial with coefficients in terms of $a_1$, $a_2$, and $a_3$:"
    answer += "\[ \\boxed{" + latex(final_simplified_polynomial) + ".}\]"

    answer += "By inspection, we can see that"
    answer += "\[ \\boxed{\epsilon=" + latex(epsilon_value) + ".}\]"

    extracted_answer = "$$ \\boxed{\epsilon=" + latex(epsilon_value) + "} $$"

    return question, answer, question_type, answer_type, extracted_answer


# # Sample Usage:
# n1, n2 = generate_n1n2(max_degree=25)
# eval_path = 'data/train/small_batch_examples/polynomial_type_1_100.xlsx'
# res = nondimensionalize_polynomial1(n1, n2, eval=eval_path)
# if res is not None:
#     question, answer, question_type, answer_type, extracted_answer = res
#     print(question)
# else: 
#     print('Failed to generate unique question. Please try again.')