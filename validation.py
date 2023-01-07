##########################################
#   ___ __  __ ___  ___  ___ _____ ___   #
#  |_ _|  \/  | _ \/ _ \| _ |_   _/ __|  #
#   | || |\/| |  _| (_) |   / | | \__ \  #
#  |___|_|  |_|_|  \___/|_|_\ |_| |___/  #
#                                        #
##########################################

import pandas as pd
from typing import List, Dict, Any
from pandas import DataFrame, Series 

#########################################################
#   ___  ___ ___ ___ _  _ ___ _____ ___ ___  _  _ ___   #
#  |   \| __| __|_ _| \| |_ _|_   _|_ _/ _ \| \| / __|  #
#  | |) | _|| _| | || .` || |  | |  | | (_) | .` \__ \  #
#  |___/|___|_| |___|_|\_|___| |_| |___\___/|_|\_|___/  #
#                                                       #
#########################################################


class ConvertData:
    """ Convert the series data consistenly. Behavior-Oriented Class """
    def ToDate(self, input:Series) -> Series:
        return pd.to_datetime(input, errors="coerce", infer_datetime_format=True)
    
    def ToFloat(self, input:Series) -> Series:
        return pd.to_numeric(input, errors="coerce", downcast="float")
    
    def ToInt(self, input:Series) -> Series:
        return pd.to_numeric(input, errors="coerce", downcast="integer")
    

class ProcessData:
    """ Process data. Behavior-Oriented Class """
    def __init__(self, df):
        self.df: pd.DataFrame = df
    
    def CreateDf(self):
        """ Create a dataframe reporter or validator. """
        col_del = ["Unit", "Min", "Max", "Format", "Source_Table", "Source_List"]
        
        dfr = self.df.copy()
        dfr.drop(col_del, axis=1, inplace=True)
        return dfr
    
    def UnpackData(self):
        colAttr, colMin, colMax, colSTable, colSList = self.df["Attribute_Name"], \
            self.df["Min"], self.df["Max"], self.df["Source_Table"], self.df["Source_List"]
        return colAttr, colMin, colMax, colSTable, colSList


class ValidateData:
    """ Validate the data consistently. Behavior-Oriented Class """
    def __init__(self):
        self.ConvertData = ConvertData()
        
        
    def _transform_dtype(self, input:Series, data_type:type) -> Any:
        """ Transform the input into the proper datatype. """
        if isinstance(input, list):
            input = pd.Series(input)

        if data_type=="float" or data_type==float:
            return self.ConvertData.ToFloat(input)
        elif data_type=="int" or data_type==int:
            return self.ConvertData.ToInt(input)
        elif data_type=="date":
            return self.ConvertData.ToDate(input)
        else:
            raise ValueError("The Data Type is invalid.")
    
    
    def _transform_to_number(self, inputs:list, number:int=1) -> List[int]:
        """ Convert to represented number and error. """
        if not isinstance(inputs, list):
            try:
                inputs = inputs.to_list()
            except:
                inputs = [inputs]
                
        result = [0 if input is True else number for input in inputs]
        return result
    
    
    def _bool_comparison(self, input_one:Series, input_two:Series) -> List[int]:
        """ Compare two booleans. """
        result = []
        for bool_1, bool_2 in zip(input_one, input_two):
            if not bool_1 and not bool_2:
                result.append(True)
            else:
                result.append((bool_1 and bool_2))
        return result
    
    
    def Input(self, input:Series, override:bool=False) -> List[int]:
        """ Validate if the input is a null value. """
        if isinstance(input, list):
            input = pd.Series(input)  
        
        result = ~pd.isnull(input)
        if not override:
            return self._transform_to_number(result, 2)
        return result.to_list()
    
    
    def TwoInput(self, input_one:Series, input_two:Series) -> List[int]:
        """ Validate two input, if one input is none, both gets False value. -> 
            Validating Source Table and List """
            
        valid_one = self.Input(input_one, override=True)
        valid_two = self.Input(input_two, override=True)
        valid_comp = self._bool_comparison(valid_one, valid_two)
        
        result = self._transform_to_number(valid_comp, 5)
        return result
    
    
    def Number(self, input:Series, data_type=float) -> List[int]:
        """ Validate if the input is a number or float. """
        validate = self._transform_dtype(input, data_type=data_type)
        
        result = self.Input(validate, override=True)
        result = self._transform_to_number(result, 6)
        return result
    
    
    def Date(self, input:Series) -> List[int]:
        """ Validate if the input datatype is a date. """
        validate = self._transform_dtype(input, data_type="date")
        
        result = self.Input(validate, override=True)
        result = self._transform_to_number(result, 7)
        return result
    
    
    def Characters(self, input:Series) -> List[int]:
        """ Validate if the input can be converted into numeric value. """
        # validate = []
        # for data in input:
        #     data = str(data)
        #     if data.isdigit() or data.isnumeric():
        #         validate.append(False)
        #     else:
        #         validate.append(True)
        validate = input.str.isdigit()
        
        result = self.Input(validate, override=True)
        result = self._transform_to_number(result, 8)
        return result
    
    
    def MinMax(self, input_min:Series, input_max:Series, data_type:type) -> List[int]:
        """ Compare two input values. """
        
        # Check if the data_type is string, no need to compare
        if data_type=="str" or data_type==str:
            return [1] * int(input_min.shape[0])
        
        min = self._transform_dtype(input_min, data_type)
        max = self._transform_dtype(input_max, data_type)

        result = min < max
        result = self._transform_to_number(result, 4)
        return result

    
######################################
#   ___ ___  ___   ___ ___ ___ ___   #
#  | _ | _ \/ _ \ / __| __/ __/ __|  #
#  |  _|   | (_) | (__| _|\__ \__ \  #
#  |_| ||_\\___/ \___|___|___|___/   #
#                                    #
###################################### 
    
if __name__ == "__main__":
    None