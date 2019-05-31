import pygame as pg

# resolution
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
MIGHTY_BLUE = (79, 153, 209)
OLIVE = (102, 102, 0)
GRAY = (204, 204, 204)

# images
angryRobot = pg.image.load('angry_robot.png')
cross = pg.image.load('cross.png')
circle = pg.image.load('circle.png')

pg.init()

# the display handle and caption_text setting command
displayWindow = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption('Win or Die Deluxe')


def display_message(size: int, message: str, color: tuple, position: tuple) -> None:
    """
    Display message of desired size and color at desired position

    :param size : the size of message. The bigger size, the bigger text will be displayed
    :param message: content of message. String that will be displayed
    :param color: color defined by the 3 - RGB - tuple
    :param position: x and y coordinated of the displayed text
    """
    text = pg.font.Font(None, size)
    text_surf = text.render(message, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = position
    displayWindow.blit(text_surf, text_rect)


def maintain_button(position: tuple, width: int, height: int, rect_color: tuple, message: str,
                    mess_color: tuple, desired_action=None) -> None:
    """
    Display button at desired position. Also calls chosen function after it was clicked.

    :param desired_action: function that will be called after button click
    :param height: height of button
    :param width: width of button
    :param message: text that will be displayed on the button
    :param mess_color: color of text, displayed on the button
    :param rect_color: color of the button
    :param position: x and y coordinated of the button
    """
    mouse_pos = pg.mouse.get_pos()
    mouse_clicked = pg.mouse.get_pressed()

    if (position[0] - width/2) < mouse_pos[0] < (position[0] + width/2) and \
            position[1] < mouse_pos[1] < (position[1] + height):
        if mouse_clicked[0] == 1 and desired_action is not None:
            pg.time.delay(200)
            if desired_action():
                return
    pg.draw.rect(displayWindow, rect_color, ((position[0]-(width/2), position[1]), (width, height)))
    display_message(int(height/2), message, mess_color, (position[0], position[1] + height/2))


def resize_image(image: pg.SurfaceType, size: int, is_cross: bool) -> pg.SurfaceType:
    """
    Function that is responsible for resizing the passed image. The app is build the way, that only cross or circle
    are possible to be passed.

    :param image: This is the pygames class, that represents image
    :param size: Size of game board
    :param is_cross: Deciding which image is passed
    :return: Resized image
    """
    if is_cross:
        x = 1.38
        y = 1.38
    else:
        x = 1.87
        y = 1.87

    image_rect = image.get_rect()
    image = pg.transform.scale(image, (int(x/size * image_rect.width), int(y/size * image_rect.height)))
    return image
