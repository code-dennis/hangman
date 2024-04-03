# Hangman in Python 3.12

This hangman project showcases how to use collections and functions to create more readable and better performing Python code.

The project contains three versions of the hangman game that can all be played in the python console.
  1) The file week123.py contains a version of hangman that contains only basic variables, loops and conditions.
  2) week56.py expands on the week123 version by introducing simple collections and functions.
  3) week7.py concludes the showcase by adding complex collections and functions.

------------------------------------------------------------------------------------------------------------------------------
To succesfully run week56.py and week7.py you need to add the emulate terminal option in the run configuration settings.
This has to be done in order to hide the word the leading player is typing so that the guessing player does not see it. 

------------------------------------------------------------------------------------------------------------------------------
1. Right click on the week56.py file in the project overview and select More Run/Debug -> Modify Run Configuration...
2. Click on Modify Options in the run configurations window.
3. Select Emulate terminal in console output.
4. You can now see the option added on the bottom of the run configurations window.
5. Click OK to save the new configuration
6. You can now see the run configuration in top top right corner of the main PyCharm window - next to the play button.
7. Repeat these steps for both the week7.py.
  
If you want to hide the input in main.py, you need to implement the getWordToGuess function from week56.py add the emulate terminal option there as well. 

See screenshots folder for images of these steps.

In the screenshots folder you can also find examples of how to set player names from outside the application. 
Week56 uses args as parameter inputs and week7 uses kwargs.

------------------------------------------------------------------------------------------------------------------------------

The main.py file is a copy of week123.py. 
Here you can experiment with adding collections and functions all you want.

If the code breaks and you don't know how to fix it anymore,
You can simply start over by copying the code from week123.py to main.py.

In the roadmap file you can see the steps that the code consists of.

See the challenge file for more challenges once you got the hang of functions and collections.

Good luck and have fun!
