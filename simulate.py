# pirate_agent.py
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel
from person_agents.single_person_agent import *
from person_agents.prompt_template.ollama_structure import *
from utils import *

class JargonWord(BaseModel):
    jargon: str
    meaning: str
    jargon_user: str
    backrgound: str
    
if __name__ == '__main__':
    # EXAMPLE USAGE
    blackbeard = SinglePirateAgent("blackbeard")
    blackbeard.generate_new_jargon("Grab the Women", 10)
    """
    blackbeard_iss = blackbeard.get_iss()
    blackbeard_known_jargon = blackbeard.known_jargon.get_full_dict_str()
    example_big_event = "Yesterday, the Black Death broke out in the entire sea area. It was a disease that no one had ever seen before. A large number of people got sick and black ulcers appeared on their skin and they died painfully. We have never seen such a large-scale disease disaster."
    prompt_input = [blackbeard_iss, blackbeard_known_jargon, "Blackbeard", example_big_event, "Grab the woman"]
    ollama_param = {"model": blackbeard.model, "format": JargonWord.model_json_schema(), "if_stream": False}
    prompt_template = "person_agents/prompt_template/single_jargon_word_translation.txt"
    prompt = generate_prompt(prompt_input, prompt_template)
    print(prompt)
    fail_safe = get_fail_safe()
    output = OLLAMA_safe_generate_response(prompt, ollama_param, 5, fail_safe,
                                   __func_validate, __func_clean_up)
    correct_form_output = JargonWord.model_validate_json(output)
    print(correct_form_output)
    """
