from collections import defaultdict
import re



def updateLuaDecoded(luadecoded_serialized, luadecoded_additions):
    stats = luadecoded_serialized["stats"]
    # luadecoded_serialized["stats"]["ef202237873822643b1f533fc865a353"]["times"]["F-14B"]["total"] = 10.005
    # add_key(stats, ["ef202237873822643b1f533fc865a353","times","F-14B","total"], { ["total"] : 0, ["inAir"] : 0, })
    # print(stats)
    additions_list = luadecoded_additions.split("\n")
    for addition in additions_list:
        addition_value = re.search(r"(?<==)[\s\S]*", addition)
        if addition_value:
            value = addition.split(" = ", 1)[1]
            if re.match(r"^{", value):
                continue
            # print(addition) 
            # exec(addition)
    return stats

# def updateLuaDecoded(luadecoded_serialized, luadecoded_additions):
#     additions_list = luadecoded_additions.split("\n")
#     for addition in additions_list:
#         additionlist = []
#         key_1_regex = re.search(r"(.*?)\[", addition) #filters the "stats" from the beginning (can also be other string) and removes it from the front
#         if key_1_regex:
#             additionlist.append(key_1_regex.group(1))
#             # print(additionlist)
#             addition = re.sub(additionlist[0], "", addition)
#             print(addition)
#         keys_2_regex = re.search(r"(.*?) =", addition)
#         if keys_2_regex:
#                 # additionlist.append(keys_2.group(1))
#             keys_2_array = re.sub(r"\[\"", ",", keys_2_regex.group(1))
#             keys_2_array = re.sub(r"\"\]", "", keys_2_array)
#             if keys_2_array:
#                 keys_2_array = keys_2_array.split(",")
#                 for i in keys_2_array:
#                     if i != '':
#                         additionlist.append(i)
#             # keys_2_regex = re.sub("\"]", "", keys_2_regex.group(1))
#                 # addition = re.sub(additionlist[0], "", addition)
#         # print(addition)
#         addition_value = re.search(r"(?<==).*", addition)
#         # print(addition_value.group(0))
    
#         add_key(luadecoded_serialized, additionlist, addition_value.group(0))


#     # print(luadecoded_additions)
#     return luadecoded_serialized

def add_key(d, keys, value):
    if len(keys) == 1:
        d[keys[0]] = value
    else:
        key = keys.pop(0)
        if key not in d:
            d[key] = {}
        add_key(d[key], keys, value)