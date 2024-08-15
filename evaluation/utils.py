import re
from IPython.display import display, Markdown, Latex
from sympy.parsing.latex import parse_latex
from sympy import sympify, N
import json
import pandas as pd
import numpy as np

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def read_clean_csv(csv_path):
    df = pd.read_csv(csv_path)
    df = df.replace({np.nan: None})
    return df

def display_content(input_str, show_display=True):
    latex_str = input_str.replace(r'\[', ' $').replace(r'\]', '$ ').replace(r'\(', ' $').\
        replace(r'\)', ' $').replace('$$\\', ' $').replace('$\\', ' $').replace('$$','$ ').\
        replace('\\begin{align*}',' $').replace('\\end{align*}','$')
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

def convert_to_numbers(string_list):
    result = []
    for num in string_list:
        try:
            result.append(float(num))
        except Exception as e:
            print(f"Error: {e}")
            result.append(0)
    return result

def compare_lists_within_threshold(list1, list2,threshold):
    result = []
    for val1, val2 in zip(list1, list2):
        try:
            if val1 is None or val2 is None:
                result.append(False)
            else:
                num1 = N(sympify(val1))
                num2 = N(sympify(val2))
                diff = abs(num1 - num2)
                #avg = (num1 + num2) / 2
                if abs(diff / num2) <= threshold:
                    result.append(True)
                else:
                    result.append(False)
        except (TypeError, ValueError):
            result.append(False)
    return result

def list_diff(list1, list2):
    result = []
    for val1, val2 in zip(list1, list2):
        try:
            if val1 is None or val2 is None:
                result.append(None)
            else:
                num1 = N(sympify(val1))
                num2 = N(sympify(val2))
                diff = abs(num1 - num2)
                result.append(diff)
        except (TypeError, ValueError):
            result.append(None)
    return result