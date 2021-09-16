import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Muro(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image_original = pygame.image.load("assets/cell/muro.png")
        self.image = pygame.transform.scale(self.image_original, (width, width))
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    #Es como dibujar el draw image
    def render(self, display):
        display.blit(self.image, (self.rect.x,self.rect.y))


class Cell:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.muro_sprite = pygame.sprite.Group()
        self.muro = Muro(width)
        self.is_muro = False;

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_muro(self):
        muro = Muro(self.width)
        muro.rect.x = self.x
        muro.rect.y = self.y

        self.muro = muro
        self.muro_sprite.add(muro)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def get_is_muro(self):
        return self.is_muro

    def set_is_muro(self, value):
        self.is_muro = value

    def draw_muro(self, display):
        self.muro.render(display)

    def __lt__(self, other):
        return False


