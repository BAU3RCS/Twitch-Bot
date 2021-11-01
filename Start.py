from Socket import sendMessage                      # Imports snedmessage function from Socket
import socket                                       # Imports socket library

def joinRoom(s):                                    # Defines how the bot joins the stream room
    readbuffer=""                                   # Creates readbuffer and starts the while loop
    Loading=True
    while Loading:
        readbuffer = str(s.recv(1024))              # Recieves 1024 bytes of data
        temp = readbuffer.split("\\r\\n")
        for line in temp:
            print(line)
            if ("End of /NAMES list" in line):
                Loading=False                       # This ends th process of joing the room
        readbuffer = temp.pop()
    bs=sendMessage(s, "Successfully joined chat!")
    return bs
    
