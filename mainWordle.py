#modules
import json
import random
import tkinter as tk
import functools





#stores the state of the current game
class gameSessionData():

    def __init__(self):
        
        self.gameOver = False
        self.currentGuess = 0
        self.answerBank = getAnswers()
        self.wordBank = sorted(getWords() + self.answerBank)
        #keyWord, the word you have to find, is a random word from all the possible answers
        self.keyWord = random.choice(self.answerBank)
        self.keyboard = ["q","w","e","r","t","y","u","i","o","p",
                        "a","s","d","f","g","h","j","k","l",0,
                        "\N{RETURN SYMBOL}","z","x","c","v","b","n","m","\N{BACK WITH LEFTWARDS ARROW ABOVE}",0]
        self.letterRows = [0]*6
        self.keyboardBtns = [0]*30





def binarySearch(array,target):

    bottom = 0
    top = len(array) - 1


    while top >= bottom:

        mid = (top + bottom) // 2

        if array[mid] == target:
            return True

        elif array[mid] < target:
            bottom = mid + 1

        else:
            top = mid - 1


    return False





def getAnswers():

    with open("wordData/wordleAnswers.json", "r") as readFile:
        return json.load(readFile)





def getWords():

    with open("wordData/wordleWords.json", "r") as readFile:
        return json.load(readFile)





#updates the text in the first free row to the letters of your guess
def updateWordleBoard(guess,colours,outputRow):

    for index in range(5):
        outputRow[index]["text"] = guess[index].upper()
        outputRow[index]["bg"] = colours[index]





#updates the colour of the keys on the keyboard when letters are entered
def updateKeyboard(gameData,letter,newColour):

    currentKey = gameData.keyboardBtns[gameData.keyboard.index(letter)]
    colourWeight = ["grey","#555555","orange","green"]


    #if the new colour is "heavier" than the current key colour
    if colourWeight.index(newColour) > colourWeight.index(currentKey["bg"]):
        currentKey["bg"] = newColour
        currentKey["activebackground"] = newColour





#gets a list of colours to be displayed on the wordle board
def getColours(gameData,guess):

    keyWord = list(gameData.keyWord)
    colours = ["grey"]*5


    #loop to find shared letters in the same place
    for index in range(5):

        if keyWord[index] == guess[index]:
            updateKeyboard(gameData,guess[index],"green")
            colours[index] = "green"
            #adds a hash to stop these letters being compared again
            keyWord[index] = "#"
            guess[index] = "#"
                      

    #loop to find shared letters in a different place
    for firstIndex in range(5):

        if guess[firstIndex] == "#":
            continue


        for secondIndex in range(5):
                
            if keyWord[secondIndex] == guess[firstIndex]:
                updateKeyboard(gameData,guess[firstIndex],"orange")
                colours[firstIndex] = "orange"
                #adds a hash to stop these letters being compared again
                keyWord[secondIndex] = "#"
                guess[firstIndex] = "#"
                break


            elif secondIndex == 4:
                updateKeyboard(gameData,guess[firstIndex],"#555555")

        
    return colours





#the game
def wordle():



    def handleKeypress(event):
        updateGuess(event.keysym)



    #updates the current entry within the final row
    def updateGuess(update):

        if currentGameData.gameOver == False:

            #adds the entered letter to the final row of the grid
            if update.lower() in "abcdefghijklmnopqrstuvwxyz":

                for letterLbl in currentGameData.letterRows[-1]:

                    if letterLbl["text"] == "":

                        letterLbl["text"] = update.upper()
                        break

            
            #removes the last letter from the final row of the grid
            elif update == "BackSpace" or update == "\N{BACK WITH LEFTWARDS ARROW ABOVE}":

                for letterLbl in reversed(currentGameData.letterRows[-1]):

                    if letterLbl["text"] != "":

                        letterLbl["text"] = ""
                        break


            elif update == "Return" or update == "\N{RETURN SYMBOL}":
                guessVerify()



    def guessVerify():

        #gets a string of guess from final row
        guess = "".join([letterLbl["text"].lower() for letterLbl in currentGameData.letterRows[-1]])


        #reset final row
        for letterLbl in currentGameData.letterRows[-1]:
            letterLbl["text"] = ""
        

        #if guess is a valid word
        if len(guess) == 5 and binarySearch(currentGameData.wordBank,guess):
            
            currentColours = getColours(currentGameData,list(guess))
            updateWordleBoard(guess,currentColours,currentGameData.letterRows[currentGameData.currentGuess])
            currentGameData.currentGuess += 1

            #end game if user has guessed correct word or has made 6 guesses
            if currentColours == ["green"]*5:
                endGame("Well Done!")
            elif currentGameData.currentGuess == 6:
                endGame("Game Over!")



    def endGame(message):

        currentGameData.gameOver = True
        window.unbind("<Key>")

        finishLbl = tk.Label(text=f"{message}\nThe word was {currentGameData.keyWord.upper()}", font=("Arial",30),
                            bg="grey", fg="white",
                            padx=70, pady=41)   
        finishLbl.grid(row=0, column=1)



    currentGameData = gameSessionData()

    

    window = tk.Tk()
    window.title("Gav's Wordle Clone")
    window.geometry("1240x850")
    window.configure(bg="white")
    window.bind("<Key>",handleKeypress)



    #wordle board code - - - - - start
    wordleBoardFrame = tk.Frame(bg=window["bg"])
    wordleBoardFrame.rowconfigure([0,1,2,3,4,5], minsize=100)
    wordleBoardFrame.columnconfigure([0,1,2,3,4], minsize=100)
    wordleBoardFrame.grid(row=0, column=0, padx=75, pady=90)


    for r in range(6):

        letterLbls = [0]*5

        for c in range(5):

            letterLbl = tk.Label(wordleBoardFrame, font=("Arial",25), bg="grey", fg="white")
            letterLbls[c] = letterLbl
            letterLbl.grid(row=r, column=c, sticky="nesw", padx=5, pady=5)

        currentGameData.letterRows[r] = letterLbls
    #wordle board code - - - - - end



    #keyboard code - - - - - start
    keyboardFrame = tk.Frame(bg=window["bg"])
    keyboardFrame.rowconfigure([0,1,2], minsize=50)
    keyboardFrame.columnconfigure([0,1,2,3,4,5,6,7,8,9], minsize=50)
    keyboardFrame.grid(row=0, column=1, padx=20, pady=90)


    for r in range(3):
        for c in range(10):

            currentKey = currentGameData.keyboard[r*10 + c]
            if currentKey == 0:
                continue

            keyBtn = tk.Button(keyboardFrame, relief=tk.FLAT, 
                                text=f"{currentKey.upper()}", font=("Arial",20), 
                                bg="grey", fg="white", activebackground="grey", activeforeground="white",
                                #binds the updateGuess function to the button with the current key as the variable
                                #the functools.partial() method allows each button created in the loop to have a unique function
                                command=functools.partial(updateGuess,currentKey))
            currentGameData.keyboardBtns[r*10 + c] = keyBtn
            keyBtn.grid(row=r, column=c, sticky="nesw", padx=2, pady=2)
    #keyboard code - - - - - end



    window.mainloop()





wordle()