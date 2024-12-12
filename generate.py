# Consistent Persona Simulation
import argparse
import json
from random import random

from scenarios.education import Education
from scenarios.therapist import Therapist
import os
import os.path as osp
from openai import OpenAI
import numpy as np


def generate_conversations(scenario, agent, user, num_conv, api_key, use_vanilla=False):
    client = OpenAI(
        api_key=api_key,
    )
    num_turn = 5
    conv_list = []
    for _ in range(num_conv):
        user_type = scenario.sample_user_type()
        topic = scenario.sample_topic()
        conv = {
            "user_type": user_type,
            "topic": topic,
        }
        agent_system_prompt = scenario.generate_prompt_for_oracle_agent(user_type, topic)
        user_system_prompt = scenario.generate_prompt_for_user_candidate(user_type, topic, use_vanilla=use_vanilla)
        agent_messages = [{
            "role": "system",
            "content": agent_system_prompt,
        }]
        user_messages = [{
            "role": "assistant",
            "content": user_system_prompt,
        }]
        conversation = ''
        for _ in range(num_turn):
            # generate agent utterance
            agent_utterance = client.chat.completions.create(
                model=agent,
                messages=agent_messages,
            ).choices[0].message.content
            agent_messages.append({
                "role": "assistant",
                "content": agent_utterance,
            })
            user_messages.append({
                "role": "user",
                "content": agent_utterance,
            })
            conversation += agent_utterance + '\n\n'
            # generate user utterance
            user_utterance = client.chat.completions.create(
                model=user,
                messages=user_messages,
            ).choices[0].message.content
            user_messages.append({
                "role": "assistant",
                "content": user_utterance,
            })
            agent_messages.append({
                "role": "user",
                "content": user_utterance,
            })
            conversation += user_utterance + '\n\n'
        conv['conversation'] = conversation
        conv_list.append(conv)
    return conv_list



def main():
    np.random.seed(42)
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', required=True)
    parser.add_argument('-m', '--model', required=True)
    parser.add_argument('-n', '--num_conv', default=1, type=int)
    parser.add_argument('--oracle_model', default='gpt-4o')
    parser.add_argument('-d', '--data_dir', default='./data')
    parser.add_argument('--api_key', required=True)
    parser.add_argument('--use_vanilla', action='store_true')
    args = parser.parse_args()

    if args.scenario == 'education':
        scenario = Education()
    elif args.scenario == 'therapist':
        scenario = Therapist()
    else:
        raise ValueError(f'Scenario {args.scenario} not implemented')           # Add your scenario here

    if args.model not in ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo-0125']:       # Models with lower prices
        raise ValueError(f'Model {args.model} not supported')

    if args.oracle_model != 'gpt-4o':
        raise ValueError(f'Oracle model {args.oracle_model} not supported')     # Use GPT-4o as the most powerful model

    conversations = generate_conversations(scenario, args.oracle_model, args.model, args.num_conv, args.api_key, args.use_vanilla)
    if not osp.exists(args.data_dir):
        os.makedirs(args.data_dir)
    filename = f'conv_{args.scenario}_{args.oracle_model}_{args.model}_{args.num_conv}.json'
    if args.use_vanilla:
        filename = f'conv_{args.scenario}_{args.oracle_model}_{args.model}_{args.num_conv}_vanilla.json'
    with open(osp.join(args.data_dir, filename), 'w') as f:
        json.dump(conversations, f)


if __name__ == '__main__':
    main()
