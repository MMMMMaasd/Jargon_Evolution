# pirate_agent.py
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel
from person_agents.scratch import *
from person_agents.known_jargon import *
from person_agents.prompt_template.ollama_structure import *
from utils import func_clean_up, func_validate
import os

class JargonWord(BaseModel):
    jargon: str
    meaning: str
    jargon_user: str
    backrgound: str
    
class SinglePirateAgent:
    #persona = 人格
    def __init__(self, name: str, model: str = "llama3"):
        self.name = name
        
        """
        Stanford's generative agents memory design
        # PERSONA MEMORY
        # If there is already memory in folder_mem_saved, we load that. Otherwise,
        # we create new memory instances.
        # <s_mem> is the persona's spatial memory.
        f_s_mem_saved = f"{folder_mem_saved}/bootstrap_memory/spatial_memory.json"
        self.s_mem = MemoryTree(f_s_mem_saved)
        # <s_mem> is the persona's associative memory.
        f_a_mem_saved = f"{folder_mem_saved}/bootstrap_memory/associative_memory"
        self.a_mem = AssociativeMemory(f_a_mem_saved)
        # <scratch> is the persona's scratch (short term memory) space.
        scratch_saved = f"{folder_mem_saved}/bootstrap_memory/scratch.json"
        self.scratch = Scratch(scratch_saved)
        """
        
        self.id = str(uuid.uuid4())
        # Python dict with key as string and value as string
        self.memory: List[Dict[str, str]] = []
        self.memory = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        scratch_saved = os.path.join(base_dir, name, "bootstrap_memory", "scratch.json")
        print(scratch_saved)
        self.scratch = Scratch(scratch_saved)
        self.model = model
        known_jargon_saved = os.path.join(base_dir, name, "bootstrap_memory", "known_jargons.json")
        self.known_jargon = JargonDict(known_jargon_saved)
    
    def get_iss(self):
        return self.scratch.get_str_iss()
    
    
    def generate_new_jargon(self, word, terminate_cond):
        iss = self.get_iss()
        known_jargon_str = self.known_jargon.get_full_dict_str()
        example_big_event = "Yesterday, the Black Death broke out in the entire sea area. It was a disease that no one had ever seen before. A large number of people got sick and black ulcers appeared on their skin and they died painfully. We have never seen such a large-scale disease disaster."
        prompt_input = [iss, known_jargon_str, self.name, example_big_event, word]
        ollama_param = {"model": self.model, "format": JargonWord.model_json_schema(), "if_stream": False}
        prompt_template = "person_agents/prompt_template/single_jargon_word_translation.txt"
        prompt = generate_prompt(prompt_input, prompt_template)
        print(prompt)
        def get_fail_safe():
            fs = 8
            return fs
        fail_safe = get_fail_safe()
        start_counter = 0
        while(start_counter <= terminate_cond):
            output = OLLAMA_safe_generate_response(prompt, ollama_param, 5, fail_safe, func_validate, func_clean_up)
            print(output)
            correct_form_output = JargonWord.model_validate_json(output)
            new_jargon = correct_form_output.jargon
            new_word = correct_form_output.meaning
            if ((self.known_jargon.jargon_translate_to_word(new_jargon) == "Can't find in dict") and new_word == word):
                self.known_jargon.jargon_dict[word] = new_jargon
                base_dir = os.path.dirname(os.path.abspath(__file__))
                known_jargon_saved = os.path.join(base_dir, self.name, "bootstrap_memory", "known_jargons.json")
                with open(known_jargon_saved, 'w') as outfile:
                    outfile.write(json.dumps(self.known_jargon.jargon_dict, indent=2))
                return correct_form_output
            start_counter += 1
        return False
        
        
    # Let's say we want to ask a single priate to translate a English word to a jargon word
    def translate_jargon(self, prompt_message: str) -> str:
        messages = [{"role": "system", "content": self.persona}]
        messages += self.memory[-5:] # Last five memory
        messages.append({"role": "user", "content": prompt_message}) # main prompt for this say
        """
        messages=[
        {'role': 'system', 'content': '你是一个中世纪海盗'},
        {'role': 'user', 'content': '帮我起一个黑话名字，用来代指“藏宝图”'}
        ]
        """
        response = ollama.chat(model=self.model, messages=messages, format=JargonWord.model_json_schema())
        jargon_translation = JargonWord.model_validate_json(response.message.content)
        #reply = response['message']['content']
        self.memory.append({"role": "user", "content": prompt_message})
        self.memory.append({"role": "assistant", "content": jargon_translation})
        # We need a language detection model here to make sure it is in english
        return jargon_translation

if __name__ == '__main__':
    blackbeard = SinglePirateAgent("blackbeard", "You are a medieval pirate who is good at communicating in English jargon. Your answers can only be in English.")
    prompt_message = """
        Give me a pirate jargon name for this word: Treasure Map.
        Everything include the jargon itself must be in English, no other language!

        Return your answer strictly in JSON with the following format:
        {
        "jargon": <jargon name>,
        "meaning": <original word>,
        "jargon_speaker": <who speak this jargon>
        "background": <story of where this jargon come from>
        }
        """.strip()
    jargon_translation = blackbeard.translate_jargon(prompt_message)
    print(jargon_translation)
