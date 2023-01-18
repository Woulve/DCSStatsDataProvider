import re
import ast
import json

##The slmod log file contains an initial array, and every event is appended to the file as a lua assignment.
#So to get new data, which is not yet serialized into the first lua dict, we have to modify the dict for every line after the initial dict in the log file.
#This can be toggled in the config file by setting 'enablerealtimeupdates' to false.

#Merge two dicts together. dict.update doesn't work, for whatever reason (might be because of the lua.decode), so we have to do it manually.
def recursive_dict_merge(dict1, dict2):
    for key in dict2:
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            recursive_dict_merge(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]
    return dict1

def convert_lua_notation_to_python(lua_string: str):

    python_obj = {}

    try:
        # Split the string by '=' to separate the variable name and value
        variable, value = lua_string.strip().split(' = ', 1)

        # Validate the input string by checking if it's a correct lua assignment
        if not variable.startswith('stats[') or not variable.endswith(']'):
            raise ValueError('Invalid lua assignment')

        # Split the variable name by '[' and ']' to separate the keys
        keys = [k.strip('"]') for k in variable.split('[') if k]

        # Validate the keys by checking if they are enclosed in double quotes
        for key in keys:
            key = key.strip('"')

        # Create a nested dictionary based on the keys
        current_dict = python_obj
        for key in keys[:-1]:
            current_dict = current_dict.setdefault(key, {})

        # Evaluate the value
        try:
            value = value.replace('[','').replace(']','').replace(' = ',' : ') #object
            value = value.replace('nil','None') #None
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            pass
        current_dict[keys[-1]] = value
    except Exception as e:
        print(f"An error occured while parsing the string: {e}")
    return python_obj


def updateLuaDecoded(luadecoded_serialized, luadecoded_additions):
    additions_list = luadecoded_additions.split("\n")
    for addition in additions_list:
        if addition != "":
            try:
                luadecoded_serialized = recursive_dict_merge(luadecoded_serialized, convert_lua_notation_to_python(addition))
            except:
                return luadecoded_serialized

    return luadecoded_serialized