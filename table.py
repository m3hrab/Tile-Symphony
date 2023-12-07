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