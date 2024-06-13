# Imports
import numpy as np
from sympy import *
from type3 import *
from deduplication import CustomLatexPrinter

custom_printer = CustomLatexPrinter()
init_printing(latex_printer=custom_printer)


def solve_delta_corrected_term(answer, center, validity, poly_eqn, x_var, term_trunc=3, eps_var=None, specific_val_eps=None):

    if term_trunc == 1:
        return ValueError("Need term_trunc to be larger than 1.")

    answer += "\[ \overline{{x}} + \delta =" + latex(center) + "+ \delta \] \n"
    answer += "Substitute this into $P(x)$ for $x$ and equate to $0$: \n"

    delta = symbols('\delta') # delta is the sum of eps terms (expansion)
    poly_delta = poly_eqn.subs(x_var, center + delta) # this is delta subbed back into the original eqn

    answer += "\[" + latex(poly_delta) +"=0. \]"
    answer += "\n We then expand this expression to get \n"

    poly_delta = poly_delta.expand()

    answer += "\[" + latex(poly_delta) + "=0 \] \n "
    answer += "and represent it as a series of $\mathcal{O}"+f"({term_trunc-1})$ in $\delta$, discarding higher order $\delta$ terms \n"

    poly_delta = poly_delta.series(delta, n=term_trunc).removeO() # selects correct number of terms

    answer += "\[" + latex(poly_delta) + "\\approx 0 .\] \n "
    answer += "We can then solve the expression for the correction $\delta$ to $\mathcal{O}"+f"({term_trunc-1})$, and get "

    sol = solve(poly_delta, delta) # solve for delta
    sol = [simplify(d) for d in sol]

    if len(sol) > 1:
        answer += "\[ \delta = " + latex(sol) + " .\] \n "
        answer += f"Note that here we find {len(sol)} solutions for $\delta$ for the root $\overline{{x}} =" + latex(center) + f"$ because we're calculating corrections to "+"$\mathcal{O}"+f"({term_trunc-1})$. "
        answer += "We need to apply the definition $\delta < \overline{x}$ to select the smaller one. "
        answer += f"We do this using our knowledge of the regime of validity for this root—since this root is valid for {validity} $\epsilon$ we select (rounded to two decimal places) "

        # get 2 solutions for delta — one will take you closer to root and other further away
        # need to select the correct delta: use the fact that delta < root approx
        if validity == "small":
            test_eps = 0.0001
        elif validity == "large":
            test_eps = 10000

        if eps_var:
            delta_eval = [d.subs(eps_var, test_eps).evalf() for d in sol]
            delta_correction = min(delta_eval, key=abs)

            # check that it's smaller than the root approx:
            try:
                root_mag = abs(center.subs(eps_var, test_eps)).evalf()
            except:
                root_mag = abs(center)
            if np.abs(delta_correction) < root_mag:
                answer += "\[ \\boxed{ \\delta \\approx" + latex(delta_correction) + ".} \] \n"
            else:
                raise Exception("Cannot calculate corrections.")

    else:
        delta_correction = sol[0] # only option
        answer += "\[ \\boxed{ \\delta \\approx" + latex(delta_correction) + ".} \] \n"

    if specific_val_eps:
        delta_correction = simplify(delta_correction.subs(eps_var, specific_val_eps))

    return delta_correction, answer


def get_delta_corrections(soln_info, poly_eqn, answer, x_var, term_trunc=3, eps_var=None, specific_val_eps=None):
    
    question_type = "polynomial_roots_corrections"
    answer_type = "math_expression_lst"

    question = "Consider the polynomial"
    question += "\[P(x) =" + latex(poly_eqn) + ".\] \n"
    question += "Find approximate expressions for all roots of the polynomial in the limit of small positive $\epsilon$ and large positive $\epsilon$. "
    question += f"Use a series expansion to calculate improved formulae for these roots to order {term_trunc-1} i.e. calculate "+"$\mathcal{O}"+f"({term_trunc-1})$ corrections for each root. "
    
    answer += "We now need to calculate correction terms for these roots to give us better approximations. "
    answer += "We consider the ansatz that the root is given by $\overline{x} + \delta$, "
    answer += "where the correction term $\delta$ is the sum of higher order terms of $\epsilon$ that we initially neglected in our approximation $\overline{x}$. "
    answer += "By definition, $ \delta < \overline{x} .$ \n"

    answer += "We plug this ansatz into the polynomial and perform a series expansion in $\delta$. We keep terms only up to "+"$\mathcal{O}"+f"({term_trunc-1})$ in $\delta$. "
    answer += "Then, we set the expression equal to 0 and solve for $\delta$. \\vspace{1em} \n\n"

    extracted_answer = []

    for i, (validity, roots) in enumerate(soln_info):
        corrections = []

        answer += "\\underline{" +f"Regime {i+1}: valid for {validity} $\epsilon$" + "} \n\n"
        for j, guess in enumerate(roots):
            answer += "\\underline{" + f"Root {j+1}: $" + latex(guess) + "$} \n"
            correction, answer = solve_delta_corrected_term(answer=answer, center=guess,
                                                            validity=validity,
                                                            poly_eqn=poly_eqn, x_var=x_var,
                                                            term_trunc=term_trunc,
                                                            eps_var=eps_var,
                                                            specific_val_eps=specific_val_eps)
            corrections.append(correction)
        
        extracted_answer.append(latex(corrections))
        soln_info[i].append(corrections)

    answer += f"\n\n We have thus found "+"$\mathcal{O}"+f"({term_trunc-1})$ corrections for all {degree(poly_eqn, gen=x_var)} root approximations in both regimes. "
    # soln_info contains (validity, [roots], [corrections])

    # # NOTE: THIS CURRENTLY DOES NOT REPEAT ALL ROOTS, ONLY 3!!!
    # small_roots = []
    # large_roots = []
    # for root in soln_info:
    #     if root[0] == "small":
    #         small_roots.append(root[1][0]+root[2][0])
    #     else:
    #         large_roots.append(root[1][0]+root[2][0])

    # answer += "\[ \\boxed{ \\begin{cases}" + latex(small_roots) + "&\\text{ for small $\epsilon$ }; \\\\ "
    # answer += latex(large_roots) + "&\\text{ for large $\epsilon$: } \\end{cases} } \]"

    return soln_info, question, answer, question_type, answer_type, extracted_answer


# # Sample Usage:

# polynomial = generate_nondimensionalized(10) # generates random polynomial
# x, eps = symbols('x epsilon')

# # implement type 3 functions to solve for roots
# soln_info, q, a, q_type, a_type, extracted_answer = solve_roots(polynomial)
# # soln_info contains (validity, [roots])

# # implement type 4 functions to solve for corrections
# no_corr_terms=2
# soln_info, q, a, q_type, a_type, extracted_answer = get_delta_corrections(soln_info, 
#                                                                           polynomial, a, x, 
#                                                                           eps_var=eps, 
#                                                                           term_trunc=no_corr_terms)
# # soln_info contains (validity, [roots], [corrections])
# print(soln_info)
# print(extracted_answer)