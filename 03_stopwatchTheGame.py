# template for "Stopwatch: The Game"

# Import the required module 
import simplegui

# define global variables

# The counter we will use to increment time (units: 10 ms)
counter = 0
seconds = 0
minutes = 0
tries = 0
successes = 0
running_game = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    """ Format timer events as seconds, minutes, and 10 ms increments. """
    global counter, seconds, minutes
    # Increment seconds
    if t == 10:
        seconds += 1
        counter = 0
    # Increment minutes
    if seconds == 60:
        minutes += 1
        seconds = 0
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    """ Start the timer. """
    global running_game
    running_game = True
    timer.start()
    
def stop_button_handler():
    """ Stop the timer, and increment a success or failure. """
    global tries, successes, running_game
    if running_game == True:
       tries += 1
       if counter == 0:
            successes += 1
    running_game = False
    timer.stop()      
    
def reset_button_handler():
    """ Reset the game. """
    global counter, seconds, minutes, tries, successes 
    timer.stop()
    counter = 0
    seconds = 0
    minutes = 0
    tries = 0
    successes = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    """ Counter that runs every timer interval. """
    global counter
    counter += 1
   
# define draw handler
def draw_handler(canvas):
    """ Draw timer output to the canvas """
    global counter, seconds, minutes
    # Apply the format function
    format(counter)
    # Draw times less than 1 second
    if seconds < 10:
        canvas.draw_text(str(minutes) + ":" + str(0)+ str(seconds) + "." + str(counter),(52, 130), 80, 'White', 'serif') 
    # Draw times greater than 1 second
    elif seconds >= 10:
        canvas.draw_text(str(minutes) + ":" + str(seconds) + "." + str(counter),(52, 130), 80, 'White', 'serif') 
    # Draw successes and failures
    canvas.draw_text(str(successes) + "/" + str(tries),(200, 50), 40, 'Green', 'serif')
       
# create frame
frame = simplegui.create_frame("Stopwatch:The Game", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.add_button("Start", start_button_handler)
frame.add_button("Stop", stop_button_handler)
frame.add_button("Reset", reset_button_handler)
frame.set_draw_handler(draw_handler)
# Add a quit button?

# start frame
frame.start()

# Please remember to review the grading rubric

