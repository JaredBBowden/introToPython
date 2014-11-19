# implementation of card game - Memory

import simplegui
import random
import math

# To-do
# This is odd... but the turns don't reset (after a button press) until the next
# turn has registered.

# This math operation I am using to set the mouse coordinates is
# not the best.

# helper function to initialize globals
def new_game():
    """
    Rest all varibels to default
    """
    global exposed, deck_cards, state, turns
    turns = 0
    # Game state
    state = 0
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
    # STEP 1: Model the deck of cards 
    deck_cards = [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8]
    correct_cards = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False] 
    # STEP 3: Shuffle the deck using random.shuffle
    random.shuffle(deck_cards)
         
# define event handlers
def mouseclick(pos):
    """
    Rules that define the logic of the memory game, flip cards, and count turns
    """
    # add game state logic here
    global deck_cards, state, exposed, first_card, second_card, turns 
    # After many compicated attempts, this seems to be the best approach:
    # We can find the postion of our numbers (defined below) by rounding 
    # down the x cordinate of the mouse position  
    selection = math.floor(pos[0] /50)
    
    # Rules for the first flip
    if state == 0:
        state = 1
        first_card = selection
        # Turn the card over
        exposed[selection] = True
    
    # Second flip
    elif state == 1:
        if not exposed[selection]:
            state = 2
            # Identify the card that was flipped
            second_card = selection
            exposed[second_card] = True
            turns += 1
      
    elif state == 2:
        # If cards are the same, move back to previous game state
        if not exposed[selection]:
            if deck_cards[first_card] == deck_cards[second_card]:
                pass
            # If cards are not the same, flip over
            else:
                exposed[first_card] = False
                exposed[second_card] = False
            # Identify the card that was flipped
            first_card = selection
            exposed[first_card] = True
            state = 1       
        # Count turns    
        label.set_text("Turns = " + str(turns))       
            
#cards are logically 50x100 pixels in size    
def draw(canvas):
    # Loop: do this 16 times. This index will be use for to render both cards AND numbers.
    for i in range(16):
        # Having some issues with spacing of these nunbers. Perhaps add some lines to emphasize
        # separation.
        if exposed[i]:
            canvas.draw_text(str(deck_cards[i]), [((50 * i) + 10), 70], 60, "White")
        # Draw a polygone.
        else:
            #canvas.draw_text(str(deck_cards[i]), [((50 * i) + 10), 70], 60, "Green")
            canvas.draw_polygon([(50 * i, 50), (((50 * i) + 50), 50)], 60, 'Green')
    # Well, this is ugly, but I think it makes things a little more clear.        
    for g in range(17):
        canvas.draw_line((0 + g * 50, 0), (0 + g * 50, 100), 5, 'Red')
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
