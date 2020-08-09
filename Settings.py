# Connection Settings, do not touch

HOST = "irc.twitch.tv"
PORT = 6667

settingsFileRead = open("Settings.txt", "r")
setLine = settingsFileRead.readline()
temp = 1
passcode = ""
username = ""
channel = ""
for c in setLine:
    if c == '|':
        temp = temp + 1
    elif temp == 1:
        passcode = passcode + c
    elif temp == 2:
        username = username + c
    elif temp == 3:
        channel = channel + c

settingsFileRead.close()

# Passcode is an OAuth code for the bot username
PASS = passcode

# Name of the bot
NICK = username

# Channel the bot is in
CHANNEL = channel

def getPass():
    global PASS
    return PASS

def getNick():
    global NICK
    return NICK

def getChannel():
    global CHANNEL
    return CHANNEL


