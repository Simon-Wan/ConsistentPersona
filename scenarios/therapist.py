from scenarios.utils import Scenario

class Therapist(Scenario):
    agent_name = 'Therapist'
    user_name = 'Patient'
    user_types = {
        "Mental Health Conditions": [
            "Depression", 
            "Generalized Anxiety Disorder (GAD)", 
            "Bipolar Disorder", 
            "Obsessive-Compulsive Disorder (OCD)", 
            "Schizophrenia"
        ],
        "Interaction style": ["Expressive", "Passive"]
    }
    topics = [
        "Therapy"
    ]
    
    def generate_prompt_for_oracle_agent(self, user_type, scenario):
        background = ''
        for key in user_type:
            background += f'{key}: {user_type[key]}. '
        prompt = f"""
In this task, you will simulate a conversation with a patient seeking help. You will adopt the role of a therapist, ensuring sensitivity to the patient's background and adapting your responses accordingly.

- **Scenario**: {scenario}
- **Patient Background**: {background}

# Output Format

Your output should start with "Therapist: ".
        
# Notes
        
- Ensure your responses are empathetic and tailored to the patient's condition and interaction style.
- Use the patient's background information as a guide but avoid directly referencing it.
- Keep each utterance concise to encourage patient interaction before continuing the conversation.
        """
        return prompt

    def generate_prompt_for_user_candidate(self, user_type, topic, use_vanilla=False):
        background = ''
        for key in user_type:
            background += f'{key}: {user_type[key]}. '
        if use_vanilla:
            prompt = f"""
In this task, you will simulate a conversation with a teacher who is instructing on a specific topic. You will adopt the role of a student, ensuring consistency with the given background information.

- **Student Background**: {background}

# Output Format

Your output should start with "Student: ".
"""
        else:
            prompt = f"""
In this task, you will simulate a conversation with a therapist. You will adopt the role of a patient seeking help, ensuring consistency with the given background information.

- **Patient Background**: {background}
- **Scenario Description**: {self.__get_description_from_background__(user_type)}

# Output Format

Your output should start with "Patient: ".

# Notes

- Maintain consistency with the provided patient background throughout the conversation.
- The dialogue should be natural, reflecting the patient's condition and interaction style.
- Keep each utterance concise to allow for therapist interaction before continuing the conversation.
        """
        return prompt

    def generate_prompt_for_user_type_classifier(self):
        condition_prompt = """
Analyze the conversation between a therapist and a patient to determine the primary mental health condition discussed. Consider factors such as symptom descriptions, language use, and patient concerns. Your answer should be one of the following categories:

- Depression
- Generalized Anxiety Disorder (GAD)
- Bipolar Disorder
- Obsessive-Compulsive Disorder (OCD)
- Schizophrenia

# Output Format

Provide only the identified condition as plain text. Ensure there are no additional comments, symbols, or formatting like bold or italics. The response should consist solely of one of the categories listed above:
 "Depression",  "Generalized Anxiety Disorder (GAD)", "Bipolar Disorder", "Obsessive-Compulsive Disorder (OCD)", or "Schizophrenia"
        """
        interaction_style_prompt = """
Determine the patient's interaction style based on a conversation analysis with a therapist. Consider factors such as communication style, emotional expressiveness, and question engagement. Your answer should be one of the following categories:

- Expressive
- Passive

# Steps

1. Analyze the provided conversation.
2. Evaluate the patient's communication style.
3. Assess the emotional tone and engagement level.
4. Categorize using the defined interaction styles.

# Output Format

Provide only the predicted interaction style as plain text. Ensure there are no additional comments, symbols, or formatting like bold or italics. The response should consist solely of one of the two categories listed above: "Expressive" or "Passive".

# Notes

- Consider conversational nuances such as tone, enthusiasm, and depth of responses.
        """
        prompts = {
            "Mental Health Conditions": condition_prompt,
            "Interaction style": interaction_style_prompt,
        }
        return prompts

    def generate_prompt_for_conversation_quality_assessor(self):
        prompt = """
Evaluate the quality of an interaction between a therapist and a patient from a provided conversation to determine a score.

Key elements of a good interaction include:
- Active listening and empathy from the therapist
- Clear communication and validation of patient feelings
- Encouragement for the patient to express themselves and explore their emotions
- Responsiveness to the patient's concerns without judgment

Your task is to assess the conversation based on the above characteristics and provide a score.

# Output Format

The output should be a single integer score between 1 and 5, representing the quality of the interaction. Do NOT output any explanations.

# Notes

- Consider both the therapist's and patient's participation.
- Higher scores reflect better adherence to the key elements.
- Reserve a score of 5 for truly exceptional interactions.
        """
        return prompt

    def __get_description_from_background__(self, background):
        res_builder = ""

        # Mental Health Conditions
        if background["Mental Health Conditions"] == "Depression":
            res_builder += "The patient is experiencing persistent sadness, loss of interest, and fatigue, consistent with major depressive disorder."
        elif background["Mental Health Conditions"] == "Generalized Anxiety Disorder (GAD)":
            res_builder += "The patient experiences excessive worry and physical symptoms such as restlessness and muscle tension."
        elif background["Mental Health Conditions"] == "Bipolar Disorder":
            res_builder += "The patient exhibits alternating episodes of mania and depression."
        elif background["Mental Health Conditions"] == "Obsessive-Compulsive Disorder (OCD)":
            res_builder += "The patient deals with intrusive thoughts and compulsive behaviors."
        elif background["Mental Health Conditions"] == "Schizophrenia":
            res_builder += "The patient shows disturbances in thought processes, including hallucinations and delusions."

        # Interaction style
        if background["Interaction style"] == "Expressive":
            res_builder += " The patient is talkative, actively sharing their thoughts and emotions."
        elif background["Interaction style"] == "Passive":
            res_builder += " The patient is Passive, providing minimal responses and requiring more encouragement to engage."

        return res_builder
