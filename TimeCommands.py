from Socket import sendMessage
from HangmanActive import getHangman, setHangman
import string, time

running = True

def timedMessages(s):
    readbuffer = ""
    time_start = time.time()
    seconds = 0

    while running:
        seconds = int(time.time() - time_start)

        if seconds % 600 == 0:
            sendMessage(s, "Pokemon hangman is available to play! If you want to play, just type '!hangman' in chat!")
            setHangman(True)
            time.sleep(1)
    print("TIME COMMANDS DISCONNECTED")
    return

def setRunning():
    global running
    running = False
    return
        

    
   
