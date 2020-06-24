import pygame
from PlayerInformation import PlayerPositions


class Ball:
    def __init__(self, x, y, vx, vy, radius, velocity):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.velocity = velocity
        self.radius = radius

    def show(self, screen, colour):
        pygame.draw.circle(screen, colour, (self.x, self.y), self.radius)

    def update(
            self,
            screen,
            colour,
            background_colour,
            border_size,
            screen_height,
            screen_width,
            paddle_player,
            paddle_ai,
            player_information):

        self.show(screen, background_colour)

        new_x = self.x + self.vx * self.velocity
        new_y = self.y + self.vy * self.velocity

        left_border_present = PlayerPositions.Left not in player_information.get_selected_positions()
        right_border_present = PlayerPositions.Right not in player_information.get_selected_positions()

        if player_information.ai_player and self.ball_hits_paddle(new_x, new_y, paddle_ai):
            self.vx = - self.vx
        elif player_information.human_player and self.ball_hits_paddle(new_x, new_y, paddle_player):
            self.vx = - self.vx
        elif left_border_present and self.ball_hits_left_border(new_x, border_size):
            self.vx = - self.vx
            self.x = round(border_size + self.radius + 1)
        elif right_border_present and self.ball_hits_right_border(new_x, screen_width, border_size):
            self.vx = - self.vx
            self.x = round(screen_width - border_size - self.radius - 1)
        elif self.ball_hits_top_border(new_y, border_size, screen_height):
            self.vy = - self.vy
            self.y = round(border_size + self.radius + 1)
        elif self.ball_hits_bottom_border(new_y, border_size, screen_height):
            self.vy = - self.vy
            self.y = round(screen_height - border_size - self.radius - 1)
        elif not left_border_present and self.ball_hits_left_border(new_x, border_size):
            raise Exception("Border was hit")
        elif not right_border_present and self.ball_hits_right_border(new_x, screen_width, border_size):
            raise Exception("Border was hit")
        else:
            self.x = round(new_x)
            self.y = round(new_y)
            self.show(screen, colour)

    def ball_hits_bottom_border(self, new_y, border_size, screen_height):
        return new_y > screen_height - border_size - self.radius

    def ball_hits_top_border(self, new_y, border_size, screen_height):
        return new_y < border_size + self.radius

    def ball_hits_paddle(self, new_x, new_y, paddle):
        if paddle.position == PlayerPositions.Right:
            return new_x + self.radius >= paddle.get_left_x_position() \
                   and paddle.get_top_y_position() <= new_y <= paddle.get_bottom_y_position()
        elif paddle.position == PlayerPositions.Left:
            return new_x - self.radius <= paddle.get_right_x_position() \
                and paddle.get_top_y_position() <= new_y <= paddle.get_bottom_y_position()

        raise Exception()

    def ball_hits_right_border(self, new_x,  screen_width, border_size):
        return new_x + self.radius >= screen_width - border_size

    def ball_hits_left_border(self, new_x,  border_size):
        return new_x - self.radius <= border_size


