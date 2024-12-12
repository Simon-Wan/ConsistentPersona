import json
from openai import OpenAI
import argparse
import os.path as osp
import numpy as np


def get_quality(client, model, interaction1: str, interaction2: str, model1: str, model2: str):
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

Which interaction is higher quality based on these criteria? Output either (1) or (2):
Answer: (
    """
    result = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ]
    ).choices[0].message.content
    if result.startswith("1"):
        return model1
    elif result.startswith("2"):
        return model2

def model_compare(args):
    client = OpenAI(
        api_key=args.api_key,
    )
    filename1 = f'conv_{args.scenario}_{args.oracle_model}_{args.model1}_{args.num_conv}.json'
    filename2 = f'conv_{args.scenario}_{args.oracle_model}_{args.model2}_{args.num_conv}.json'
    with open(osp.join(args.data_dir, filename1), 'r') as f:
        content1 = json.load(f)
    with open(osp.join(args.data_dir, filename2), 'r') as f:
        content2 = json.load(f)
    points = {model: 0 for model in [args.model1, args.model2]}
    for c1, c2 in zip(content1, content2):
        should_i_swap = np.random.choice([True, False])
        if should_i_swap:
            q = get_quality(client, args.oracle_model, c1['conversation'], c2['conversation'], args.model1, args.model2)
        else:
            q = get_quality(client, args.oracle_model, c2['conversation'], c1['conversation'], args.model2, args.model1)
        points[q] += 1
    print(f"{args.model1} vs {args.model2}: {points[args.model1]} {points[args.model2]}")


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
    args = parser.parse_args()
    model_compare(args)


if __name__ == '__main__':
    main()
