class Node():
    def __init__(self, pariente=None, posicion=None):
        self.parent = pariente
        self.position = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.position == otro.position