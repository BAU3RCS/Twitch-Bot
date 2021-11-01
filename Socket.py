                                                                        # This file is for making the connection to the Twitch IRC server etc
import socket, ssl                                                      # Imports socket library used for connections in python

from Twitch_Bot_Settings import HOST,PORT,BOT,PASS,CHANNEL             # Imports infor needed some settings file

def opensocket():                                                       # Defines function for main script
    s=socket.socket()                                                   # This creates a standard non encrypted TCP socket or connection
    ##wraper=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)                       # SSL/TLS version
    ##s=wraper.wrap_socket(socket.socket(),server_hostname=HOST)        # Creates socket and wraps the tcp port in SSL/TLS version 1/2 and readies the port for using encryption
    s.connect((HOST,PORT))                                              # Connects to server
    s.send(bytes('PASS '+PASS+'\r\n',"UTF-8"))                          # Sends password first as that is IRC protocal
    s.send(bytes('NICK '+BOT+'\r\n',"UTF-8"))                           # Sending username now
    s.send(bytes('JOIN #'+CHANNEL+'\r\n',"UTF-8"))                      # Joins Streamer's Chat
    return s


def sendMessage(s, message):                                            # Funtion to send messages with chatbot
    s.send(bytes("PRIVMSG #"+str(CHANNEL)+" :"+message+'\r\n',"UTF-8")) # Sends message through the socket
    bs="BOT NAME : "+message                                            # Prints message
    print(bs)
    return bs
