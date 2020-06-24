import random
import pygame

two_players = True
screen_height = 600
screen_width = 1200
border_size = round(screen_height / 50)
initial_paddle_y = round(screen_height / 2)
paddle_width = border_size
paddle_height = round(screen_height / 8)
initial_ball_x = round(screen_width / 2)
initial_ball_y = round(screen_height / 2)
initial_ball_vx = random.uniform(-2, 2)
initial_ball_vy = random.uniform(-2, 2)
ball_radius = round(screen_height / 50)
ball_velocity = random.uniform(2, 4)
border_colour = pygame.Color("red")
paddle_colour = pygame.Color("white")
ball_colour = pygame.Color("white")
background_colour = pygame.Color("black")
frame_rate = 70
losing_image = pygame.image.load(r'C:\Arwyn\Coding\Squash Pong\LosingImage.jpg')