# utils.py
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel
from person_agents.single_person_agent import *
from person_agents.prompt_template.ollama_structure import *

def func_clean_up(ollama_response, prompt=""):
    cr = ollama_response.strip()
    if cr[-1] == ".":
      cr = cr[:-1]
    return cr

def func_validate(ollama_response, prompt=""):
    try: func_clean_up(ollama_response, prompt="")
    except: return False
    return True
    
def get_fail_safe():
    fs = 8
    return fs
    
