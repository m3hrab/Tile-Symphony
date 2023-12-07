import pygame 
import random
from player import Player
from card import Tile
from table import Table
from settings import Button, Label
PLAYER_TURN_EVENT = pygame.USEREVENT + 1

class Game():

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.players = []
        self.table = Table()
        self.tile_pool = []
        self.current_player = None
        self.current_tile = None
        self.current_player_index = 0
        self.time_left = settings.time_left
        self.two_random_tiles = []
        self.selected_tile = None

        self.dragged_tiles = []
        self.is_confirm_button_clicked = False
        self.is_show_tiles_button_clicked = False
        self.is_play_for_me_button_clicked = False
        self.is_see_more_button_clicked = False
        self.is_previous_button_clicked = True
        

        self.table_width = settings.screen_width // 60
        self.table_height = (settings.screen_height - settings.player_rack_height - 20) // 75

        self.table_grid = [[None for _ in range(self.table_width)] for _ in range(self.table_height)]
        self.previous_table_grid =  [[None for _ in range(self.table_width)] for _ in range(self.table_height)]

    def initialize_game(self, number_of_players):
        self.create_players(number_of_players)
        self.create_tile_pool()
        # Shuffle the tile pool
        random.shuffle(self.tile_pool)

        # Distribute 14 random tiles to each player
        for player in self.players:
            for _ in range(14):
                player.rack.append(self.tile_pool.pop())

        self.current_player = self.players[0]
        pygame.time.set_timer(PLAYER_TURN_EVENT, (self.settings.time_left * 1000))
        self.turn_start_time = pygame.time.get_ticks()
        self.create_info_card()

    def create_players(self, number_of_players):
        for i in range(number_of_players):
            self.players.append(Player("bot" + str(i + 1))) 

    def create_tile_pool(self):
        # colors = ["black", "blue", "green", "red", "yellow"]
        colors = ["blue", "green", "red", "yellow", "pink"]
        for color in colors:
            for number in range(1, 16):
                for _ in range(2):
                    self.tile_pool.append(Tile(number, color))


    def find_consecutive_sets(self, grid):
        consecutive_sets = []

        # Iterate through rows
        for i in range(len(grid)):
            # Iterate through columns
            j = 0
            while j < len(grid[0]):
                # If the current cell in not None, find consecutive cells horizontally
                if grid[i][j] is not None:
                    # consecutive_set = [(i, j)]
                    consecutive_set = [grid[i][j]]
                    k = j + 1
                    while k < len(grid[0]) and grid[i][k] is not None:
                        consecutive_set.append(grid[i][k])
                        k += 1

                    consecutive_sets.append(consecutive_set)

                    # Move to the next cell after the consecutive set
                    j = k
                else:
                    j += 1

        return consecutive_sets

    def handle_turn(self):
        
        # check if any tiles are added to the table_grid
        if len(self.dragged_tiles) != 0 or self.table_grid != self.previous_table_grid:
            # Check confirm button is clicked
            if self.is_confirm_button_clicked or self.table_grid != self.previous_table_grid:
                # find all the valid sets
                self.table.sets = self.find_consecutive_sets(self.table_grid)
                # check if all sets are valid
                if self.table.are_all_sets_valid():
                    self.previous_table_grid = []
                    for row in self.table_grid:
                        self.previous_table_grid.append(row.copy())
                    self.dragged_tiles = []

                    # Make the turn
                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.current_player = self.players[self.current_player_index]
                    self.settings.game_trun_sound.play()
                    
                    # Update the time
                    pygame.time.set_timer(PLAYER_TURN_EVENT, (self.settings.time_left * 1000))
                    self.time_left = self.settings.time_left
                    self.turn_start_time = pygame.time.get_ticks()
                    self.is_confirm_button_clicked = False


                else:

                    self.table_grid = []
                    for row in self.previous_table_grid:
                        self.table_grid.append(row.copy())
                    for tile in self.dragged_tiles:
                        self.current_player.rack.append(tile)

                    self.dragged_tiles = []

                    if self.time_left >= 1:
                        return
                    
                    # Make the turn
                    self.current_player.rack.append(self.tile_pool.pop())
                    self.current_player_index = (self.current_player_index + 1) % len(self.players)
                    self.current_player = self.players[self.current_player_index]
                    self.settings.game_trun_sound.play()
                    
                    # Update the time
                    pygame.time.set_timer(PLAYER_TURN_EVENT, (self.settings.time_left * 1000))
                    self.time_left = self.settings.time_left
                    self.turn_start_time = pygame.time.get_ticks()

                return 

            else:
                self.table_grid = []
                for row in self.previous_table_grid:
                    self.table_grid.append(row.copy())
                for tile in self.dragged_tiles:
                    self.current_player.rack.append(tile)

                self.dragged_tiles = []
                if self.time_left >= 1:
                    return
                # self.settings.game_invalid_turn_sound.play()
                
        self.current_player.rack.append(self.tile_pool.pop())
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.current_player = self.players[self.current_player_index]

        # Update the time
        pygame.time.set_timer(PLAYER_TURN_EVENT, (self.settings.time_left * 1000))
        self.time_left = self.settings.time_left
        self.turn_start_time = pygame.time.get_ticks()
        self.settings.game_trun_sound.play()

        self.is_play_for_me_button_clicked = False
        self.is_show_tiles_button_clicked = False
        
    def update_time_left(self):
        current_time = pygame.time.get_ticks()
        self.time_left = self.settings.time_left - (current_time - self.turn_start_time) / 1000  # Update the time left
            

    def check_game_over(self):
        # Game is over when one player has no more tiles
        for player in self.players:
            if len(player.rack) == 0:
                return True
        return False
    
    def get_two_random_tiles(self):
        self.two_random_tiles.append(self.tile_pool.pop())
        self.two_random_tiles.append(self.tile_pool.pop())

    def draw_two_random_tiles(self):
        for i, tile in enumerate(self.two_random_tiles):
            tile.rect.x = self.settings.player_rack_width + 40 
            tile.rect.y = self.settings.screen_height  - (100 + i * tile.rect.height)
            tile.draw(self.screen)


    def create_info_card(self):
        x = self.settings.screen_width - 220
        y = self.settings.screen_height - 200

        # timer
        self.timer_label = Label(x, y, f"Time left: {str(int(self.time_left))}", 20, (0,0,255))
        # player name
        self.player_name_label = Label(x, y + 30, f"Player: {self.current_player.name}", 20, (255,255,255))
        # tiles left
        self.tiles_left_label = Label(x, y + 60, f"Tiles left: {len(self.tile_pool)}", 20, (255,255,255))
        # make turn button
        self.make_turn_button = Button((0,255, 0), x, y + 90, 100, 30,"Make Turn")
        # confirm button
        self.confirm_button = Button((0,255, 0), x+110, y + 90, 100, 30, "Confirm")
        # show tiles button
        self.show_tiles_button = Button((0,255, 0), x, y + 130, 100, 30, "Show Tiles")
        # play for me button
        self.play_for_me_button = Button((0,255, 0), x+110, y + 130, 100, 30, "Play for me")

        # See more button
        self.see_more_button = Button((0,255, 0), x-600, y + 155, 100, 30, "See More")
        self.previous_button = Button((0,255, 0), x-490, y + 155, 140, 30, "Show Previous")

    def update_info_card(self):
        self.timer_label.update_text(f"Time left: {str(int(self.time_left))}", (255,255,255))
        self.player_name_label.update_text(f"Player: {self.current_player.name}", (255,255,255))
        self.tiles_left_label.update_text(f"Tiles left: {len(self.tile_pool)}", (255,255,255))

    def display_info_card(self):

        self.timer_label.draw(self.screen)
        self.player_name_label.draw(self.screen)
        self.tiles_left_label.draw(self.screen)
        self.see_more_button.draw(self.screen)
        if "bot" not in self.current_player.name or self.is_play_for_me_button_clicked:
            self.make_turn_button.draw(self.screen)
            self.confirm_button.draw(self.screen)
        else:
            self.show_tiles_button.draw(self.screen)
            self.play_for_me_button.draw(self.screen)

        if self.is_see_more_button_clicked:
            self.previous_button.draw(self.screen)

        elif self.is_previous_button_clicked:
            self.see_more_button.draw(self.screen)

    def draw_current_player_rack(self):
        
        flag = False
        if len(self.current_player.rack) > 28 and self.is_see_more_button_clicked:
            flag = True

        if "bot" not in self.current_player.name:
            self.current_player.draw_rack(self.screen, self.settings, flag)
        
        elif "bot" in self.current_player.name:
            if self.is_show_tiles_button_clicked or self.is_play_for_me_button_clicked:
                self.current_player.draw_rack(self.screen, self.settings, flag)

    def draw_table(self):
        # Draw the player's table

        for y, row in enumerate(self.table_grid):
            for x, tile in enumerate(row):
                if tile is not None:
                    tile.rect.x = x * 60 - (3 * x)
                    tile.rect.y = y * 75
                    tile.draw(self.screen)