##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

from typing import List, Dict
from pandas import DataFrame, Series

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################


class ValidationScore:
    """ Scoring for the Validator. The scoring is meant for easier  """
    def __init__(self):
        self.score = {
            0:"", # Valid
            1:"", # Data is not validated
            2:"", # Data is null
            
            3:"Error: Table or Lists are not found.", 
            4:"Error: Value comparison invalid.",
            5:"Error: Both values must be present.",
            
            6:"Error: Datatype must be a number or an integer.",
            7:"Error: Datatype must be a date.",
            8:"Error: Datatype must be a string.",
            9:"Error: Value out of range."
        }
        
        self.score_complete = {
            0:"Valid Data.", # Valid
            1:"Value is not validated.", # Data is not validated
            2:"Value is null.", # Data is null
            
            3:"Error: Table or Lists are not found.", 
            4:"Error: Value comparison invalid.",
            5:"Error: Both values must be present.",
            
            6:"Error: Datatype must be a number or an integer.",
            7:"Error: Datatype must be a date.",
            8:"Error: Datatype must be a string.",
            9:"Error: Value out of range."
        }
    
    def get_score(self, input_df:DataFrame, complete:bool=False) -> DataFrame:
        """ Based on the input integer, get the equivalent score. """
        ref_cols = ["Min", "Max", "Source Table", "Source List"]
        
        result_df = input_df.copy()
        if complete:
            result_df[ref_cols] = result_df[ref_cols].replace(
                to_replace=self.score_complete
            )
        else:
            result_df[ref_cols] = result_df[ref_cols].replace(
                to_replace=self.score
            )
        return result_df
    
    
######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| ||_\\___/ \___|___|___|___/   #
#                                    #
###################################### 
    
if __name__ == "__main__":
    None