# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        # Phase 1.1, draw the ship with thrusters OFF.
        # Phase 1.5 turn the thrusters on and off. This is going to 
        # Require an additional method, below
        if self.thrust:
            canvas.draw_image(self.image,(135,45),(90,90), self.pos, (90,90), self.angle)
        else:
            canvas.draw_image(self.image,(45,45),(90,90), self.pos, (90,90), self.angle)
        
    def assign_thrust(self, thrust):
        self.thrust = thrust
        
    # Phase 3.1, shoot a missile and play the sound.
    def shoot(self):
        global a_missile
        missile_foward_vector = angle_to_vector(self.angle)  
        # missel should be come from the nose of the ship, and move at a constant rate from the ship
        # From image info, we know that the ship is 45 pixels from nose-to-tail.
        missel_pos = [self.pos[0] + 45 * missile_foward_vector[0], self.pos[1] + 45 * missile_foward_vector[1]]  
        # Adjust this int to change the speed of the missile
        missel_vel = [self.vel[0] + missile_foward_vector[0] * 5, self.vel[1] + missile_foward_vector[1] * 5]  
        a_missile = Sprite(missel_pos, missel_vel, 0, 0, missile_image, missile_info, missile_sound)  
        missile_sound.play()  
    
    
    def update(self):
        # Phase 1.3, update angle by angular velocity.
        self.angle += self.angle_vel 
        
        # Phase 1.2, update the ship position based on its velocity
        # Phase 1.10, modify the ship's update method such that the ship's 
        # position wraps around the screen
        # Phase 1.11, add friction to the ship's update method 
        
        # Add "friction"
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99
        
        # Update postion
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        #Ensure that the ship wraps
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT   
    
        # Phase 1.7, play the thurst sound when True
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        
        # Phase 1.8, use the angle_to_vector to compute the forward
        # vector pointing in the direction the ship is facing based on 
        # the ship's angle.
        forward_vector = angle_to_vector(self.angle)
        
        # Phase 1.9, accelerate the ship when thrusting.
        if self.thrust:
            self.vel[0] += forward_vector[0] * 0.1
            self.vel[1] += forward_vector[1] * 0.1
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        # Phase 2.1a,modifying the draw handler to draw the 
        # actual image and the update handler to make the
        # sprite move and rotate
        canvas.draw_image(self.image,(45,45),(90,90), self.pos, (90,90), self.angle)
        # A a more modular draw command to render missiles
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size,self.angle)
        
    def update(self):
        # Phase 2.1b update rock position...    
        self.pos[0]+= self.vel[0]  
        self.pos[1]+= self.vel[1]  
        # Ensure that rocks with wrap-around the screen
        self.pos[0] = self.pos[0] % WIDTH   
        self.pos[1] = self.pos[1] % HEIGHT  
        
        # and rotation
        self.angle += self.angle_vel
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # Phase 4, draw lives and score
    canvas.draw_text('lives: ' + str(lives), (15, 25), 30, "White")  
    canvas.draw_text('score: ' + str(score), (15, 65), 30, "White") 
    
# Phase 1.4a, add left and right key handlers, and register them below.
def keydown(key):
    if key == simplegui.KEY_MAP["left"]:  
        my_ship.angle_vel -= 0.1
    elif key == simplegui.KEY_MAP["right"]:  
        my_ship.angle_vel += 0.1
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.assign_thrust(True)
    elif key==simplegui.KEY_MAP['space']:  
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["right"]:  
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.assign_thrust(False)
    

# timer handler that spawns a rock    
# Phase 2.2, spawn a rock once every second (called with the timer
# handler below), with random velocity, position, and angular velocity.
# Values should be both positive and negative
# (self, pos, vel, ang, ang_vel, image, info, sound = None)
def rock_spawner():
    global a_rock
    pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)] 
    vel = [random.randint(1, 4) * random.choice([1,-1]), random.randint(1, 4) * random.choice([1,-1])]
    ang = random.random()
    ang_vel = random.randint(1,5) * random.choice([0.01,-0.01])
    a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 1, 1, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
