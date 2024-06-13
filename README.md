# HARDMath Dataset

This is the repository for HARDMath: A Benchmark Dataset for Challenging Problems in Applied Mathematics.

This repository host the [full dataset](./data/HARDMath.json) and the evaluation dataset, together with the generation and evaluation code described in the paper. The format of the data is detailed below.

### Dataset Format:
**“question” (str):** the text containing the applied mathematics problem  
**“solution” (str):** the text containing the worked solution and the boxed final solution  
**“question_type” (str):** the category the problem/solution falls into (options include “integral,” “ODE,” “nondimensionalization_numeric,” etc.)  
**“answer_type” (str):** the type of final solution to the applied mathematics problem (options include “math_expression” for problems that only contain one solution regime, and “list” for problems that contain two solution regimes)  
**“extracted_answer” (str):** LaTeX expressions containing the final boxed solution, which is a list of expressions if there are multiple solution regimes, the expression itself if there is only one solution regime, or a float if the solution is a numerical value  
**“small_eval_point” (float):** the $x$ value at which the numerical solutions and approximate solutions are evaluated for the “small” solution regime  
**“small_analytical” (float):** the numerical value of the analytical solution evaluated at small_eval_point  
**“small_numerical” (float):** the numerical value of the ground truth (numerical) solution evaluated at small_eval_point  
**“large_eval_point” (float):** the $x$ value at which the numerical solutions and approximate solutions are evaluated for the “large” solution regime  
**“large_analytical” (float):** the numerical value of the ground truth (numerical) solution evaluated at large_eval_point  
**“large_numerical” (float):** the numerical value of the ground truth (numerical) solution evaluated at large_eval_point  
