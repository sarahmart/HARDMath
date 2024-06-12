import os
import io
import time
import argparse 
import utils
import create_prompt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # input
    parser.add_argument('--data_dir', type=str, default='data')
    parser.add_argument('--input_file', type=str, default='eval_HARDMath.json')
    parser.add_argument('--example_file', type=str, default='example_HARDMath.json')
    # output
    parser.add_argument('--output_dir', type=str, default='results/response/nondimensionalization_symbolic')
    parser.add_argument('--output_file', type=str, default='nondimensionalization_symbolic_0shot_gpt4.json')
    # model
    #parser.add_argument('--model', type=str, default='gpt-3.5-turbo', 
                        #choices = ['gpt-3.5-turbo', 'claude-2', 'gpt4', 'gpt-4-0613', 'bard'])
    #parser.add_argument('--key', type=str, default='', help='key for llm api')
    # prompt
    parser.add_argument('--prompt_file', type=str, default=None)  
    parser.add_argument('--shot_num', type=int, default=0)
    parser.add_argument('--question_type', type=str, default='nondimensionalization_symbolic')
    # other settings
    #parser.add_argument('--rerun', action='store_true', help='rerun answer extraction for all problems')
    #parser.add_argument('--debug', action='store_true', help='debug mode')
    args = parser.parse_args()

    # load data
    input_file = os.path.join(args.data_dir, args.input_file)
    print(f"Reading {input_file}...")
    data = utils.read_json(input_file)

    # load data
    example_file = os.path.join(args.data_dir, args.example_file)
    print(f"Reading {example_file}...")
    examples = utils.read_json(example_file)

    # load or create prompt
    if args.query_file:
        prompt_file = os.path.join(args.data_dir, args.prompt_file)
        if os.path.exists(prompt_file):
            print(f"Loading existing {prompt_file}...")
            query_data = utils.read_json(prompt_file)
    else:
        print("\nCreating new prompts...")
        # create query
        query_data = create_prompt.create_query_prompt_batch(data, examples, args)
    
    # output file
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(args.output_dir, args.output_file)
     