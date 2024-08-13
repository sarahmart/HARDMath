# HARDMath: A Benchmark Dataset for Challenging Problems in Applied Mathematics

This is the repository for HARDMath: A Benchmark Dataset for Challenging Problems in Applied Mathematics.

This repository hosts the [full dataset](./data/HARDMath.json) and the [evaluation dataset](./evaluation/data/eval_HARDMath.json), together with the generation and evaluation code described in the paper. The format of the data is detailed below.

### Introduction
HARDMath is a dataset of challenging, graduate-level problems in applied mathematics that can be used for language model training and evaluation. Unlike other popular mathematical datasets, HARDMath contains problems that require more advanced problem-solving skills and approximation methods.

The dataset contains a train set of 1,050 problems and a test set of 437 problems, divided across seven different problem types. A "Word Problem in Context" set is also introduced, which consists of 40 handwritten problems that require asymptotic reasoning in the context of plausible real-world scenarios. 

### Data Access
Our full datasets of problems and solutions are stored in the `data` directory. They are available in either CSV or JSON format.

### Dataset Format
In the CSV and JSON files containing our data, each problem stores the following information:
- **“question” (str):** the text containing the applied mathematics problem  
- **“solution” (str):** the text containing the worked solution and the boxed final solution  
- **“question_type” (str):** the category the problem/solution falls into (options include “integral,” “ODE,” “nondimensionalization_numeric,” etc.)  
- **“answer_type” (str):** the type of final solution to the applied mathematics problem (options include “math_expression” for problems that only contain one solution regime, and “list” for problems that contain two solution regimes)  
- **“extracted_answer” (str):** LaTeX expressions containing the final boxed solution, which is a list of expressions if there are multiple solution regimes, the expression itself if there is only one solution regime, or a float if the solution is a numerical value  
- **“small_eval_point” (float):** the $x$ value at which the numerical solutions and approximate solutions are evaluated for the “small” solution regime  
- **“small_analytical” (float):** the numerical value of the analytical solution evaluated at small_eval_point  
- **“small_numerical” (float):** the numerical value of the ground truth (numerical) solution evaluated at small_eval_point  
- **“large_eval_point” (float):** the $x$ value at which the numerical solutions and approximate solutions are evaluated for the “large” solution regime  
- **“large_analytical” (float):** the numerical value of the ground truth (numerical) solution evaluated at large_eval_point  
- **“large_numerical” (float):** the numerical value of the ground truth (numerical) solution evaluated at large_eval_point  

### Data Generation
To generate problems and their solutions, navigate to the `src` directory and choose the type of problem you would like to generate. Running the `[problem_type]_generator.ipynb` Jupyter notebook will generate $n$ problems and their solutions, and save the results in a .csv file. The number of problems can be set by the variable `num_problems` near the top of each notebook.
