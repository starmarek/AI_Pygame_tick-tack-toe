from Display import *


class Player(GameScreenDisplay):
        player_move_in_progress = True

        def player_handle_move(self):
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
