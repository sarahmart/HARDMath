import re
import answer_extraction 
import utils
import numpy as np
import pandas as pd



def create_problem_dict(question, solution, small_eval_point, small_analytical, small_numerical, \
                        large_eval_point, large_analytical, large_numerical, extrcated_answer=None, question_type=None, answer_type=None):
    # of the df already provides extracted answer, we directly load it 
    if extrcated_answer:
        #answer_val = list(map(latex2sympy,extrcated_answer))
        answer_val = extrcated_answer
    else:
        # TODO: check this part 
        answer_val = answer_extraction.extract_final_answer_allform(solution, pattern = re.compile(r'\\approx|='),latex_wrap=r'\$(.*?)\$',answer_type=answer_type)
    if answer_type is None:
        answer_type = answer_extraction.answer_type_extract(answer_val)

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
        "answer_type": answer_type,
        "answer_val": answer_val,
        "precision": precision,
        "small_eval_point":small_eval_point,
        "small_analytical":small_analytical,
        "small_numerical":small_numerical,
        "large_eval_point":large_eval_point,
        "large_analytical":large_analytical,
        "large_numerical":large_numerical
    }

    return problem_dict
def create_example_dict_all(row):
    question = row["question"]
    solution = row["solution"]
    question_type = row["question_type"]
    example_dict = {
        "question": question,
        "solution": solution,
        "question_type": question_type
    }
    return example_dict

def create_problem_example_dict_all(df,example_list,problem_dict_path = "data/eval_HARDMath.json",example_dict_path = "data/examples_HARDMath_1shot.json"):
    problem_dict_all = {}
    example_dict_all = {}
    for i, row in df.iterrows():
        pid = str(i)
        if i in example_list:
            example_dict = create_example_dict_all(row)
            example_dict_all[pid]=example_dict
        else:
            question = row["question"]
            solution = row["solution"]
            solution_latex = utils.display_content(solution, False)
            extrcated_answer = row["extracted_answer"]
            question_type = row["question_type"]
            answer_type = row["answer_type"]
            small_eval_point = row["small_eval_point"]
            small_analytical = row["small_analytical"]
            small_numerical = row["small_numerical"]
            large_eval_point = row["large_eval_point"]
            large_analytical = row["large_analytical"]
            large_numerical = row["large_numerical"]
            problem_dict = create_problem_dict(question, solution_latex, small_eval_point, small_analytical, small_numerical, \
                            large_eval_point, large_analytical, large_numerical, extrcated_answer, question_type, answer_type)
            problem_dict_all[pid]=problem_dict
    utils.save_json(problem_dict_all, problem_dict_path)
    print(f"Saved {len(problem_dict_all)} problems to {problem_dict_path}")
    if example_dict_all != {}:
        utils.save_json(example_dict_all, example_dict_path)
        print(f"Saved {len(example_dict_all)} examples to {example_dict_path}")
    return problem_dict_all,example_dict_all

