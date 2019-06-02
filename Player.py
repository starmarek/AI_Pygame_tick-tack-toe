from Display import *


class Player(GameScreenDisplay):
    """
    Represents the human player.
    """
    player_move_in_progress = True  # deciding whether it's player's turn right now

    def player_handle_move(self) -> None:
        """
        Function checks if mouse cursor is located inside of one of the grid's boxes. If yes, then it prints
        the cross image into that box. If the cursor is located in the box and player has clicked the mouse button, then
        it adds element into 2d tags array.
        """
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in range(1, self.size + 1):
            x = i * self.gap_size + (i - 1) * self.box_size
            for j in range(1, self.size + 1):
                y = j * self.gap_size + (j - 1) * self.box_size
                if x < mouse_pos[0] < x + self.box_size and y < mouse_pos[1] < y + self.box_size and self.tags[i-1][j-1] is None:
                    displayWindow.blit(self.cross, (x, y))

                    if mouse_click[0] == 1:
                        self.tags[i-1][j-1] = 'x'
                        self.player_move_in_progress = False
