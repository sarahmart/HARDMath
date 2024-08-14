import re

# automatic answer extraction using \boxed{} in the response


def extract_boxed_content(latex_response, latex_wrap = r'\$(.*?)\$'):
    matches = re.findall(latex_wrap, latex_response, re.DOTALL)
    boxed_list = [match for match in matches if "boxed" in match]
    if not boxed_list:
        print ("No boxed content found in the response.")
        return None
    last_answer = boxed_list[-1]
    return last_answer

def extract_final_answer(last_answer, pattern):
    start_idx = last_answer.find('boxed{') + 6
    end_idx = last_answer.rfind('}')
    final_answer = last_answer[start_idx:end_idx]
    parts = pattern.split(final_answer)
    parts = [part.strip() for part in parts if part.strip()]
    return parts[-1] if parts else final_answer

def extract_final_answer_list(last_answer):
    small_ans_match = re.search(r'boxed{\[(.*?),', last_answer)
    large_ans_match = re.search(r',(.*?)\]}', last_answer)
    small_ans = small_ans_match.group(1) if small_ans_match else None
    large_ans = large_ans_match.group(1) if large_ans_match else None
    return [small_ans, large_ans]

def extract_final_answer_allform(latex_response, pattern = re.compile(r'\\approx|='),latex_wrap=r'\$(.*?)\$',answer_type=None):
    last_answer = extract_boxed_content(latex_response,latex_wrap)
    if not last_answer:
        return None
    if answer_type == 'float' or 'math_exprssion':
        return extract_final_answer(last_answer, pattern)
    if answer_type == 'list':
        return extract_final_answer_list(last_answer)
    return last_answer

def fetch_scores(data_dict):
    scores = []
    for key, value in data_dict.items():
        if 'score' in value:
            scores.append(value['score'])
    return scores

def categorize_scores(data_dict):
    incorrect = 0
    partial = 0
    correct = 0
    
    for value in data_dict.values():
        if 'score' in value:
            score = value['score']
            if score == 0:
                incorrect += 1
            elif score == 1:
                correct += 1
            else:
                partial += 1
    
    return [incorrect, partial, correct]