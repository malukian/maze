import cursor
import console.console as cs
import datetime as dt
from game.Game import Game


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
    except FileNotFoundError:
        print("You haven't played any game...   :(")


def find_time(start_time, end_time):
    diff_time = end_time - start_time

    # Show time of game
    if diff_time.total_seconds() == 0.0:
        str_time = "The game is not over"
    elif diff_time.total_seconds() >= 60.0:
        str_time = "%.f" % (diff_time.total_seconds() // 60) + ' min ' + "%.1f" % (
                diff_time.total_seconds() % 60) + ' sec'
    else:
        str_time = "%.1f" % diff_time.total_seconds() + ' sec'

    print("\nResult:", str_time)
    return str_time


def main():
    # Hide cursor during the game
    cursor.hide()
    cs.space()

    cs.print_art()
    cs.print_info()
    cs.enter_to_continue()

    # Game's run
    while True:

        level = cs.ask_level()

        # Check what ask_level() returns
        if level is None:
            break
        elif level == "info":
            cs.space()
            read_results()
            cs.enter_to_continue()
            continue

        # Create the game
        game = Game(level)
        game.add_player_and_finish()
        game.print_maze()

        start_time = dt.datetime.now()
        end_time = game.navigation()
        # Navigation returns time when game is ended.

        # Write result to results.txt
        # d - day, b - month, Y - year, X - local time
        write_result(
            end_time.strftime("%d %b %Y %X") + " : " + str(level) + "x" + str(level) + " : " +
            find_time(start_time, end_time) + "\n"
        )

        cs.enter_to_continue()

    cs.print_bye()
    cursor.show()


if __name__ == '__main__':
    main()
