# --- Hangman v2.0 | Functions & Collections  --- #

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


def updateAndShowGuessedChars(chars, guess):
    chars.add(guess.lower())
    print(f"you guessed: {chars}\n")


def showWinLoseMessage(mistakes, maxMistakes, player, word):
    if mistakes == maxMistakes:
        print(f"You've run out of guesses {player}!")
    else:
        print(f"That's right {player}! Well done")
    print(f"The word was: {word}\n")


def changePlayerRoles(leader, guesser):
    temp = guesser
    guesser = leader
    leader = temp
    return (leader, guesser)


def printList(list, separator=""):
    print(toString(list, separator))


# joining a list to a string returns the list as a concatenated string
def toString(list, separator=""):
    return separator.join(list)


def updateAndShowHighscore(highscore, current, mistakes, maxMistakes):
    # E. update scores if guessing player has won
    if mistakes != maxMistakes:
        highscore[current] = 1 if not highscore.get(current) else highscore[current] + 1
    # F. show scores
    for (player, value) in highscore.items():
        print(f"score {player}:{value}")
    print()


def main(*args):
    arguments = args[0][1:]

    # A. Initialize the game
    # ---------------------------------

    # A1. create gallows (galg)
    gallows = list("___________\n"
                   "| /    |   \n"
                   "|/     |   \n"
                   "|          \n"
                   "|          \n"
                   "|          \n"
                   "|          \n"
                   "|          \n"
                   "|          \n"
                   "|__________")

    # A2. create body parts
    head = "(x_x)"
    shoulders = "/|\\"
    arm = "^"
    body = "|"
    leftLeg = "/"
    leftFoot = "_|"
    rightLeg = "\\"
    rightFoot = "|_"

    # A3. create players
    print("Welcome to hangman!")
    print("\n=====================================\n")
    player1 = arguments[0] if len(arguments) > 0 else input("Player 1, what is your name: ")
    player2 = arguments[1] if len(arguments) > 1 else input("Player 2, what is your name: ")

    # A4. set the leader & the guesser
    leader = player1
    guesser = player2

    # A5. create player scores
    scores = {player1: 0, player2: 0}

    # A6. set maxMistakes
    maxMistakes = 9

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
        # ----------------------------------
        # while word is not guessed and guessing player still has tries left
        while toString(hiddenWord) != wordToGuess and mistakes != maxMistakes:

            # C1. show current hidden word
            print("-------------------------------------\n")
            print(f"the word is: {toString(hiddenWord)}")

            # C2. get guessing player's guess
            guess = input(f"{guesser}, guess a character: ")

            # C3. check if guess is valid
            if len(guess) > 1 or len(guess) == 0:
                print("please guess only 1 character at a time")
                continue
            elif toString(guessedChars).find(guess.lower()) != -1:
                print(f"you already guessed:{guess}")
                print(f"you guessed: {guessedChars}\n")
                continue

            # C4. find guess in word to guess
            # ===============================================================

            # Note: it's easier to find characters in a string than in a list
            guessIndex = toString(wordToGuess).find(guess.lower())
            isGuessFound = guessIndex != -1

            # -------------------------------------------------------------
            # C5. guess is not in word: update mistakes & hangman
            # -------------------------------------------------------------

            if not isGuessFound:
                print(f"{guess} is not correct\n")
                mistakes += 1
                # NOTE: now that hangman is a list
                #       it allows us to assign body parts directly
                match mistakes:
                    case 1: hangman[41] = head
                    case 2: hangman[54] = shoulders
                    case 3: hangman[67] = body
                    case 4: hangman[65] = arm
                    case 5: hangman[69] = arm
                    case 6: hangman[78] = leftLeg
                    case 7: hangman[80] = rightLeg
                    case 8: hangman[89] = leftFoot
                    case 9: hangman[91] = rightFoot
                printList(hangman)

            # -------------------------------------------------------------
            # C6. guess is correct: update guessed word
            # -------------------------------------------------------------

            # NOTE: we look for every place of the guessed character
            #       by repeating the search until all places are found
            # EXAMPLE: if we look for c in the word 'character':
            #          1. we first find c on index 0
            #          2. then we look for the next c in the remaining word: 'haracter'
            #          3. we find c again on index 5 (of the original word)
            #          4. again we look for the next c in the remaining word: 'ter'
            #          5. no c is found --> isGuessFound is False, and we exit the while loop
            while isGuessFound:
                # we reveal the next place the guessed character is found in the wordToGuess
                hiddenWord[guessIndex] = wordToGuess[guessIndex]
                # we look for the next place the guessed character is found
                guessIndex = toString(wordToGuess).find(guess.lower(), guessIndex + 1)
                # we update if there is another place of the guessed character
                isGuessFound = guessIndex != -1

            # =================================================================================

            # C7. update & show guessed characters
            updateAndShowGuessedChars(guessedChars, guess)

        print("#####################################\n")

        # D.  Conclude the round
        # ----------------------------------

        # D1. show win or lose message
        showWinLoseMessage(mistakes, maxMistakes, guesser, wordToGuess)

        # D2. update scores if guesser has won
        # D3. show player scores
        updateAndShowHighscore(scores, guesser, mistakes, maxMistakes)

        # D4. change player roles
        # NOTE: we set the values of both player variables
        #       to the two return values of the changePlayers function
        (leader, guesser) = changePlayerRoles(leader, guesser)

        print("#####################################\n")


main(sys.argv)
