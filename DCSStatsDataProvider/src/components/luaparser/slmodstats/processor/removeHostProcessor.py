def removeHost(luadecoded):
    updatedlua = {}
    # print(luadecoded)
    #loop through luadecoded and remove host
    for type in luadecoded:
        updatedlua[type] = {}
        for ucid in luadecoded[type]:
            if ucid != "host":
                updatedlua[type][ucid] = luadecoded[type][ucid]
    return updatedlua