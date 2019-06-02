from Bot import *
from Player import *


class GameScreenMechanics(Bot, Player):
    def __init__(self, size, win_con):
        super().__init__(size, win_con)

    def move_player(self) -> None:
        """
        Calls the method of Player class that is responsible for handling the player move.
        """
        self.player_handle_move()

    def move_bot(self) -> None:
        """
        Calls the method of Bot class that is responsible for handling the bot move.
        It also changes the value of flag, so the next move will be the Players move.
        """
        self.bot_handle_move()
        self.player_move_in_progress = True
