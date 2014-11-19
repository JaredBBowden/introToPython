# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

# Import the required modules
import simplegui
import math
import random

# helper function to start and restart the game
def new_game():
    """ New game defaults to a range of 0 - 100 unless button is pressed """
    print "Welcome to the guess the number game!"
    print "Game defaults to a range of 0 - 100, select a button for more options."
    print ""
    return range100()
    
# define event handlers for control panel
def range100():
    """ Start a game with range of 0 to 100. """
    # button that changes the range to [0,100) and starts a new game 
    global secret_number
    global guess_limit
    global game_type
    game_type = 0
    secret_number = random.randrange(0, 100)
    print " "
    print "New game. Range is between 0 and 100"
    guess_limit = 7
    print "guesses remaining: " + str(guess_limit)
    print ""
    
def range1000():
    """ Start a game with range of 0 to 1000. """
    # button that changes the range to [0,1000) and starts a new game     
    global secret_number
    global guess_limit
    global game_type
    game_type = 1
    secret_number = random.randrange(0, 1000)
    print " "
    print "New game. Range is between 0 and 1000"
    guess_limit = 10
    print "guesses remaining: " + str(guess_limit)
    print ""
    
def input_guess(guess):
    """ Play guess the number. """
    global secret_number
    global guess_limit
    global game_type
    guess_limit -= 1
    print "Guesses remaining: " + str(guess_limit)
    print "Guess was " + guess
    guess = int(guess)
    # main game logic goes here	
    if guess_limit >= 1:
        if guess > secret_number:
            print "Lower"
            print ""
        elif guess < secret_number:
            print "Higher"
            print ""
        elif guess == secret_number:
            print "Correct!"
            if game_type == 1:
                return range1000()
            else:
                return range100()
        else:
            print "Invalid input"
    else:
        print "You are out of guesses, game over"
        if game_type == 1:
            return range1000()
        else:
            return range100()

# create frame
f = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
f.add_input("Enter a guess", input_guess, 200)
f.add_button("Range: 0 - 100", range100, 200)
f.add_button("Range: 0 - 1000", range1000, 200)            

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric

