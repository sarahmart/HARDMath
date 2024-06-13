import os
import io
import time
import argparse 
import utils
import create_prompt
import models
from tqdm import tqdm
import answer_extraction
from sympy import simplify

def verify_response(response):
    if isinstance(response, str):
        response = response.strip() 
    if response == "" or response == None:
        return False
    return True

def compare_answers(extracted_answer, model_answer):
    if model_answer is None:
        return 0
    else:
        if simplify(extracted_answer - model_answer) == 0:
            return 1
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--input_file', type=str, default='eval_HARDMath.json')
    parser.add_argument('--example_file', type=str, default='example_HARDMath_1shot.json')
    # output
    parser.add_argument('--output_dir', type=str, default='results/response/nondimensionalization_symbolic')
    parser.add_argument('--output_file', type=str, default='nondimensionalization_symbolic_1shot_gpt4.json')
    # model
    parser.add_argument('--model', type=str, default='gpt-4-turbo', 
                        choices = ['gpt-4-turbo','gpt-3.5-turbo', 'gpt-4o','llama3-8b','codellama-13b'])
    parser.add_argument('--key', type=str, default='')
    parser.add_argument('--sys_prompt', type=str, default='math_assistant',choices=['math_assistant','grader','none'])
    # prompt
    parser.add_argument('--prompt_file', type=str, default=None)  
    parser.add_argument('--shot_num', type=int, default=1)
    parser.add_argument('--question_type', type=str, default='nondimensionalization_symbolic',
                        choices=['nondimensionalization_symbolic','nondimensionalization_numeric',
                                 'integral','ode','polynomial_roots'])
    parser.add_argument('--integral_subtype', type=str, default=None, choices=['traditional','laplace'])
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--server_ip', type=str, default='10.120.16.254')
    # other settings
    args = parser.parse_args()

    # load data
    input_file = os.path.join(args.data_dir, args.input_file)
    print(f"Reading {input_file}...")
    data = utils.read_json(input_file)

    # load examples
    example_file = os.path.join(args.data_dir, args.example_file)
    print(f"Reading {example_file}...")
    examples = utils.read_json(example_file)

    # load or create prompt
    if args.query_file:
        prompt_file = os.path.join(args.data_dir, args.prompt_file)
        if os.path.exists(prompt_file):
            print(f"Loading existing {prompt_file}...")
            prompt_data = utils.read_json(prompt_file)
    else:
        print("Creating new prompts...")
        # create query
        prompt_data = create_prompt.create_query_prompt_batch(data, examples, args)

    # output file
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, args.output_file)
     
    # load results
    if os.path.exists(output_file):
        print(f"Reading existing {output_file}...")
        results = utils.read_json(output_file)
    else:
        results = {}
    
    # load model
    print(f"Loading {args.model}...")
    if "gpt" in args.model:
        if args.key == '':
            print("Loading openai token from environment variable")
            key = os.getenv("OPENAI_API_KEY")
        else:
            key = args.key
        if args.sys_prompt == 'none':
            model = models.GPT_Model(args.model, key)
        elif args.sys_prompt == 'math_assistant':
            system_prompt = "You are a helpful assistant designed to help with advanced applied mathematics problems, \
            specifically focusing on tasks like nondimensionalizing polynomials, using approximation methods to solve for polynomial \
            roots, PDEs, intergrals etc. When given a physical math question, you should answer the question according to user's prompt."
            model = models.GPT_Model(args.model, key, temperature=args.temperature, system_prompt=system_prompt)
        elif args.sys_prompt == 'grader':
            system_prompt = "You are a helpful grading assistant designed to help with advanced applied mathematics problems, \
            specifically focusing on tasks like nondimensionalizing polynomials, using approximation methods to solve for polynomial roots, PDEs, intergrals etc. \
            When given a response and a ground truth solution, you should score the response according to user's grading criteria."
            model = models.GPT_Model(args.model, key, temperature=args.temperature, system_prompt=system_prompt)
    else:
        server_url = f"http://{args.server_ip}:11434/api/generate"
        model = models.Ollama_Server(server_url, args.model,args.temperature)
    print(f"Model loaded.")

    # filter problems for testing
    test_pids = list(data.keys())
    print("Number of test problems in total:", len(test_pids))

    skip_pids = []
    print("Removing problems with existing valid response...")
    for pid in test_pids:
        if pid in results and 'response' in results[pid]:
            response = results[pid]['response']
            if verify_response(response):
                skip_pids.append(pid)
    test_pids = [pid for pid in test_pids if pid not in skip_pids]
    print("Number of test problems to run:", len(test_pids))
    
    # tqdm, enumerate results
    for _, pid in enumerate(tqdm(test_pids)):
        problem_dict = data[pid]
        user_prompt = prompt_data[pid]
        print(f"Generating response for {pid}...")
        try:
            results[pid]['prompt'] = user_prompt
            response = model.get_response(user_prompt)
            results[pid]['response'] = response
            if args.question_type.contains('nondimensionalization'):
                extracted_answer = problem_dict['answer_val']
                results[pid]['extracted_answer'] = extracted_answer
                latex_response = utils.display_content(response,False)
                model_answer = answer_extraction.extract_final_answer_allform(latex_response)
                results[pid]['model_answer'] = model_answer
                results[pid]['score'] = compare_answers(extracted_answer, model_answer)
            else:
            # grading answers using gpt-4o
                print("Scoring using gpt-4o method. Creating grading prompts...")
                # create grading prompt
                grading_model = models.GPT_Model("gpt-4o", key)
                grading_prompt = create_prompt.create_grading_prompt(latex_response, problem_dict['solution'],\
                                question_type=args.question_type,integral_subtype=args.integral_subtype)
                results[pid]['grade_prompt'] = grading_prompt
                grade_response = model.get_response(grading_prompt)
                results[pid]['grade_response'] = grade_response
                latex_grade_response = utils.display_content(grade_response,False)
                results[pid]['score'] = answer_extraction.extract_final_answer_allform(latex_grade_response)
        
        except Exception as e:
            print(e)
            print(f"Error in processing for {pid}")
            results[pid]['error'] = e
    
        try:
            print(f"Saving results to {output_file}...")
            utils.save_json(results, output_file)
            print(f"Results saved.")
        except Exception as e:
            print(e)
            print(f"Error in saving {output_file}")