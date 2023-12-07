class Table():
    def __init__(self):
        self.sets = []

    def add_set(self, set):
        self.sets.append(set)

    def is_set_valid(self, group):
        if len(group) < 3:
            return False
        if len(group) <= 5 and len(set(tile.color for tile in group)) != 1:
            numbers = [tile.number for tile in group]
            colors = [tile.color for tile in group]

            return len(set(numbers)) == 1 and len(set(colors)) == len(colors)
        
        else:
            numbers = sorted(tile.number for tile in group)
            colors = [tile.color for tile in group]

            if len(set(colors)) != 1:
                print("Colors are not the same")
                return False

            is_even = numbers[0] % 2 == 0
            for i in range(1, len(numbers)):
                if (numbers[i] % 2 == 0) != is_even or numbers[i] != numbers[i-1] + 2:
                    print("Numbers are not consecutive")
                    return False
                
            return True
            
            

    def are_all_sets_valid(self):
        return all(self.is_set_valid(set) for set in self.sets)
    
    def get_score(self):
        return sum(len(set) for set in self.sets)
    
    def get_sets(self):
        return self.sets


class Tile:
    def __init__(self, number, color):
        self.number = number
        self.color = color

# Create a Table object
table = Table()

# Create some sets
set1 = [Tile(1, 'red'), Tile(1, 'blue'), Tile(1, 'green')]
set2 = [Tile(2, 'red'), Tile(4, 'red'), Tile(6, 'red'), Tile(8, 'red'), Tile(10, 'red')]
set3 = [Tile(3, 'blue'), Tile(3, 'red'), Tile(3, 'green'), Tile(3, 'yellow')]

# Add the sets to the table
# table.add_set(set1)
table.add_set(set2)
# table.add_set(set3)

# Check if all sets are valid
print("Are all sets valid?", table.are_all_sets_valid())

# Print the score
print("Score:", table.get_score())

self.bg_image = pygame.image.load("assets/images/bg.jpg")
self.bg_rect = self.bg_image.get_rect()

def draw_bg(self, screen):
    screen.blit(self.bg_image, self.bg_rect)