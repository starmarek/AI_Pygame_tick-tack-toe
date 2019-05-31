from Global import *


class Player:

    @staticmethod
    def handle_move(board_size, box_size, gap_size, tags, resized_cross):
        mouse_pos = pg.mouse.get_pos()
        mouse_click = pg.mouse.get_pressed()

        for i in range(1, board_size + 1):
            y = i * gap_size + (i - 1) * box_size
            for j in range(1, board_size + 1):
                x = j * gap_size + (j - 1) * box_size
                if x < mouse_pos[0] < x + box_size and y < mouse_pos[1] < y + box_size:
                    displayWindow.blit(resized_cross, (x, y))

                    if mouse_click[0] == 1:
                        tags[i-1][j-1] = 'x'
