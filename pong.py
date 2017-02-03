# import modules
import os
import pygame

# pygame specific locals/constants
from pygame.locals import *

# some resource related warnings
if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

# initializations
pygame.init()

# a bit similar to CodeSkulptor frame creation -- we'll call the window the canvas
canvas = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pong")

# Pygame Wrapper functions -- resource loading sanity checks
# Taken from the "Monkey tutorial" and updated for 3.3 by me
#
# load Image:
# A colorkey is used in graphics to represent a color of the image
# that is transparent (r, g, b). -1 = top left pixel colour is used.
def load_image(name, colorkey=None):
    fullname = os.path.join('data\images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()
    return image, image.get_rect()

# Load Sound
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data\sounds', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', name)
        raise SystemExit(message)
    return sound

# need to create fonts and colour objects in PyGame
#fontObj = pygame.font.Font('ARBERKLEY.ttf', 32)
#fontObj2 = pygame.font.Font('ARBERKLEY.ttf', 24)
fontObj3 = pygame.font.Font(pygame.font.match_font('timesnewroman'), 32)

gold_color = pygame.Color(255, 215, 0)
white_color = pygame.Color(255, 255, 255)

# ------------------------Begin Your CodeSkulptor Port-------------------------

import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 1000
HEIGHT = 600     
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 160
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
direction = LEFT
score1 = 0
score2 = 0
screen_width = 1000
screen_height = 600
screen=pygame.display.set_mode([screen_width,screen_height])
# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [10,10]
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [600,300]
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120,240) /30
        ball_vel[1] = -random.randrange(60,180) /30
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(120,240) /30
        ball_vel[1] = -random.randrange(60,180)  /30
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(direction)
    score1=0
    score2=0 
# create frame

# start frame
new_game()
count = 0
draw_colour = white_color
def draw_handler(canvas):

    # clear canvas -- fill canvas with uniform colour, then draw everything below.
    # this removes everything previously drawn and refreshes 
    canvas.fill((0, 0, 0))
    

    # draw example
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    pygame.draw.line(screen,(255,255,255),[WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2 )
    pygame.draw.line(screen,(255,255,255),[PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 2 )
    pygame.draw.line(screen,(255,255,255),[WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 2 )
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) or ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):        
        ball_vel[0] *= -1
        if (ball_pos[0] > WIDTH/2):             
            if (ball_pos[1] < paddle2_pos) or (ball_pos[1] > paddle2_pos + PAD_HEIGHT):
                score1 += 1 
                spawn_ball(LEFT) 
        if (ball_pos[0] < WIDTH/2):
            if (ball_pos[1] < paddle1_pos) or (ball_pos[1] > paddle1_pos + PAD_HEIGHT ):
                score2 += 1
                spawn_ball(RIGHT)
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - BALL_RADIUS):
         ball_vel[1] = -ball_vel[1]
     
    # draw ball
    pygame.draw.circle(screen,(255,255,255),[int(ball_pos[0]),int(ball_pos[1])],BALL_RADIUS,20)
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = paddle1_pos + paddle1_vel
    paddle2_pos = paddle2_pos + paddle2_vel
    if paddle1_pos >= 440:
        paddle1_pos = 440
    if paddle1_pos <= 0:
        paddle1_pos = 0
    if paddle2_pos <= 0:
        paddle2_pos = 0
    if paddle2_pos >= 440:
        paddle2_pos = 440
    # draw paddles
    paddle1 = pygame.draw.polygon(screen,(255,255,255),[[0, paddle1_pos], [PAD_WIDTH, paddle1_pos],[PAD_WIDTH, (paddle1_pos) + PAD_HEIGHT ],[0, (paddle1_pos) + PAD_HEIGHT]],4) 
    paddle2 = pygame.draw.polygon(screen,(255,255,255),[[WIDTH, paddle2_pos], [WIDTH - PAD_WIDTH, paddle2_pos],[WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT], [WIDTH, paddle2_pos + PAD_HEIGHT]],4)
    # determine whether paddle and ball collide    
    if ball_pos[0]==28:
        if ball_pos[1] in range(paddle1_pos-80,paddle1_pos+80):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] += 0.5 * ball_vel[0]
    if ball_pos[0]==971.8:
        if ball_pos[1] in range(paddle2_pos-80,paddle2_pos+80):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] = 0.5 * ball_vel[0] + ball_vel[0]
          
    # draw scores
    fontObj3 = pygame.font.Font(pygame.font.match_font('timesnewroman'), 36)
    text_draw = fontObj3.render(str(score1),36,draw_colour)
    screen.blit(text_draw,[WIDTH/2-60,60])
    text_draw1 = fontObj3.render(str(score2),36,draw_colour)
    screen.blit(text_draw1,[WIDTH/2+60,60])
    # update the display
    pygame.display.update()

def t_example():
    global draw_colour
    if draw_colour == white_color:
        draw_colour = gold_color
    else:
        draw_colour = white_color

# pygame has no start() and stop() methods -- 0 time is off any other value is on
# set some on/off constants for readability with each timer
TIMER_OFF = 0

# timer for example -- 1500 milliseconds when on
TIMER_EXAMPLE_ON = 1500
# set the timer name to its user event for readability
timer_example = USEREVENT + 1
pygame.time.set_timer(timer_example, TIMER_EXAMPLE_ON) 			

# call this function to start everything
# could be thought of as the implemntation of the CodeSkulptor frame .start() method.
def main():
    # initialize loop until quit variable
    running = True
    
    # create our FPS timer clock
    clock = pygame.time.Clock()    

#---------------------------Frame is now Running-----------------------------------------
    
    # doing the infinite loop until quit -- the game is running
    while running:
        
        # event queue iteration
        for event in pygame.event.get():
            
            # window GUI ('x' the window)
            if event.type == pygame.QUIT:
                running = False

            # input - key and mouse event handlers
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
                # just respond to left mouse clicks
                #if pygame.mouse.get_pressed()[0]:
                    #mc_handler(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
				global paddle1_vel, paddle2_vel
				if event.key == pygame.K_w:
					paddle1_vel -= 10
				if event.key == pygame.K_s:
					paddle1_vel += 10
				if event.key == pygame.K_UP:
					paddle2_vel -= 10
				if event.key == pygame.K_DOWN:
					paddle2_vel += 10
                #kd_handler(event.key)
            if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					paddle1_vel += 10
				if event.key == pygame.K_s:
					paddle1_vel -= 10
				if event.key == pygame.K_UP:
					paddle2_vel += 10
				if event.key == pygame.K_DOWN:
					paddle2_vel -= 10
				

            # timers
            elif event.type == timer_example:
                t_example()
          
                
        # the call to the draw handler
        draw_handler(canvas)
        
        # FPS limit to 60 -- essentially, setting the draw handler timing
        # it micro pauses so while loop only runs 60 times a second max.
        clock.tick(60)
        
#-----------------------------Frame Stops------------------------------------------

    # quit game -- we're now allowed to hit the quit call
    pygame.quit ()

# this calls the 'main' function when this script is executed
# could be thought of as a call to frame.start() of sorts
if __name__ == '__main__': main() 
