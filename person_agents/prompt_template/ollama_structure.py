"""
Author: Michael Bian (zb2253@nyu.edu)

File: gpt_structure.py
Description: Wrapper functions for calling local LLama APIs.
"""
import random
import time
import uuid
import ollama
from typing import List, Dict
from pydantic import BaseModel

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def ChatGPT_single_request(prompt):
  temp_sleep()

  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
  )
  return completion["choices"][0]["message"]["content"]


# ============================================================================
# #####################[SECTION 1: CHATGPT-3 STRUCTURE] ######################
# ============================================================================

def GPT4_request(prompt):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-3's response.
  """
  temp_sleep()

  try:
    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except:
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


def ChatGPT_request(prompt):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-3's response.
  """
  # temp_sleep()
  try:
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except:
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"


def GPT4_safe_generate_response(prompt,
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False):
  prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose:
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat):

    try:
      curr_gpt_response = GPT4_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]
      
      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose:
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except:
      pass

  return False


def ChatGPT_safe_generate_response(prompt,
                                   example_output,
                                   special_instruction,
                                   repeat=3,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False):
  # prompt = 'GPT-3 Prompt:\n"""\n' + prompt + '\n"""\n'
  prompt = '"""\n' + prompt + '\n"""\n'
  prompt += f"Output the response to the prompt above in json. {special_instruction}\n"
  prompt += "Example output json:\n"
  prompt += '{"output": "' + str(example_output) + '"}'

  if verbose:
    print ("CHAT GPT PROMPT")
    print (prompt)

  for i in range(repeat):

    try:
      curr_gpt_response = ChatGPT_request(prompt).strip()
      end_index = curr_gpt_response.rfind('}') + 1
      curr_gpt_response = curr_gpt_response[:end_index]
      curr_gpt_response = json.loads(curr_gpt_response)["output"]

      # print ("---ashdfaf")
      # print (curr_gpt_response)
      # print ("000asdfhia")
      
      if func_validate(curr_gpt_response, prompt=prompt):
        return func_clean_up(curr_gpt_response, prompt=prompt)
      
      if verbose:
        print ("---- repeat count: \n", i, curr_gpt_response)
        print (curr_gpt_response)
        print ("~~~~")

    except:
      pass

  return False


# ============================================================================
# ###################[SECTION 2: ORIGINAL GPT-3 STRUCTURE] ###################
# ============================================================================

def GPT_request(prompt, gpt_parameter):
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response.
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of
                   the parameter and the values indicating the parameter
                   values.
  RETURNS:
    a str of GPT-3's response.
  """
  temp_sleep()
  try:
    response = openai.Completion.create(
                model=gpt_parameter["engine"],
                prompt=prompt,
                temperature=gpt_parameter["temperature"],
                max_tokens=gpt_parameter["max_tokens"],
                top_p=gpt_parameter["top_p"],
                frequency_penalty=gpt_parameter["frequency_penalty"],
                presence_penalty=gpt_parameter["presence_penalty"],
                stream=gpt_parameter["stream"],
                stop=gpt_parameter["stop"],)
    return response.choices[0].text
  except:
    print ("TOKEN LIMIT EXCEEDED")
    return "TOKEN LIMIT EXCEEDED"


def safe_generate_response(prompt,
                           gpt_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False):
  if verbose:
    print (prompt)

  for i in range(repeat):
    curr_gpt_response = GPT_request(prompt, gpt_parameter)
    if func_validate(curr_gpt_response, prompt=prompt):
      return func_clean_up(curr_gpt_response, prompt=prompt)
    if verbose:
      print ("---- repeat count: ", i, curr_gpt_response)
      print (curr_gpt_response)
      print ("~~~~")
  return fail_safe_response


def get_embedding(text, model="text-embedding-ada-002"):
  text = text.replace("\n", " ")
  if not text:
    text = "this is blank"
  return openai.Embedding.create(
          input=[text], model=model)['data'][0]['embedding']
          
          
# ============================================================================
# ###################[SECTION 3: LOCAL OLLAMA STRUCTURE] ###################
# ============================================================================
    
def OLLAMA_request(prompt, ollama_parameter):
  temp_sleep()
  try:
    response = ollama.chat(
                model=ollama_parameter["model"],
                messages=[{"role": "user", "content": prompt}],
                format=ollama_parameter["format"],
                stream=ollama_parameter["if_stream"])
    if (ollama_parameter["format"]):
        return response.message.content
    return response['message']['content']
  except:
    print ("ERROR DURING OLLAMA REQUEST")
    return "ERROR DURING OLLAMA REQUEST"

def OLLAMA_safe_generate_response(prompt,
                           ollama_parameter,
                           repeat=5,
                           fail_safe_response="error",
                           func_validate=None,
                           func_clean_up=None,
                           verbose=False):
  # Debug help
  if verbose:
    print (prompt)

  for i in range(repeat):
    curr_ollama_response = OLLAMA_request(prompt, ollama_parameter)
    if func_validate(curr_ollama_response, prompt=prompt):
      return func_clean_up(curr_ollama_response, prompt=prompt)
    if verbose:
      print ("---- repeat count: ", i, curr_ollama_response)
      print (curr_ollama_response)
      print ("~~~~")
  return fail_safe_response
  
def generate_prompt(curr_input, prompt_lib_file):
  """
  Takes in the current input (e.g. comment that you want to classifiy) and
  the path to a prompt file. The prompt file contains the raw str prompt that
  will be used, which contains the following substr: !<INPUT>! -- this
  function replaces this substr with the actual curr_input to produce the
  final promopt that will be sent to the GPT3 server.
  ARGS:
    curr_input: the input we want to feed in (IF THERE ARE MORE THAN ONE
                INPUT, THIS CAN BE A LIST.)
    prompt_lib_file: the path to the promopt file.
  RETURNS:
    a str prompt that will be sent to OpenAI's GPT server.
  """
  if type(curr_input) == type("string"):
    curr_input = [curr_input]
  curr_input = [str(i) for i in curr_input]

  f = open(prompt_lib_file, "r")
  prompt = f.read()
  f.close()
  for count, i in enumerate(curr_input):
    prompt = prompt.replace(f"!<INPUT {count}>!", i)
  if "<commentblockmarker>###</commentblockmarker>" in prompt:
    prompt = prompt.split("<commentblockmarker>###</commentblockmarker>")[1]
  return prompt.strip()






















