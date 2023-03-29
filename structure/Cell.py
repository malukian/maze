class Cell:
    # The "Cell" is a point in the grid which may be surrounded by walls.

    # A wall separates a pair of cells in the Nord-South or West-East directions.
    walls_pairs = {"Nord": "South", "South": "Nord", "East": "West", "West": "East"}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"Nord": True, "South": True, "East": True, "West": True}

    def check_all_walls(self):
        # Check this cell still have all walls.
        return all(self.walls.values())

    def delete_wall(self, other, wall):
        # Delete the wall between cells - self and other.
        self.walls[wall] = False
        other.walls[Cell.walls_pairs[wall]] = False
