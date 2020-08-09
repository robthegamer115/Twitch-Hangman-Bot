import socket
from Settings import HOST, PORT, getPass, getNick, getChannel

def openSocket():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + getPass() + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + getNick() + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + getChannel() + " \r\n", "UTF-8"))
    return s

def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + getChannel() + " :" + message + "\r\n"
    s.send(bytes(messageTemp, "UTF-8"))
    print("SENT: " + message)
