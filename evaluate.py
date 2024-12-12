# Consistent Persona Simulation
import argparse
import json
from scenarios.education import Education
import os.path as osp
from openai import OpenAI


def evaluate_conversations(scenario, conversations, api_key, rater):
    client = OpenAI(
        api_key=api_key,
    )
    quality_score_list = []
    user_type_success_counter = {key: [] for key in scenario.user_types.keys()}
    user_type_prompts = scenario.generate_prompt_for_user_type_classifier()
    # quality_prompt = scenario.generate_prompt_for_conversation_quality_assessor()
    for conv in conversations:
        # quality_score = client.chat.completions.create(
        #     model=rater,
        #     messages=[
        #         {"role": "system", "content": quality_prompt},
        #         {"role": "user", "content": conv['conversation']}
        #     ],
        # ).choices[0].message.content
        # print(quality_score)
        # score = None
        # for n in range(1, 6):
        #     if str(n) in quality_score:
        #         score = n
        # quality_score_list.append(score)
        for key in scenario.user_types.keys():
            prediction = client.chat.completions.create(
                model=rater,
                messages=[
                    {"role": "system", "content": user_type_prompts[key]},
                    {"role": "user", "content": conv['conversation']}
                ]
            ).choices[0].message.content
            print(conv['user_type'][key], prediction)
            user_type_success_counter[key].append(int(conv['user_type'][key] in prediction))
    # print(quality_score_list)
    print(user_type_success_counter)
    # print("conversation quality", sum(quality_score_list) / len(quality_score_list))
    for key in scenario.user_types.keys():
        print(key, sum(user_type_success_counter[key])/len(user_type_success_counter[key]))


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

    evaluate_conversations(scenario, conversations, args.api_key, args.oracle_model)


if __name__ == '__main__':
    main()
