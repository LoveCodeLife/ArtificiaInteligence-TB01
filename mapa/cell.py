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

    # Es como dibujar el draw image
    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Coin(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image_original = pygame.image.load("assets/cell/coin.png")
        self.image = pygame.transform.scale(self.image_original, (width, width))
        self.rect = self.image.get_rect()

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Garden(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image_original = pygame.image.load("assets/cell/garden.png")
        self.image = pygame.transform.scale(self.image_original, (width, width))
        self.rect = self.image.get_rect()

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


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
        self.coin_sprite = pygame.sprite.Group()
        self.coin = Coin(width)
        self.is_coin = False;
        self.garden_sprite = pygame.sprite.Group()
        self.garden = Garden(width)
        self.is_garden = False;

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

    def make_coin(self):
        coin = Coin(self.width)
        coin.rect.x = self.x
        coin.rect.y = self.y

        self.coin = coin
        self.coin_sprite.add(coin)

    def make_garden(self):
        garden = Garden(self.width)
        garden.rect.x = self.x
        garden.rect.y = self.y

        self.garden = garden
        self.garden_sprite.add(garden)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def get_is_muro(self):
        return self.is_muro

    def set_is_muro(self, value):
        self.is_muro = value

    def draw_muro(self, display):
        self.muro.render(display)

    def get_is_coin(self):
        return self.is_coin

    def set_is_coin(self, value):
        self.is_coin = value

    def draw_coin(self, display):
        self.coin.render(display)

    def get_is_garden(self):
        return self.is_garden

    def set_is_garden(self, value):
        self.is_garden = value

    def draw_garden(self, display):
        self.garden.render(display)

    def __lt__(self, other):
        return False
