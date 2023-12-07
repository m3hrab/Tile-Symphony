import pygame 
import sys
from player import Player

# Custom Event
PLAYER_TURN_EVENT = pygame.USEREVENT + 1

def handle_mouse_down(event, gamescreen, settings):
    mouse_pos = pygame.mouse.get_pos()


    if "bot" in gamescreen.current_player.name:
        if gamescreen.is_play_for_me_button_clicked:
            # Check if a tile in the table grid is clicked
            for y, row in enumerate(gamescreen.table_grid):
                for x, tile in enumerate(row):
                    if tile is not None and tile.rect.collidepoint(mouse_pos):
                        settings.click_sound.play()
                        gamescreen.selected_tile = tile
                        gamescreen.table_grid[y][x] = None
                        break
            
            # Check if a tile in the player's rack is clicked
            if gamescreen.selected_tile is None:
                for tile in gamescreen.current_player.rack:
                    if tile.rect.collidepoint(mouse_pos):
                        settings.click_sound.play()
                        gamescreen.selected_tile = tile
                        gamescreen.current_player.rack.remove(gamescreen.selected_tile)
                        gamescreen.dragged_tiles.append(gamescreen.selected_tile)
                        break
    
    else:
        # Check if a tile in the table grid is clicked
        for y, row in enumerate(gamescreen.table_grid):
            for x, tile in enumerate(row):
                if tile is not None and tile.rect.collidepoint(mouse_pos):
                    settings.click_sound.play()
                    gamescreen.selected_tile = tile
                    gamescreen.table_grid[y][x] = None
                    break
        
        # Check if a tile in the player's rack is clicked
        if gamescreen.selected_tile is None:
            for tile in gamescreen.current_player.rack:
                if tile.rect.collidepoint(mouse_pos):
                    settings.click_sound.play()
                    gamescreen.selected_tile = tile
                    gamescreen.current_player.rack.remove(gamescreen.selected_tile)
                    gamescreen.dragged_tiles.append(gamescreen.selected_tile)
                    break

    if event.button == 1 and gamescreen.selected_tile == None:
        mouse_pos = pygame.mouse.get_pos()

        # Check if the confirm button is clicked
        if gamescreen.confirm_button.is_over(mouse_pos) and len(gamescreen.dragged_tiles) > 0:
            settings.click_sound.play()
            gamescreen.is_confirm_button_clicked = True
            handle_player_turn_event(gamescreen, settings) 
        
        # Check is show tiles button is clicked
        if gamescreen.show_tiles_button.is_over(mouse_pos):
            settings.click_sound.play()
            gamescreen.is_show_tiles_button_clicked = True

        # Check is play for me button is clicked
        if gamescreen.play_for_me_button.is_over(mouse_pos):
            settings.click_sound.play()
            gamescreen.is_play_for_me_button_clicked = True
            gamescreen.is_show_tiles_button_clicked = True

        
        # Check see more button is clicked
        if gamescreen.see_more_button.is_over(mouse_pos) and len(gamescreen.current_player.rack) > 28:
            settings.click_sound.play()
            gamescreen.is_see_more_button_clicked = True
            gamescreen.is_previous_button_clicked = False

        elif gamescreen.previous_button.is_over(mouse_pos):
            settings.click_sound.play()
            gamescreen.is_previous_button_clicked = True
            gamescreen.is_see_more_button_clicked = False

        # Make turn button
        if len(gamescreen.two_random_tiles) != 2:
            if gamescreen.make_turn_button.is_over(mouse_pos):
                settings.click_sound.play()
                gamescreen.get_two_random_tiles() 


        # Choose a tile from the two random tiles
        elif len(gamescreen.two_random_tiles) == 2:
            if gamescreen.two_random_tiles[0].rect.collidepoint(mouse_pos):
                settings.click_sound.play()
                gamescreen.current_player.rack.append(gamescreen.two_random_tiles[0])
                gamescreen.tile_pool.append(gamescreen.two_random_tiles[1])
                gamescreen.two_random_tiles = []

                #Update the Players turn
                gamescreen.current_player_index = (gamescreen.current_player_index + 1) % len(gamescreen.players)
                gamescreen.current_player = gamescreen.players[gamescreen.current_player_index]
                gamescreen.settings.game_trun_sound.play()

                # Reset the timer
                pygame.time.set_timer(PLAYER_TURN_EVENT, (settings.time_left * 1000))
                gamescreen.time_left = settings.time_left
                gamescreen.turn_start_time = pygame.time.get_ticks()
            
            elif gamescreen.two_random_tiles[1].rect.collidepoint(mouse_pos):
                settings.click_sound.play()
                gamescreen.current_player.rack.append(gamescreen.two_random_tiles[1])
                gamescreen.tile_pool.append(gamescreen.two_random_tiles[0])
                gamescreen.two_random_tiles = []


                # Update the Players turn
                gamescreen.current_player_index = (gamescreen.current_player_index + 1) % len(gamescreen.players)
                gamescreen.current_player = gamescreen.players[gamescreen.current_player_index]
                gamescreen.settings.game_trun_sound.play()

                # Reset the timer
                pygame.time.set_timer(PLAYER_TURN_EVENT, (settings.time_left * 1000))
                gamescreen.time_left = settings.time_left
                gamescreen.turn_start_time = pygame.time.get_ticks() 

            # if len(gamescreen.two_random_tiles) == 2:
            #     gamescreen.tile_pool.append(gamescreen.two_random_tiles[0])
            #     gamescreen.tile_pool.append(gamescreen.two_random_tiles[1])
            #     gamescreen.two_random_tiles = []

def handle_mouse_motion(gamescreen):
    mouse_pos = pygame.mouse.get_pos()
    if gamescreen.selected_tile != None:
        mouse_pos = pygame.mouse.get_pos()
        gamescreen.selected_tile.rect.center = mouse_pos 

def handle_mouse_up(gamescreen, settings):
    if gamescreen.selected_tile != None:
        settings.click_sound.play()
        grid_x = round(gamescreen.selected_tile.rect.x / gamescreen.selected_tile.rect.width)
        grid_y = round(gamescreen.selected_tile.rect.y / gamescreen.selected_tile.rect.height)
        
        # Check if the grid position is within the bounds of the table grid and the cell is empty
        if (0 <= grid_x < gamescreen.table_width and 0 <= grid_y < gamescreen.table_height and
            gamescreen.table_grid[grid_y][grid_x] is None):
            # Place the tile in the nearest grid cell
            gamescreen.table_grid[grid_y][grid_x] = gamescreen.selected_tile
            # Reset the tile's position to the top-left corner of the grid cell
            gamescreen.selected_tile.rect.x = grid_x * gamescreen.selected_tile.rect.width
            gamescreen.selected_tile.rect.y = grid_y * gamescreen.selected_tile.rect.height
        else:
            # Return the tile to the player's rack
            gamescreen.current_player.rack.append(gamescreen.selected_tile)
            gamescreen.dragged_tiles = []

        # Deselect the tile
        gamescreen.selected_tile = None

def handle_game_screen_events(event, gamescreen, settings):
    if event.type == pygame.MOUSEBUTTONDOWN:
        handle_mouse_down(event, gamescreen, settings)
    elif event.type == pygame.MOUSEMOTION:
        handle_mouse_motion(gamescreen)
    elif event.type == pygame.MOUSEBUTTONUP:
        handle_mouse_up(gamescreen, settings)
    if event.type == PLAYER_TURN_EVENT:
        handle_player_turn_event(gamescreen, settings)

def handle_player_turn_event(gamescreen, settings):
    gamescreen.handle_turn()
    if len(gamescreen.two_random_tiles) == 2:
        gamescreen.tile_pool.append(gamescreen.two_random_tiles[0])
        gamescreen.tile_pool.append(gamescreen.two_random_tiles[1])
        gamescreen.two_random_tiles = []

def handle_events(current_screen, gamescreen, settings):
    # Watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if current_screen == gamescreen:
            handle_game_screen_events(event, gamescreen, settings)

def handle_start_screen_events(startscreen, gamescreen, settings):
    next_screen = startscreen.run_screen()
    if next_screen is not None:
        gamescreen.players.append(Player(next_screen[0]))
        gamescreen.initialize_game(next_screen[1])
        settings.game_trun_sound.play()
        return gamescreen
    return startscreen



def update_gamescreen(screen, gamescreen):
    if not gamescreen.check_game_over():
        gamescreen.update_time_left()
        gamescreen.draw_current_player_rack()
        gamescreen.draw_table()
        # gamescreen.draw_hud()
        gamescreen.update_info_card()
        gamescreen.display_info_card()
        if gamescreen.time_left > 0 and len(gamescreen.two_random_tiles) != 0:
            gamescreen.draw_two_random_tiles()

        if gamescreen.selected_tile is not None:
            gamescreen.selected_tile.draw(screen)

def update_screen(screen, settings, current_screen, gamescreen):
    # Draw the screen table
    # screen.fill(settings.bg_color)
    settings.draw_bg(screen, 2)

    # Draw the player rack bg
    settings.draw_racks(screen)

    if current_screen == gamescreen:
        update_gamescreen(screen, gamescreen)
            
    # Make the most recently drawn screen visible
    pygame.display.flip()
    pygame.time.Clock().tick(60)