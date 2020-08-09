import string

# Returns the username of whoever sent the message
def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user

# Returns the message that the user sent
def getMessage(line):
    separate = line.split(":", 2)
    message = separate[2]
    message = message[0:len(message) - 1]
    return message

# Checks to see if the message is twitch sending a Ping
def checkPing(line):
    separate = line.split(":", 2)
    possiblePing = separate[0]
    return possiblePing
