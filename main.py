from ollama import Client
from pydantic import BaseModel
import json, random, os
from dotenv import load_dotenv

class Character_attributes(BaseModel):
    dexterity: int
    perception: int
    knowledge: int
    strength: int
    mechanical: int
    technical: int

class SWD6_character(BaseModel):
    name: str
    species: str
    attributes: Character_attributes
    inventory: list[str]
    backstory: str

load_dotenv()
client = Client(host=os.environ["OLLAMA_HOST"])
attribute_list = ["dexterity", "perception", "knowledge", "strength", "mechanical", "technical"]    
preference_attributes = random.sample(attribute_list, k=random.choice([0, 1, 2, 3]))

def calculate_character_attributes(preferred: list):
    attributes = {}
    print("Preferred attributes:", preferred)
    if not preferred:
        new_list = attribute_list[:]
        random.shuffle(new_list)
        # 3D+1 for one attribute and 2D+2 for one attribute, 3D for else
        for index, attr in enumerate(new_list):
            attributes[attr] = "3D+1" if index == 0 else "2D+2" if index == len(new_list) - 1 else "3D"

        # Sorting attributes dict so that order is the same as in attribute_list
        index_map = {attribute: i for i, attribute in enumerate(attribute_list)}
        attributes = dict(sorted(attributes.items(), key=lambda item: index_map[item[0]]))
        return attributes

    else:
        if len(preferred) == 1:
            for attr in attribute_list:
                attributes[attr] = "4D+2" if attr in preferred else "2D+2"

        elif len(preferred) == 2:
            for attr in attribute_list:
                attributes[attr] = "4D+1" if attr in preferred else "2D+1"
            
        else:
            for attr in attribute_list:
                attributes[attr] = "3D+2" if attr in preferred else "2D+1"
        
        return attributes
        

def ask_create_character():
    response = client.chat(
        messages=[
            {
                "role": "user",
                "content": f"Create a character for Star Wars D6 Roleplaying game from Westend Games. Give the character a random name from Star Wars galaxy and a random Star Wars species. Leave attributes empty. Give character a very short backstory. Create a few items from Star Wars universe in inventory. Then return character in predefined format." 
            }
        ],
        model="gemma3:1b",
        format=SWD6_character.model_json_schema()
    )
    return response

response = ask_create_character()
character_json = response.message.content
SWD6_character.model_validate_json(character_json, strict=True)
character = json.loads(character_json)
character["attributes"] = calculate_character_attributes(preference_attributes)

print(f"Name: {character["name"]}")
print(f"Species: {character["species"]}")
print(f"Attributes:")
print(f" Dexterity: {character["attributes"]["dexterity"]}")
print(f" Perception: {character["attributes"]["perception"]}")
print(f" Knowledge: {character["attributes"]["knowledge"]}")
print(f" Strength: {character["attributes"]["strength"]}")
print(f" Mechanical: {character["attributes"]["mechanical"]}")
print(f" Technical: {character["attributes"]["technical"]}")
print(f"Inventory: {character["inventory"]}")
print(f"Backstory: {character["backstory"]}")






