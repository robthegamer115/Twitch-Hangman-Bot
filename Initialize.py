import string
from Socket import sendMessage

# Joins the twitch room
def joinRoom(s):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            print(line)
            Loading = loadingComplete(line)
    sendMessage(s, "Bot Successfully Joined")

# Checks lines until loading the twitch room is complete
def loadingComplete(line):
    if "End of /NAMES list" in line:
       return False
    else:
       return True
