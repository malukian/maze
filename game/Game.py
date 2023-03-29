import console.console as cs
import datetime as dt
import keyboard
from structure.Maze import Maze


class Game:

    def __init__(self, user_side, player_x=1, player_y=1):
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

    def print_path(self, x, y):
        # At first, we decode the grid stack to final maze in the console
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

        cs.space()
        cs.print_art()

        # If 0 - two free places, if 1 - two walls, else icon
        # 2 symbols because the maze was a square
        for y in range(self.side):
            print("\n", end="")
            for x in range(self.side):
                if self.final_maze[y][x] == 0:
                    print("  ", end="")
                elif self.final_maze[y][x] == 1:
                    print('\u2593' * 2, end="")
                else:
                    print(self.final_maze[y][x], end="")
        print()

    def navigation(self):
        # Player navigation via the keyboard (cursor keys)

        x = self.player_x
        y = self.player_y

        time = dt.datetime.now()

        running = True
        not_pressed = True

        while running:

            inp = keyboard.read_key(suppress=True)

            if not_pressed:

                self.final_maze[y][x] = 0

                match inp:
                    case "esc":
                        running = False
                    case "h":
                        self.print_path(x, y)
                        continue
                    case "a":
                        if self.final_maze[y][x - 1] != 1:
                            x -= 2
                    case "d":
                        if self.final_maze[y][x + 1] != 1:
                            x += 2
                    case "w":
                        if self.final_maze[y - 1][x] != 1:
                            y -= 2
                    case "s":
                        if self.final_maze[y + 1][x] != 1:
                            y += 2
                    case _:
                        pass

                self.final_maze[y][x] = self.player
                self.print_maze()

                if self.final_maze[self.finish_y][self.finish_x] == self.player:
                    # Check the finish of the game
                    time = dt.datetime.now()
                    print("\nYou have won!")
                    running = False

                not_pressed = False
            else:
                not_pressed = True

        return time
