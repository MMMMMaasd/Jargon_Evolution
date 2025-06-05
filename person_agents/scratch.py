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
        
class Scratch:
    def __init__(self, f_saved):
        # WORLD INFORMATION
        # Perceived world time.
        self.curr_time = None
        # THE CORE IDENTITY OF THE PERSONA
        # Base information about the persona.
        # WORLD INFORMATION
        # Perceived world time.
        #self.curr_time = None
        # Current x,y tile coordinate of the persona.
        #self.curr_tile = None
        # Perceived world daily requirement.
       # self.daily_plan_req = None
        self.name = None
        self.first_name = None
        self.last_name = None
        self.age = None
        # L0 permanent core traits.
        self.innate = None
        # L1 stable traits.
        self.learned = None
        # L2 external implementation.
        self.currently = None
        self.belong_pirate_group = None
        self.position = None
        #self.lifestyle = None
        #self.living_area = None
        self.chatting_with = None
        # <chat> is a list of list that saves a conversation between two personas.
        # It comes in the form of: [["Dolores Murphy", "Hi"],
        #                           ["Maeve Jenson", "Hi"] ...]
        self.chat = None
        
        
        #Initialization
        if(check_if_file_exists(f_saved)):
            with open(f_saved, 'r') as json_file:
                data = json.load(json_file)
                if data["curr_time"]:
                    self.curr_time = datetime.datetime.strptime(data["curr_time"],
                                                  "%B %d, %Y, %H:%M:%S")
                else:
                    self.curr_time = None
                self.name = data["name"]
                self.first_name = data["first_name"]
                self.last_name = data["last_name"]
                self.age = data["age"]
                self.innate = data["innate"]
                self.leanred = data["learned"]
                self.currently = data["currently"]
                self.belong_pirate_group = data["belong_pirate_group"]
                self.position = data["position"]
                self.chatting_with = data["chatting_with"]
                self.chat = data["chat"]
                
    def get_str_iss(self):
        """
        ISS stands for "identity stable set." This describes the commonset summary
        of this persona -- basically, the bare minimum description of the persona
        that gets used in almost all prompts that need to call on the persona.

        INPUT
        None
        OUTPUT
        the identity stable set summary of the persona in a string form.
        EXAMPLE STR OUTPUT
        Name: Blackbeard
        Age: 30
        Innate traits: Brutal, cunning, theatrical
        Learned traits: Expert in naval ambush, skilled at reading fear
        Currently: Blackbeard is preparing to raid a merchant convoy spotted near the eastern trade route. He’s gathering his crew, loading extra gunpowder, and planning to strike at dawn when the mist is thick.
        Belonged pirate group: Blackbeard crew
        Position: Captain of the ship Queen Anne's Revenge. leader of the Blackbeard crew.
        """
        commonset = ""
        commonset += f"Name: {self.name}\n"
        commonset += f"Age: {self.age}\n"
        commonset += f"Innate traits: {self.innate}\n"
        commonset += f"Learned traits: {self.learned}\n"
        commonset += f"Currently: {self.currently}\n"
        commonset += f"Belonged pirate group: {self.belong_pirate_group}\n"
        commonset += f"Position: {self.position}\n"
        commonset += f"Current Date: {self.curr_time.strftime('%A %B %d, %Y')}\n"
        print(commonset)
        return commonset


    def get_str_name(self):
        return self.name


    def get_str_firstname(self):
        return self.first_name


    def get_str_lastname(self):
        return self.last_name


    def get_str_age(self):
        return str(self.age)


    def get_str_innate(self):
        return self.innate


    def get_str_learned(self):
        return self.learned


    def get_str_currently(self):
        return self.currently
        
    def get_str_pirate_group(self):
        return self.belong_pirate_group
        
    def get_str_position(self):
        return self.position
