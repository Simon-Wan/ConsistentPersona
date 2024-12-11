# Consistent Persona Simulation
import argparse
import json
from scenarios.education import Education
import os
import os.path as osp


def evaluate_conversations(scenario, conversations, api_key):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', required=True)
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-n', '--num_conv', default=1, type=int)
    parser.add_argument('--oracle_model', default='gpt-4o')
    parser.add_argument('-d', '--data_dir', default='./data')
    parser.add_argument('--api_key', required=True)
    args = parser.parse_args()

    if args.scenario == 'education':
        scenario = Education()
    else:
        raise ValueError(f'Scenario {args.scenario} not implemented')           # Add your scenario here

    if args.model not in ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo-0125']:       # Models with lower prices
        raise ValueError(f'Model {args.model} not supported')

    if args.oracle_model != 'gpt-4o':
        raise ValueError(f'Oracle model {args.oracle_model} not supported')     # Use GPT-4o as the most powerful model

    filename = f'conv_{args.scenario}_{args.oracle_model}_{args.model}_{args.num_conv}.json'
    with open(osp.join(args.data_dir, filename), 'r') as f:
        conversations = json.load(f)

    evaluate_conversations(scenario, conversations, args.api_key)


if __name__ == '__main__':
    main()
