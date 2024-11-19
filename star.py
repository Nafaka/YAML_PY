import numpy as np
import yaml
import os
import argparse

def load_file (file_path):
    if not os.path.exists(file_path):
        raise ValueError("No file bro")
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def save_file (file_path, data):
    with open(file_path, 'w') as f:
        yaml.dump(data, f)

def star_search(nodes, start, goal, heuristic, additional_info=None, city_names=None):
    num_city = len(nodes)
    open_list = [(0, 0, start, [])]  # fs, gs, curr_city, path
    closed_list = [float('inf')] * num_city  # smallest
    expand_nodes = 0

    while open_list:
        open_list.sort(key=lambda x: x[0])
        f_score, g_score, curr_city, path = open_list.pop(0)

        if g_score >= closed_list[curr_city]:
            continue
        closed_list[curr_city] = g_score
        expand_nodes += 1
        print(f"Expanding node: {curr_city}, Total Expanded Nodes: {expand_nodes}")

        if curr_city == goal:
            print(f"Goal reached: {curr_city}, Expanded Nodes: {expand_nodes}")
            return {
                "cost": float(g_score),
                "path": [city_names[i] for i in path + [curr_city]],
                "expanded_nodes": expand_nodes,
                "heuristic": {f"city_{city_names[i]}": heuristic(i, additional_info) for i in range(num_city) if city_names[i] not in ['start', 'end']}
            }

        for neighbor, cost in enumerate(nodes[curr_city]):
            if cost == float('inf'):
                continue
            new_gs = g_score + cost
            new_heuristic = heuristic(neighbor, additional_info)
            open_list.append((new_gs + new_heuristic, new_gs, neighbor, path + [curr_city]))

    raise ValueError("No path bro")

def heuristic1(node, additional_info=None):
    return 0.0

def heuristic2(node, additional_info):
    return float(additional_info[node]["line_of_sight_distance"])

def heuristic3(node, additional_info):
    data = additional_info[node]
    return float(data["line_of_sight_distance"] + 0.5 * data["altitude_difference"])

def parse_nodes(problem, additional_info):
    nodes = sorted([key.split("_")[1] for key in problem if key.startswith("city_")])
    nodes_indices = {city: i for i, city in enumerate(nodes)}

    num_nodes = len(nodes)
    all_nodes = [[float('inf')] * num_nodes for _ in range(num_nodes)]

    for city, details in problem.items():
        if city.startswith("city_") and "connects_to" in details:
            curr_city = nodes_indices[city.split("_")[1]]
            for neighbor, cost in details["connects_to"].items():
                neighbor_city = nodes_indices[neighbor]
                all_nodes[curr_city][neighbor_city] = cost

    additional_info_list = [{"line_of_sight_distance": 0, "altitude_difference": 0} for _ in range(num_nodes)]
    for city, info in additional_info.items():
        node = nodes_indices[city.split("_")[1]]
        additional_info_list[node] = info

    return all_nodes, nodes_indices, additional_info_list

def main(input_file, output_prefix):
    problem_data = load_file(input_file)
    problem = problem_data["problem"]
    additional_info = problem_data.get("additional_information", {})

    start_city = problem["city_start"]
    goal_city = problem["city_end"]

    graph, city_indices, additional_info_list = parse_nodes(problem, additional_info)
    start_idx = city_indices[start_city]
    goal_idx = city_indices[goal_city]

    # names handlign
    city_names = {}
    for k, v in city_indices.items():
        if "_" in k:
            city_names[v] = k.split("_")[1]
        else:
            city_names[v] = k

    # Uniform-Cost Search
    part1_solution = star_search(graph, start_idx, goal_idx, heuristic1, city_names=city_names)
    save_file(f"{output_prefix}-1.yaml", {"solution": part1_solution})

    # Line-of-sight heuristic
    part2_solution = star_search(graph, start_idx, goal_idx, heuristic2, additional_info_list, city_names)
    save_file(f"{output_prefix}-2.yaml", {"solution": part2_solution})

    # Enhanced heuristic
    part3_solution = star_search(graph, start_idx, goal_idx, heuristic3, additional_info_list, city_names)
    save_file(f"{output_prefix}-3.yaml", {"solution": part3_solution})

if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser(description="A* Search Algorithm for Route Finding")
    parser.add_argument("input_file", type=str, help="Path to the input YAML file")
    parser.add_argument("output_prefix", type=str, help="Prefix for the output files")
    args = parser.parse_args()

    main(args.input_file, args.output_prefix)



