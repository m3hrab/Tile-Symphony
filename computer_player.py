import itertools

class ComputerPlayer:
    def __init__(self, name):
        self.best_moves = []

    def find_best_move(self, rack, table_tiles):
        # Check if there are more than 2 same number tiles with different colors in the rack
        numbers = [tile.number for tile in rack]
        colors = [tile.color for tile in rack]

        for number in numbers:
            if numbers.count(number) >= 2 and len(set(colors)) > 1:
                # Find all tiles with the same number
                same_number_tiles = [tile for tile in rack if tile.number == number]
                # Find all possible combinations of tiles with the same number
                best_moves = list(itertools.combinations(same_number_tiles, 2))
        # Store all the number
        for i in range(len(colors)):
            temp_numbers = []
            if colors.count(colors[i]) >= 5:
                temp = []
                for j in range(i, len(colors)):
                    if colors[j] == colors[i]:
                        temp.append(numbers[j])
                temp_numbers.append(sorted(temp))
        

        if len(set(colors)) != 1:
            print("Colors are not the same")
            return False

        is_even = numbers[0] % 2 == 0
        for i in range(1, len(numbers)):
            if (numbers[i] % 2 == 0) != is_even or numbers[i] != numbers[i-1] + 2:
                print("Numbers are not consecutive")
                return False
            
