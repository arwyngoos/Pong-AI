from enum import Enum


class PlayerInformation:
    def __init__(self, ai_player, human_player, ai_position, human_position):
        self.ai_player = ai_player
        self.human_player = human_player
        self.ai_position = ai_position
        self.human_position = human_position

    def get_selected_positions(self):
        positions = []
        if self.ai_position is not None:
            positions.append(self.ai_position)
        if self.human_position is not None:
            positions.append(self.human_position)

        return positions


class PlayerPositions(Enum):
    Left = 1,
    Right = 2
