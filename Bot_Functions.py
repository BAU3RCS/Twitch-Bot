from Socket import sendMessage
from random import shuffle

def giveaway(user, message, s, bs):
    global giveawayUsers,giveawayRunning                                                        # Tells function to use the global variables giveawayUsers and giveawayRunning
    if "!giveaway"in message:
        if user == "/////" or user == "/////":                                                  # Checks if !giveaway is in the messages and if the appropriate user typed the message
            giveawayUsers=[]                                                                    # Clears giveawayUsers so that the last giveaway's entrees don't count
            bs=sendMessage(s,"There is a giveaway running! Type !enter to enter the giveaway")  # Sends a message alerting users that a giveaway is happening
            giveawayRunning=['']                                                                # Establishes that a giveaway is running within Python
    elif "!enter"in message and giveawayRunning==['']:
        if user not in giveawayUsers:                                                           # Checks for !enter in the message, if a giveaway is running, and if they user is not already entered
            giveawayUsers.append(user)                                                          # Adds user to the giveawayUsers list
            bs=sendMessage(s,"/w "+user+" You have entered the giveaway.")                      # Sends a private message telling the user that they have been entered
    elif "!endgiveaway" in message:
        if user == "/////" or user == "/////":                                                  # Checks for !endgiveaway in the message and if the appropriate user sent the message
            giveawayRunning=[]                                                                  # Establishes that a giveaway is no longer running
            shuffle(giveawayUsers)                                                              # Shuffles the giveawayUsers list
            bs=sendMessage(s,"The giveaway is now over. The winner is "+giveawayUsers[0])       # Sends a chatmessage that declares the winner
    return bs                                                                                   # Returns what the message the bot sent
                           


def poll(message, user, s,bs):
    global yesList,noList                                                                       # Tells the function to use the global variables yesList and noList
    if "!poll" in message:
        if user=="/////" or user=="/////":                                                      # Checks for poll in the message and if the appropriate user sent the message
            noList=[]
            yesList=[]                                                                          # Clears the noList and yesList
            poll=message[6:len(message)]                                                        # Sets the poll variable as the text after !poll in the message
            bs=sendMessage(s, "Cast your vote! "+poll)                                          # Sends a message that declares that a poll is running and says what the poll is

    elif message=="!yes":
        if user not in yesList and user not in noList:
            yesList.append(user)                                                                # If the user typed !yes and is not in either list, then the user is added to the yes list

    elif message=="!no":
        if user not in yesList and user not in noList:
            noList.append(user)                                                                 # If the user typed !no and is not in either list, then the user is added to the no list

    elif message=="!endpoll":
        if user=="/////" or user=="/////":                                                      # Checks if the appropriate user sent the message !endpoll
            if len(yesList) > len(noList):
                bs=sendMessage(s, "The votes are in! The answer is yes.")
            elif len(yesList) < len(noList):
                bs=sendMessage(s, "The votes are in! the answer is no.")
            else:
                bs=sendMessage(s, "It's a tie!")                                                # Compares the length of noList and yesList, and prints the appropriate message
    return bs
