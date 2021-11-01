#Brandon Bauer & Ijahmin Balser
#4/10/19 - 5/2/19

from Socket import opensocket,sendMessage                                                           # Importing information and functions from other files
from Start import joinRoom
from random import shuffle
from Twitch_Bot_Settings import CHANNEL
from Bot_Functions import giveaway, poll

import sys,datetime,time,threading                                                                  # Importing python libraries used in thi file


f=str(datetime.datetime.now())                                                                      # This setups the file name for logging the chat
fn=f.split()
fnn=fn[0]+'_'+fn[1]
ff=fnn.replace('.','_').replace(':','-')
logs='logs\\'+ff+'.txt'

with open(logs,'w+') as FI:                                                                         # Opens the log file named above for logging used during the bots runtime 
    s=opensocket()                                                                                  # Creates the socket
    bs=joinRoom(s)                                                                                  # Joins the Channel
    FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                                          # Logs joining the channel

    bs=''                                                                                           # These are variables, lists, and strings used in the code further down
    commands=[]
    outputs=[]
    readbuffer = ""
    giveawayRunning=[]
    giveawayUsers=[]
    noList=[]
    yesList=[]
    pollRunning=False

    def getUser(line):                                                                              # This defines finding the user in the output from the server 
        try:
            separate = line.split(":",2)
            user = separate[1].split("!",1)[0]
        except:
            user='byteboy'
        return user

    def getMessage(line):                                                                           # This defines finding the message portion of the output from the server
        try:
            separate = line.split(":",2)
            message = separate[2]
            message = message[0:len(message)-5]
        except:
            message=line
        return message

    def checkMessage(user, message, bs):                                                            # This checks the message for banned words and if they are found timeout the user
        with open('bannedwords.txt','r') as banw:
            bannw=banw.readlines()
            bq=bannw[0].split(',')
            for i in bq:
                if i.upper() == message.upper():
                    bs=sendMessage(s,"/timeout "+user)
        return bs

    def pongers(message,bs):                                                                        # This is an inside joke; it responds to user input in the chat
        if 'PING' in message.upper()and 'tmi.twitch.tv' not in message:
            bs=sendMessage(s,"PONGERS")
            nbs=bs
            with open('pongs.txt','r') as ps:
                psr=ps.readline()
            try:
                nps=int(psr)+1
            except:
                nps=1
            bs=sendMessage(s,"PONGERS Number: "+str(nps))
            with open('pongs.txt','w') as ps:
                ps.write(str(nps))
        else:
            nbs=''
            bs=''
        return bs,nbs
    
    def pingit():                                                                                   # This is essentially the keep alive for the connection to the server. This sends a desired response every 4 and a half mins.
        threading.Timer(300, pingit).start()
        s.send(bytes('PONG tmi.twitch.tv\r\n',"UTF-8"))
        FI.write(str(datetime.datetime.now())+' '+'Bot:'+'PONG tmi.twitch.tv'+'\n')
        print('bot is ponging')

    pingit()                                                                                        # This runs the response function
    while True:                                                                                     # This is the main loop which runs until the bot is shutdown
        readbuffer = readbuffer+str(s.recv(1024))                                                   # This tells the server and us to communicate 1024 bytes at a time and sets the information to a readable string
        temp = readbuffer.split("\r\n")                                                             # This splits the incoming message and cuts off the carriage and end line
        for line in temp:                                                                           # This runs for the majority of the rest of the main loop and checks the line for certain things defined below
            FI.write(str(datetime.datetime.now())+' '+line+' '+'\n')                                # This writes the incoming message in the log file
            bs=''                                                                                   # This clears the variable used for logging things from various functions and is used multiple  times later as well
            user = getUser(line)                                                                    # Calls on function
            message = getMessage(line)                                                              # Calls on function
            print(user+" typed: "+message)                                                          # This prints the user and their message in the pyhton console in either idle or cmd
            bs,nbs=pongers(message,bs)                                                              # Calls inside joke function
            try:                                                                                    # This is a exceptipon or error handling as when the function doesn't run no values would be returned and it would crash other wise
                FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                              # Logging
                FI.write(str(datetime.datetime.now())+' '+nbs+' '+'\n')                             # Logging
                bs=''
            except:
                pass                                                                                # This tells the program move on
                
            bs=checkMessage(user, message, bs)                                                      # Calls on checkmessage function
            try:                                                                                    # Same error handling as above and is the same as it occurs several more times below
                FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                              # Logging
                bs=''
            except:
                pass
            bs=giveaway(user, message, s,bs)                                                        # Calls on a giveaway function
            try:                                                                                    # Error handling
                FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                              # Logging
                bs=''
            except:
                pass
            bs=poll(message, user, s,bs)                                                            # Calls on a poll function
            try:                                                                                    # Error handling
                FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                              # Logging
                bs=''
            except:
                pass
            try:                                                                                    # This is an error handling loop to prevent crashing again for a small if loop that allows me to add banned words
                if '!addbannedword' in message:
                    with open('bannedwords.txt','a') as banw:
                        if user=='/////' or user=='/////':
                            wo=message.split()
                            bw=wo[1]
                            banw.write(','+bw)
            except:
                pass
            try:                                                                                    # This is an error handling loop to prevent crashing again for a small if loop that allows me to remove banned words
                if '!rembannedword' in message:
                    with open('bannedwords.txt','r') as banw:
                        if user=='/////' or user=='/////':
                            bannwr=banw.readlines()
                            bqr=bannwr[0].split(',')
                            for wr in bqr:
                                qw=message.split()
                                bwr=qw[1]
                                if wr.upper()==bwr.upper():
                                    bqr.remove(bwr)
                                    bqn=bqr
                    with open('bannedwords.txt','w') as banw:
                        for nl in bqn:
                            banw.write(nl+',')
            except:
                pass
            if message.upper()=='!STOP' and user=='/////':                                          # This allows me to properly stop the bots main loop and terminate the connection via the twitch chat
                time.sleep(1)                                                                       # Pauses before closing
                bs=sendMessage(s,'Bye Nerds')
                FI.write(str(datetime.datetime.now())+' '+bs+' '+'\n')                              # Logging
                sys.exit()                                                                          # Officially exits
        readbuffer = ""                                                                             # This resets the buffer for each new line recieved
