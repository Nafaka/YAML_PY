"""
Check the output file of a submission.

python test_output.py yaml_problem yaml_solution
"""

import argparse
import pandas as pd
import os
import logging
import yaml
import numpy as np

if __name__ == "__main__":
    print("Testing output file.")
    logging.basicConfig(encoding='utf-8', level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('yaml_problem')
    parser.add_argument('yaml_solution')

    args = parser.parse_args()
    
    # verify files exist
    if not os.path.exists(args.yaml_problem):
        logging.error(f"YAML file {args.yaml_file} not found.")
        raise ValueError(f"File not found: {args.yaml_file}")
    
    if not os.path.exists(args.yaml_solution):
        logging.error(f"YAML file {args.yaml_solution} not found.")
        raise ValueError(f"File not found: {args.yaml_solution}")

    # Load problem description
    with open(args.yaml_problem, "rt") as f:
        try:
            problem = yaml.safe_load(f)
        except:
            logging.error(f"Could not load problem description from {args.yaml_problem}.")
            raise ValueError()
        
    cities = problem['problem']['cities']
    
    # Load solution description
    with open(args.yaml_solution, "rt") as f:
        try:
            solution = yaml.safe_load(f)
        except:
            logging.error(f"Could not load problem description from {args.yaml_solution}.")
            raise ValueError()
    
    # Check for existence of solution part
    if 'solution' not in solution:
        logging.error(f"'solution' not found at top-level in {args.yaml_solution}.")
        raise ValueError()
    
    solution = solution['solution']

    # Check for existence and type of cost
    if 'cost' not in solution:
        logging.error(f"'cost' not found within 'solution' in {args.yaml_solution}.")
        raise ValueError()
    
    if not (isinstance(solution["cost"], float) or isinstance(solution["cost"], int)):
        logging.error(f"'cost' within 'solution' is not a float or int.")
        raise ValueError()

    # check for existence and type of exanded nodes
    if 'expanded_nodes' not in solution:
        logging.error(f"'expanded_nodes' not found within 'solution' in {args.yaml_solution}.")
        raise ValueError()
    
    if not isinstance(solution["expanded_nodes"], int):
        logging.error(f"'cost' within 'expanded_nodes' is not an int.")
        raise ValueError()

    # check that path consists of cities
    if 'path' not in solution:
        logging.error(f"'path' not found within 'solution' in {args.yaml_solution}.")
        raise ValueError()
    
    path = solution['path']
    for city in path:
        if city not in cities:
            logging.error(f"city {city} in path not valid in 'solution/path' in {args.yaml_solution}.")
            raise ValueError()

    # check for all entries and proper type of values in heuristic
    if 'heuristic' not in solution:
        logging.error(f"'heuristic' not found within 'solution' in {args.yaml_solution}.")
        raise ValueError()
    for city in cities:
        heuristic = solution["heuristic"]
        field = f"city_{city}"
        if field not in heuristic:
            logging.error(f"'{field}' not found within 'solution/heuristic' in {args.yaml_solution}.")
            raise ValueError()
        
        if not (isinstance(heuristic[field], float) or isinstance(heuristic[field], int)):
            logging.error(f"'{field}' within 'solution/heuristic' is not a float or int.")
            raise ValueError()
    
    print("Output file seems to be ok.")