# pirate_agent.py
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel
from person_agents.single_person_agent import *
from person_agents.prompt_template.ollama_structure import *

class JargonWord(BaseModel):
    jargon: str
    meaning: str
    jargon_user: str
    backrgound: str

def __func_clean_up(ollama_response, prompt=""):
    cr = ollama_response.strip()
    if cr[-1] == ".":
      cr = cr[:-1]
    return cr

def __func_validate(ollama_response, prompt=""):
    try: __func_clean_up(ollama_response, prompt="")
    except: return False
    return True
    
def get_fail_safe():
    fs = 8
    return fs
    
if __name__ == '__main__':
    # EXAMPLE USAGE
    blackbeard = SinglePirateAgent("blackbeard", "You are a medieval pirate who is good at communicating in English jargon. Your answers can only be in English.")
    example_iss = """
       Name: Blackbeard
       Age: 30
       Innate traits: Brutal, cunning, theatrical
       Learned traits: Expert in naval ambush, skilled at reading fear
       Currently: Blackbeard is preparing to raid a merchant convoy spotted near the eastern trade route. He’s gathering his crew, loading extra gunpowder, and planning to strike at dawn when the mist is thick.
      Belonged pirate group and position: Captain of the ship Queen Anne's Revenge. leader of the Blackbeard crew.
    """.strip()
    
    example_known_jargon = """
        set sail: Wash the pineapple
        kill him: Cutting the apple
    """
    example_big_event = "Yesterday, the Black Death broke out in the entire sea area. It was a disease that no one had ever seen before. A large number of people got sick and black ulcers appeared on their skin and they died painfully. We have never seen such a large-scale disease disaster."
    prompt_input = [example_iss, example_known_jargon, "Blackbeard", example_big_event, "Grab the woman"]
    ollama_param = {"model": blackbeard.model, "format": JargonWord.model_json_schema(), "if_stream": False}
    prompt_template = "person_agents/prompt_template/single_jargon_word_translation.txt"
    prompt = generate_prompt(prompt_input, prompt_template)
    fail_safe = get_fail_safe()
    output = OLLAMA_safe_generate_response(prompt, ollama_param, 5, fail_safe,
                                   __func_validate, __func_clean_up)
    correct_form_output = JargonWord.model_validate_json(output)
    print(correct_form_output)
 
