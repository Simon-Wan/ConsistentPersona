from typing import List, Dict
import numpy as np


class Scenario:
    agent_name: str = ''
    student_name: str = ''
    user_types: Dict[str, List[str]] = {}
    topics: List[str] = []

    def generate_prompt_for_oracle_agent(self, user_type, topic):
        raise NotImplementedError

    def generate_prompt_for_user_candidate(self, user_type, topic, use_vanilla=False):
        raise NotImplementedError

    def generate_prompt_for_user_type_classifier(self):
        raise NotImplementedError

    def generate_prompt_for_conversation_quality_assessor(self):
        raise NotImplementedError

    def sample_user_type(self):
        keys = list(self.user_types.keys())
        user_type = {}
        for key in keys:
            user_type[key] = np.random.choice(self.user_types[key])
        return user_type

    def sample_topic(self):
        return np.random.choice(self.topics)
