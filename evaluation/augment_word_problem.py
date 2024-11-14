import os
import re
import argparse 
import utils
import create_prompt
import models
from tqdm import tqdm
import answer_extraction
from sympy import simplify, sympify
import random


# subfdomains dictionary for each domain
domains = {
    "physics": [
        "Fluid Flow", "Hydrodynamics", "Groundwater", "Open Channel Flow", "Spray Dynamics", "Turbulence", "Viscosity",
        "Erosion", "Circuit Analysis", "Electromagnetic Induction", "Vibration Analysis", "Resonance",
        "Damped Oscillations", "Rotational Dynamics", "Spring-Mass Systems", "Frictional Forces", "Heat Transfer",
        "Thermal Conductivity", "Cooling Systems", "Energy Storage", "Battery Dynamics", "Thermodynamic Cycles",
        "Thermal Resistance", "Orbital Mechanics", "Celestial Motion", "Rocket Dynamics", "Satellite Trajectories",
        "Gravitational Influence", "Asteroid Deflection", "Tidal Forces"
    ],
    "biology": [
        "Population Dynamics", "Predator-Prey Models", "Neuroscience", "Signal Transmission", "Epidemiology",
        "Enzyme Kinetics", "Biochemical Reactions", "Cell Growth", "Pollutant Dispersion", "Habitat Migration"
    ],
    "chemistry": [
        "Biochemical Reactions", "Enzyme Kinetics", "Pollutant Dispersion", "Temperature Gradients", "Thermodynamic Cycles",
        "Energy Storage", "Battery Dynamics", "Thermal Conductivity"
    ],
    "economics": [
        "Supply and Demand", "Economic Cycles", "Trend Propagation", "Social Dynamics", "Market Equilibrium",
        "Spread of Opinions", "Population Economics", "Resource Allocation"
    ]
}

def verify_response(response):
    if isinstance(response, str):
        response = response.strip() 
    if response == "" or response == None:
        return False
    return True

def compare_answers(extracted_answer, model_answer):
    if model_answer is None:
        return 0
    try:
        # Convert the string answers to sympy expressions
        extracted_answer_expr = utils.safe_parse_latex(extracted_answer)
        model_answer_expr = utils.safe_parse_latex(model_answer)
        # Compare the simplified difference
        if simplify(extracted_answer_expr - model_answer_expr) == 0:
            return 1
    except Exception as e:
        print(f"Error in comparing answers: {e}")
        return 0
    
    return 0


def load_model(args, role):
    """
    Load and return the appropriate model based on the provided arguments.

    Parameters:
        args (Namespace): The arguments passed to the script, including model type, key, system prompt, etc.

    Returns:
        model: An instance of the model class, either GPT_Model or Ollama_Server.
    """
    # Load the API key from environment or use the provided key
    key = os.getenv("OPENAI_API_KEY") if args.key == '' else args.key
    print("Loading openai token from environment variable" if args.key == '' else "Using provided API key")

    if role == 'grader':
            system_prompt = (
                "You are a helpful grading assistant designed to help with advanced applied mathematics problems, "
                "specifically focusing on tasks like nondimensionalizing polynomials, using approximation methods to solve for polynomial roots, PDEs, integrals, etc. "
                "When given a response and a ground truth solution, you should score the response according to the user's grading criteria."
            )
            #print(args.grader)
            model = models.GPT_Model(args.grader, key, temperature=args.temperature, system_prompt=system_prompt)
    else:
        if "gpt" in args.model or "o1" in args.model:
            
            # Determine the system prompt
            if role == 'none':
                model = models.GPT_Model_openrouter(args.model, key)
            elif role == 'math_assistant':
                system_prompt = (
                    "You are a helpful assistant designed to help with crafting advanced applied mathematics problems, "
                    "specifically focusing on tasks like nondimensionalizing polynomials, using approximation methods to solve for polynomial "
                    "roots, PDEs, integrals, etc. When given a math question, you should rewrite the question according to the user's prompt."
                )
                model = models.GPT_Model_openrouter(args.model, key, temperature=args.temperature, sleep_time=args.sleep_time, system_prompt=system_prompt)
        else:
            # For non-GPT models, load from the server
            server_url = f"http://{args.server_ip}:11434/api/generate"
            model = models.Ollama_Server(server_url, args.model, args.temperature)

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--input_file', type=str, default='HARDMath_mini.json')
    parser.add_argument('--example_file', type=str, default='word_problems_HARDMath.json')
    # output
    parser.add_argument('--output_dir', type=str, default='results/LLM_word_problems/ode')
    parser.add_argument('--output_file', type=str, default='ode_gpt4o.json')
    # model
    parser.add_argument('--model', type=str, default='gpt-4o', 
                        choices = ['gpt-4-turbo','gpt-4o','openai/o1-mini'])
    parser.add_argument('--grader', type=str, default='gpt-4o', 
                        choices = ['gpt-4o','gpt-4-turbo'])
    parser.add_argument('--key', type=str, default='')
    # prompt
    parser.add_argument('--prompt_file', type=str, default=None)  
    parser.add_argument('--shot_num', type=int, default=0)
    parser.add_argument('--question_type', type=str, default='ODE',
                        choices=['nondimensionalization_symbolic','nondimensionalization_numeric',
                                 'integral','ODE','polynomial_roots'])
    parser.add_argument('--integral_subtype', type=str, default=None, choices=['traditional','laplace'])
    parser.add_argument('--temperature', type=float, default=0.0)
    parser.add_argument('--sleep_time', type=float, default=0.1)
    parser.add_argument('--server_ip', type=str, default='10.120.16.254')
    parser.add_argument('--domain_seed', type=str, default='physics', choices = ['physics','biology','chemistry', 'economics'])
    parser.add_argument('--num_problems', type=int, default=None)
    # other settings
    args = parser.parse_args()
    # load data
    input_file = os.path.join(args.data_dir, args.input_file)
    print(f"Reading {input_file}...")
    all_data = utils.read_json(input_file)
    data = {key: value for key, value in all_data.items() if value.get('question_type') == args.question_type}
    if args.question_type == 'integral':
        if args.integral_subtype == 'traditional':
            data = {key: value for key, value in data.items() if value.get('answer_type') == 'list'}
        else:
            data = {key: value for key, value in data.items() if value.get('answer_type') == 'math_expression'}
    # load examples
    example_file = os.path.join(args.data_dir, args.example_file)
    print(f"Reading {example_file}...")
    all_examples = utils.read_json(example_file)
    examples = {k: v for k, v in data.items() if v["question_type"] == args.question_type}

    # load or create prompt
    if args.prompt_file:
        prompt_file = os.path.join(args.data_dir, args.prompt_file)
        if os.path.exists(prompt_file):
            print(f"Loading existing {prompt_file}...")
            prompt_data = utils.read_json(prompt_file)
    else:
        print("Creating new prompts...")
        # create query
        prompt_data = create_prompt.create_word_augment_prompt_batch(data, domains, args.domain_seed)

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
    model = load_model(args, 'math_assistant')
    print(f"Model loaded.")

    # filter problems for testing
    test_pids = list(data.keys())
    print("Number of test problems in total:", len(test_pids))

    skip_pids = []
    print("Removing problems with existing valid response...")
    for pid in test_pids:
        if pid in results and 'aug_question' in results[pid]:
            augmented_question = results[pid]['aug_question']
            if verify_response(augmented_question):
                skip_pids.append(pid)
    test_pids = [pid for pid in test_pids if pid not in skip_pids]
    print("Number of test problems to run:", len(test_pids))

    # Add subselection of n problems if specified
    if args.num_problems and args.num_problems > 0:
        import random
        n = min(args.num_problems, len(test_pids))  # Ensure we don't try to select more than available
        test_pids = random.sample(test_pids, n)
        print(f"Randomly selected {n} problems for testing")

    # tqdm, enumerate results
    for _, pid in enumerate(tqdm(test_pids)):
        problem_dict = data[pid]
        solution = problem_dict['solution']
        user_prompt = prompt_data[pid]['prompt']
        subdomain_seed = prompt_data[pid]['subdomain_seed']
        #print(results)
        print(f"Rewriting question for {pid}...")
        try:
            results[pid] = {}
            results[pid]['question_prompt'] = user_prompt
            augmented_question = model.get_response(user_prompt)
            latex_response = utils.display_content(augmented_question,False)
            results[pid]['aug_question'] = augmented_question
            augmented_sol_prompt = create_prompt.create_word_augment_sol_prompt(augmented_question, solution, subdomain_seed)
            results[pid]['solution_prompt'] = augmented_sol_prompt
            linker_sentence = model.get_response(augmented_sol_prompt)
            augmented_solution = [linker_sentence, solution]
            results[pid]['aug_solution'] =  "\n".join([e for e in augmented_solution if e != ""])
            
            # grading answers using gpt-4o
            print("Scoring problem plausibility using gpt-4o method. Creating grading prompts...")
            # create grading prompt
            grading_model = load_model(args, 'grader')
            grading_prompt = create_prompt.create_word_augment_grading_prompt(augmented_question, subdomain_seed)
            results[pid]['grade_prompt'] = grading_prompt
            grade_response = grading_model.get_response(grading_prompt)
            results[pid]['grade_response'] = grade_response
            latex_grade_response = utils.display_content(grade_response,False)
            results[pid]['score'] = answer_extraction.extract_final_answer_allform(latex_response = latex_grade_response,answer_type = 'float')
        
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