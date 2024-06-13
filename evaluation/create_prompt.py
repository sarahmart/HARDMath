
examples = []

def create_demo_prompt(examples, shot_num):
    demo_prompt = ""
    if shot_num > 0:
        demos = []
        shot_num = min(shot_num, len(examples))
        for example in examples[:shot_num]:
            prompt = f"Example question: {example['question']}\n"

            # Include solution examples
           
            solution = example['solution'].strip()
            prompt += f"Example solution: {solution}\n"
        

            demos.append(prompt)

        demo_prompt = "\n".join(demos)
    return demo_prompt

def create_query_prompt(problem, examples, shot_num):
    # demo prompt
    demo_prompt = create_demo_prompt(examples,shot_num)

    # problem setup`
    question = problem['question']
    answer_type = problem['answer_type']
    precision = problem['precision']
    question_text = f"Question: {question}"
    question_type = problem['question_type']
    # Hint and prompt setup based on problem and answer type
    hint_text = ""
    assert answer_type in ["math_expression", "float", "list"]
    assert question_type in ["integral", "ode","polynomial_roots", "nondimensionalization_symbolic", 'nondimentionalization_numeric']
    if answer_type == "math_expression":
        if question_type == 'integral':
            hint_text = "Hint: Please answer the question requiring an answer in a SymPy convertible \
                formula containing formulas of variable \\(x\\) and math operation expressions and provide \
                the final answer, e.g., \\(x^{3}\\) inside a Latex boxed format \\[boxed{}\\]."
        elif question_type == 'nondimensionalization_symbolic':
            hint_text = "Hint: Please answer the question requiring an answer in a SymPy convertible \
                formula containing variables and math operation expressions and provide the final answer,\
                e.g., \\(x^{3}\\), \\(frac{x}{y}\\) inside a Latex boxed format \\[boxed{}\\]."
    elif answer_type == "float" and precision == 2:
        hint_text = "Hint: Please answer the question requiring a floating-point number with two decimal\
              places and provide the final value, e.g., 0.80, 3.12, inside a Latex boxed format \\[boxed{}\\]."   
    elif answer_type == "list":
        if question_type == 'ode':
            hint_text = "Hint: Please answer the question requiring a Python list containing SymPy \
                convertible formula of $y = f(x)$ and provide the final list, e.g., \
                $[y = 1 - x^{3}, y = -6/(x-5)]$, inside a Latex boxed format \\[boxed{}\\]."
        elif question_type == "polynomial_roots" or "integral":
            hint_text = "Hint: Please answer the question requiring two Python lists containing SymPy \
                convertible formulas of variable $\\epsilon$ and math operation expressions and provide the \
                final list e.g., $[\\epsilon^{3}, \\frac{1}{\\epsilon}]$ inside a Latex boxed format \\[boxed{}\\]."
    elements = [question_text, hint_text, "Solution: "]
    test_query = "\n".join([e for e in elements if e != ""])
    query = (demo_prompt + "\n\n" + test_query).strip()
    return query

def create_query_prompt_batch(problem_metadata_json, examples, args):
    prompt_dict = {}
    question_specific_examples = {key: value for key, value in examples.items() if value.get('question_type') == args.question_type}
    for pid, problem in problem_metadata_json.items():
        prompt = create_query_prompt(
            problem = problem, 
            examples = question_specific_examples,
            shot_num = args.shot_num,
            )
        prompt_dict[pid] = prompt
    return prompt_dict

def create_grading_prompt(latex_response, solution_latex, question_type=None,integral_subtype=None):
    common_query = f"Please take this response: {latex_response}\n\n and this ground truth \
        solution: {solution_latex} and grade the response based on the following criteria:"
    if question_type == "polynomial_roots":
        grade_guide = "1) Check both the small and large $\epsilon$ solutions. \
            2) For each solution, give full credit if it completely matches the elements in the \
            answer key; give partial credit proportional to the number of matching roots between \
            the response and the answer key; give no credit if it is completely wrong. \
            3) For both partial and no credit briefly state the error reason. \
            4) Average the scores for the small and large epsilon solutions to obtain a final score between 0 and 1.\
            5) Give the final grading as a float in Latex boxed format \\[boxed{}\\]"
    elif question_type == "integral" and integral_subtype == "traditional_integral":
        grade_guide = "1) Check both the small and large $\epsilon$ solutions. \
        2) For each solution, give full credit if it matches the formula in the answer key; \
        give no credit if it is completely wrong and briefly state the reason for the error. \
        3) Average the scores for the small and large epsilon solutions to obtain a final score between 0 and 1.\
        4) Give the final grading as a float in Latex boxed format \\[boxed{}\\"
    elif question_type == "integral" and integral_subtype == "laplace_integral":
        grade_guide = "1) Check the large $x$ final solution. \
        2) Give full credit if it matches the formula in the answer key; \
        give half credit if the response get to the checkpoint where it correctly identifies \
        \(t_0\) where $f$ attains its maximum and attempt performing Taylor's expansion around \
        it but the final answer is wrong; give no credit if it is completely wrong. \
        3) For both partial and no credit briefly state the error reason.\
        4) Give the final grading as a float in Latex boxed format \\[boxed{}\\]"
    elif question_type == "ode":
        grade_guide = "1) Check both the small and large $\epsilon$ solutions. \
        2) For each solution, give full credit if it matches the formula in the answer key; \
        give no credit if it is completely wrong and briefly state the reason for the error. \
        3) Average the scores for the small and large epsilon solutions to obtain a final score between 0 and 1. \
        4) Give the final grading as a float in Latex boxed format \\[boxed{}\\]"
    query = f"{common_query}\n\n{grade_guide}"
    return query

