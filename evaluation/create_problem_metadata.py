import re
import answer_extraction 
import utils
import numpy as np
import pandas as pd
import json

def create_problem_dict(question, solution, pid, extrcated_answer=None, question_type=None, answer_type=None):
    # of the df already provides extracted answer, we directly load it 
    if extrcated_answer:
        #answer_val = list(map(latex2sympy,extrcated_answer))
        answer_val = extrcated_answer
    else:
        # TODO: check this part 
        answer_val = answer_extraction.extract_final_answer_allform(solution, pattern = re.compile(r'\\approx|='),latex_wrap=r'\$(.*?)\$',answer_type=None)
    if answer_type is None:
        answer_type = utils.answer_type_extract(answer_val)

    # Determine the precision for float types
    precision = None
    if answer_type == "float":
        decimal_part = answer_val.split('.')[-1]
        precision = len(decimal_part)

    # Construct the problem dictionary
    problem_dict = {
        "question": question,
        "solution": solution,
        "question_type": question_type,
        "answer_val": answer_val,
        "answer_type": answer_type,
        "precision": precision,
        "pid": pid
    }

    return problem_dict

def create_problem_dict_all(df,problem_dict_path = "data/eval_problems/eval_HARDMath.json"):
    problem_dict_all = []
    for i, row in df.iterrows():
        question = row["question"]
        solution = row["solution"]
        solution_latex = utils.display_content(solution, False)
        pid = str(i)
        extrcated_answer = row["extracted_answer"]
        question_type = row["question_type"]
        answer_type = row["answer_type"]
        problem_dict = create_problem_dict(question, solution_latex, pid, extrcated_answer, question_type, answer_type)
        problem_dict_all.append(problem_dict)
    with open(problem_dict_path, mode='w', encoding='utf-8') as jsonfile:
        json.dump(problem_dict_all, jsonfile, ensure_ascii=False, indent=4)

    print(f"Saved {len(problem_dict_all)} problems to {problem_dict_path}")
    return problem_dict_all

