import pygame


class Paddle:
    def __init__(self, x, y, width, height, position):
        self.x = x
        self.y = y
        self.position = position
        self.width = width
        self.height = height

    def show(self, screen, colour, screen_width):
        rectangle = pygame.Rect(
            (self.get_left_x_position(), self.get_top_y_position()),
            (self.width, self.height))

        pygame.draw.rect(screen, colour, rectangle)

    def update(self, screen, screen_width, screen_height, border_size, predicted_y=None):
        self.show(screen, pygame.Color("black"), screen_width)

        if predicted_y is not None:
            new_y = predicted_y
        else:
            new_y = pygame.mouse.get_pos()[1]

        if new_y + self.height / 2 <= (screen_height - border_size) \
                and new_y - self.height / 2 >= border_size:
            self.y = new_y

        self.show(screen, pygame.Color("white"), screen_width)

    def get_left_x_position(self):
        return self.x - self.width / 2

    def get_right_x_position(self):
        return self.x + self.width / 2

    def get_top_y_position(self):
        return self.y - self.height / 2

    def get_bottom_y_position(self):
        return self.get_top_y_position() + self.height
