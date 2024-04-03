# --- Hangman v3.0 | Anonymous Functions & Complex Collections  --- #

import msvcrt
import sys


# get a word from the current player entered in secret
# created with help from these two stackoverflow pages.
# https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input
# https://stackoverflow.com/questions/30534218/pycharm-msvcrt-kbhit-and-msvcrt-getch-not-working
# TODO: backspace does not yet work properly
def getWordToGuess(prompt):
    print(prompt)
    word = ''
    while True:
        x = msvcrt.getch().decode("utf-8")
        if x == '\r':
            break
        print('*', end='', flush=True)
        word += str(x)
    print()
    return word


def printList(list, delimiter=""):
    print(toString(list, delimiter))


# joining a list to a string returns the list as a concatenated string
def toString(list, delimiter=""):
    return delimiter.join(list)


# save all indices of items for which the lambda function returns True
def findIndices(collection, lambdo):
    return [index for index, item in enumerate(collection) if lambdo(item)]

    # older version
    # indices = []
    # for index, item in enumerate(list):
    #    if lambdo(item):
    #        indices.append(index)
    # return indices


def updateHangman(hangman, hangMap, lambdo, parts, partIndex):
    # NOTE: we find all places where a character is on the hangMap
    mapIndices = findIndices(hangMap, lambdo)
    for index in mapIndices:
        # NOTE: we offset all indices found with the saved offset of that (body or gallows) part
        index -= parts[1]
        # NOTE: we 'draw' the next part on the actual hangman
        hangman[index] = parts[partIndex]


def updateAndShowGuess(chars, guess):
    chars.add(guess.lower())
    print(f"you guessed: {chars}\n")


def showWinLoseMessage(mistakes, maxMistakes, player, word):
    if mistakes == maxMistakes:
        print(f"You've run out of guesses {player}!")
    else:
        print(f"That's right {player}! Well done")
    print(f"The word was: {word}\n\n")


def updateAndShowHighscore(highscore, player, mistakes, maxMistakes):

    # D2. update scores if player has won
    playerWon = mistakes != maxMistakes
    if hs := highscore.get(player):
        if not playerWon:
            # D2A. Reset current streak if player did not win
            highscore[player] = (hs[0], 0, playerWon)
        else:
            # D2B. Update highscore and increase current streak and if player won.
            highscore[player] = (max(hs[0], hs[1] + 1), hs[1] + 1, playerWon)
    else:
        # D2C. First entry for player, save if player has won or not.
        score = 1 if playerWon else 0
        highscore[player] = (score, score, playerWon)

    # D3. show player scores
    for (player, values) in highscore.items():
        print(f"{player} has guessed {values[0]} words right in a row")
        print(f"{player}'s current streak is {values[1]}")
        print(f"Last guess was: {"correct" if values[2] else "wrong"} \n")


def changePlayerRoles(leader, guesser):
    temp = guesser
    guesser = leader
    leader = temp
    return (leader, guesser)


def main(**kwargs):

    # A. Initialize the game
    # ---------------------------------

    # A1. create gallows (galg)
    gallows = list("           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "           \n"
                   "___________")

    # NOTE: we create a second list with a map where all the parts go
    #       with this setup we can also easily build the gallows
    #       before hanging the man.
    hangMap = list("11111111111\n"
                   "0 3    2   \n"
                   "03     2   \n"
                   "0      4   \n"
                   "0      5   \n"
                   "0    7 6 8 \n"
                   "0     9 A  \n"
                   "0     B C  \n"
                   "0          \n"
                   "0__________")

    # A2. create body parts
    # Note: for each part we say:
    #       1. Which character on the hangMap should be replaced
    #       2. How many spaces to the left we need to offset the placement
    #       3. The character to which the places on the hangMap should be changed
    bodyAndGallowsParts = [('0', 0, "|"),
                           ('1', 0, "-"),
                           ('2', 0, "|"),
                           ('3', 0, "/"),
                           ('4', 2, "(o_o)", "{x_x}"),
                           ('5', 1, "/|\\"),
                           ('6', 0, "|"),
                           ('7', 0, "^"),
                           ('8', 0, "^"),
                           ('9', 0, "/"),
                           ('A', 0, "\\"),
                           ('B', 1, "_|"),
                           ('C', 1, "|_")]

    # A3. create players
    print("Welcome to hangman!")
    print("\n=====================================\n")

    player1 = kwargs["player1"] if kwargs.get("player1") else input("Player 1, what is your name: ")
    player2 = kwargs["player2"] if kwargs.get("player2") else input("Player 2, what is your name: ")

    # A4. set the leader & the guesser
    leader = player1
    guesser = player2

    # A5. create player scores
    highscores = {player1: (0, 0, False), player2: (0, 0, False)}

    # A6. set maxMistakes
    maxMistakes = len(bodyAndGallowsParts)

    # A7. start the game loop
    while True:

        # B. The round setup
        # ---------------------------------------------

        # B1. set current mistakes to 0
        mistakes = 0
        # B2. create copy of gallows to draw hangman on
        hangman = gallows.copy()

        # B3. create a place to store guessed characters
        guessedChars = set()
        print("\n=====================================\n")

        # B4. get word to guess from the current leader
        wordToGuess = getWordToGuess(f"{leader}, enter a word to be guessed by {guesser}").lower()

        # B5. create hidden word based on word to guess
        hiddenWord = list("________________________________________")
        hiddenWord = hiddenWord[:len(wordToGuess)]  # a string with the same amount of stripes as the word to guess
        print()

        # C. The guessing loop
        # while word is not guessed and other player still has tries left
        while toString(hiddenWord) != wordToGuess and mistakes != maxMistakes:

            # C1. show current hidden word
            print("-------------------------------------\n")
            print(f"the word is: {toString(hiddenWord)}")

            # C2. get guessing player's guess
            guess = input(f"{guesser}, guess a character: ")

            # C3. check if guess is valid
            if len(guess) > 1 or len(guess) == 0:
                print("please guess only 1 character at a time")
            elif toString(guessedChars).find(guess.lower()) != -1:
                print(f"you already guessed: {guess}")
                print(f"you guessed: {guessedChars}\n")
            else:

                # C4. find guess in word to guess
                # ===============================================================

                guessIndices = findIndices(wordToGuess, lambda char: char == guess.lower())

                # -------------------------------------------------------------
                # C5. guess is not in word: update mistakes & hangman
                # -------------------------------------------------------------

                if len(guessIndices) == 0:
                    print(f"{guess} is not correct\n")

                    # NOTE: now that we use the hangMap to set where parts are assigned,
                    #       we don't have to hardcode the places of where parts go.
                    # convert to hex value (0-F)
                    updateHangman(hangman, hangMap, lambda char: char == format(mistakes, 'X'),
                                  bodyAndGallowsParts[mistakes], 2)
                    mistakes += 1
                    if mistakes == maxMistakes:
                        # NOTE: now that we have a function to place parts of the hangman, we can also change them
                        #       the head will change from o_o to x_x when the player has lost.
                        headIndex = 4
                        updateHangman(hangman, hangMap, lambda char: char == str(headIndex),
                                      bodyAndGallowsParts[headIndex], 3)
                    printList(hangman)

                # -------------------------------------------------------------
                # C6. guess is correct: update guessed word
                # -------------------------------------------------------------

                # NOTE: Because we get all indices inside the findIndices function, the update part is a lot simpler.
                for index in guessIndices:
                    hiddenWord[index] = wordToGuess[index]

                # C7. update & show guessed characters
                updateAndShowGuess(guessedChars, guess)

        print("#####################################\n")

        # D.  Conclude the round
        # ----------------------------------

        # D1. show win or lose message
        showWinLoseMessage(mistakes, maxMistakes, guesser, wordToGuess)

        # D2. update scores if player has won
        # D3. show player scores
        updateAndShowHighscore(highscores, guesser, mistakes, maxMistakes)

        print("#####################################\n")

        # D4. change player roles
        # NOTE: we set the values of both player variables
        #       to the two return values of the changePlayers function
        (leader, guesser) = changePlayerRoles(leader, guesser)


printList(sys.argv, ", ")
sysdict = dict(arg.split('=') for arg in sys.argv[1:]) if len(sys.argv) > 0 else {}
print(sysdict)
main(**sysdict)
