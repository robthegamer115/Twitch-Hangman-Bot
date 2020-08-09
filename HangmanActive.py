hangman = True

# return if a new round of hangman can begin
def getHangman():
    global hangman
    return hangman

# set hangman to either true or false
def setHangman(x):
    global hangman
    hangman = x
    return
