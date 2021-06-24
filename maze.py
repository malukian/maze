##############################################################################
####               __  __                ___                              ####
####              |  \/  |__ _ ______   / __|__ _ _ __  ___               ####
####              | |\/| / _` |_ / -_) | (_ / _` | '  \/ -_)              ####
####              |_|  |_\__,_/__\___|  \___\__,_|_|_|_\___|              ####
##############################################################################
# BSRN Alternative 7 - Maze Game
# Inna Kuzmina, Victoria Gordeeva, Maksim Lukianov

import random
import cursor
import datetime as dt
from getkey import getkey, keys
from traceback import print_exc

class Cell:
    # The "Cell" is a point in the grid which may be surrounded by walls.
    # Walls: north, east, south, west.

    # A wall separates a pair of cells in the Nord-South or West-East directions.
    # There is a dictionary as list of key:value pairs
    walls_pairs = {"Nord": "South", "South": "Nord", "East": "West", "West": "East"}

    def __init__(self, x, y):
        # Initialize the cell at (x,y). At first it is surrounded by walls.
        self.x = x
        self.y = y
        self.walls = {"Nord": True, "South": True, "East": True, "West": True}

    def check_all_walls(self):
        # Check this cell still have all walls.
        # All() returns True if all items in the iterable are true, otherwise it returns False.
        return all(self.walls.values())

    def delete_wall(self, other, wall):
        # Delete the wall between cells - self and other.
        self.walls[wall] = False
        other.walls[Cell.walls_pairs[wall]] = False
####################################################################################################
class Maze:
    # The Maze, represented as a grid of cells.

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

    def copy_maze_to_binary_list(self):
        # Copy the maze as list of 0's and 1's.
        # 1 is a wall, 0 is a free place.

        # Side's size in the console
        side = self.user_side * 2 + 1

        # At first all points are 1
        maze_in_list = [[1 for x in range(side)] for y in range(side)]

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

        # The dictionary with direction and index from (0, 0)
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
        totalnum = self.user_side ** 2

        # Stack
        cells_stack = []

        # Entry position
        current_cell = self.cell_at(self.sx, self.sy)

        # Total number of visited cells during maze construction.
        visitednum = 1

        while visitednum < totalnum:
            neighbours = self.find_unvisited_neighbours(current_cell)

            if not neighbours:
                # We have reached a dead end: backtrack.
                # Take the last visited cell as current cell and remowe it from stack.
                current_cell = cells_stack.pop()
                continue

            # Choose a random neighbouring cell and delete wall.
            direction, next_cell = random.choice(neighbours)
            current_cell.delete_wall(next_cell, direction)

            # Add the current cell in stack and move to the next cell.
            cells_stack.append(current_cell)
            current_cell = next_cell
            visitednum += 1

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
            if cell.walls[direction] == False:
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
                # We have reached a dead end: backtrack.
                # Add walls back and close this path.
                for wall in current_cell.walls:
                	if current_cell.walls[wall] == False:
                		current_cell.walls[wall] = True
                		# Backtracking_neighbour is the last visited cell, its wall is also added.
                		backtracking_neighbour.walls[Cell.walls_pairs[wall]] = True
                # Take the last visited cell as current cell and remowe it from stack.
                current_cell = path_stack.pop()
                continue

            # Choose a random neighbouring cell.
            next_cell = random.choice(neighbours)

            # Add the current cell in stack and move to the next cell.
            path_stack.append(current_cell)
            current_cell = next_cell

        return path_stack
####################################################################################################
class Game:

    def __init__(self, user_side, player_x = 1, player_y = 1):
    	# Initialize the Maze-Game
        self.user_side = user_side
        self.player_x = player_x
        self.player_y = player_y

        # Start position to make a maze
        sx = self.user_side // 2
        sy = self.user_side // 2

        # Create the maze
        maze = Maze(self.user_side, sx, sy)
        maze.make_maze()
        self.final_maze = maze.copy_maze_to_binary_list()
        self.path_stack = maze.find_path(self.user_side)

        # Icons. 2 symbols for icon.
        self.player = ':)'
        self.finish = '$$'

        # Side's size in the console
        self.side = self.user_side * 2 + 1
        # Finish position
        self.finish_y = self.side - 2
        self.finish_x = self.side - 2

    def add_player_and_finish(self):
        # Start and finish positions
 
        self.final_maze[self.player_y][self.player_x] = self.player
        self.final_maze[self.finish_y][self.finish_x] = self.finish

    def cls():
        # Imitates the clear of console
        print("\n" * 50)

    def print_path(self, x, y):
    	# At first we decode the grid stack to final maze in the console
    	for cell in self.path_stack:
    		self.final_maze[2 * cell.y + 1][2 * cell.x + 1] = "<>"

    	# Start position and player
    	self.final_maze[self.player_x][self.player_y] = "()"
    	self.final_maze[y][x] = self.player

    	self.print_maze()

    	# After print_maze() add back 0's for the next print
    	for cell in self.path_stack:
    		self.final_maze[2 * cell.y + 1][2 * cell.x + 1] = 0

    def print_maze(self):
        # Return a representation of the maze.

        Game.cls()

        Display.print_art()

        # If 0 - two free places, if 1 - two walls, else icon
        # 2 symbols because the maze was a square
        for y in range(self.side):
            print("\n\t", end = "")
            for x in range(self.side):
                if self.final_maze[y][x] == 0:
                    print("  ", end = "")
                elif self.final_maze[y][x] == 1:
                    print('\u2593' * 2, end = "")
                else:
                    print(self.final_maze[y][x], end = "")
        print()

    def navigation(self):
        #Player navigattion via the keyboard (letters or cursor keys). The getkey module is used here.
        #The complete description of the instalation can be found in our folder in the file named getkeyinstall.
        userInput = ""
        x = self.player_x
        y = self.player_y

        endtime = dt.datetime.now()

        while True:

            userInput = getkey()

            # Start from player positions, check the move in the list, if OK:
            # delete player in the old position and create in the new one, then print the maze.

            if userInput == "q":
                break

            elif userInput == "h":
            	self.print_path(x, y)

            elif userInput == "a" or userInput == keys.LEFT:
                if self.final_maze[y][x - 1] != 1:
                    self.final_maze[y][x] = 0
                    x -= 2
                    self.final_maze[y][x] = self.player
                    self.print_maze()

            elif userInput == "d" or userInput == keys.RIGHT:
                if self.final_maze[y][x + 1] != 1:
                    self.final_maze[y][x] = 0
                    x += 2
                    self.final_maze[y][x] = self.player
                    self.print_maze()

            elif userInput == "w" or userInput == keys.UP:
                if self.final_maze[y - 1][x] != 1:
                    self.final_maze[y][x] = 0
                    y -= 2
                    self.final_maze[y][x] = self.player
                    self.print_maze()
  
            elif userInput == "s" or userInput == keys.DOWN:
                if self.final_maze[y + 1][x] != 1:
                    self.final_maze[y][x] = 0
                    y += 2
                    self.final_maze[y][x] = self.player
                    self.print_maze()

            if self.final_maze[self.finish_y][self.finish_x] == self.player:
                # Check the finish of the game
                endtime = dt.datetime.now()
                print("\n\n\t\tYou have won!")
                break
        return endtime
####################################################################################################
class Display:
    # Welcome message
    art = """

    ##############################################################################
    ####               __  __                ___                              ####
    ####              |  \/  |__ _ ______   / __|__ _ _ __  ___               ####
    ####              | |\/| / _` |_ / -_) | (_ / _` | '  \/ -_)              ####
    ####              |_|  |_\__,_/__\___|  \___\__,_|_|_|_\___|              ####
    ##############################################################################


    """

    messages = ("\tThis python script simulates the maze game. User has an opportunity to", 
                "\tchoose the size of the labyrinth and enjoy playing in free time.",
                "",
                "\tThis  program  was developed as part of the examination for 'Operating",
                "\tSystems and Computer Networks' modules of the IBIS/EBIS (International",
                "\t/Engineering Business Information Systems) degree program at Frankfurt",
                "\tUniversity of Applied Sciences in 2021.",
                "",
                "\tContributors:",
                "\t\t-Inna Kuzmina",
                "\t\t-Viktoria Gordeeva",
                "\t\t-Maksim Lukianov"
                )
    welcome_message = "\n".join(messages)

    def print_art():
        print(Display.art)

    def print_welcome():
        print(Display.welcome_message)

    def ask_key_to_continue():
        user_input = ""
        print("\n\n\n\t\t\t..... Press any key to continue .....")
        user_input = getkey()
        Game.cls()

    def ask_maze_size():
        print("Please enter the size of maze in the range from 2 to 25:")
        # Input validation. Only integer numbers are allowed.
        try:
            cursor.show()
            user_side = int(input())
            # Limitation of maze
            if not 1 < user_side < 26:
            	raise Exception
            cursor.hide()

        except Exception:

            print("\n\tValueError!")
            print("\tValue must be integer number in the range[2;25]\n")
            user_side = Display.ask_maze_size()

        return user_side

    def print_bye():
    	print("\n\t\t\tExiting...")
    	print("\n\t\t\tBye!")

    def ask_level():
    # Choice between 4 options of size and watch statistics after few games
        level_menu = '''

        		Navigation: W A S D / cursor keys
        		Use Q (quit) to end the game
        		Use H (help) to see the right path

        		+--------------------------------+
        		#                                #
        		#       [1] Level 1: 10x10       #
        		#                                #
        		#       [2] Level 2: 15x15       #
        		#                                #
        		#       [3] Level 3: 20x20       #
        		#                                #
        		#       [4] Your own level       #
        		#                                #
        		#       [5] Statistics           #
        		#                                #
        		#       [0] Exit :(              #
        		#                                #
        		+--------------------------------+
        '''

        print(level_menu)

        user_input = ""

        user_input = getkey()

        if user_input == '0':
            return 0

        elif user_input == '1':
            return 10

        elif user_input == '2':
	        return 15

        elif user_input == '3':
            return 20

        elif user_input == '4':
            return Display.ask_maze_size()

        elif user_input == '5':
          	return -1

        else:
        	print("\n\tWrong key!")
        	return Display.ask_level()
####################################################################################################
class Main_Class:

	def write_result(result):
		# "a" - will create a file if the specified file does not exist
		file = open("maze_results.txt", "a")
		file.write(result)
		file.close()

	def read_results():
		# Open and read the file
		try:
			file = open("maze_results.txt", "r")
			print(file.read())
		except Exception:
			print("You haven't played any game...   :(")
	
	def main():
		# Main function

		# Hide cursor during the game
		cursor.hide()
		Game.cls()

		Display.print_art()
		Display.print_welcome()
		Display.ask_key_to_continue()

		# Game's run
		while True:

			try:
				# Menu
				level = Display.ask_level()

				# Check what ask_level() returns
				if level == 0:
					break
				elif level == -1:
					Game.cls()
					Main_Class.read_results()
					Display.ask_key_to_continue()
					continue

				# Create the game
				game = Game(level)
				game.add_player_and_finish()
				game.print_maze()

				starttime = dt.datetime.now()
				endtime = game.navigation()
				# Navigation returns time when game is ended.

				difftime = endtime - starttime

				# Show time of game
				if difftime.total_seconds() == 0.0:
					strtime = "The game is not over"
				elif difftime.total_seconds() >= 60.0:
					strtime = "%.f" % (difftime.total_seconds() // 60) + ' min ' + "%.1f" % (difftime.total_seconds() % 60) + ' sec'
				else:
					strtime = "%.1f" % difftime.total_seconds() + ' sec'

				print("\n\t\tResult:", strtime)

				# Write result to results.txt
				# d - day, b - month, Y - year, X - local time
				Main_Class.write_result(endtime.strftime("%d %b %Y %X") + " : " + str(level) + "x" + str(level) + " : " + strtime + "\n")

				Display.ask_key_to_continue()

			except Exception:
				print("\n\tSomething is wrong...   :(\n")
				#print_exc()

		Display.print_bye()

		cursor.show()
####################################################################################################
# Main
Main_Class.main()