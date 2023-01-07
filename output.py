##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

from dataclasses import dataclass, field
from pandas import DataFrame, Series
from typing import List, Optional, Dict

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################

@dataclass
class OutputData:
    """ Stores the data that is validates. Data oriented class """
    input_df: DataFrame
    
    input_min:      List[int]
    input_max:      List[int]
    input_stable:   List[int]
    input_slist:    List[int]
    
    def CreateDf(self):
        self.input_df["Min"] = self.input_min
        self.input_df["Max"] = self.input_max
        self.input_df["Source Table"] = self.input_stable
        self.input_df["Source List"] = self.input_slist
        return self.input_df
        
        
######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| ||_\\___/ \___|___|___|___/   #
#                                    #
###################################### 
    
if __name__ == "__main__":
    None