# pirate_agent.py
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel

class JargonWord(BaseModel):
    jargon: str
    meaning: str
    jargon_user: str
    backrgound: str

class SinglePirateAgent:
    #persona = 人格
    def __init__(self, name: str, persona: str, model: str = "llama3"):
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
        self.persona = persona
        # Python dict with key as string and value as string
        self.memory: List[Dict[str, str]] = []
        self.memory = []
        self.model = model

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
