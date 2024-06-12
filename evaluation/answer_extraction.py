import re

# automatic answer extraction using \boxed{} in the response

def answer_type_extract(answer_val):
    if answer_val:
        if re.search(r'[a-zA-Z]', answer_val):
            answer_type = "math_expression"
        elif re.search(r'\d+\.\d+', answer_val):
            answer_type = "float"
        elif re.search(r'^\d+$', answer_val):
            answer_type = "int"
        elif re.search(r'\[.*\]', answer_val):
            answer_type = "list"
        else:
            answer_type = "uncertain"  
    else:
        answer_type = "Answer extraction error"
    return answer_type

def extract_boxed_content(latex_response, latex_wrap = r'\$(.*?)\$'):
    matches = re.findall(latex_wrap, latex_response, re.DOTALL)
    boxed_list = [match for match in matches if "boxed" in match]
    if not boxed_list:
        print ("No boxed content found in the response.")
        return None
    final_answer = boxed_list[-1]
    return final_answer

def extract_final_answer(final_answer, pattern):
    parts = pattern.split(final_answer)
    parts = [part.strip() for part in parts if part.strip()]
    final_expression = parts[-1] if parts else final_answer
    # deal with the case where the final answer is a nested boxed expression
    if "{" or "}" in final_expression:
        start_idx = final_expression.find('{') + 1
        end_idx = final_expression.rfind('}')
        return final_expression[start_idx:end_idx]
    return final_expression

def extract_final_answer_list(final_answer):
    small_ans_match = re.search(r'boxed{\[(.*?),', final_answer)
    large_ans_match = re.search(r',(.*?)\]}', final_answer)
    small_ans = small_ans_match.group(1) if small_ans_match else None
    large_ans = large_ans_match.group(1) if large_ans_match else None
    return [small_ans, large_ans]

def extract_final_answer_allform(latex_response, pattern = re.compile(r'\\approx|='),latex_wrap=r'\$(.*?)\$',answer_type=None):
    final_answer = extract_boxed_content(latex_response,latex_wrap = latex_wrap)
    if not final_answer:
        return None
    if answer_type == 'float' or 'math_exprssion':
        return extract_final_answer(final_answer, pattern)
    if answer_type == 'list':
        return extract_final_answer_list(final_answer)