# scratch.py
import datetime
import json
import sys

def check_if_file_exists(file_path_to_check):
    try:
        with open(file_path_to_check) as temp : pass
        return True
    except:
        return False
        
class JargonDict:
    def __init__(self, f_saved):
        self.jargon_dict = None
        
        
        #Initialization
        if(check_if_file_exists(f_saved)):
            with open(f_saved, 'r') as json_file:
                data = json.load(json_file)
                self.jargon_dict = data
                
    def get_full_dict_str(self):
        """
        EXAMPLE STR OUTPUT
        set sail: Wash the pineapple
        kill him: Cutting the apple
        """
        commonset = ""
        for key, value in self.jargon_dict.items():
            commonset += f"{key}: {value}\n"
        return commonset


    def jargon_translate_to_word(self, jargon):
        for key, value in self.jargon_dict.items():
            if(value == jargon):
                return key
        return "Can't find in dict"
    
    def word_translate_to_jargon(self, word):
        if word in self.jargon.keys():
            return self.jargon_dict[word]
        return "Can't find in dict"

            
