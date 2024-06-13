# Imports
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from sympy import *


x, eps = symbols('x epsilon')


# helper function to find the closest analytical root to the actual numerical root
def find_closest(num, list):
    return min(list, key=lambda x: np.abs(complex(*x) - num))


# helper function to calculate the errors between the analytical and numerical roots
def compare(num_roots, ana_roots):
    relative_errors = []
    for num_root in num_roots:
        closest = find_closest(num_root, ana_roots)
        error = np.abs(num_root - complex(*closest))
        if np.abs(num_root) != 0:
            relative_error = error / np.abs(num_root)
            relative_errors.append(relative_error)
    return relative_errors


# function to check root validity of analytical against numerical roots
def check_roots(soln_info, polynomial, x_var=x, eps_var=eps, corr=True):
  '''x_var and eps_var should be Sympy symbols,
  use corr=False to skip checking corrections (for Problem Type 3)'''

  all_ana_small = []
  all_ana_large = []
  if corr: 
      all_corr_small = []
      all_corr_large = []
      

  # evaluate analytical roots and corrections at correct eps
  for regime in soln_info:
    
    if corr:
        # regime is a lst [validity, [root_approx], [deltas]]
        validity, ana_roots, deltas = regime
    else:
        validity, ana_roots = regime

    ana_roots = [simplify(root) for root in ana_roots]

    if validity == "small":
      eps_value = 0.01

      ana_roots_eval = [N(root.subs(eps_var, eps_value)) for root in ana_roots]
      ana_roots_real = [complex(root).real for root in ana_roots_eval]
      ana_roots_imag = [complex(root).imag for root in ana_roots_eval]
      [all_ana_small.append((re, im)) for re, im in zip(ana_roots_real, ana_roots_imag)]
      
      if corr:
        corrections = [N(delta.subs(eps_var, eps_value)) for delta in deltas]
        corr_ana_roots = [root + delta for root, delta in zip(ana_roots_eval, corrections)]
        corr_roots_real = [complex(root).real for root in corr_ana_roots]
        corr_roots_imag = [complex(root).imag for root in corr_ana_roots]
        [all_corr_small.append((re, im)) for re, im in zip(corr_roots_real, corr_roots_imag)]

    elif validity == "large":
      eps_value = 100

      ana_roots_eval = [N(root.subs(eps_var, eps_value)) for root in ana_roots]
      ana_roots_real = [complex(root).real for root in ana_roots_eval]
      ana_roots_imag = [complex(root).imag for root in ana_roots_eval]
      [all_ana_large.append((re, im)) for re, im in zip(ana_roots_real, ana_roots_imag)]
      
      if corr:
        corrections = [N(delta.subs(eps_var, eps_value)) for delta in deltas]
        corr_ana_roots = [root + delta for root, delta in zip(ana_roots_eval, corrections)]
        corr_roots_real = [complex(root).real for root in corr_ana_roots]
        corr_roots_imag = [complex(root).imag for root in corr_ana_roots]
        [all_corr_large.append((re, im)) for re, im in zip(corr_roots_real, corr_roots_imag)]

  # small numeric
  eps_value = 0.01
  poly = polynomial.subs(eps_var, eps_value)
  poly_obj = Poly(poly, x)
  coefficients = poly_obj.all_coeffs()
  num_roots_small = np.roots(coefficients)

  # large numeric
  eps_value = 100
  poly = polynomial.subs(eps_var, eps_value)
  poly_obj = Poly(poly, x)
  coefficients = poly_obj.all_coeffs()
  num_roots_large = np.roots(coefficients)

  # now the 'all' lists contain all analytic values, and num lists contain all numeric
  # compare: find closest roots
  as_errs = compare(num_roots_small, all_ana_small)
  al_errs = compare(num_roots_large, all_ana_large)

  threshold = 0.1 # accept approximations that are off by up to 10\% of the actual value — "close enough"
  as_good = max(as_errs) <= threshold
  al_good = max(al_errs) <= threshold

  if corr:
    cs_errs = compare(num_roots_small, all_corr_small)
    cl_errs = compare(num_roots_large, all_corr_large)
    cs_good = max(cs_errs) <= threshold
    cl_good = max(cl_errs) <= threshold
    
    good_approx = as_good and cs_good and al_good and cl_good
    good_corr = (np.mean(cs_errs) < np.mean(as_errs)) and (np.mean(cl_errs) < np.mean(al_errs))

    return good_approx, good_corr, [[num_roots_small, all_ana_small, all_corr_small],
                                    [num_roots_large, all_ana_large, all_corr_large]]
  else:
    good_approx = as_good and al_good
    return good_approx, [[num_roots_small, all_ana_small],
                         [num_roots_large, all_ana_large]]


def code_block_generator(answer, polynomial, soln_info, x_var=x, eps_var=eps):

    answer += "\n\n Now let's verify our analytical solutions, along with their correction terms, against numerical solutions.\n\n"

    answer += """\n\n \\textbf{Code Block Content:}\n\n"""
    answer += """\\begin{verbatim}
    # helper function to find the closest analytical root to the actual numerical root
    def find_closest(num, list):
        return min(list, key=lambda x: np.abs(complex(*x) - num))


    # helper function to calculate the errors between the analytical and numerical roots
    def compare(num_roots, ana_roots):
        relative_errors = []
        for num_root in num_roots:
            closest = find_closest(num_root, ana_roots)
            error = np.abs(num_root - complex(*closest))
            if np.abs(num_root) != 0:
                relative_error = error / np.abs(num_root)
                relative_errors.append(relative_error)
        return relative_errors


    # function to check root validity of analytical against numerical roots
    def check_roots(soln_info, polynomial, x_var=x, eps_var=eps, corr=True):
    '''x_var and eps_var should be Sympy symbols,
    use corr=False to skip checking corrections (for Problem Type 3)'''

    all_ana_small = []
    all_ana_large = []
    if corr: 
        all_corr_small = []
        all_corr_large = []
        

    # evaluate analytical roots and corrections at correct eps
    for regime in soln_info:
        
        if corr:
            # regime is a lst [validity, [root_approx], [deltas]]
            validity, ana_roots, deltas = regime
        else:
            validity, ana_roots = regime

        ana_roots = [simplify(root) for root in ana_roots]

        if validity == "small":
        eps_value = 0.1

        ana_roots_eval = [N(root.subs(eps_var, eps_value)) for root in ana_roots]
        ana_roots_real = [complex(root).real for root in ana_roots_eval]
        ana_roots_imag = [complex(root).imag for root in ana_roots_eval]
        [all_ana_small.append((re, im)) for re, im in zip(ana_roots_real, ana_roots_imag)]
        
        if corr:
            corrections = [N(delta.subs(eps_var, eps_value)) for delta in deltas]
            corr_ana_roots = [root + delta for root, delta in zip(ana_roots_eval, corrections)]
            corr_roots_real = [complex(root).real for root in corr_ana_roots]
            corr_roots_imag = [complex(root).imag for root in corr_ana_roots]
            [all_corr_small.append((re, im)) for re, im in zip(corr_roots_real, corr_roots_imag)]

        elif validity == "large":
        eps_value = 10

        ana_roots_eval = [N(root.subs(eps_var, eps_value)) for root in ana_roots]
        ana_roots_real = [complex(root).real for root in ana_roots_eval]
        ana_roots_imag = [complex(root).imag for root in ana_roots_eval]
        [all_ana_large.append((re, im)) for re, im in zip(ana_roots_real, ana_roots_imag)]
        
        if corr:
            corrections = [N(delta.subs(eps_var, eps_value)) for delta in deltas]
            corr_ana_roots = [root + delta for root, delta in zip(ana_roots_eval, corrections)]
            corr_roots_real = [complex(root).real for root in corr_ana_roots]
            corr_roots_imag = [complex(root).imag for root in corr_ana_roots]
            [all_corr_large.append((re, im)) for re, im in zip(corr_roots_real, corr_roots_imag)]

    # small numeric
    eps_value = 0.1
    poly = polynomial.subs(eps_var, eps_value)
    poly_obj = Poly(poly, x)
    coefficients = poly_obj.all_coeffs()
    num_roots_small = np.roots(coefficients)

    # large numeric
    eps_value = 10
    poly = polynomial.subs(eps_var, eps_value)
    poly_obj = Poly(poly, x)
    coefficients = poly_obj.all_coeffs()
    num_roots_large = np.roots(coefficients)

    # now the 'all' lists contain all analytic values, and num lists contain all numeric
    # compare: find closest roots
    as_errs = compare(num_roots_small, all_ana_small)
    al_errs = compare(num_roots_large, all_ana_large)

    threshold = 0.1 # accept approximations that are off by up to 10\% of the actual value — "close enough"
    as_good = max(as_errs) < threshold
    al_good = max(al_errs) < threshold

    if corr:
        cs_errs = compare(num_roots_small, all_corr_small)
        cl_errs = compare(num_roots_large, all_corr_large)
        cs_good = max(cs_errs) < threshold
        cl_good = max(cl_errs) < threshold
        
        good_approx = as_good and cs_good and al_good and cl_good
        good_corr = (np.mean(cs_errs) < np.mean(as_errs)) and (np.mean(cl_errs) < np.mean(al_errs))

        return good_approx, good_corr, [[num_roots_small, all_ana_small, all_corr_small],
                                        [num_roots_large, all_ana_large, all_corr_large]]
    else:
        good_approx = as_good and al_good
        return good_approx, [[num_roots_small, all_ana_small],
                            [num_roots_large, all_ana_large]]
    """

    answer += f"""
    # Define the relevant variables
    x, eps = symbols('x epsilon')

    # Define the polynomial
    polynomial = {polynomial}

    """

    answer += f"""
    # Define the analytical solutions already found
    # soln_info contains [validity, [roots], [corrections]]
    soln_info = {soln_info}

    """

    answer += """
    # Call the function to check the validity of our analytical roots against the numerical roots for this polynomial
    good_approx, good_corr, root_to_plot = check_roots(soln_info, polynomial, a)

    # Execution result --> for the execution block
    (good_approx & good_corr)

    """

    answer += """\\end{verbatim} \n\n"""

    return answer


def plot_root_corr(roots_to_plot, polynomial):
    num_roots_small, all_ana_small, all_corr_small = roots_to_plot[0]
    num_roots_large, all_ana_large, all_corr_large = roots_to_plot[1]

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].scatter(np.real(num_roots_small), np.imag(num_roots_small),
                   c='lightblue', s=120, zorder=0)
    axs[0].scatter([root[0] for root in  all_ana_small], [root[1] for root in  all_ana_small],
                   c='orange', zorder=1, s=80)
    axs[0].scatter([root[0] for root in  all_corr_small], [root[1] for root in  all_corr_small],
                   edgecolors='purple', facecolors='none', zorder=2, s=80)

    axs[1].scatter(np.real(num_roots_large), np.imag(num_roots_large),
                   c='lightblue', s=120, zorder=0, label="numeric roots")
    axs[1].scatter([root[0] for root in  all_ana_large], [root[1] for root in  all_ana_large],
                   c='orange', zorder=1, s=80, label="analytic roots")
    axs[1].scatter([root[0] for root in  all_corr_large], [root[1] for root in  all_corr_large],
                   edgecolors='purple', facecolors='none', zorder=2, s=80,
                   label='corrected analytic roots')

    axs[1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    axs[0].set_xlabel("Re($x^*$)")
    axs[0].set_ylabel("Im($x^*$)")
    axs[0].set_title("Roots for small $\epsilon = 0.001$")
    axs[1].set_xlabel("Re($x^*$)")
    axs[1].set_title("Roots for large $\epsilon = 1000$")
    plt.suptitle("Comparison of analytic and numerical roots of $P(x)=" + latex(polynomial) + "$.")
    plt.savefig("verifications_1st_order.png")
    plt.show()
    return


def plot_roots(polynomial, soln_info, x_var=x, eps_var=eps):

    fig = plt.Figure(figsize=(16, 4))

    poly_coeffs = Poly(polynomial, x_var).all_coeffs()
    poly_coeffs.pop(0)

    eps_list = [pow(10, eps) for eps in np.linspace(-2, 3, 500)] # all eps
    y_num_all = np.array([np.roots([epsilon]+poly_coeffs) for epsilon in eps_list])

    eps_mat = np.array(eps_list)[:, None].repeat(len(poly_coeffs), axis=1)
    plt.scatter(np.real(y_num_all), np.imag(y_num_all), s=35, cmap='Blues', c=eps_mat, vmin=10^(-4), vmax=10^7)

    eps_small = np.array(eps_list[:int(len(eps_list)/4)])
    eps_large = np.array(eps_list[-int(len(eps_list)/3):])

    for i, (validity, roots, corrections) in enumerate(soln_info):

        if validity == "small":
            for root, corr in zip(roots, corrections):
                root_func = lambdify(eps, root, "numpy")
                corr_func = lambdify(eps, corr, "numpy")

                small_roots_real = np.real(root_func(eps_small))
                small_roots_imag = np.imag(root_func(eps_small))
                plt.scatter(small_roots_real, small_roots_imag, s=1, color='#8fce00')

                delta_re = np.real(corr_func(eps_small))
                delta_im = np.imag(corr_func(eps_small))
                plt.scatter(small_roots_real+delta_re, small_roots_imag+delta_im,
                            s=1, color='purple')

        else:
            for root, corr in zip(roots, corrections):
                large_roots_real = [re(root.subs(eps, eps_val)) for eps_val in eps_large]
                large_roots_imag = [im(root.subs(eps, eps_val)) for eps_val in eps_large]
                plt.scatter(large_roots_real, large_roots_imag, s=1, color='pink')

                delta_re = [re(corr.subs(eps, eps_val)) for eps_val in eps_large]
                delta_im = [im(corr.subs(eps, eps_val)) for eps_val in eps_large]
                plt.scatter(large_roots_real+delta_re, large_roots_imag+delta_im,
                            s=1, color='orange')

    labels = ['numerical solutions, coloured by $\epsilon$',
              'analytical solutions for small $\epsilon$',
              'corrected solutions for small $\epsilon$',
              'analytical solutions for large $\epsilon$',
              'corrected solutions for large $\epsilon$']
    num = Patch(color='#6ca9e0')
    ana_small = Patch(color='#8fce00')
    corr_small = Patch(color='purple')
    ana_large = Patch(color='pink')
    corr_large = Patch(color='darkorange')
    plt.legend([num, ana_small, corr_small, ana_large, corr_large], labels,
               bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel("Re($x^*$)")
    plt.ylabel("Im($x^*$)")
    plt.title("All roots of $P(x)$ plotted on the complex plane.")
    plt.savefig("all_eps_plot.png")
    plt.show()


def verification_plot_code_block_generator(roots_to_plot, answer):

    answer += """Finally, let's generate some sample code as a visual sanity check for our analytical solution."""

    answer += """\\begin{verbatim} \n\n
    # Define a function to plot the roots and corrections for small and large epsilon values
    def plot_root_corr(roots_to_plot, polynomial):
      num_roots_small, all_ana_small, all_corr_small = roots_to_plot[0]
      num_roots_large, all_ana_large, all_corr_large = roots_to_plot[1]

      fig, axs = plt.subplots(1, 2, figsize=(10, 5))

      axs[0].scatter(np.real(num_roots_small), np.imag(num_roots_small),
                    c='lightblue', s=120, zorder=0)
      axs[0].scatter([root[0] for root in  all_ana_small], [root[1] for root in  all_ana_small],
                    c='orange', zorder=1, s=80)
      axs[0].scatter([root[0] for root in  all_corr_small], [root[1] for root in  all_corr_small],
                    edgecolors='purple', facecolors='none', zorder=2, s=80)

      axs[1].scatter(np.real(num_roots_large), np.imag(num_roots_large),
                    c='lightblue', s=120, zorder=0, label="numeric roots")
      axs[1].scatter([root[0] for root in  all_ana_large], [root[1] for root in  all_ana_large],
                    c='orange', zorder=1, s=80, label="analytic roots")
      axs[1].scatter([root[0] for root in  all_corr_large], [root[1] for root in  all_corr_large],
                    edgecolors='purple', facecolors='none', zorder=2, s=80,
                    label='corrected analytic roots')

      axs[1].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

      axs[0].set_xlabel("Re($x^*$)")
      axs[0].set_ylabel("Im($x^*$)")
      axs[0].set_title("Roots for small $\epsilon = 0.001$")
      axs[1].set_xlabel("Re($x^*$)")
      axs[1].set_title("Roots for large $\epsilon = 1000$")
      plt.suptitle("Comparison of analytic and numerical roots of $P(x)=" + latex(polynomial) + "$.")
      plt.show()
      plt.close()
      return

    """

    answer += """\\end{verbatim} \n\n"""
    answer += """You can call this function using our previously defined polynomial and \\texttt{soln\_info:}"""

    answer += """\\begin{verbatim}
    plot_roots(polynomial, soln_info)
    \\end{verbatim}\n\n
    """

    answer += """We can also write a function to plot the roots for various $\epislon$ values:"""

    answer += """\\begin{verbatim}
    def plot_roots(polynomial, soln_info, x_var=x, eps_var=eps):

      fig = plt.Figure(figsize=(16, 4))

      poly_coeffs = Poly(polynomial, x_var).all_coeffs()
      poly_coeffs.pop(0)

      eps_list = [pow(10, eps) for eps in np.linspace(-2, 3, 500)] # all eps
      y_num_all = np.array([np.roots([epsilon]+poly_coeffs) for epsilon in eps_list])

      eps_mat = np.array(eps_list)[:, None].repeat(len(poly_coeffs), axis=1)
      plt.scatter(np.real(y_num_all), np.imag(y_num_all), s=35, cmap='Blues', c=eps_mat, vmin=10^(-4), vmax=10^7)

      eps_small = np.array(eps_list[:int(len(eps_list)/4)])
      eps_large = np.array(eps_list[-int(len(eps_list)/3):])

      for i, (validity, roots, corrections) in enumerate(soln_info):

          if validity == "small":
              for root, corr in zip(roots, corrections):
                  root_func = lambdify(eps, root, "numpy")
                  corr_func = lambdify(eps, corr, "numpy")

                  small_roots_real = np.real(root_func(eps_small))
                  small_roots_imag = np.imag(root_func(eps_small))
                  plt.scatter(small_roots_real, small_roots_imag, s=1, color='#8fce00')

                  delta_re = np.real(corr_func(eps_small))
                  delta_im = np.imag(corr_func(eps_small))
                  plt.scatter(small_roots_real+delta_re, small_roots_imag+delta_im,
                              s=1, color='purple')

          else:
              for root, corr in zip(roots, corrections):
                  large_roots_real = [re(root.subs(eps, eps_val)) for eps_val in eps_large]
                  large_roots_imag = [im(root.subs(eps, eps_val)) for eps_val in eps_large]
                  plt.scatter(large_roots_real, large_roots_imag, s=1, color='pink')

                  delta_re = [re(corr.subs(eps, eps_val)) for eps_val in eps_large]
                  delta_im = [im(corr.subs(eps, eps_val)) for eps_val in eps_large]
                  plt.scatter(large_roots_real+delta_re, large_roots_imag+delta_im,
                              s=1, color='orange')

      labels = ['numerical solutions, coloured by $\epsilon$',
                'analytical solutions for small $\epsilon$',
                'corrected solutions for small $\epsilon$',
                'analytical solutions for large $\epsilon$',
                'corrected solutions for large $\epsilon$']
      num = Patch(color='#6ca9e0')
      ana_small = Patch(color='#8fce00')
      corr_small = Patch(color='purple')
      ana_large = Patch(color='pink')
      corr_large = Patch(color='darkorange')
      plt.legend([num, ana_small, corr_small, ana_large, corr_large], labels,
                bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
      plt.xlabel("Re($x^*$)")
      plt.ylabel("Im($x^*$)")
      plt.title("All roots of $P(x)$ plotted on the complex plane.")
      plt.show()
      plt.close()
      return

      """

    answer += """\\end{verbatim} \n\n"""
    answer += """We can again call this function using our previously defined variables:"""

    answer += """\\begin{verbatim}
    plot_roots(polynomial, soln_info)
    \\end{verbatim} \n\n
    """

    return answer