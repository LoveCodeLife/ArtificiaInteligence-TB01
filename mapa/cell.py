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
        # self.position_x, self.position_y = 0, 0

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


class Camino(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image_original = pygame.image.load("assets/cell/camino.png")
        self.image = pygame.transform.scale(self.image_original, (width, width))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


class Cell:
    def __init__(self, row, col, width, total_rows, total_columns):
        self.row = col
        self.col = row
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.muro_sprite = pygame.sprite.Group()
        self.muro = Muro(width)
        self.is_muro = False
        self.coin_sprite = pygame.sprite.Group()
        self.coin = Coin(width)
        self.is_coin = False
        self.garden_sprite = pygame.sprite.Group()
        self.garden = Garden(width)
        self.is_garden = False
        self.total_columns = total_columns
        # El mejor camino
        self.camino = Camino(width)
        self.camino_sprite = pygame.sprite.Group()

        self.is_camino = False
        self.is_start = False
        self.is_end = False

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_murrooo(self):
        return self.is_muro;

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.is_start = True
        self.is_garden = False
        self.is_camino = False
        self.is_coin = False
        self.is_end = False
        self.color = ORANGE

    def make_end(self):
        self.is_start = False
        self.is_garden = False
        self.is_camino = False
        self.is_coin = False
        self.is_end = True
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, (64, 224, 208), (self.x, self.y, self.width, self.width))

    #Methods by muro
    def get_is_muro(self):
        return self.is_muro

    def set_is_muro(self, value):
        self.is_muro = value

    def draw_muro(self, display):
        self.muro.render(display)

    def make_muro(self):
        muro = Muro(self.width)
        muro.rect.x = self.x
        muro.rect.y = self.y

        self.muro = muro
        self.muro_sprite.add(muro)

    #Methods by coin
    def get_is_coin(self):
        return self.is_coin

    def set_is_coin(self, value):
        self.is_coin = value

    def draw_coin(self, display):
        self.coin.render(display)

    def make_coin(self):
        coin = Coin(self.width)
        coin.rect.x = self.x
        coin.rect.y = self.y

        self.coin = coin
        self.coin_sprite.add(coin)

        self.is_muro = False
        self.is_coin = False
        self.is_start = True
        self.is_garden = False
        self.is_camino = False
        self.is_coin = True
        self.is_end = False

        self.is_camino = False

    #Methods by garden
    def get_is_garden(self):
        return self.is_garden

    def set_is_garden(self, value):
        self.is_garden = value

    def draw_garden(self, display):
        self.garden.render(display)

    def make_garden(self):
        garden = Garden(self.width)
        garden.rect.x = self.x
        garden.rect.y = self.y

        self.garden = garden
        self.garden_sprite.add(garden)

    #Methods by camino
    def get_is_camino(self):
        return self.is_camino

    def set_is_camino(self, value):
        self.camino = value

    def draw_camino(self, display):
        self.camino.render(display)

    def make_path(self):
        camino = Camino(self.width)
        camino.rect.x = self.x
        camino.rect.y = self.y

        self.camino = camino
        self.camino_sprite.add(camino)

        self.is_muro = False
        self.is_coin = False
        self.is_start = True
        self.is_garden = False
        self.is_camino = False
        self.is_coin = False
        self.is_end = False

        self.is_camino = True

    def make_closed(self):
        self.color = RED

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_murrooo():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_murrooo():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_columns - 1 and not grid[self.row][self.col + 1].is_murrooo():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_murrooo():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
