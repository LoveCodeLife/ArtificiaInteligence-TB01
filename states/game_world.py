import pygame, os
from states.state import State
from states.pause_menu import PauseMenu
from mapa.map import Mapa

class Game_World(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.player = Player(self.game)
        self.ROWS = 50
        self.map = Mapa(self.game,self.ROWS)
        self.time = 100

        #TODO COIN_YELLOW  el coin_blue sera para agregar + 5 segundos de tiempo
        self.coins_blue = []
        self.coins_red = []
        self.initialize_coins()
        self.clock = pygame.time.Clock()

        #TODO COIN_RED el coin_blue será para obtener el camino mas corto

    def initialize_coins(self):
        #Initialize coins blue
        coin01 = self.map.get_grid_map()[19][55]
        coin02 = self.map.get_grid_map()[2][41]
        coin03 = self.map.get_grid_map()[32][9]
        coin04 = self.map.get_grid_map()[25][43]

        coin01.make_coin()
        coin02.make_coin()
        coin03.make_coin()
        coin04.make_coin()

        self.coins_blue.append(coin01)
        self.coins_blue.append(coin02)
        self.coins_blue.append(coin03)
        self.coins_blue.append(coin04)

        #Initialize coin_blue red
        coinred01 = self.map.get_grid_map()[40][54]

        coinred01.make_coin_red()

        self.coins_red.append(coinred01)

    def update(self,delta_time, actions):
        # Check if the game was paused 
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions,self.map)

    def render(self, display):
        self.clock.tick(10000)
        self.map.draw(display)
        self.player.render(display)

        #Si el jugador se encuentra en la posicion tal

        for coin in self.coins_blue:
            self.coin_yellow(coin)

        position = 54,40
        positionFinal = 76,47
        positionCoin01 = 55,19
        positionCoin02 = 41,2
        positionCoin03 = 9,32
        positionCoin04 = 43,25

        if(self.player.get_position_in_grid(self.map) == positionCoin01):
            self.time = 100
        if(self.player.get_position_in_grid(self.map) == positionCoin02):
            self.time = 100
        if(self.player.get_position_in_grid(self.map) == positionCoin03):
            self.time = 100
        if(self.player.get_position_in_grid(self.map) == positionCoin04):
            self.time = 100

        self.map.update_vecinos()
        if(self.player.get_position_in_grid(self.map) == position):
            print("AQUI ESTOYY")

            #Points inicio y final le meti hardcode XD seee
            start = self.map.get_grid_map()[40][54]
            end = self.map.get_grid_map()[47][77]
            start.make_coin_red()
            end.make_coin()

            self.map.algorithm(self.map.get_grid_map(),start, end)
        else:
            self.map.reset_camino()

        #TODO PRINT CONTADOR
        self.time -=0.1
        font = pygame.font.SysFont(None, 40)
        self.game.draw_text(display, str(int(self.time)), (255, 255, 255), self.game.GAME_W / 5, self.game.GAME_H / 5)

        print("AQUI ESTOY", self.player.get_position_in_grid(self.map))
        if(self.player.get_position_in_grid(self.map) == positionFinal):
            #print("AQUI ESTOY")
            self.game.draw_text(display, "YOU WINNNNNNNNNNNNNN", (255,255,255), self.game.GAME_W/2, self.game.GAME_H/2 )
            self.game.draw_text(display, "GAME", (255,255,255), self.game.GAME_W / 2, (self.game.GAME_H  / 2) + 30)

        if(self.time <= 0 ):
            self.time = 0
            self.game.draw_text(display, "YOU LOSE", (255,255,255), self.game.GAME_W / 2, (self.game.GAME_H  / 2) + 30)

    def coin_yellow(self, coin_yellow):
        #print("TIME", self.time)
        if(self.player.get_position_in_grid(self.map) == coin_yellow.get_pos()):
            self.time = self.time + 10

    def coin_red(self, coin_red):
        if(self.player.get_position_in_grid(self.map) == coin_yellow.coin_red()):
            start.make_coin()
            end.make_coin()
            self.map.draw(display)
            self.map.algorithm(self.map.get_grid_map(),start, end)
            self.map.update_vecinos()

class Player():
    def __init__(self,game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y= 15,15
        self.current_frame, self.last_frame_update = 0,0

    def get_position_in_grid(self, map):
        self.row = (self.position_x + (self.size_image.get_height()*0.50) ) // map.get_width_muro()
        self.colum = (self.position_y + (self.size_image.get_width()*0.90)) // map.get_width_muro()
        return  self.row, self.colum

    def is_permitted(self, map,position_x,position_y):
        self.row = (self.position_x + (self.size_image.get_height()*0.50) ) // map.get_width_muro()
        self.colum = (self.position_y + (self.size_image.get_width()*0.90)) // map.get_width_muro()
        #print("Postion: ", self.position_x)
        #print("Columna: ", colum)
        #print("Fila: ", row)
        #wssssssssprint("tamaño muro", map.get_width_muro())
        if map.get_cell(int(self.row+position_x),int(self.colum+position_y)).get_is_muro():
            #print("SHOQUE ", map.get_cell(int(self.row+position_x),int(self.colum+position_y)).get_with())

            return False
        else:
            return True

    def is_wingame(self,map,position_x, position_y):
        self.row = (self.position_x + (self.size_image.get_height() * 0.50)) // map.get_width_coin()
        self.colum = (self.position_y + (self.size_image.get_width() * 0.90)) // map.get_width_coin()
        if map.get_cell(int(self.row+position_x),int(self.colum+position_y)).get_is_coin_blue():
            print("WIN")
            return False
        else:
            return True

    def update(self,delta_time, actions,map):
        # Get the direction from inputs
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]

        # Update the position
        if self.is_permitted(map,10 * delta_time * direction_x,10 * delta_time * direction_y):
            self.position_x += 100 * delta_time * direction_x
            self.position_y += 100 * delta_time * direction_y
            #print("direction X", direction_x)
            #print("direction Y", direction_y)
        else:
            self.position_x -= 1 * delta_time * direction_x
            self.position_y -= 1 * delta_time * direction_y

        #if self.position_x == coin_pos[0] or self.position_y == coin_pos[1]:
        #    return 1
        #    print("")
        #else:
        #    return 0
        #Si la pos del jugador x o y esta dentro del map [X,Y] del cell
        #print("Ultimo x: ", ult_x)
        #print("Ultimo y: ", ult_y)
        #print("ACTUAL X: ", self.position_x)
        #print("ACTUAL Y: ", self.position_y)

        #print("Direction x: ", direction_x)
        #print("Direction y: ", direction_y)
        # Animate the sprite
        self.animate(delta_time,direction_x,direction_y)

    def set_position(self,x,y, map):
        columna = self.colum * map.get_width_muro()

    def render(self, display):
        display.blit(self.curr_image, (self.position_x,self.position_y))

    def animate(self, delta_time, direction_x, direction_y):
        # Compute how much time has passed since the frame last updated
        self.last_frame_update += delta_time
        # If no direction is pressed, set image to idle and return
        if not (direction_x or direction_y): 
            self.curr_image = self.curr_anim_list[0]
            return
        # If an image was pressed, use the appropriate list of frames according to direction
        if direction_x:
            if direction_x > 0: self.curr_anim_list = self.right_sprites
            else: self.curr_anim_list = self.left_sprites
        if direction_y:
            if direction_y > 0: self.curr_anim_list = self.front_sprites
            else: self.curr_anim_list = self.back_sprites
        # Advance the animation if enough time has elapsed
        if self.last_frame_update > .15:
            self.last_frame_update = 0
            self.current_frame = (self.current_frame +1) % len(self.curr_anim_list)
            self.curr_image = self.curr_anim_list[self.current_frame]

    def load_sprites(self):
        # Get the diretory with the player sprites
        self.sprite_dir = os.path.join(self.game.sprite_dir, "player")
        self.front_sprites, self.back_sprites, self.right_sprites, self.left_sprites = [],[],[],[]

        # Load in the frames for each direction
        for i in range(1,5):
            self.front_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_front" + str(i) +".png")))
            self.back_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_back" + str(i) +".png")))
            self.right_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_right" + str(i) +".png")))
            self.left_sprites.append(pygame.image.load(os.path.join(self.sprite_dir, "player_left" + str(i) +".png")))
        # Set the default frames to facing front
        self.curr_image = self.front_sprites[0]
        self.curr_anim_list = self.front_sprites
        self.size_image = self.front_sprites[0].convert()
        print(self.size_image)