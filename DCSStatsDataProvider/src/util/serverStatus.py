# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(host, port)
# s.send("some data")
# # don't close socket just yet... 
# # do some other stuff with the data (normal string operations)
# if s.stillconnected() is true:
#     s.send("some more data")
# if s.stillconnected() is false:
#     # recreate the socket and reconnect
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(host, port)
#     s.send("some more data")
# s.close()