# --- Hangman v1.0 --- #

# A. Initialize the game
# ---------------------------------

# A1. create gallows (galg)
gallows = ("___________\n"
           "| /    |   \n"
           "|/     |   \n"
           "|          \n"
           "|          \n"
           "|          \n"
           "|          \n"
           "|          \n"
           "|          \n"
           "|__________\n")

# A2. create body parts
head = "(x_x)"
shoulders = "/|\\"
arm = "^"
body = "|"
leftLeg = "/"
rightLeg = "\\"
leftFoot = "_|"
rightFoot = "|_"

# A3. create players
print("Welcome to hangman!")
print("\n=====================================\n")
player1 = input("Player 1, what is your name: ")
player2 = input("Player 2, what is your name: ")

# A4. set the leader & the guesser
leader = player1
guesser = player2

# A5. create player scores
scorePlayer1 = 0
scorePlayer2 = 0

# A6. set maxMistakes
maxMistakes = 9

# A7. start the game loop
while True:

    # B. The round setup
    # ---------------------------------------------

    # B1. set current mistakes to 0
    mistakes = 0

    # B2. create copy of gallows to draw hangman on
    hangman = gallows

    # B3. create a place to store guessed characters
    guessedChars = ""

    print("\n=====================================\n")

    # B4. get word to guess from the current leader
    # TODO: hide input from player entering the word to guess
    wordToGuess = input(f"{leader}, enter a word to be guessed by {guesser}\n").lower()

    # B5. create hidden word based on word to guess
    hiddenWord = "________________________________________"
    hiddenWord = hiddenWord[:len(wordToGuess)]  # a string with the same amount of stripes as the word to guess
    print()

    # C. The guessing loop
    # ----------------------------------
    # while word is not guessed and guessing player still has tries left
    while hiddenWord != wordToGuess and mistakes != maxMistakes:

        # C1. show current hidden word
        print("-------------------------------------\n")
        print(f"the word is: {hiddenWord}")

        # C2. get guessing player's guess
        guess = input(f"{guesser}, guess a character: ")

        # C3. check if guess is valid
        if len(guess) > 1 or len(guess) == 0:
            print("please guess only 1 character at a time")
            continue
        elif guessedChars.find(guess.lower()) != -1:
            print(f"you already guessed: {guess}")
            print(f"you guessed: {guessedChars} \n")
            continue

        # C4. find guess in word to guess
        # =================================================================================

        guessIndex = wordToGuess.find(guess.lower())
        isGuessFound = guessIndex != -1

        # -------------------------------------------------------------
        # C5. guess is not in word: update mistakes & hangman
        # -------------------------------------------------------------

        if not isGuessFound:
            print(f"{guess} is not correct\n")
            mistakes += 1
            if mistakes == 1:
                hangman = hangman[:41] + head + hangman[42:]
            elif mistakes == 2:
                hangman = hangman[:58] + shoulders + hangman[59:]
            elif mistakes == 3:
                hangman = hangman[:73] + body + hangman[74:]
            elif mistakes == 4:
                hangman = hangman[:71] + arm + hangman[72:]
            elif mistakes == 5:
                hangman = hangman[:75] + arm + hangman[76:]
            elif mistakes == 6:
                hangman = hangman[:84] + leftLeg + hangman[85:]
            elif mistakes == 7:
                hangman = hangman[:86] + rightLeg + hangman[87:]
            elif mistakes == 8:
                hangman = hangman[:95] + leftFoot + hangman[96:]
            elif mistakes == 9:
                hangman = hangman[:98] + rightFoot + hangman[99:]
            print(hangman)

        # -------------------------------------------------------------
        # C6. guess is correct: update guessed word
        # -------------------------------------------------------------

        while isGuessFound:
            hiddenWord = hiddenWord[:guessIndex] + wordToGuess[guessIndex] + hiddenWord[guessIndex + 1:]
            guessIndex = wordToGuess.find(guess.lower(), guessIndex+1)
            isGuessFound = guessIndex != -1

        # =================================================================================

        # C7. update & show guessed characters
        if len(guessedChars) == 0:
            guessedChars += "'" + guess.lower() + "'"
        else:
            guessedChars += ", '" + guess.lower() + "'"
        print(f"you guessed: {guessedChars}\n")

    # D.  Conclude the round
    # ----------------------------------

    print("#####################################\n")

    # D1. show win or lose message
    if mistakes == maxMistakes:
        print(f"You've run out of guesses {guesser}! \n")
    else:
        print(f"That's right {guesser}! Well done\n")

        # D2. update scores if player has won
        if guesser == player1:
            scorePlayer1 += 1
        elif guesser == player2:
            scorePlayer2 += 1

    print(f"The word was: {wordToGuess}\n")

    # D3. show player scores
    print(f"score {player1}: {scorePlayer1}")
    print(f"score {player2}: {scorePlayer2}")
    print("\n#####################################\n")

    # D4. change player roles
    temp = guesser
    guesser = leader
    leader = temp
