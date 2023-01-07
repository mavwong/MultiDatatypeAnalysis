#################################################################
##            _ _ _                                            ##
##  __      _(_) | | _____      __                             ##
##  \ \ /\ / / | | |/ _ \ \ /\ / /                             ##
##   \ V  V /| | | | (_) \ V  V /                              ##
##    \_/\_/ |_|_|_|\___/ \_/\_/                               ##
##     _         _                        _   _                ##
##    /_\  _   _| |_ ___  _ __ ___   __ _| |_(_) ___  _ __     ##
##   //_\\| | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \    ##
##  /  _  \ |_| | || (_) | | | | | | (_| | |_| | (_) | | | |   ##
##  \_/ \_/\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|   ##
##                                                             ##
################################################################# 

##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

import pandas as pd
from pathlib import Path
import time

from utils import print_section
from enums import ValidationDataType
from scoring import ValidationScore
from validation import ValidateData, ProcessData
from output import OutputDF

#############################################
#   ___ _____ _   _  _ ___   _   ___ ___    #
#  / __|_   _/_\ | \| |   \ /_\ | _ |   \   #
#  \__ \ | |/ _ \| .` | |) / _ \|   | |) |  #
#  |___/ |_/_/ \_|_|\_|___/_/ \_|_|_|___/   #
#                                           #
#############################################


# Paths
PATH_FILE = Path(__file__).parent.resolve()
PATH_DATA = PATH_FILE / "data"
PATH_RAW_DATA = PATH_DATA / "raw_data"
PATH_OUTPUT = PATH_FILE / "output"

# Input File
INPUT_CSV = PATH_RAW_DATA / "sample.csv"

# Output Files
OUTPUT_NAME = str(INPUT_CSV.stem) + "_valid.xlsx"
OUTPUT_CSV = PATH_OUTPUT / OUTPUT_NAME

# Global Variables
TEST = False
RUN_MAIN = True
EXPORT = True
CONV_SCORE = False


#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################


def load_csv(input_path:Path) -> pd.DataFrame:
    """ Load CSV based on the path. """
    df = pd.read_csv(input_path)
    return df

def error_compare(main_list:list, error_list:list) -> list:
    """ Compare two list """
    result = []
    for index, data in enumerate(main_list):
        if int(data)==int(0):
            result.append(error_list[index])
        else:
            result.append(int(data))
    return result

def scoring_compare(*error_lists:list) -> list:
    result = len(error_lists[0]) * [0]
    for x in error_lists:
        result = error_compare(x, result)
    return result

def getScore(input_df:pd.DataFrame) -> pd.DataFrame:
    """ Get Score representation based on number list or series. """
    valid_score = ValidationScore()
    result_df = valid_score.get_score(input_df=input_df)
    return result_df
    

######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| ||_\\___/ \___|___|___|___/   #
#                                    #
###################################### 

df = pd.read_excel(OUTPUT_CSV)

df_result = getScore(df)