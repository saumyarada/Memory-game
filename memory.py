# Memory Game
# The player tries to find two matching tiles by selecting tiles from a rectangular grid. Once all tiles are matched, game is over
# a single person game that tracks the score of the player as the time taken to complete the game, where a lower score is better
# Mini Project 3-- Saumya Rada

import pygame, random, time


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      self.score = 0
      
      # === game specific objects
      self.board_size = 4
      self.image_files = ['image1.bmp','image2.bmp','image3.bmp','image4.bmp','image5.bmp','image6.bmp','image7.bmp','image8.bmp']
      self.board = [] # will be represented by a list of lists
      self.image_list = []
      self.load_images()
      self.create_board()
      self.current_tiles = []
      self.matched_tiles = []
      
   def load_images(self):
      # load images from the file into the image list
      for image in self.image_files:
         loaded_image = pygame.image.load(image)
         self.image_list.append(loaded_image)
      self.image_list = self.image_list + self.image_list
      random.shuffle(self.image_list)
      
   def create_board(self): 
      # creates the grid of images
      index = 0
      for row_index in range(0,self.board_size):
         row = []
         for col_index in range(0,self.board_size):
            image = self.image_list[index]
            index = index +1
            width  = image.get_width()
            height = image.get_height()
            x = col_index *width
            y = row_index * height
            tile = Tile(x,y,width,height,image,self.surface)
            row.append(tile)
         self.board.append(row)
         
   def draw_score(self):
      # draws the score on to the window
      score_string = str(self.score)
      # step 1 create a font object
      font_size = 90
      fg_color = pygame.Color('white')
      font = pygame.font.SysFont('',font_size)
      # step 2 render the font
      text_box = font.render(score_string, True,fg_color,self.bg_color)
      x = self.surface.get_width() - text_box.get_width()
      y = 0
      location = (x,y)
      self.surface.blit(text_box,location)   

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.MOUSEBUTTONUP and self.continue_game:
            self.handle_mouse_up(event.pos)
            
   def handle_mouse_up(self,position):
      # position is bound to event.pos
      # position is the (x,y) location of the click
      for row in self.board:
         for tile in row:
            if tile.can_select(position):
            # asking the tile have you been selected?
               tile.change()
               self.current_tiles.append(tile)
               
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.surface.fill(self.bg_color) # clear the display surface first
      # draw the board
      for row in self.board:
         for tile in row:
            tile.draw()
      self.draw_score()
      pygame.display.update() # make the updated surface appear on the display
      
   def all_matched(self):
      # checks if all the tiles have been matched and returns a bool value 
      all_matched = False
      if len(self.matched_tiles) == 16:
         all_matched = True
      return all_matched
   
   def check_matching(self):
      # checks if two exposed tiles have matching images and appends them to a list if matching
      if self.current_tiles[0].check_matched(self.current_tiles[1]):
         for tile in self.current_tiles:
            self.matched_tiles.append(tile)
         self.current_tiles = []
      else:
         for tile in self.current_tiles:
            tile.change()
         self.current_tiles = []           

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.score = pygame.time.get_ticks()//1000
      if len(self.current_tiles) == 2:
         self.check_matching()
         time.sleep(0.5)      

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if self.all_matched():
         self.continue_game = False

class Tile:
   # A class is a blueprint --- > Properties and behavior
   def __init__(self,x,y,width,height,image,surface):
      self.rect = pygame.Rect(x,y,width,height)
      self.color = pygame.Color('black')
      self.border_width= 10
      self.hidden_image = pygame.image.load('image0.bmp')
      self.hidden = True
      self.content = image
      self.matched = False
      self.surface = surface
      
   def draw(self):
      # draws image onto the window depending on the condition it matches
      if self.hidden == True:
         # Draws the question mark
         pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)
         self.surface.blit(self.hidden_image, self.rect)   
      else:
         # Draws the image
         pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)
         self.surface.blit(self.content, self.rect)  
         
   def change(self):
      # changes the state of the tile (exposed or not) depending on its previous state
      if self.hidden == True:
         self.hidden = False
      else:
         self.hidden = True
      
   def check_matched(self,other):
      # checks if the drawn image of one tile is the same as the other
      # other is a parameter of type Tile and is the Tile which is being compared
      matched = False
      if self.content == other.content and not self.hidden:
         matched = True
      return matched
   
   def can_select(self, position):
      # checks if the click made by the user is valid (can have a consequence)
      # position is a parameter of type tuple and contains the position of the click
      valid_click = False
      if self.rect.collidepoint(position) and self.hidden == True:
         valid_click = True  
      return valid_click      


main()