import pygame
import sys
import random
import pygame.freetype
import copy
from pygame.locals import *
#the color of the eggs
redColor = pygame.Color(81, 201, 111)
#the color of the background
#blackColor = pygame.Color(0, 0, 0)
blackColor = pygame.Color(171,190,206)
#the color of the snake
whiteColor = pygame.Color(21, 50, 253)

#quits the game, used when the snake hits the side of the window
def gameover():
    pygame.quit()
    sys.exit()

# randomly respawns the eggs on a random spot on the window
def respawn(l):
    x = random.randrange(1, 32)
    y = random.randrange(1, 24)
    fp = [int(x * 20), int(y * 20)]
    if not fp in (l):
        return fp
    else:
        return respawn(l)

# if the first element appears in the rest of the list, pop all elemments after the second appearance
# used to cut the snake if it hits its own tail
def cut(lst):
    for i in range(len(lst) - 1, 0, -1):
        if lst[i] == lst[0]:
            del lst[i:len(lst)]
                    
def pause(window):
    paused = True

    pygame.mixer.music.load('sound\\TheWorld.mp3')
    pygame.mixer.music.play(0,0.0)
    # f=open("the_world.wav")
    # pygame.mixer.Sound(f).play()

    pixels = pygame.surfarray.pixels2d(window)
    pixels ^= 2 ** 32 - 1
    # del pixels

    pygame.display.flip()
     
    # fonts = pygame.font.SysFont('arial.ttf', 50)
    # words = fonts.render("Press q to quit or e to continue", True, (255,255,0))
    # window.blit(words, )
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    gameover()
                elif event.key == K_p:
                    paused = False
     
               
     


def main():
    #initialize
    pygame.init()
    #delares a variable to control the speed of the game
    fpsClock = pygame.time.Clock()

    background = pygame.image.load('image\\background.png')
    snake = pygame.image.load('image\\snake.png')
    snake_head = pygame.image.load('image\\snake_head.png')
    food = pygame.image.load('image\\food.png')

    level = 5
    backward = False;
    past_snake = []
    feu_food = []
    #creates the window
    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('snake')
    #the startinf point for the snake (x,y)
    snakePosition = [100, 100]
    #the list represents the snake, each element is one part of the body
    snakeBody = [[100, 100], [80, 100], [60, 100]]
    #starting position for the egg
    foodPosition = [300, 300]
    # a flag that shows if the egg is eaten or not, 1 means its not
    foodflag = 1
    direction = 'right'
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover()
                # changes the direction string in to the direction according to the key
                # pressed
                # cannot change the direction into the opposite direction as the current
                # one
                # for example, if the current direction string is left, pressing d won't
                # change the direction
            elif event.type == KEYDOWN:
                if event.key == K_d and direction != 'left':
                    direction = 'right'
                elif event.key == K_w and direction != 'down':
                    direction = 'up'
                elif event.key == K_a and direction != 'right':
                    direction = 'left'
                elif event.key == K_s and direction != 'up':
                    direction = 'down'
                elif event.key == K_p:
                    pause(window)
                elif event.key == K_f:
                	if not backward:
	                	pygame.mixer.music.load('sound\\bites_the_dust.mp3')
	                	pygame.mixer.music.play(0,0.0)
                	backward = not backward;


        # moves the position of the snake according to the direction string
        if backward:
        	if len(past_snake) > 0:
	        	snakeBody = past_snake[-1][0]
	        	if not past_snake[-1][1] == foodPosition:
	        		feu_food.append(copy.deepcopy(foodPosition))
	        		level -= 0.6
	        	foodPosition = past_snake[-1][1]
	        	snakePosition = past_snake[-1][2]
	        	direction = past_snake[-1][3]
	        	past_snake.pop()
        else:
        	past_snake.append([snakeBody[:], foodPosition[:], snakePosition[:], direction])
	        if direction == 'right':
	            snakePosition[0] += 20
	        elif direction == 'left':
	            snakePosition[0] -= 20    
	        elif direction == 'up':
	            snakePosition[1] -= 20
	        elif direction == 'down':
	            snakePosition[1] += 20
	        # every time the snake moves, it detects if the snake hit its own tail or
	        # not,
	        # if so, it cuts its own tail and perform the cut method that was defined
	        # above
	        cut(snakeBody)
	          

	        #adds a new piece of the snakes body to the beginning of snakebody, to
	        #represent the snake moving forwards
	        # will pop the last piece of snake body so the length won't change, if on this
	        # move, the snake eats the egg,
	        # the snake will not pop for this turn so the length of the snake will be
	        # longer
	        snakeBody.insert(0, list(snakePosition))
	        # checks if the head of the snake overlaps with the food after every move
	        # the snake takes
	        if snakePosition[0] == foodPosition[0] and snakePosition[1] == foodPosition[1]:
	            foodflag = 0
	            # pygame.mixer.music.load('sound\\made_in_heaven.mp3')
	            # pygame.mixer.music.play(0,0.0)
	            level +=0.6
	        else:
	            snakeBody.pop()
	        if foodflag == 0:
	        	if len(feu_food) > 0 and not [int(feu_food[-1][0] * 20), int(feu_food[-1][1] * 20)] in snakeBody:
	        		foodPosition = feu_food.pop()
	        	else:
	        		foodPosition = respawn(snakeBody)
	        	foodflag = 1



        window.blit(background, (0,0))
        # draws the snake and the egg
        for position in snakeBody:
        	window.blit(snake, (position[0], position[1]))
        window.blit(snake_head, (snakeBody[0][0], snakeBody[0][1]))
        window.blit(food, (foodPosition[0], foodPosition[1]))
        pygame.display.flip()
        # quits if the snake hits the side of the window
        if snakePosition[0] > 620 or snakePosition[0] < 0:
            gameover()
        elif snakePosition[1] > 460 or snakePosition[1] < 0:
            gameover()
        # pace of the game
        if backward:
        	fpsClock.tick(level *10)
        else:
        	fpsClock.tick(level)

if __name__ == '__main__':
    main()