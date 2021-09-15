import pygame, os
from states.state import State
from states.pause_menu import PauseMenu
from mapa.map import Mapa

class Game_World(State):
    def __init__(self, game):
        State.__init__(self,game)
        self.player = Player(self.game)
        self.grass_img = pygame.image.load(os.path.join(self.game.assets_dir, "map", "grass.png"))
        self.ROWS = 30;
        self.map = Mapa(self.game,self.ROWS)

    def update(self,delta_time, actions):
        # Check if the game was paused 
        if actions["start"]:
            new_state = PauseMenu(self.game)
            new_state.enter_state()
        self.player.update(delta_time, actions,self.map)

    def render(self, display):
        display.blit(self.grass_img, (0,0))
        self.map.draw(display)
        self.player.render(display)
        

class Player():
    def __init__(self,game):
        self.game = game
        self.load_sprites()
        self.position_x, self.position_y = 189,200
        self.current_frame, self.last_frame_update = 0,0


    def is_permitted(self, map,position_x,position_y):
        self.row = (self.position_x + (self.size_image.get_height()*0.50) ) // map.get_width_muro()
        self.colum = (self.position_y + (self.size_image.get_width()*0.90)) // map.get_width_muro()
        #print("Columna: ", colum)
        #print("Fila: ", row)
        #print("tamaño muro", map.get_width_muro())
        if map.get_cell(int(self.row+position_x),int(self.colum+position_y)).get_is_muro():
            print("SHOQUE ")
            return False
        else:
            return True

    def update(self,delta_time, actions, map):
        # Get the direction from inputs
        direction_x = actions["right"] - actions["left"]
        direction_y = actions["down"] - actions["up"]

        # Update the position
        if self.is_permitted(map,100 * delta_time * direction_x,100 * delta_time * direction_y):
            self.position_x += 100 * delta_time * direction_x
            self.position_y += 100 * delta_time * direction_y
            print("direction X", direction_x)
            print("direction Y", direction_y)

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