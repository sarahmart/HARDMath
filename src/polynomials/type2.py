# Imports
import random
import numpy as np
import pandas as pd
from sympy import * 
from deduplication import *


# Generates a list of coefficients corresponding to a random polynomial
def generate_polynomial(max_degree, num_terms, coeff_bounds):
    """
    Inputs:
    max_degree (int): The maximum degree of the polynomial.
    num_terms (int)
    coeff_bounds (tuple): (lower bound, upper bound)

    Outputs:
    coefficients (list)
    """
    # Initialize array of coeffs
    coefficients = [0] * (max_degree + 1)

    # Check number of terms
    if num_terms > max_degree + 1:
        raise ValueError("Number of terms cannot be more than the degree of the polynomial + 1")
    # Randomly choose positions for the (#) non-zero coefficients
    non_zero_positions = random.sample(range(max_degree), num_terms - 1)

    # Assign random values within the bounds to the chosen positions
    for pos in non_zero_positions:
        # Loop to make sure it is nonzero bc selecting from [-, +] includes 0
        while coefficients[pos] is None or coefficients[pos] == 0:
          coefficients[pos] = random.randint(coeff_bounds[0], coeff_bounds[1])

    # Ensure the highest degree term is non-zero
    if coefficients[-1] == 0:
        # While loop until it is nonzero
        while coefficients[-1] is None or coefficients[-1] == 0:
          coefficients[-1] = random.randint(coeff_bounds[0], coeff_bounds[1])

    return coefficients


# Helper function to convert list of coefficients into a sympy expression
def sympy_polynomial_from_coefficients(coefficients):
    """
    Inputs:
    coefficients (list): A list of coefficients, where the index represents the power of x.

    Outputs:
    polynomial (sympy expression): The polynomial expression.
    """
    x = symbols('x')
    coefficients_reverse = coefficients
    coefficients_reverse.reverse()
    polynomial = sum(coef * x**i for i, coef in enumerate(coefficients_reverse))
    return polynomial


# Solves nondimensionalization problem given coefficients
def nondimensionalize_polynomial2(coefficients):
    """
    Inputs:
    coefficients (list): The list of coefficients

    Outputs:
    question (string): Latex for problem
    answer (string): Latex for answer
    question_type (string) = type of problem (question)
    answer_type (string) = type of solution (answer)
    """

    question = ""
    answer = ""
    question_type = "nondimentionalization_numeric"
    answer_type = "float"

    # Find nonzero coefficients & powers in the format [(coefficient, power)]
    nonzero_coeffs = [(coeff, len(coefficients) - idx - 1) for idx, coeff in enumerate(coefficients) if coeff != 0]
    # Find largest, second largest powers
    sorted_coeffs = sorted(nonzero_coeffs, key=lambda x: x[1], reverse=True)
    n1 = sorted_coeffs[0][1]
    n2 = sorted_coeffs[1][1]
    sign1 = np.sign(nonzero_coeffs[0][0])
    sign2 = np.sign(nonzero_coeffs[1][0])
    sign3 = np.sign(nonzero_coeffs[2][0])
    a1_absvalue = abs(nonzero_coeffs[0][0])
    a2_absvalue = abs(nonzero_coeffs[1][0])
    a3_absvalue = abs(nonzero_coeffs[2][0])

    # Define sympy symbols
    x, y, a1, a2, a3, epsilon = symbols('x y a_1 a_2 a_3 epsilon')

    # Generate sympy polynomial a1*x^n1 + a2*x^n2 + a3
    n1r, n2r = Rational(n1), Rational(n2)
    polynomial_x = sign1*a1 * x**n1r + sign2*a2 * x**n2r + sign3*a3 # included signs

    answer += "For now, we ignore the numeric values of the coefficients and instead call them $a_1, a_2, a_3$. Our polynomial is then:"
    answer += "\[" + latex(polynomial_x) + ".\] "

    # Branching for if first coefficient is negative
    if sign1 < 0:
        polynomial_x *= (-1)
        answer += "\nSince the first coefficient is negative, we multiply the entire expression by -1:"
        answer += "\[" + latex(polynomial_x) + "\]"

    # Define x = (a/b)y
    x_sub = ((a3/a2)**Rational(1/n2r)) * y

    # Substitute
    polynomial_y = polynomial_x.subs(x, x_sub).expand()

    # Simplify before dividing by a3
    simplified_polynomial = polynomial_y / a3

    # Further simplify the expression
    final_simplified_polynomial = simplify(simplified_polynomial)

    # Substitute know values for a1, a2, a3
    final_simplified_polynomial_subs = final_simplified_polynomial.subs([(a1, a1_absvalue), (a2, a2_absvalue), (a3, a3_absvalue)]).simplify()

    # Find value of epsilon
    epsilon_value = list(final_simplified_polynomial_subs.expand().args)[::-1][0] / (y**n1)
    epsilon = simplify(N(epsilon_value.evalf()))

    # Round epsilon to 2 decimal places for display
    try:
        if epsilon.is_real and epsilon.is_number:
            # If epsilon is real
            formatted_eps = f"$$\\boxed{{\\epsilon \\approx{float(epsilon):.2f}}}\\]$$"
        else:
            # If epsilon is complex
            real_part = float(re(epsilon))
            imag_part = float(im(epsilon))
            formatted_eps = f"$$\\boxed{{\\epsilon \\approx{real_part:.2f} {'+' if imag_part >= 0 else '-'} {abs(imag_part):.2f}i}}\\]$$"
    except TypeError:
        # Handle cases where conversion to float fails --> fallback to showing expression
        formatted_eps = f"$$\\boxed{{\\epsilon \\approx {epsilon}}}\\]$$" 

    # Return question and answer
    question += "Nondimensionalize the polynomial \[P(x) = "
    question += latex(sympy_polynomial_from_coefficients(coefficients)) + "\] "
    question += f"into a polynomial of the form $\\epsilon y^{{{n1}}} \pm y^{{{n2}}} \pm 1$. Solve for $\\epsilon$."

    answer += "Using substitution"
    answer += "\[" + "x=" + latex(x_sub) + "\]"

    answer += "\ngives the expression"
    answer += "\[" + latex(polynomial_y) + ".\]"

    answer += "\nDividing all terms by the coefficient remaining in front of the constant term gives us the nondimensionalized polynomial with coefficients in terms of $a_1, a_2, a_3$: "
    answer += "\[" + latex(final_simplified_polynomial) + "\]"

    answer += "\nSubstituting in the known numeric values for $a_1, a_2, a_3$ (using their absolute values as we have already accounted for sign), we get: "
    answer += "\[" + latex(final_simplified_polynomial_subs) + "\]"

    answer += "\nFrom inspection of this nondimensionalized equation, we can now identify $\\epsilon$: "
    answer += "\[ \\epsilon=" + latex(epsilon_value) + "\\implies \\boxed{" + f"\\epsilon \\approx{formatted_eps}" + ".}\]"

    extracted_answer = "$$\\boxed{" + f"\\epsilon \\approx{formatted_eps}" + "}$$"

    return question, answer, question_type, answer_type, extracted_answer


# # Sample Usage:
# coefficients = generate_polynomial(max_degree=10, num_terms=3, coeff_bounds=[-10,10])

# # check against existing set:
# eval_path = 'data/train/small_batch_examples/polynomial_type_2_100.xlsx'
# data = pd.read_excel(eval_path)

# while True:
#     coefficients = generate_polynomial(max_degree=10, num_terms=3, coeff_bounds=[-10, 10])
#     new_poly_latex = latex(sympy_polynomial_from_coefficients(coefficients))

#     if q_exists(new_poly_latex, data):
#         print('Question already exists in eval set. Generating again.')
#         continue
    
#     question, answer, question_type, answer_type, extracted_answer = nondimensionalize_polynomial2(coefficients)
#     break

# # print(question)
# # print(answer)