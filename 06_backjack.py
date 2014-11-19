# Mini-project #6 - Blackjack

# WARNING there are some fairly verbose comments in here.
# I didn't have time to curate things; the result is some pretty
# stream-of-consciousness code

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            
# define hand class
# This appears to be working -- tested
class Hand:
    def __init__(self):
        # The players hand, represented as a list 
        self.cards = []               
        
    def __str__(self):
        # return a string representation of a hand
        # We can do this with the methods we have for returning suit and rank objects. However,
        # we will have to make them strings
        return "Hand contains " + " ".join([str(c) for c in self.cards])
        
    def add_card(self, card):
        # Append a card to the hand-list we initialized, above
        self.cards.append(card)
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        
        # Alright... we need a way to count aces.
        # Also, initialize a variable to sum the value of a hand
        aces = 0 
        hand_value = 0     
       
        # an ace should be added at full value (11), providing it doesn't
        # result in a bust.
        for c in self.cards:
            # Computer hand value before aces
            rank = c.get_rank()
            hand_value += VALUES.get(rank)
            if c == "A" and hand_value >= 10:
                hand_value += 10
             
        return hand_value
                
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        # I suppose we just need to lay the cards to they don't overlap on the canvas.
        # We should have a method to specify position already... so, we want the horizontal position 
        # to itterate as we add more cards.        
        p = 0      
        for c in self.cards:        
            c.draw(canvas, (pos[0] + (72 * p), pos[1]))
            p += 1
   
# define deck class
# Tested, and appears to work.
class Deck:
    def __init__(self):
        
        # We want to make an object, and this object is a collection of cards -- represented as a list
        self.cards = []
        # Now presumably, we will want to populate this list with cards. Do we have a method to do this?
        # We have each of the characteristics represented as a list, and we have a card method that we
        # should be able to sting these things together.
        for suit in SUITS:
            for rank in RANKS:	          
                # append to the cards (deck) object                
                self.cards.append(Card(suit, rank))            
       
    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.cards)
        
    def deal_card(self):
        # deal a card object from the deck
        return random.choice(self.cards)
    
    def __str__(self):
        # return a string representing the deck
        # Use the same list comprehension that we used for the previous method.
        return "Deck contains " + " ".join([str(c) for c in self.cards])

#define event handlers for buttons

# For the deal handler, we are going to need the deal_card method of Deck, and add_card method of hand
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    # Add a variable to track the score.
    
    # If the player shuffles while play is running, count as a loss
    if in_play == True:
        score -= 1
        outcome = "Dealer wins."
        in_play = False
    
    if in_play == False:
            
        # Here, we want to deal 2 cards to the dealer, and the player
       
        # I suppose the first step is to make a list of random cards with deal_card, and then add these
        # cards to player and dealer hands with add_card
        
        # Make a deck object
        deck = Deck()
        
        # Use the shuffle method of deal
        deck.shuffle()
        
        # We now have a shuffled list of cards, but we need to initialize some hands to we can
        # add cards to this
        
        # This was confusing at first, but we can intialize these variables with the class name.
        # Now, when we add cands to this (other method), we can take advantage of all the nested 
        # methods associated with Hand.
        player_hand = Hand()
        dealer_hand = Hand()
        
        # Now deal two cards to the player, and the dealer
        
        # Hmm... According to the instructions, there's another step in here where I need to deal
        # a card before I add the card. Oh, this needs to be rolled into our loop.
        
        for x in range(2):
            # Basically, we want to run this method twice.
            player_hand.add_card(deck.deal_card())
            dealer_hand.add_card(deck.deal_card())
            
        # Alright, now we should have two cards in each hand... if all that worked. For now, we want to
        # print this to the console. If our hand methods are working, we should be
        # able to just print this out....
        
        print "Player hand is: ", player_hand
        print "Dealer hand is: ", dealer_hand
        
        # Now we want to use the get_value method on these hands, so we can compare
        # them.
        
        print "player: ", player_hand.get_value()
        print "dealer: ", dealer_hand.get_value()
        
        outcome = "Hit or stand?"
        in_play = True

def hit():
    
    # replace with your code below
    global outcome, in_play, score
    # if the hand is in play, hit the player
    if in_play == True:
        if player_hand.get_value() <= 21:
            # Add another card 
            player_hand.add_card(deck.deal_card())
            # Value the hand. If the value is higher than 21, print a bust message
        if player_hand.get_value() > 21:
            outcome = "You have busted. New Deal?"
            in_play = False
            score -= 1
        if player_hand.get_value() == 21:
            outcome = "Player has won!"
            in_play = False
            score =+ 1
     
    
def stand():
    # replace with your code below
    global outcome, in_play, score
    
    # Update the dealers deck 
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    
    if dealer_hand.get_value() > 21:
        outcome = "Player has won!"
        in_play = False
        score += 1 
    
    if player_hand.get_value() > 21:
        outcome = "You have busted"
        in_play = False
        score -= 1
        
    if (player_hand.get_value() > dealer_hand.get_value()) and player_hand.get_value() <= 21:
        outcome = "Player has won!"
        in_play = False
        score += 1
    
    if (player_hand.get_value() < dealer_hand.get_value()) and dealer_hand.get_value() <= 21:
        outcome = "Dealer has won."
        in_play = False
        score -= 1
    
    elif player_hand.get_value() == dealer_hand.get_value():
        outcome = "Dealer has won."
        in_play = False
        score -= 1
        
    
# draw handler    
def draw(canvas):
    # Draw text for the title of the game
    canvas.draw_text("Blackjack", (10, 60), 60, "Red")
    
    # Draw the hands on the canvas
    dealer_hand.draw(canvas, [10, 300])    
    player_hand.draw(canvas, [10, 500])
    
    # Label dealer and player hands
    canvas.draw_text("Dealer", (10, 290), 40, "White")
    canvas.draw_text("Player", (10, 490), 40, "White")
    
    
    # Going to just draw an image over the first card of the dealers hand, to hide
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (46, 348), CARD_BACK_SIZE)
    
    # Draw some text feedback for outcome
    canvas.draw_text(outcome, (10, 120), 40, "White")
    
    # Draw the score
    canvas.draw_text(("Score: " + str(score)), (425, 60), 40, "White")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
