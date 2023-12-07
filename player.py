class Player():

    def __init__(self, name) -> None:
        self.name = name
        self.rack = []
        self.score = 0

    def add_tile(self, tile):
        self.rack.append(tile)

    def remove_tile(self, tile):
        self.rack.remove(tile)

    def calculate_score(self):
        self.score = 0
        for tile in self.rack:
            self.score += tile.number 

    def draw_rack(self, screen, settings, flag):

        if len(self.rack) <= 28 or not flag:
            temp = settings.y
            for i, tile in enumerate(self.rack):
                tile.rect.x = settings.x + (i%14) * tile.rect.width - (5*(i%14))
                tile.rect.y = temp 

                # If the tile goes off the right edge of the rack, move it to the next row
                if tile.rect.x + (tile.rect.width * 2) > settings.player_rack_width:
                    temp += tile.rect.height 

                tile.draw(screen)
        
        elif flag:
            
            temp = settings.y
            # Draw the tiles from the first position on the rack
            for i, tile in enumerate(self.rack[14:]):
                tile.rect.x = settings.x + (i%14) * tile.rect.width 
                tile.rect.y = temp

                if tile.rect.x + (tile.rect.width * 2) > settings.player_rack_width:
                    temp += tile.rect.height 

                tile.draw(screen)