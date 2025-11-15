from game import PHASE_LOOKUP, PLACES
from google import genai
import json
import os

api_key = None
with open("GEMINI_API_KEY", "r") as f:
    api_key = f.readline().rstrip()

client = genai.Client(api_key=api_key)


FINAL_INSTRUCTION = """
The conversation has concluded.
You must now process the *entire* conversation history (all messages from the user) and provide a single, complete JSON object.
Do not add any text before or after the JSON.
The JSON structure must be:
{
    "my_plans": ["A list of places you are planning to go to, the player might've affected this. The places must exist"],
    "heard": ["A list of important pieces of information or dialogue the user shared that you heard."]
}
Be concise and focus only on information conveyed by the user.
"""


class Conversation:
    def __init__(self, character, phase):
        self.character = character
        self.phase = phase
        self.chat = client.chats.create(model="gemini-2.5-flash", config={"system_instruction": 
        f"""
            You are {character.get_name()}, a simple villager living in a small town.
            Your goal is to converse naturally with the user, who is another character in the town.
            You must adopt the tone and knowledge of a friendly, small-town resident.
            The small town only has these places where you can go: {", ".join(PLACES)}

            Current Knowledge:
            It is currently {PHASE_LOOKUP[phase]}.
            You are currently in {character.get_current_place()},
            You have previously been in: {", ".join(character.get_history())},
            You have previously seen: {", ".join(character.get_seen())}
            You have previously heard: {", ".join(character.get_heard())}
            You plan to go to these places next: {", ".join(character.get_plans())}
            You are going to those places at: {", ".join(PHASE_LOOKUP[phase:])} (you may only move during those times)
        """
        })

    def send_message(self, user_input):
        return self.chat.send_message(user_input)

    
    def end_conversation(self):
        final_response = self.chat.send_message(FINAL_INSTRUCTION)



        try:
            # The AI is instructed to output only JSON, so we try to parse it
            formatted_output = json.loads(final_response.text.strip())
            if len(formatted_output["my_plans"]) == len(self.character.plans):
                self.character.plans = formatted_output["my_plans"]

            for new in formatted_output["heard"]:
                self.character.add_heard(new)


        except json.JSONDecodeError:
            print("Error: Could not parse the structured output as JSON.")
            print("Raw response:")
            print(final_response.text)

