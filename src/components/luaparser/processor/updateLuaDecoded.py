import re
import ast

##The slmod log file contains an initial array, and every event is appended to the file as a lua assignment.
#So to get new data, which is not yet serialized into the first lua dict, we have to modify the dict for every line after the initial dict in the log file.
#This might cause performance issues for very long log files, because we have to loop over the whole file.
#This can be toggled in the config file by setting 'enablerealtimeupdates' to false.

#Merge two dicts together. dict.update doesn't work, for whatever reason (might be because of the lua.decode), so we have to do it manually.
def recursive_dict_merge(dict1, dict2): 
    for key in dict2:
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            recursive_dict_merge(dict1[key], dict2[key])
        else:
            dict1[key] = dict2[key]
    return dict1

#makes a list of keys and a value into a usable python dict, like {'stats': {'ef202237873822643b1f533fc865a353': {'times': {'F-14B':{'total':10.005}}}}}
def array_to_dict(keys, value):
    if isinstance(value, str) and '.' in value:
        value = float(value)
    for key in reversed(keys):
        value = {key: value}
    return value

#changes the lua notation of e.g. stats["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = 10.005 to be a list of each key, with the value
def convert_lua_notation_to_python(lua):
    assignment = lua.split(" = ", 1)[0]
    tablename = re.match(r"^\w+", assignment).group()
    assignment = re.sub(r"^\w+\[", "[", assignment)
    assignment = re.sub(r'\"\]\[\"', ',', assignment)
    assignment = re.sub(r'\[\"', '', assignment)
    assignment = re.sub(r'\"\]', '', assignment)
    assignment_list = assignment.split(",")
    assignment_list.insert(0, tablename)
    value = lua.split(" = ", 1)[1]
    value = re.sub(r" ", "", value)
    value = re.sub(r'true', 'True', value)
    value = re.sub(r'false', 'False', value)
    
    if re.match(r"\{", value):#if value is a dict
        value = re.sub(r"\[", "", value)
        value = re.sub(r"\]", "", value)
        value = re.sub(r"\=", ":", value)
        value = ast.literal_eval(value)
    return array_to_dict(assignment_list, value)

def updateLuaDecoded(luadecoded_serialized, luadecoded_additions):
    additions_list = luadecoded_additions.split("\n")
    for addition in additions_list:
        if addition != "":
            try:
                luadecoded_serialized = recursive_dict_merge(luadecoded_serialized, convert_lua_notation_to_python(addition))
            except:
                return ''

    return luadecoded_serialized