import pygame
import sys
import random
import pygame.freetype
import copy
from pygame.locals import *


#quits the game, used when the snake hits the side of the window
def gameover():
    '''
    closes the window
    '''
    pygame.quit()
    sys.exit()

def respawn(l):
    '''
	randomly respawns the eggs on a spot on the window that isn't on the snake
	'''
    x = random.randrange(1, 32)
    y = random.randrange(1, 24)
    fp = [int(x * 20), int(y * 20)]
    if not fp in (l):
        return fp
    else:
        return respawn(l)


def eats_own_tail(lst):
    '''
	cuts the snake body if the head of the snake hits the body of the snake
	'''
    for i in range(len(lst) - 1, 0, -1):
        if lst[i] == lst[0]:
            del lst[i:len(lst)]
                    
def pause(window):
    '''
	pauses the game if p is presses, while the game is paused, press q to quit the game
	'''
    paused = True

    pygame.mixer.music.load('sound\\TheWorld2.mp3')
    pygame.mixer.music.play(0,0.0)


    pixels = pygame.surfarray.pixels2d(window)
    pixels ^= 2 ** 32 - 1

    pygame.display.flip()
     

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

    pygame.init()

    fps_Clock = pygame.time.Clock()

    is_background = pygame.image.load('image\\background.png')
    snake = pygame.image.load('image\\snake.png')
    snake_head = pygame.image.load('image\\snake_head.png')
    food = pygame.image.load('image\\food.png')

    level = 5
    is_backward = False;
    past_snake = []
    fu_food = []

    window = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('snake')
    #the startinf point for the snake (x,y)
    snake_Position = [100, 100]
    #the list represents the snake, each element is one part of the body
    snake_Body = [[100, 100], [80, 100], [60, 100]]

    food_Position = [300, 300]
    # a flag that shows if the egg is eaten or not, 1 means its not
    is_food_eaten = 1
    direction = 'right'
    
    while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    gameover()
                    '''
                    directions for the snake - refer to README file
                    '''
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
                    	if not is_backward:
    	                	pygame.mixer.music.load('sound\\bites_the_dust2.mp3')
    	                	pygame.mixer.music.play(0,0.0)
                    	is_backward = not is_backward;
            if is_backward:
            	if len(past_snake) > 0:
    	        	snake_Body = past_snake[-1][0]
    	        	if not past_snake[-1][1] == food_Position:
    	        		fu_food.append(copy.deepcopy(food_Position))
    	        		level -= 0.6
    	        	food_Position = past_snake[-1][1]
    	        	snake_Position = past_snake[-1][2]
    	        	direction = past_snake[-1][3]
    	        	past_snake.pop()
            else:
            	past_snake.append([snake_Body[:], food_Position[:], snake_Position[:], direction])
    	        if direction == 'right':
    	            snake_Position[0] += 20
    	        elif direction == 'left':
    	            snake_Position[0] -= 20
    	        elif direction == 'up':
    	            snake_Position[1] -= 20
    	        elif direction == 'down':
    	            snake_Position[1] += 20

    	        eats_own_tail(snake_Body)



    	        snake_Body.insert(0, list(snake_Position))

    	        if snake_Position[0] == food_Position[0] and snake_Position[1] == food_Position[1]:
    	            is_food_eaten = 0

    	            level +=0.6
    	        else:
    	            snake_Body.pop()
    	        if is_food_eaten == 0:
    	        	if len(fu_food) > 0 and not [int(fu_food[-1][0] * 20), int(fu_food[-1][1] * 20)] in snake_Body:
    	        		food_Position = fu_food.pop()
    	        	else:
    	        		food_Position = respawn(snake_Body)
    	        	is_food_eaten = 1



            window.blit(is_background, (0,0))

            for position in snake_Body:
            	window.blit(snake, (position[0], position[1]))
            window.blit(snake_head, (snake_Body[0][0], snake_Body[0][1]))
            window.blit(food, (food_Position[0], food_Position[1]))
            pygame.display.flip()

            if snake_Position[0] > 620 or snake_Position[0] < 0:
                gameover()
            elif snake_Position[1] > 460 or snake_Position[1] < 0:
                gameover()

            if is_backward:
            	fps_Clock.tick(level *10)
            else:
            	fps_Clock.tick(level)

    if __name__ == '__main__':
        main()