
import csv
import random
import json
import os
import re
from IPython.display import display, Markdown, Latex
import pandas as pd
import sympy as sp
from sympy import simplify, cos, sin, expand, Eq
from sympy.parsing.latex import parse_latex
from sympy import sympify, N

def display_content(input_str, show_display=True):
    latex_str = input_str.replace(r'\[', ' $').replace(r'\]', '$ ').replace(r'\(', ' $').replace(r'\)', ' $').replace('$\\', ' $').replace('$','$ ')
    if show_display:
        display(Latex(latex_str))
    return latex_str

def convert_to_numbers(string_list):
    result = []
    for num in string_list:
        try:
            result.append(float(num))
        except Exception as e:
            print(f"Error: {e}")
            result.append(None)
    return result

def safe_parse_latex(latex_str):
    try:
        return parse_latex(latex_str)
    except Exception as e:
        print(f"Error parsing LaTeX: {e}")
        return None
    
def parse_frac_expression(frac_expression):

    # Regular expression to extract the numerator and denominator
    pattern = re.compile(r'\\frac{(\d+)}{(\d+)}')

    # Search for the pattern in the string
    match = pattern.search(frac_expression)
    if match:
        # Extract numerator and denominator
        numerator = int(match.group(1))
        denominator = int(match.group(2))
        
        # Convert to float
        result = float(numerator) / float(denominator)
        print("The floating-point result is:", result)
    else:
        print("No fraction found in the string.")