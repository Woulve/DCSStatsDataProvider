def removeHost(luadecoded):
    updatedlua = {}
    # print(luadecoded)
    #loop through luadecoded and remove host
    updatedlua = {}
    for ucid in luadecoded:
        if ucid != "host":
            updatedlua[ucid] = luadecoded[ucid]
    return updatedlua