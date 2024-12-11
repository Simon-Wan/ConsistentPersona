from scenarios.utils import Scenario


class Education(Scenario):
    agent_name = 'Teacher'
    user_name = 'Student'
    user_types = {
        "education level": ["primary school", "high school", "university"],
        "preferred learning style": ["conceptual", "analytical", "interactive"]
    }
    topics = [
        "Rainbows",
        "Decimals",
        "Probability",
        "Light",
        "Ecosystems",
        "States of Matter",
        "Sound Waves",
        "Force",
        "The Solar System",
        "Electric Circuits",
        "Reflection and Refraction",
        "Time",
        "Friction",
        "Density",
        "Photosynthesis",
        "Thermometers",
        "Eclipses",
        "Acids and Bases",
        "The Fibonacci Sequence",
        "Blood Circulation",
    ]

    def generate_prompt_for_oracle_agent(self, user_type, topic):
        background = ''
        for key in user_type:
            background += f'{key}: {user_type[key]}. '
        prompt = f"""
        In this task, you will simulate a conversation with a student by instructing on a specific topic, taking into account their background information.

        - **Topic**: {topic}
        - **Student Background**: {background}

        # Output Format

        Your output should start with "Teacher: ".
        
        # Notes 
        
        - Ensure your responses are adaptive to the student's needs and understanding level.
        - The conversation should be natural and educational, adapting the teaching style and content to the student's background.
        - Use the student's background information as a guide; avoid directly referencing it.
        - Keep each utterance concise to allow for student interaction before continuing the conversation.
        """
        return prompt

    def generate_prompt_for_user_candidate(self, user_type, topic):
        background = ''
        for key in user_type:
            background += f'{key}: {user_type[key]}. '
        prompt = f"""
        In this task, you will simulate a conversation with a teacher who is instructing on a specific topic. You will adopt the role of a student, ensuring consistency with the given background information.

        - **Student Background**: {background}

        # Output Format

        Your output should start with "Student: ".

        # Notes 

        - Maintain consistency with the provided student background throughout the conversation. 
        - The dialogue should be engaging and indicative of the student’s understanding and curiosity regarding the topic.
        - Keep each utterance concise to allow for teacher interaction before continuing the conversation.
        """
        return prompt
