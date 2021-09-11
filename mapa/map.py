import pygame

from mapa.cell import Cell, GREY

class Mapa():
    def __init__(self, game, rows):
        self.game = game
        self.rows = rows
        self.width_muro = game.GAME_H // rows
        self.columns = game.GAME_W // self.width_muro
        self.map = self.make_map()


    def make_map(self):
        map = []
        for i in range(self.rows):
            map.append([])
            for j in range(self.columns):
                cell = Cell(j,i, self.width_muro, self.rows)
                map[i].append(cell)
                if i == 0 or j == 0 or i == self.rows - 1 or j == self.columns -1:
                    cell.make_muro()
                    cell.set_is_muro(True)

        print("filas: " ,self.rows )
        print("columnas: " , self.columns )
        print("lado : ", self.width_muro)
        return map

    def make_muro(self,row, col):
        for i in range(self.rows):
            for j in range(self.columns):
                if(i == row and col == j):
                    self.map[i][j].make_muro()
                    self.map[i][j].set_is_muro(True)

    def draw_grid(self, win):
        gap = self.width_muro
        for i in range(self.rows):
            pygame.draw.line(win, GREY, (0, i * gap), (self.game.GAME_W, i * gap))
            for j in range(self.columns):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, self.game.GAME_H))

    def draw(self, win):
        for row in self.map:
            for spot in row:
                if spot.get_is_muro():
                    spot.draw_muro(win)
                else:
                    continue
        self.draw_grid(win)
        pygame.display.update()
