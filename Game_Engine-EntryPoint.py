from Mechanics import *


class GameEngine:
    """
    Class that runs all the outer (main) loops of the program.
    Which means, that runs all the major screens and manages their functionalities.
    """
    def __init__(self):
        """
        Init of the main objects
        """
        self.game_mechanics = None
        self.entry_display = EntryScreenDisplay()

    def run_end_screen(self, message: str) -> None:
        """
        Screen that is showed to user after the game is over (either win, draw or loose).
        User must click anywhere in the screen to continue.

        :param message: Massage which should be displayed.
        """
        end_screen = True
        while end_screen:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    end_screen = False
                    pg.time.delay(200)

            self.entry_display.display_message(250, message, BLUE, (400, 400))
            self.entry_display.display_message(255, message, WHITE, (400, 400))
            self.entry_display.display_message(102, 'Click to continue...', BLUE, (400, 500))
            self.entry_display.display_message(100, 'Click to continue...', WHITE, (400, 500))

            pg.display.update()

    def run_main_screen(self) -> int:
        """
        Runs the game screen.
        Prints the actual state of the board and the grid.
        Handles the moves and decides whose turn is right now.
        After each turn checks if there is a winner or a draw.
        :return Integer that is used in the maintain_button function that called this function.
        """
        run = True
        self.game_mechanics = GameScreenMechanics(self.entry_display.board_size, self.entry_display.win_cond)
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False

            self.game_mechanics.draw_components()
            if self.game_mechanics.player_move_in_progress:
                self.game_mechanics.move_player()
            else:
                self.entry_display.display_message(100, 'WAIT A SEC...', BLUE, (400, 400))
                pg.display.update()
                self.game_mechanics.move_bot()
                self.game_mechanics.player_move_in_progress = True
            pg.display.update()
            self.game_mechanics.draw_components()

            if self.game_mechanics.check_if_win('o'):
                run = False
                self.run_end_screen('YOU DIE')
            elif self.game_mechanics.check_if_win('x'):
                run = False
                self.run_end_screen('YOU WIN')
            elif self.game_mechanics.full_board():
                run = False
                self.run_end_screen('DRAW')
        return 1

    def run_first_screen(self) -> None:
        """
        Runs first screen which show up to user after game launch.
        It handles the changes to the board size and winning condition made by user via buttons.
        It gives an option to start the game.
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        quit()
            self.entry_display.print_components(self.run_main_screen)
            pg.display.update()


# Entry point
if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()


