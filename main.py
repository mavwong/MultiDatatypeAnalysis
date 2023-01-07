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
from enums import ValidationDataType, CAT_DTYPES_NAME, CAT_DTYPES_VALUE
from scoring import ValidationScore
from validation import ValidateData, ProcessData
from output import OutputData

from typing import List, Dict, Optional
from pandas import DataFrame, Series 

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
OUTPUT_PROCESSING = PATH_OUTPUT / "processing.xlsx"

# Global Variables
RUN_TEST =      False
RUN_MAIN =      True
EXPORT =        True


#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################


def _compare(main_list:list, error_list:list) -> List[int]:
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
        result = _compare(x, result)
    return result

def score(input_df:pd.DataFrame, complete:bool=False) -> pd.DataFrame:
    """ Get Score representation based on number list or series. """
    valid_score = ValidationScore()
    if complete:
        result_df = valid_score.get_score(input_df=input_df, complete=True)
    else:
        result_df = valid_score.get_score(input_df=input_df, complete=False)
    return result_df

def drop_categories(input_df:DataFrame, columns:str, categories:Series) -> DataFrame:
    """ Drop inconsistent categories. """
    inc_cats = set(input_df[columns]).difference(categories)
    inc_rows = input_df[columns].isin(inc_cats)
    
    # Inconsistent data vs Consistent Data
    inc_datas = input_df[inc_rows]
    con_datas = input_df[~inc_rows]
    return con_datas

def load_and_process_data(input_path:Path, export:bool=False) -> DataFrame:
    """ Load csv. Process the dataframe. """
    if not isinstance(input_path, Path):
        input_path = Path(input_path)
        
    df = pd.read_csv(input_path)
    
    # Process the data type
    df = df.astype({
        "Attribute_Name":"object", 
        "Validation_Type":"category",
        "Min":"object",
        "Max":"object",
        "Unit / Format":"object"
    })
    
    # Remove whitespaces from the column
    df["Attribute_Name"].str.strip()
    
    # Make categories consistent
    df = drop_categories(df, "Validation_Type", CAT_DTYPES_NAME)
    
    # Drop duplicates
    df.drop_duplicates(subset=['Attribute_Name'], keep='first', inplace=True)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    # Export to excel
    if export:
        df.to_excel(OUTPUT_PROCESSING)
    return df


######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| ||_\\___/ \___|___|___|___/   #
#                                    #
###################################### 


def test() -> None:
    None

def main() -> None:
    df = load_and_process_data(INPUT_CSV, export=True)
    dfg = df.groupby("Validation_Type")
    
    # Group the datatype with the same process.
    same_process = ["Date", "Integer", "Number"]
    
    result_df = []
    validate = ValidateData()
    
    for current_dtype in ValidationDataType:
        for grp_name, grp_df in dfg:
            
            # Date, Integer, Number Process
            if current_dtype.name == grp_name and current_dtype.name in same_process:
                process = ProcessData(grp_df)
                
                dfg_number = process.CreateDf()
                _, colMin, colMax, colSTable, colSList = process.UnpackData()
                
                # VALIDATE MIN, MAX AND MINMAX COMPARISON
                vldMinMax_boolcomp = validate.TwoInput(colMin, colMax)
                vldColMin_na = validate.Input(colMin) 
                vldColMax_na = validate.Input(colMax)
                
                if current_dtype.name == ValidationDataType.Number.name or \
                    current_dtype == ValidationDataType.Integer.name:
                    vldColMin_dt = validate.Number(colMin, data_type=current_dtype.value)
                    vldColMax_dt = validate.Number(colMax, data_type=current_dtype.value)
                    vldColMinMax = validate.MinMax(colMin, colMax, data_type=current_dtype.value)
                elif current_dtype.name == ValidationDataType.Date.name:
                    vldColMin_dt = validate.Date(colMin)
                    vldColMax_dt = validate.Date(colMax)
                    vldColMinMax = validate.MinMax(colMin, colMax, data_type=current_dtype.value)
                
                # VALIDATION SOURCE TABLE AND SOURCE LIST
                vldColSources_boolcomp = validate.TwoInput(colSTable, colSList)
                vldColSTable_na = validate.Input(colSTable)
                vldColSList_na = validate.Input(colSList)
                
                # ERROR AND COMPARE - MIN COLUMN
                vldColMin = scoring_compare(
                    vldMinMax_boolcomp, 
                    vldColMin_na, 
                    vldColMin_dt, 
                    vldColMinMax
                )
                
                # ERROR AND COMPARE - MAX COLUMN
                vldColMax = scoring_compare(
                    vldMinMax_boolcomp, 
                    vldColMax_na, 
                    vldColMax_dt, 
                    vldColMinMax
                )
                
                # ERROR AND COMPARE - SOURCE TABLE and SOURCE LIST
                vldColSTable = scoring_compare(vldColSources_boolcomp,vldColSTable_na)
                vldColSList = scoring_compare(vldColSources_boolcomp,vldColSList_na)
                
                # DATAFRAME VALIDATOR
                output_data = OutputData(
                    input_df=dfg_number,
                    input_min=vldColMin,
                    input_max=vldColMax,
                    input_stable=vldColSTable,
                    input_slist=vldColSList
                )
                
                # CREATE DATAFRAME VALIDATOR
                result_df.append(output_data.CreateDf())
                

            elif current_dtype.name == grp_name:
                process = ProcessData(grp_df)
            
                dfg_text = process.CreateDf()
                _, colMin, colMax, colSTable, colSList = process.UnpackData()
                
                # VALIDATE MIN, MAX AND MINMAX COMPARISON
                vldMinMax_boolcomp = validate.TwoInput(colMin, colMax)
                vldColMin_na = validate.Input(colMin) 
                vldColMax_na = validate.Input(colMax)
                vldColMin_dt = validate.Characters(colMin)
                vldColMax_dt = validate.Characters(colMax)
                vldColMinMax = validate.MinMax(colMin, colMax, current_dtype.value)
                
                # VALIDATION SOURCE TABLE AND SOURCE LIST
                vldColSources_boolcomp = validate.TwoInput(colSTable, colSList)
                vldColSTable_na = validate.Input(colSTable)
                vldColSList_na = validate.Input(colSList)
                
                # ERROR AND COMPARE - MIN COLUMN
                vldColMin = scoring_compare(vldColMin_dt, vldColMinMax)
                
                # ERROR AND COMPARE - MAX COLUMN
                vldColMax = scoring_compare(vldColMax_dt, vldColMinMax)
                
                # ERROR AND COMPARE - SOURCE TABLE and SOURCE LIST
                vldColSTable = scoring_compare(vldColSources_boolcomp,vldColSTable_na)
                vldColSList = scoring_compare(vldColSources_boolcomp,vldColSList_na)

                # DATAFRAME VALIDATOR
                output_data = OutputData(
                    input_df=dfg_text,
                    input_min=vldColMin,
                    input_max=vldColMax,
                    input_stable=vldColSTable,
                    input_slist=vldColSList
                )
                
                # CREATE DATAFRAME VALIDATOR
                result_df.append(output_data.CreateDf())
                
                
    # Concat and Final processing
    df_output = pd.concat(result_df)
    df_output.sort_index(inplace=True)
    
    # Convert the score into string representation
    df_output_rep = score(df_output, complete=False)
    df_output_comp = score(df_output, complete=True)
        
    # Write the dataframe to excel file
    if EXPORT:
        with pd.ExcelWriter(OUTPUT_CSV) as writer:
            df_output.to_excel(writer,      sheet_name="1-Score")
            df_output_rep.to_excel(writer,  sheet_name="2-Representation")
            df_output_comp.to_excel(writer, sheet_name="3-Complete")


if __name__ == "__main__":
    start_time = time.time()
    
    if RUN_TEST:
        print_section("Running test")
        test()
    
    if RUN_MAIN:
        print_section("Running main")
        main()
    
    time_diff = time.time() - start_time
    print_section(f"File Commenced. \t\tTime: {time_diff:.4f}s")