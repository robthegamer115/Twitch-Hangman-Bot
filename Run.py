from Socket import openSocket, sendMessage
from HangmanActive import getHangman, setHangman
from Initialize import joinRoom
from Read import getUser, getMessage, checkPing
from Settings import getChannel
from TimeCommands import timedMessages, setRunning
import string, time, ast, random, threading

s = openSocket()
joinRoom(s)

#Initialize Variables
readbuffer = ""
running = True
hangmanInProgress = False
time_start = time.time()

#Read from the points file
pointFileRead = open("Points.txt", "r")
pointLine = pointFileRead.readline()
pointCatalog = ast.literal_eval(pointLine)
pointFileRead.close()

#Read from the hangman file
hangFileRead = open("Hangman.txt", "r")
hangLine = hangFileRead.readline()
hangmanCatalog = ast.literal_eval(hangLine)
hangFileRead.close()

#Separate threads for time commands and chat commands
t1 = threading.Thread(target=timedMessages, args=(s,))
t1.start()

# Prepare to read a line in the twitch chat
while running:
    readbuffer = readbuffer + s.recv(1024).decode("UTF-8")
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    # When a line appears, check if it's just a twitch automatic message
    for line in temp:
        testPing = checkPing(line)
        if len(testPing) != 0:
            if testPing == "PING ":
                print("PONG")
                s.send(bytes("PONG :tmi.twitch.tv", "UTF-8"))
                sendMessage(s, "YOU SHOULD NEVER SEE THIS MESSAGE IN CHAT!")
                line = "PING :Twitch!Twitch@Twitch.tmi.twitch.tv PRIVMSG #Twitch :PING "
            else:
                print("ERROR: checkPing returned " + testPing)
                
        # Extract the user and message from the line, print it out in terminal, update seconds
        user = getUser(line)
        message = getMessage(line)
        print(user + " said " + message)
        seconds = int(time.time() - time_start)

        # Reset the possible hangman answers so that the full master list is used again (CHANNEL ONLY)
        if user == getChannel() and message == "!addPokes":
            read = open("HangmanMasterList.txt", "r")
            add = open("Hangman.txt", "w")
            answer = read.readline()
            hangmanCatalog = {}
            while answer != "DONE\n":
                hangmanCatalog.update({answer:0})
                answer = read.readline()
            add.write(str(hangmanCatalog))
            print("Done!")

        # Shut down the hangman bot (CHANNEL ONLY)
        if user == getChannel() and message == "!quit":
            sendMessage(s, "Bot is now shutting down")
            running = False
            setRunning()

        # Get information about hangman and who made it
        if message == "!aboutHangman":
            sendMessage(s, "This hangman bot was created by robthegamer115! If there are"
                        + " any bugs, issues, questions, or ideas for new features, message"
                        + " robthegamer115 on twitch at robthegamer115!")

        # Get a link to the rules of hangman
        if message == "!hangmanrules":
            sendMessage(s, "If you want to view the rules of hangman, click here: https://pastebin.com/wLsfPa7f")

        # Get the number of points you have
        if message == "!points":
            if user not in pointCatalog:
                pointCatalog.update({user: 0})
            sendMessage(s, str (pointCatalog[user]))

        # Get the position you are in compared to all other users
        if message == "!position":
            if user not in pointCatalog:
                pointCatalog.update({user: 0})
            sortedPoints = sorted(pointCatalog.values())
            place = 0
            tied = False
            for x in range (len(sortedPoints)):
                if (sortedPoints[x] == pointCatalog[user]):
                    if place > 0:
                       tied = True 
                    place = len(sortedPoints) - x
            placeString = str (place) 
            if tied:
                sendMessage(s, user + " is currently tied in position " + placeString)
            else:
                sendMessage(s, user + " is currently in position " + placeString)

        # Find out who the top 10 users are, and the number of points they have
        if message == "!top10":
            sortedPoints = sorted(pointCatalog.values())
            pointarray = ["-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1", "-1"]
            namearray = ["ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR", "ERR"]
            posarray = ["1st", ", 2nd", ", 3rd", ", 4th", ", 5th", ", 6th", ", 7th", ", 8th", ", 9th", ", 10th"]
            for x in range(0, len(sortedPoints)):
                if x < 10:
                    pointarray[x] = sortedPoints[len(sortedPoints) - (x + 1)]
            for x in pointCatalog:
                unused = True
                for y in range(0, len(sortedPoints)):
                    if y < 10 and pointCatalog[x] == pointarray[y] and namearray[y] == "ERR" and unused:
                        namearray[y] = x
                        unused = False
            top10string = ""
            for x in range(0, min(10, len(sortedPoints))):
                top10string = top10string + posarray[x] + ": " + namearray[x] + " (" + str(pointarray[x]) + ")"
            sendMessage(s, top10string)

            
        # Attempt to start hangman failed because ten minutes has not passed
        if message == "!hangman" and getHangman() == False:
            sendMessage(s, "Hangman is unavailable at the moment. " +
                        "Hangman will become available in " +
                        str (600 - (seconds % 600)) + " seconds.")

        # Start hangman successfully
        if message == "!hangman" and getHangman() == True:
            hangmanInProgress = True
            setHangman(False)

            # Chooses a random entry from Hangman.txt and make sure it hasn't been called yet
            size = len(hangmanCatalog)
            target = random.randint(0,size)
            number = 0
            for y in hangmanCatalog:
                if number == target:
                    hangmanInfo = y
                number = number + 1
            if size < 5:
                read = open("HangmanMasterList.txt", "r")
                add = open("Hangman.txt", "w")
                answer = read.readline()
                hangmanCatalog = {}
                while answer != "DONE\n":
                    hangmanCatalog.update({answer:0})
                    answer = read.readline()
                add.write(str(hangmanCatalog))
                add.close()

            hangmanCatalog.pop(hangmanInfo)
            add = open("Hangman.txt", "w")
            add.write(str(hangmanCatalog))
            add.close()

            hangmanSplit = str.split(hangmanInfo, "|")
            answer = hangmanSplit[1][0: len(hangmanSplit[1]) - 1: 1]
            category = hangmanSplit[0][0: len(hangmanSplit[0]): 1]
            guessedLetters = ""
            curHangman = ""
            badusers = ""
            timeStart = seconds + 7


            # Messages sent to start game
            sendMessage(s, "Welcome to pokemon hangman! If you have any questions"
                        + " about how to play hangman, look here - https://pastebin.com/wLsfPa7f")

            time.sleep(5)
            sendMessage(s, "Alright, the category this time is " +
                        category.upper() + "! Good Luck!")

            # Puzzle Created out of '_' and '/'
            for c in answer:
                if c == " ":
                    curHangman = curHangman + " / "
                elif c == "\n":
                    curHangman = curHangman
                else:
                    curHangman = curHangman + " _ "
            time.sleep(2)
            sendMessage(s, curHangman)

        # When a letter is guessed
        if message.startswith("!guess ") and hangmanInProgress == True and user not in badusers and seconds != timeStart:
            guessSplit = str.split(message, "!guess ")
            if len(guessSplit[1]) == 1 and answer.lower() != "n":
                curHangman = ""
                guessedLetters = guessedLetters + guessSplit[1]
                for c in answer:
                    if c.lower() in guessedLetters.lower():
                        curHangman = curHangman + " " + c.lower() + " "
                    elif c == " ":
                        curHangman = curHangman + " / "
                    elif c == "\n":
                        curHangman = curHangman
                    else:
                        curHangman = curHangman + " _ "
                sendMessage(s, curHangman)

            # When an answer is guessed correctly
            else:
                if answer.lower() == guessSplit[1].lower():
                    blanksLeft = 0
                    timeEnd = seconds
                    for c in curHangman:
                        if c == "_":
                            blanksLeft += 1
                    pointsAwarded = int ((600 - (timeEnd - timeStart)) / 10 * blanksLeft)
                    if pointsAwarded < 20:
                        pointsAwarded = 20
                            
                    sendMessage(s, user + " got it correct! The answer was " +
                                    answer.lower() + "! " + user + " won " +
                                    str (pointsAwarded) + " points!" )
                    hangmanInProgress = False
                    if user not in pointCatalog:
                        pointCatalog.update({user: 0})
                    pointCatalog[user] = pointCatalog[user] + pointsAwarded
                    temp = pointCatalog.values()
                    pointFileWrite = open("Points.txt", "w")
                    pointFileWrite.write(str (pointCatalog))
                    pointFileWrite.close()

                # When an answer is guessed incorrectly
                else:
                    sendMessage(s, user + " was incorrect! The rest of you, " +
                                "keep guessing!")
                    badusers = badusers + "|" + user + "|"

# When bot is shutting down
print("CHAT COMMANDS DISCONECTED")
t1.join()
