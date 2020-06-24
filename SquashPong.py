import pygame
import Helper
import Settings
import pandas as pd
import PlayerInformation
from PlayerInformation import PlayerPositions
from sklearn.neighbors import KNeighborsRegressor

record_data = True
player_information = PlayerInformation.PlayerInformation(
    ai_player=True,
    human_player=True,
    ai_position=PlayerPositions.Left,
    human_position=PlayerPositions.Right)

if player_information.ai_player:
    pong_data = Helper.get_pong_data_for_training(player_information)

    X = pong_data.drop(columns=[' paddle_position', ' Paddle.y'])
    y = pong_data[' Paddle.y']
    alg = KNeighborsRegressor(n_neighbors=3)
    alg = alg.fit(X, y)

    df = pd.DataFrame(columns=['x', 'y', 'vx', 'vy'])

if record_data:
    file_name = Helper.random_string()
    sample_data = open(r"C:\Arwyn\Coding\Squash Pong\Training Data\{}.csv".format(file_name), "w")
    print("x, y, vx, vy, Paddle.y, paddle_position", file=sample_data)

screen, ball, paddle_player, paddle_ai, clock = Helper.initialize(
    Settings.screen_width,
    Settings.screen_height,
    Settings.initial_ball_x,
    Settings.initial_ball_y,
    Settings.initial_ball_vx,
    Settings.initial_ball_vy,
    Settings.ball_radius,
    Settings.ball_velocity,
    Settings.initial_paddle_y,
    Settings.paddle_width,
    Settings.paddle_height,
    Settings.border_colour,
    Settings.border_size,
    Settings.ball_colour,
    Settings.paddle_colour,
    player_information)



clock = pygame.time.Clock()

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
        break

    clock.tick(Settings.frame_rate)
    pygame.display.flip()

    predicted_y = None

    if player_information.ai_player:
        to_predict = df.append({'x': ball.x / Settings.screen_width,
                                'y': ball.y / Settings.screen_height,
                                'vx': ball.vx / Settings.screen_width,
                                'vy': ball.vy / Settings.screen_height},
                               ignore_index=True)
        predicted_y = round(alg.predict(to_predict)[0] * Settings.screen_height)

    try:
        ball.update(screen,
                    Settings.ball_colour,
                    Settings.background_colour,
                    Settings.border_size,
                    Settings.screen_height,
                    Settings.screen_width,
                    paddle_player,
                    paddle_ai,
                    player_information)
    except Exception as error:
        Helper.handle_main_exception(error, screen)

    if paddle_player is not None:
        paddle_player.update(screen, Settings.screen_width, Settings.screen_height, Settings.border_size, None)
    if paddle_ai is not None:
        paddle_ai.update(screen, Settings.screen_width, Settings.screen_height, Settings.border_size, predicted_y)

    if record_data:
        print("{},{},{},{},{},{}".format(
            ball.x / Settings.screen_width,
            ball.y / Settings.screen_height,
            ball.vx / Settings.screen_width,
            ball.vy / Settings.screen_height,
            paddle_player.y / Settings.screen_height,
            player_information.ai_position), file=sample_data)

