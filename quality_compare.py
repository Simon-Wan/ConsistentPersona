import json
from openai import OpenAI
import argparse
import os.path as osp
import numpy as np


def get_quality(scenario, client, model, interaction1: str, interaction2: str, model1: str, model2: str) -> int:
    """
    If the first model is better, return 0; otherwise, return 1"""
    if scenario == 'education':
        prompt = f"""
Evaluate the quality of two interactions between a teacher and a student, and determine which one demonstrates a better teaching approach.

A good interaction between a teacher and a student should be characterized by key elements such as clear and enthusiastic presentation of information, encouragement of questions and active participation, and fostering a comfortable environment for students to seek clarification, offer insights, and respectfully challenge ideas.

Consider the following interactions:

--- Start of Interaction 1 ---
{interaction1}
--- End of Interaction 1 ---

--- Start of Interaction 2 ---
{interaction2}
--- End of Interaction 2 ---

Which interaction is higher quality based on these criteria? Note output exactly 1 or 2 (no other characters should be and are allowed to use for your answer):
Answer: (
    """
    elif scenario == 'therapist':
        prompt = f"""
Evaluate the quality of two interactions between a therapist and a client, and determine which one demonstrates a better therapeutic approach.

A good interaction between a therapist and a client should be characterized by key elements such as empathetic listening, appropriate use of reflective techniques, validation of the client’s emotions, encouraging client self-awareness, and fostering a safe and non-judgmental environment for the client to express themselves freely.

Consider the following interactions:

--- Start of Interaction 1 ---
{interaction1}
--- End of Interaction 1 ---

--- Start of Interaction 2 ---
{interaction2}
--- End of Interaction 2 ---

Which interaction is higher quality based on these criteria? Note output exactly 1 or 2 (no other characters should be and are allowed to use for your answer):
Answer: (
"""
    else:
        raise NotImplementedError

    result = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ]
    ).choices[0].message.content
    if result.startswith("1"):
        return 0
    elif result.startswith("2"):
        return 1

def model_compare(args):
    client = OpenAI(
        api_key=args.api_key,
    )
    filename1 = f'conv_{args.scenario}_{args.oracle_model}_{args.model1}_{args.num_conv}.json'
    if args.m1_vanilla:
        filename1 = f'conv_{args.scenario}_{args.oracle_model}_{args.model1}_{args.num_conv}_vanilla.json'
    filename2 = f'conv_{args.scenario}_{args.oracle_model}_{args.model2}_{args.num_conv}.json'
    if args.m2_vanilla:
        filename2 = f'conv_{args.scenario}_{args.oracle_model}_{args.model2}_{args.num_conv}_vanilla.json'
    with open(osp.join(args.data_dir, filename1), 'r') as f:
        content1 = json.load(f)
    with open(osp.join(args.data_dir, filename2), 'r') as f:
        content2 = json.load(f)
    model_names = [
        f"{args.model1}_vanilla" if args.m1_vanilla else f"{args.model1}_prompted",
        f"{args.model2}_vanilla" if args.m2_vanilla else f"{args.model2}_prompted"
    ]
    points = {model: 0 for model in model_names}
    for c1, c2 in zip(content1, content2):
        should_i_swap = np.random.choice([True, False])
        if should_i_swap:
            q = get_quality(args.scenario, client, args.oracle_model, c1['conversation'], c2['conversation'], args.model1, args.model2)
            q = model_names[q]
        else:
            q = get_quality(args.scenario, client, args.oracle_model, c2['conversation'], c1['conversation'], args.model2, args.model1)
            q = model_names[q]
        points[q] += 1
    print(f"{model_names[0]} vs {model_names[1]}: {points[model_names[0]]} {points[model_names[1]]}")


def main():
    np.random.seed(42)
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', required=True)
    parser.add_argument('-m1', '--model1', required=True)
    parser.add_argument('-m2', '--model2', required=True)
    parser.add_argument('-n', '--num_conv', default=1, type=int)
    parser.add_argument('--oracle_model', default='gpt-4o')
    parser.add_argument('-d', '--data_dir', default='./data')
    parser.add_argument('--api_key', required=True)
    parser.add_argument('--m1_vanilla', default=False, action='store_true')
    parser.add_argument('--m2_vanilla', default=False, action='store_true')
    args = parser.parse_args()
    model_compare(args)


if __name__ == '__main__':
    main()
