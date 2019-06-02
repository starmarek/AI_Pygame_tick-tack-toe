from Mechanics import *


class GameEngine:
    def __init__(self):
        self.game_mechanics = None
        self.entry_display = EntryScreenDisplay()

    def run_end_screen(self, message):
        end_screen = True
        while end_screen:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    end_screen = False

            self.entry_display.display_message(250, message, BLUE, (400, 400))
            self.entry_display.display_message(255, message, WHITE, (400, 400))
            pg.display.update()

    def run_main_screen(self):
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
                self.run_end_screen('AI WINS')
            elif self.game_mechanics.check_if_win('x'):
                run = False
                self.run_end_screen('YOU WIN')
            elif self.game_mechanics.full_board():
                run = False
                self.run_end_screen('DRAW')
        return 1

    def run_first_screen(self):
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


if __name__ == '__main__':
    gE = GameEngine()
    gE.run_first_screen()


