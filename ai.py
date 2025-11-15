from game import PHASE_LOOKUP, PLACES
from google import genai
import json
import os
from pydantic import BaseModel, Field
from typing import List, Optional


# AI output json schema
class AIOutput(BaseModel):
    my_plans: List[str]
    heard: List[str]


api_key = None
with open("GEMINI_API_KEY", "r") as f:
    api_key = f.readline().rstrip()

client = genai.Client(api_key=api_key)




FINAL_INSTRUCTION = f"""
The conversation has concluded.
You must now process the *entire* conversation history (all messages from the user) and provide a single, complete JSON object.
Do not add any text before or after the JSON.
The JSON structure must be:
{{
    "my_plans": ["A list of places you are planning to go to, the player might've affected this. The allowed places are: {', '.join(PLACES)}"],
    "heard": ["A list of important pieces of information or dialogue the user shared that you heard."]
}}
Be concise and focus only on information conveyed by the user.
"""


class Conversation:
    def __init__(self, me, character, phase):
        self.me = me
        self.character = character
        self.phase = phase

        next_places = [f"{place} at {time}" for place, time in zip(character.get_plans(), PHASE_LOOKUP[phase+1:])]
        self.chat = client.chats.create(model="gemini-2.5-flash", config={"system_instruction": 
        f"""
            You are {character.get_name()}, a simple villager living in a small town.
            Your goal is to converse naturally with the user, who is another character in the town.
            Try to keep your responses short.
            You must adopt the tone and knowledge of a friendly, small-town resident.
            The small town only has these places where you can go: {", ".join(PLACES)}

            Current Knowledge:
            It is currently {PHASE_LOOKUP[phase]}.
            You are currently in {character.get_current_place()},
            You are talking to {self.me.get_name()},
            You have previously been in: {", ".join(character.get_history())},
            You have previously seen: {", ".join(character.get_seen())},
            You have previously heard: {", ".join(character.get_heard())},
            You plan to go to these places next: {", ".join(next_places)} (you may only move during those times),
            Your plan is flexible, you can deviate from it if someone asks you to.
        """
        })

    def send_message(self, user_input):
        return self.chat.send_message(user_input)

    
    def end_conversation(self):
        final_response = self.chat.send_message(FINAL_INSTRUCTION, config={
            "response_mime_type": "application/json",
            "response_json_schema": AIOutput.model_json_schema(),
        })

        try:
            # The AI is instructed to output only JSON, so we try to parse it
            formatted_output = AIOutput.model_validate_json(final_response.text.strip())

            for i in range(len(formatted_output.my_plans)):
                new_plan = formatted_output.my_plans[i]
                if i < len(self.character.plan):
                    self.character.plan[i] = formatted_output.my_plans[i]
                else:
                    self.character.plan.append(new_plan)
                

            for new in formatted_output.heard:
                self.character.add_heard(f"{self.me.get_name()} said: {new}")
            


        except json.JSONDecodeError:
            print("Error: Could not parse the structured output as JSON.")
            print("Raw response:")
            print(final_response.text)


# Detective output json schema
class DetectiveOutput(BaseModel):
    suspect: str

DETECTIVE_FINAL_INSTRUCTION = """
    The interrogation has concluded.
    You must now process the *entire* conversation history (all messages from the user) and provide a single, complete JSON object.
    Do not add any text before or after the JSON.
    The JSON structure must be:
    {{
        "suspect": "name of the suspect you think has committed the murder"
    }}
    Be concise and focus only on information conveyed by the user.
    """

class DetectiveConversation:
    def __init__(self, character):
        self.character = character

        self.question_limit = 10
        self.chat = client.chats.create(model="gemini-2.5-flash", config={"system_instruction": 
        f"""
            You are Detective Prime, an elite investigative AI tasked with solving a fictional murder case. A homicide has occurred, and there is a defined list of suspects.
            Your mission is to identify the killer using strategic questioning.
            Begin by analyzing the known facts of the murder.
            Evaluate all suspects and form preliminary hypotheses.
            Decide which suspects to interrogate based on logical leads and inconsistencies.
            You may ask only a limited number of questions in total.
            Each question must be:
            - Highly targeted
            - Evidence-driven
            - Designed to uncover contradictions, motives, alibis, or hidden information
            After each answer, reassess your strategy and update your working theory.
            Prioritize questions that close knowledge gaps or test suspect statements.
            Keep a clear list of facts, clues, contradictions, and suspect profiles.
            Make deductions explicitly and logically.
            Avoid assumptions not grounded in provided evidence.
            When confident, identify the most likely culprit.
            Provide a clear explanation of your reasoning and the evidence that led to your conclusion.
            You have {self.question_limit} questions to solve the murder, use them wisely.
        """
        })

    def send_message(self, user_input):
        return self.chat.send_message(user_input)

    
    def end_conversation(self):
        final_response = self.chat.send_message(DETECTIVE_FINAL_INSTRUCTION, config={
            "response_mime_type": "application/json",
            "response_json_schema": DetectiveOutput.model_json_schema(),
        })

        try:
            # The AI is instructed to output only JSON, so we try to parse it
            formatted_output = DetectiveOutput.model_validate_json(final_response.text.strip())

            return formatted_output.suspect
            


        except json.JSONDecodeError:
            print("Error: Could not parse the structured output as JSON.")
            print("Raw response:")
            print(final_response.text)






