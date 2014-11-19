# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# Going to initialize some global variables here
ball_pos = [WIDTH /2, HEIGHT / 2]
ball_vel = [2, 2]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    """ Set random, upward velocity for a ball positioned in the center of the canvas """
    global ball_pos, ball_vel # these are vectors stored as lists
    
    # Step 2 from instructions, reset the ball position
    ball_pos = [WIDTH /2, HEIGHT / 2]
    
    # Set the ball velocity according to a random direction, and the previous outcome
    # Ball should always go up
    ball_vel[1] = -random.randrange(120,240) / 50 
    if direction == True:
        ball_vel[0] = -random.randrange(60, 180) / 50
    else:
        ball_vel[0] = random.randrange(60, 180) / 50
   
# define event handlers
# We will assign this to a button, eventually.
def new_game():
    """ Start a new game """
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # Step 3
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    # Reset the ball in a random direction
    spawn_ball(random.choice([True, False]))    
    
def draw(canvas):
    """ Render Pong on the canvas. """
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
     
    # draw mid line and gutters
    # The mid line
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    # The left gutter 
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    # The right gutter
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # Step 4: ball bounce.
    # Reflection off the top wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # Reflection off the bottom wall
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS: 
        ball_vel[1] = -ball_vel[1]
    
    
    # Step 6: respawn if the ball touches the left or right gutters.
    # or, reflection if ball touches paddle
    
    # Ball touches left gutter
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH: 
        # Paddle1 is there, reflection
        if ball_pos[1] + BALL_RADIUS>= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            # Add 10% acceleration after each reflection
            ball_vel[0] = - ((ball_vel[0] * 0.1) + ball_vel[0]) 
        # Paddle2 is not there, point and spawn
        else:
            score2 += 1
            spawn_ball(False)
            
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH: 
        # Paddle2 is there, reflection
        if ball_pos[1] + BALL_RADIUS >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            # Add 10% acceleration after each reflection
            ball_vel[0] = - ((ball_vel[0] * 0.1) + ball_vel[0]) 
        # Paddle2 is not there
        else:
            score1 += 1
            spawn_ball(True)
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White") 
    
    # update paddle's vertical position, keep paddle on the screen
    # Paddle 1 position
    # I'm not suuuper happy with this solution, the paddle gets kinda jumps
    # on the edge of the canvas. Best I could do, for now. 
    if paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos += 1
    elif paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos -= 1
    else:
        paddle1_pos += paddle1_vel
    # Paddle 2 postion
    if paddle2_pos < 40:
        paddle2_pos += 1
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos -= 1
    else:
        paddle2_pos += paddle2_vel

    # draw paddles
    canvas.draw_line([0, paddle1_pos - HALF_PAD_HEIGHT], [0,  paddle1_pos + HALF_PAD_HEIGHT], 17, "White")
    canvas.draw_line([WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], 17, "White")
    
    # draw scores
    canvas.draw_text(str(score1), [(WIDTH / 4 * 1), 50], 60, "Red")    
    canvas.draw_text(str(score2), [(WIDTH / 4 * 3), 50], 60, "Green")
        
def keydown(key):
    """ Paddle movement when key pressed. """
    global paddle1_vel, paddle2_vel
    
    # Player 1 paddle control
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= 5   
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += 5
    # Player 2 paddle control
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= 5
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += 5
  
def keyup(key):
    """ Paddle stop when key not pressed. """
    global paddle1_vel, paddle2_vel
    
    # Player 1 paddle control
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel =  0
    # Player 2 paddle control
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel =  0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Restart', new_game, 200)

# start frame
new_game()
frame.start()

