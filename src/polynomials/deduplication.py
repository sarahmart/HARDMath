import re
import numpy as np
from sympy import *
from sympy.printing.latex import LatexPrinter


# Define a LatexPrinter class to fix printing / representation issues
class CustomLatexPrinter(LatexPrinter):
    
    def _print_Float(self, expr):
        if isinstance(expr, Complex):
            real_part = expr.as_real_imag()[0].evalf()
            imag_part = expr.as_real_imag()[1].evalf()
            return f"({real_part:.2f} + {imag_part:.2f}i)"
        elif isinstance(expr, Float):
            return f"{expr.evalf():.2f}"
        else:
            return super()._print_Float(expr)

    def _print_ImaginaryUnit(self, expr):
        return 'i' 

    def _print_Pow(self, expr):
        # Handle powers
        base_str = self._print(expr.base)
        exp_str = self._print(expr.exp)
        if expr.exp.is_Integer and expr.exp < 0:
            return fr'\frac{{1}}{{{base_str}^{{{-exp_str}}}}}'
        else:
            return f'{base_str}^{{{exp_str}}}'

    def _print_Rational(self, expr):
        # Print rational numbers as fractions
        if expr.q == 1:
            return f'{expr.p}'
        else:
            return fr'\frac{{{self._print(expr.p)}}}{{{self._print(expr.q)}}}'

    def _print_Mul(self, expr):
        # Simplify multiplication
        args = expr.as_ordered_factors()
        num_args = len(args)

        # Special case for -1 as first factor
        if num_args > 1 and args[0] == Integer(-1):
            return f'-{self._print(expr.args_cnc()[0][1])}'

        return ' '.join([self._print(arg) for arg in args])

    def _print_Add(self, expr):
        # Simplify addition
        terms = expr.as_ordered_terms()
        return ' + '.join([self._print(term) for term in terms])


# # Function to extract the polynomial from a question

# def extract_polynomial(question):
#     # Modified regular expression to extract the polynomial
#     match = re.search(r'\\\[(.*?)\\\]', question) # re.search not working ! 
#     if match:
#         return match.group(1).strip()
#     return None

def extract_polynomial(question):
    # Find the index of '\[' and '\]' characters
    start_index = question.find('\\[')
    end_index = question.find('\\]')
    
    # Check if both '\[' and '\]' are found
    if start_index != -1 and end_index != -1:
        # Extract the substring between '\[' and '\]'
        polynomial = question[start_index + 2:end_index].strip()
        
        # Remove the 'P(x) =' part
        if polynomial.startswith('P(x) ='):
            polynomial = polynomial[len('P(x) ='):].strip()
        
        # Remove full stop at end
        if polynomial.endswith('.'):
            polynomial = polynomial[:-1].strip()
        
        # Escape sequences
        polynomial = polynomial.replace('\\\\', '\\')
        
        return polynomial
    return None


def normalize_polynomial(poly):
    # Remove leading/trailing whitespace and other redundant chars
    poly = poly.strip().rstrip('.')
    # Normalize \\ vs \ 
    poly = poly.replace('\\', '\\\\')
    return poly


def q_exists(new_poly, existing_data, existing_col_name='Question'):
    
    new_poly = normalize_polynomial(new_poly)

    existing_polys = set(existing_data[existing_col_name].apply(extract_polynomial).dropna())
    normalized_existing_polys = {normalize_polynomial(poly) for poly in existing_polys}

    # Check if polynomial already exists (T/F)
    return new_poly in normalized_existing_polys


def round_numbers_in_string(input_string):
    rounded_string = []
    i = 0
    n = len(input_string)

    while i < n:
        if input_string[i].isdigit() or (input_string[i] == '.' and i + 1 < n and input_string[i + 1].isdigit()):
            start = i
            # Find the end of the numeric sequence
            while i < n and (input_string[i].isdigit() or input_string[i] == '.' or input_string[i].lower() == 'e'):
                i += 1
            # Extract and round the numeric sequence
            number_str = input_string[start:i]
            try:
                number = float(number_str)
                rounded_number = round(number, 2)
                rounded_string.append(f"{rounded_number:.2f}")
            except ValueError:
                rounded_string.append(number_str)  # If conversion fails, keep original string
        else:
            rounded_string.append(input_string[i])
            i += 1

    return ''.join(rounded_string)

# # Sample Usage:
# for i in range(len(all_data)): 
#     all_data.loc[i,'solution']=round_numbers_in_string(all_data.loc[i, 'solution'])
#     all_data.loc[i,'extracted_answer']=round_numbers_in_string(all_data.loc[i,'extracted_answer'])