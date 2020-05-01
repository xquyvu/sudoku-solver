import pygame


def aa_filled_rounded_rect(surface, rect, color, radius=0.4):

    """
    aa_filled_rounded_rect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size)*radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)

class SudokuSquare:
    """A sudoku square class."""
    def __init__(self, number=None, offset_x=0, offset_y=0, edit="Y", x_loc=0, y_loc=0):
        if number is not None:
            number = str(number)
            self.color = (2, 204, 186)
        else:
            number = ""
            self.color = (255, 255, 255)

        self.font = pygame.font.SysFont('opensans', 21)
        self.text = self.font.render(number, 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos = self.textpos.move(offset_x + 17, offset_y + 4)
        self.edit = edit
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.offset_x = offset_x
        self.offset_y = offset_y

    def draw(self):
        screen = pygame.display.get_surface()
        aa_filled_rounded_rect(screen, (self.offset_x, self.offset_y, 45, 40), self.color)

        screen.blit(self.text, self.textpos)

    def change(self, number):
        if number is not None:
            number = str(number)
        else:
            number = ""

        if self.edit == "Y":
            self.text = self.font.render(number, 1, (0, 0, 0))
            self.draw()
            return 0

        return 1

    def current_loc(self):
        return self.x_loc, self.y_loc
