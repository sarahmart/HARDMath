import re
import answer_extraction 
import utils

def create_problem_dict(question, solution, pid, extracted_solution=None, question_type=None, answer_type=None):
    # of the df already provides extracted answer, we directly load it 
    if extracted_solution:
        #answer_val = list(map(latex2sympy,extracted_solution))
        answer_val = extracted_solution
    else:
        # TODO: check this part 
        answer_extraction.get_boxed_answers(solution, pattern = re.compile(r'\\approx|='),latex_wrap=r'\$(.*?)\$',answer_type=None)
    # Determine the answer type based on answer_val
    
    if not answer_type:
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