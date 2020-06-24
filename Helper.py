import PlayerInformation
from PlayerInformation import PlayerPositions
import pygame
import Ball
import Paddle
import Settings
import Helper
import pandas as pd
import glob
import string
import random



def handle_losing_game(screen, losing_image, ):
    screen.blit(losing_image, (0, 0))
    pygame.display.flip()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()


def initialize(
        screen_width,
        screen_height,
        initial_ball_x,
        initial_ball_y,
        initial_ball_vx,
        initial_ball_vy,
        ball_radius,
        ball_velocity,
        initial_paddle_y,
        paddle_width,
        paddle_height,
        border_colour,
        border_size,
        ball_colour,
        paddle_colour,
        player_information):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))

    ball = Ball.Ball(initial_ball_x, initial_ball_y, initial_ball_vx, initial_ball_vy, ball_radius, ball_velocity)

    pygame.draw.rect(screen, border_colour, pygame.Rect((0, 0), (screen_width, border_size)))
    pygame.draw.rect(screen, border_colour, pygame.Rect((0, screen_height - border_size), (screen_width, border_size)))

    paddle_player = None
    paddle_ai = None

    if player_information.human_player:
        x_position = get_paddle_starting_x_position(player_information.human_position, screen_width, border_size)
        paddle_player = Paddle.Paddle(x_position, initial_paddle_y, paddle_width, paddle_height,
                                      player_information.human_position)
        paddle_player.show(screen, paddle_colour, screen_width)

    if player_information.ai_player:
        x_position = get_paddle_starting_x_position(player_information.ai_position, screen_width, border_size)
        paddle_ai = Paddle.Paddle(x_position, initial_paddle_y, paddle_width, paddle_height,
                                  player_information.ai_position)
        paddle_ai.show(screen, paddle_colour, screen_width)

    if PlayerPositions.Left not in player_information.get_selected_positions():
        pygame.draw.rect(screen, border_colour, pygame.Rect((0, 0), (border_size, screen_height)))
    if PlayerPositions.Right not in player_information.get_selected_positions():
        pygame.draw.rect(screen, border_colour,
                         pygame.Rect((screen_width - border_size, 0), (border_size, screen_height)))

    ball.show(screen, ball_colour)

    pygame.display.flip()
    clock = pygame.time.Clock()
    return screen, ball, paddle_player, paddle_ai, clock


def handle_main_exception(error, screen):
    if error.args[0] == 'Border was hit':
        Helper.handle_losing_game(screen, Settings.losing_image)
    # else:
    # raise Exception("Undefined error")


def change_sign_of_x_observations_if_needed(player_information, pong_data):
    ai_position = player_information.ai_position

    for index, row in pong_data.iterrows():
        if row[' paddle_position'].strip().lower() != ai_position.name.strip().lower():
            pong_data.at[index, 'x'] = 1 - row['x']
            pong_data.at[index, ' vx'] - row[' vx']

    return pong_data


def random_string(string_length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def get_pong_data_for_training(player_information):
    game_observations_dictionary = {}
    path = r"C:\Arwyn\Coding\Squash Pong\*.csv"
    for file_name in glob.glob(path):
        try:
            game_observations_dictionary[file_name] = pd.read_csv(file_name)
        except:
            continue

    pong_data = pd.DataFrame(columns=['x', ' y', ' vx', ' vy', ' Paddle.y', ' paddle_position'])
    for key in game_observations_dictionary:
        pong_data = pd.concat([pong_data, game_observations_dictionary[key]])

    pong_data = pong_data.drop_duplicates()

    return change_sign_of_x_observations_if_needed(player_information, pong_data)


def get_paddle_starting_x_position(position, screen_width, border_size):
    if position == PlayerPositions.Left:
        return border_size / 2
    if position == PlayerPositions.Right:
        return screen_width - border_size / 2
