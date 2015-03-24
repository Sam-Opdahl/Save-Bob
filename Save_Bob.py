"""

A simple hangman game with a settings menu and saving functionality.

Currently, only works on Windows and requires to be run from the command prompt (e.g 'python Save_Bob.py')

Completed on 9/1/2012

"""

import sys
import time
import os
import msvcrt
import winsound
import random

#*********************
# Global Variables
#*********************

hman = [
            "======\n"+"||   |   \n"+"||   \n"+"||  \n"+"||   \n"+"||  \n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \n"+"||   \n"+"||  \n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||   |\n"+"||   |\n"+"||  \n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \|\n"+"||   |\n"+"||  \n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \|/\n"+"||   |\n"+"||  \n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \|/\n"+"||   |\n"+"||  /\n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \|/\n"+"||   |\n"+"||  / \\\n"+"-------",
            "======\n"+"||   |   \n"+"||   O\n"+"||  \|/\n"+"||   |\n"+"||  / \\\n"+"--",
       ]

alpha = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        ]


# Currently used GameStates.
# 0 = starting
# 1 = main menu
# 2 = play game
# 3 = game stats
# 4 = options
GameState = 0

GameName = "Save Bob"

#get filepath based on if we are running from .exe or .py
if hasattr(sys, "frozen"):
    filespath =  os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding()))
else:
    filespath = os.path.dirname(__file__)
filespath += "data"

wordfile = filespath + "\\twf.dat"
settingsfile = filespath + "\\settings.ini"
scorefile = filespath + "\\ps.dat"

badinput = False

defspeed = 0.03
typespeed = defspeed
stoptype = False


#********************
# Helper Functions
#********************

def SplashScreen():
    global typespeed
    typespeed = 0

    type(GameName + " V1.0\n")
    type("||||||||||||||||||||||||||||||||||||||||||||||||" + "\n")
    type("||||||||||||||||||||||||||||||||||||||||||||||||" + "\n")
    type("||||||||||-----|||---|||-||||||-||-----|||||||||" + "\n")
    type("|||||||||--||||||--|--||--||||--||-|||||||||||||" + "\n")
    type("|||||||||--||||||-|||-|||-||||-|||-|||||||||||||" + "\n")
    type("||||||||||----|||-|||-|||--||--|||---|||||||||||" + "\n")
    type("|||||||||||||--||-----||||-||-||||-|||||||||||||" + "\n")
    type("|||||||||||||--||-|||-||||----||||-|||||||||||||" + "\n")
    type("|||||||||-----|||-|||-|||||--|||||-----|||||||||           ______________" + "\n")
    type("||||||||||||||||||||||||||||||||||||||||||||||||          |              |" + "\n")
    type("||||||||||||-----|||||----||||-----|||||||||||||          | Hi, I'm Bob! |" + "\n")
    type("||||||||||||-||||-|||-||||-|||-||||-||||||||||||          |              |" + "\n")
    type("||||||||||||-||||-||--||||--||-||||-||||||||||||          | ...uh oh.    |" + "\n")
    type("||||||||||||-----|||-||||||-||-----|||||||||||||         /|______________|" + "\n")
    type("||||||||||||-||||-||--||||--||-||||-||||||||||||        /" + "\n")
    type("||||||||||||-||||-|||-||||-|||-||||-||||||||||||       O " + "\n")
    type("||||||||||||-----|||||----||||-----|||||||||||||      \|/" + "\n")
    type("||||||||||||||||||||||||||||||||||||||||||||||||       |" + "\n")
    type("||||||||||||||||||||||||||||||||||||||||||||||||      / \\" + "\n")
    typespeed = defspeed

def clear():
    os.system("cls")

def type(string):
    global typespeed
    global stoptype

    for ltr in string:
        sys.stdout.write(ltr)
        if (stoptype == False):
            time.sleep(typespeed)
        if (msvcrt.kbhit() == True and stoptype == False): #if the user hits a key while we are typing, skip the sleeping (help out impatient users)
            stoptype = True
    flushbuffer() # flush read buffer if user types while writing to prevent unwanted keystrokes.

def endOfBlock(): #defines the beginning of a new text block
    global stoptype
    stoptype = False

def sleep(length):
    time.sleep(length)
    flushbuffer()

def Color(color):
    color = color.upper()
    if color == "BLUE":
        os.system("color 9")
    elif color == "RED":
        os.system("color C")
    elif color == "WHITE":
        os.system("color 7")
    elif color == "GREEN":
        os.system("color A")
    elif color == "PURPLE":
        os.system("color 5")

def encode(string):
    return string.encode("base64", "strict").strip()

def decode(string):
    return string.decode("base64", "strict")

def waitforkey():
    msvcrt.getch()

def EndGame():
    os.system("mode con lines=25")
    Color("white")
    clear()
    sys.exit()

def flushbuffer():
    while msvcrt.kbhit():
        msvcrt.getch()

def write(string):
    file = open(wordfile, "a")
    file.write(string)
    file.close()

def getRandomWord():
    word = ""
    file = open(wordfile, "r")
    fileLength = len(file.readlines())

    while (True):
        file.seek(0)
        randnum = random.randint(1, fileLength)
        for i in range(randnum):
            if (i == randnum - 1):
                word = decode(file.readline().strip())
                break
            file.readline()
        if (len(word) >= 5):
            break

    file.close()
    return list(word)

def updateViewList(wordlist, gltr):
    viewlist = wordlist[:]
    for i in range(len(viewlist)):
        for x in range(len(alpha)):
            if ((viewlist[i].lower() == alpha[x]) and (isNotGuessed(viewlist[i], gltr))):
                viewlist[i] = "_"
                break
    return viewlist

def isNotGuessed(listword, gltr):
    for i in range(len(gltr)):
        if (listword.lower() == gltr[i]):
            return False
    return True

def letterMatch(ltr, wordlist):
    tot = 0
    for i in range(len(wordlist)):
        if (wordlist[i].lower() == ltr):
            tot += 1
    return tot

def playInputError(inp, gltr):
    #check length of input
    if (len(inp) > 1):
            return "Please enter a single valid letter. (a-z)"

    #check for valid letters
    isValid = False
    for i in range(len(alpha)):
        if (inp == alpha[i]):
            isValid = True
            break
    if (isValid == False):
        return "Please enter a valid letter. (a-z)"

    #check if letter was already guessed
    for i in gltr:
        if (inp == i):
            return "You already guessed that letter!"

    #No error was found.
    return ""

def GetWLRatio():

    try:
        return str("%.2f" % (float(score.wins) / float(score.loses)))
    except ZeroDivisionError:
        return str("%.2f" % float(score.wins))

def GetPerfGamePercent():

    try:
        return str("%.0f" % ((float(score.perfgames) / float(score.wins)) * 100)) + "%"
    except ZeroDivisionError:
        return "0%"



#*********************
# Classes
#*********************

class Settings:

    #Get settings from settings.ini file
    def __init__ (self):
        file = open(settingsfile, "r")
        while True:
            inp = file.readline().strip()
            if len(inp) == 0:
                file.close()
                break
            div = inp.split('=')
            setattr(self, div[0], div[1])

    def set(self, sName, sOpt):
        #if option is the same as before, skip the process. Otherwise continue.
        if (getattr(self, sName) == sOpt):
            return

        #set currently used variable with new option
        setattr(self, sName, sOpt)

        #Read settings file and insert the new setting option
        with open(settingsfile, "r") as file:
            readLines = file.readlines()
            for i in range(len(readLines)):
                if (readLines[i].split('=')[0] == sName):
                    readLines[i] = sName + "=" + sOpt + "\n"
                    break
        #Overwrite existing settings file with new one
        with open(settingsfile, "w") as file:
            file.writelines(readLines)

        #if color is being changed, put the new color into effect
        if (sName == "color"):
            Color(sOpt)

settings = Settings()


class Sound:

    def intro(self):
        for i in range(2, 6):
            winsound.Beep(i * 100, 200)

    def CorrectGuess(self):
        if (settings.sound == "True"):
            winsound.Beep(1500, 200)
            winsound.Beep(3000, 200)

    def WrongGuess(self):
        if (settings.sound == "True"):
            winsound.Beep(1000, 200)
            winsound.Beep(500, 200)

    def LostRound(self):
        if (settings.sound == "True"):
            winsound.Beep(400, 200)
            winsound.Beep(500, 200)
            winsound.Beep(250, 200)

    def WonRound(self):
        if (settings.sound == "True"):
            winsound.Beep(1500, 200)
            winsound.Beep(3000, 200)
            winsound.Beep(2500, 200)


sound = Sound()


class Score:

    wins = 0
    loses = 0
    perfgames = 0

    def __init__(self):
        self.load()

    def load(self):
        try:
            with open(scorefile, "r") as file:
                data = decode(file.readline())
        except IOError:
            return #file doesn't exist yet.

        data = data.split("\n")
        self.wins = int(data[0])
        self.loses = int(data[1])
        self.perfgames = int(data[2])

    def save(self):
        with open(scorefile, "w") as file:
            toWrite = str(self.wins) + "\n" + str(self.loses) + "\n" + str(self.perfgames)
            file.write(encode(toWrite))

    def show(self):
        type("\n\nWins: " + str(self.wins) + "\n")
        type("Loses: " + str(self.loses) + "\n")
        type("Perfect Games: " + str(self.perfgames) + "\n")
        waitforkey()

score = Score()


#*******************************
# Option Menu - Change Options
#*******************************

def OptChangeSetting(CurOpt):

    global typespeed
    global badinput
    
    lastOption = 0
    toChange = []

    while (True):
        endOfBlock()
        clear()

        type("Options Menu")

        if (CurOpt == 'sound'):
            lastOption = 3
            toChange = ["True", "False"]

            type(" - Sound\n\n")
            type("Sound is currently " + ("Enabled" if settings.sound == "True" else "Disabled"))
            type("\n\nWhat would you like to do?\n")
            type("1. Enable Sound")
            type("\n2. Disable Sound")
        elif (CurOpt == 'color'):
            lastOption = 6
            toChange = ["red", "blue", "green", "purple", "white"]

            type(" - Text Color\n\n")
            type("Text color is currently " + settings.color)
            type("\n\nPick a color from below.\n")
            type("1. Red\n")
            type("2. Blue\n")
            type("3. Green\n")
            type("4. Purple\n")
            type("5. White")

        type("\n" + str(lastOption) + ". Back to Options\n\n")

        if (badinput == True):
            typespeed = defspeed
            badinput = False
            type("Please choose an option between 1 and " + str(lastOption) + "\n")

        type("Input: ")
        try:
            inp = int(raw_input().strip())
            if (inp >= 1 and inp < lastOption):
                settings.set(CurOpt, toChange[inp-1])
                continue
            elif (inp == lastOption):
                return
            else:
                raise "Exception"
        except:
                badinput = True
                typespeed = 0
                continue


#*********************
# Gamestate functions
#*********************

def MainMenu():

    global typespeed
    global GameState
    global badinput

    endOfBlock()
    clear()
    type(GameName)
    type("\n\nMain Menu\n\n")
    type("1. Play a round\n")
    type("2. View your stats\n")
    type("3. Options\n")
    type("4. Quit\n")

    if (badinput == True):
        typespeed = defspeed
        badinput = False
        type("\nInvalid input. Please select an option from above. e.g. 3")
    type("\nInput: ")

    endOfBlock()

    inp = raw_input()
    #Play Game
    if (inp == "1" or inp == "1."):
        type("\nStarting new game...")
        sleep(1)
        GameState = 2
        return
    #Game stats screen
    elif (inp == "2" or inp == "2."):
        GameState = 3
        return
    #Options Menu
    elif (inp == "3" or inp == "3."):
        GameState = 4
        return
    elif (inp == "4" or inp == "4."):
        EndGame()
    else:
        typespeed = 0
        badinput = True


def PlayGame():

    global typespeed
    global GameState

    output = ""
    guessct = 0
    guesstot = 0
    guessedltrs = []
    outcome = 0 # 0=still playing, 1=win, 2=lose

    wordlist = getRandomWord()
    viewlist = updateViewList(wordlist, guessedltrs)
    viewword = " ".join(viewlist) 

    #Add a loss now, this way if the player leaves early, it will still count as a loss.
    #if they win, this loss will be removed.
    score.loses += 1
    score.save()           
    
    while (True):
        endOfBlock()
        clear()
        type("Type \"quit\" at any time to leave the game.\n\n")
        type(hman[guessct])
        type("\n\nLetters already guessed: " + ", ".join(sorted(guessedltrs)) + "\n\n\n")
        type(viewword + "\n\n")
        #type(viewword + "\n\n")
        if (outcome != 2): type("\n")

        typespeed = defspeed
        if (len(output) > 0):
            type(output + "\n")
            output = ""

        if (outcome != 0):
            break

        type("Enter a letter: ")
        inp = raw_input().strip().lower()
        typespeed = 0

        #Check if user wants to quit
        if (inp == "quit" or inp == "\"quit\""):
            endOfBlock()
            clear()
            typespeed = defspeed
            type("If you quit, it will count as a loss.\n\n")
            type("Are you sure you want to quit (y/n)? ")
            inp = raw_input().strip().lower()
            if (inp == "y" or len(inp) == 0):
                GameState = 1
                return
            else:
                output = ""
                typespeed = 0
                continue

        #Check for input errors
        output = playInputError(inp, guessedltrs)
        if (len(output) > 0):
            continue

        guessedltrs.insert(len(guessedltrs), inp)
        
        totalmatches = letterMatch(inp, wordlist)
        if (totalmatches > 0):
            guesstot += 1
            viewlist = updateViewList(wordlist, guessedltrs)
            viewword = " ".join(viewlist)

            if (viewlist == wordlist):
                outcome = 1
                continue

            output = str(totalmatches) + " " + ("matches" if totalmatches > 1 else "match") + " found for \"" + inp + "\""
            sound.CorrectGuess()
        else:
            guesstot += 1
            guessct += 1

            if (guessct == (len(hman) - 1)):
                outcome = 2
                output = " ".join(wordlist) + "\n"
                continue

            output = "No matches found for \"" + inp + "\""

            sound.WrongGuess()

    if (outcome == 1):
        sound.WonRound()
        score.loses -= 1 #remove loss that was added earlier.
        score.wins += 1
        type("You win!\n")
        type("It took you " + str(guesstot) +" guesses.\n")
        type("You have won " + str(score.wins) + (" game." if score.wins == 1 else " games.") + "\n\n")
        if (guessct == 0):
            score.perfgames += 1
            type("Good job, you played a perfect game!\n")
            type("You've played " + str(score.perfgames) + " perfect " + ("game" if score.perfgames == 1 else "games") + " total!\n\n")
        score.save()
    if (outcome == 2):
        sound.LostRound()
        type("\nOops, you lost!\n")
        type("Better luck next time.\n\n")

    type("Play again (y/n)? ")
    inp = raw_input().strip().lower()    
    if (inp != "y" and len(inp) != 0):
        GameState = 1

    return


def ShowGameStats():

    global GameState

    endOfBlock()
    clear()
    type("Your Game Statistics\n\n\n")
    type("Total Games Played | " + str(score.wins + score.loses) + "\n")
    type("-------------------|--------\n")
    type("Wins               | " + str(score.wins) + "\n")
    type("-------------------|--------\n")
    type("Losses             | " + str(score.loses) + "\n")
    type("-------------------|--------\n")
    type("W/L Ratio          | " + GetWLRatio() + "\n")
    type("-------------------|--------\n")
    type("Perfect Games      | " + str(score.perfgames) + "\n")
    type("-------------------|--------\n")
    type("% of Games Perfect | " + GetPerfGamePercent() + "\n\n\n")

    type("Press any key to return to the main menu.")
    GameState = 1
    waitforkey()
    

def OptionsMenu():

    global GameState
    global badinput
    global typespeed

    endOfBlock()
    clear()
    type("Options Menu\n\n")
    type("Select an option you would like to change from below:\n\n")
    type("1. Sound\n")
    type("2. Text Color\n")
    type("3. Back to main menu\n\n")
    if (badinput == True):
        typespeed = defspeed
        badinput = False
        type("Invalid selection. Please choose an option from above, such as 1.\n")
    type("Input: ")
    inp = raw_input().strip()

    if (inp == "1"):
        OptChangeSetting('sound')
        return
    elif (inp == "2"):
        OptChangeSetting('color')
        return
    elif (inp == "3"):
        GameState = 1
        return
    else:
        typespeed = 0
        badinput = True
        return



#*************************************
# Program Initialization/ Entry Point
#*************************************

clear()
Color(settings.color)
os.system("mode con lines=30") #make the screen a bit taller

random.seed()


#*****************
# Main Game Loop
#*****************

while (True):
    if (GameState == 0): #Starting Game
        SplashScreen()

        if (settings.sound == "True"):
            sound.intro()
        else:
            sleep(1.4)

        endOfBlock()
        type("\n\nPress any key to continue")

        waitforkey()
        clear()
        GameState = 1
        continue
    elif (GameState == 1): #Main Menu
        MainMenu()
        continue
    elif (GameState == 2): #play game
        PlayGame()
        continue
    elif (GameState == 3): #game stats
        ShowGameStats()
        continue
    elif (GameState == 4): #options
        OptionsMenu()
        continue