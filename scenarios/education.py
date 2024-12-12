from scenarios.utils import Scenario


class Education(Scenario):
    agent_name = 'Teacher'
    user_name = 'Student'
    user_types = {
        "Education level": ["Primary school", "High school", "University"],
        "Interaction style": ["Expressive", "Passive"]
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

    def generate_prompt_for_user_type_classifier(self):
        education_level_prompt = """
Analyze the conversation between a teacher and a student to determine the student's education level. Consider factors such as language complexity, subject matter, and student responses. Your answer should be in one of the following categories:

- Primary school
- High school
- University

# Output Format

Provide only the chosen education level as plain text. Ensure there are no additional comments, symbols, or formatting like bold or italics. The response should consist solely of one of the three categories listed above: "Primary school", "High school", or "University". 

# Examples

- If the conversation indicates basic subject matter and simple language use, respond with "Primary school".
- For topics requiring some abstract thinking and mature responses, respond with "High school".
- For advanced discussions involving specialized knowledge, respond with "University".
        """
        learning_style_prompt = """
Determine the student's interaction style based on a conversation analysis with a teacher. Consider factors such as communication style, problem-solving approach, and question engagement. Your answer should be one of the following categories:

- Expressive
- Passive

# Steps

1. Analyze the provided conversation.
2. Evaluate the student's communication style.
3. Determine the problem-solving approach.
4. Assess the level of question engagement.
5. Categorize using the defined interaction styles.

# Output Format

Provide only the predicted learning style as plain text. Ensure there are no additional comments, symbols, or formatting like bold or italics. The response should consist solely of one of the two categories listed above: "Expressive" or "Passive".

# Examples

## Example Conversation 1
**Teacher**: What do you think of this problem?
**Student**: I think it can be solved by...
**Teacher**: Why do you believe that's the best approach?
**Student**: Because it seems efficient and addresses all points.
**Analysis**: Engages actively, offers and defends solution -> "Expressive"

## Example Conversation 2
**Teacher**: How do you find this topic?
**Student**: It's okay, I guess.
**Teacher**: Do you have any thoughts on improving it?
**Student**: Not really...
**Analysis**: Minimal engagement, passive responses -> "Passive"

# Notes

- Consider conversational nuances such as tone, enthusiasm, and body language where applicable.
- Ensure each example reflects a distinct engagement style, focusing on verbally discernible traits.
        """
        prompts = {
            "Education level": education_level_prompt,
            "Interaction style": learning_style_prompt,
        }
        return prompts


    def generate_prompt_for_conversation_quality_assessor(self):
        prompt = """
Evaluate the quality of an interaction between a teacher and a student from a provided conversation to determine a score.

Key elements of a good interaction include:
- Clear and enthusiastic presentation of information by the teacher
- Encouragement of questions and active participation
- Comfort for students in asking for clarification and expressing insights
- Opportunities for respectfully challenging ideas

Your task is to assess the conversation based on the above characteristics and provide a score.

# Output Format

The output should be a single integer score between 1 and 5, representing the quality of the interaction. Do NOT output any explanations.

# Notes

- Consider both the teacher's and student's participation.
- Higher scores reflect better adherence to the key elements.
- Do not easily give a score of 5, reserve it for truly exceptional interactions.
        """
        return prompt
