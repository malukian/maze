import random
from structure.Cell import Cell


class Maze:
    def __init__(self, user_side, sx, sy):
        # Initialize the maze's grid.
        # The maze consists of ( user_side * user_side ) cells.
        # The generation starts at the cell indexed at (sx, sy).
        self.user_side = user_side
        self.sx = sx
        self.sy = sy
        # Create a new map of cells
        self.maze_map = [[Cell(x, y) for x in range(user_side)] for y in range(user_side)]

    def cell_at(self, x, y):
        # Return the "Cell" object at (y, x).
        return self.maze_map[y][x]

    # add player position to class Cell
    def copy_maze_to_binary_list(self):
        # Copy the maze as list of 0's and 1's.
        # 1 is a wall, 0 is a free place.

        # Side's size in the console
        side = self.user_side * 2 + 1

        # At first all points are 1
        maze_in_list = [[1 for _ in range(side)] for _ in range(side)]

        # Places of cells in new list are 0
        for y in range(1, side, 2):
            for x in range(1, side, 2):
                maze_in_list[y][x] = 0

        # Check east and south walls and make maze's grid with 0.
        # New indexes of cells are [2*y + 1][2*x + 1], but we need the neighbouring index of wall.
        for y in range(self.user_side):
            for x in range(self.user_side):
                if not self.maze_map[y][x].walls['East']:
                    maze_in_list[2 * y + 1][2 * x + 2] = 0

                if not self.maze_map[y][x].walls['South']:
                    maze_in_list[2 * y + 2][2 * x + 1] = 0

        return maze_in_list

    def find_unvisited_neighbours(self, cell):
        # Return the list of unvisited neighbours to cell.

        # The dictionary with directions and coordinates from (0, 0)
        steps = [('West', (-1, 0)),
                 ('East', (1, 0)),
                 ('South', (0, 1)),
                 ('Nord', (0, -1))]

        neighbours = []

        # Make steps in all direction
        for direction, (dx, dy) in steps:
            x2 = cell.x + dx
            y2 = cell.y + dy

            # Check the neighbour places in the maze
            if (0 <= x2 < self.user_side) and (0 <= y2 < self.user_side):
                neighbour = self.cell_at(x2, y2)

                # check_all_walls returns True for only unvisited cells. They will be saved in list.
                if neighbour.check_all_walls():
                    neighbours.append((direction, neighbour))

        return neighbours

    def make_maze(self):
        # Main function make maze as list of cells
        # Total number of cells.
        total_num = self.user_side ** 2

        # Stack
        cells_stack = []

        # Entry position
        current_cell = self.cell_at(self.sx, self.sy)

        # Total number of visited cells during maze construction.
        visited_num = 1

        while visited_num < total_num:
            neighbours = self.find_unvisited_neighbours(current_cell)

            if not neighbours:
                # We have reached a dead end: backtrack.
                # Take the last visited cell as current cell and remove it from stack.
                current_cell = cells_stack.pop()
                continue

            # Choose a random neighbouring cell and delete wall.
            direction, next_cell = random.choice(neighbours)
            current_cell.delete_wall(next_cell, direction)

            # Add the current cell in stack and move to the next cell.
            cells_stack.append(current_cell)
            current_cell = next_cell
            visited_num += 1

    def find_neighbours(self, cell):
        # Return the list of neighbouring cells that no longer have walls between them and a current cell.

        steps = [('West', (-1, 0)),
                 ('East', (1, 0)),
                 ('South', (0, 1)),
                 ('Nord', (0, -1))]

        neighbours = []

        # Make steps in all direction
        for direction, (dx, dy) in steps:
            # Check the path is free from the wall
            if not cell.walls[direction]:
                x2 = cell.x + dx
                y2 = cell.y + dy
                # If the path is free, append the neighbour to list
                neighbour = self.cell_at(x2, y2)
                neighbours.append(neighbour)

        return neighbours

    def find_path(self, user_side):
        path_stack = []
        # We are looking for a path from start to finish
        # Entry position
        current_cell = self.cell_at(0, 0)
        # Finish cell is the last element in the maze-list (right lower corner)
        finish_cell = self.cell_at(user_side - 1, user_side - 1)

        while current_cell != finish_cell:

            neighbours = self.find_neighbours(current_cell)

            # Check that we go forward
            for neighbour in neighbours:
                # If path stack already has the neighbour, we don't need this step
                if neighbour in path_stack:
                    # Previous neighbour for case (if not neighbours)
                    backtracking_neighbour = neighbour
                    neighbours.remove(neighbour)

            if not neighbours:
                # We have reached a dead end: backtrack
                # Add walls back and close this path
                for wall in current_cell.walls:
                    if not current_cell.walls[wall]:
                        current_cell.walls[wall] = True
                        # Backtracking_neighbour is the last visited cell, its wall is also added
                        backtracking_neighbour.walls[Cell.walls_pairs[wall]] = True
                # Take the last visited cell as current cell and remove it from stack
                current_cell = path_stack.pop()
                continue

            # Choose a random neighbouring cell
            next_cell = random.choice(neighbours)

            # Add the current cell in stack and move to the next cell
            path_stack.append(current_cell)
            current_cell = next_cell

        return path_stack
