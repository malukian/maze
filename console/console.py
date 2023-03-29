import cursor
import keyboard


def space():
    print("\n" * 10)


def enter_to_continue():
    input("Press Enter to continue...")
    space()


def ask_maze_size():
    print("Please enter the size of maze in the range from 2 to 25:")
    try:
        cursor.show()
        user_side = int(input())
        # Limitation of maze
        if not 1 < user_side < 21:
            raise ValueError
        cursor.hide()
    except ValueError:
        print("\nValueError!")
        print("Value must be integer number in the range[2;20]\n")
        user_side = ask_maze_size()
    finally:
        return user_side


def print_bye():
    print("\nExiting...")
    print("\nBye!")


def ask_level():
    level_menu = '''    
    Navigation: W A S D
    "ESC" to end the game
    "h" (help) to see the path

    +--------------------------------+
    |                                |
    |       [1] Level 1: 5x5         |
    |                                |
    |       [2] Level 2: 10x10       |
    |                                |
    |       [3] Level 3: 15x15       |
    |                                |
    |       [4] Your own level       |
    |                                |
    |       [5] Statistics           |
    |                                |
    |       [Esc] Exit :(            |
    |                                |
    +--------------------------------+
    '''

    print(level_menu)

    not_pressed = True

    while True:
        inp = keyboard.read_key(suppress=True)
        if not_pressed:
            not_pressed = False
            match inp:
                case 'esc':
                    return None
                case '1':
                    return 5
                case '2':
                    return 10
                case '3':
                    return 15
                case '4':
                    return ask_maze_size()
                case '5':
                    return "info"
        else:
            not_pressed = True


# Source: https://ascii.co.uk/art/maze
art = '''
+------------------------------------------------------+
|                                                      |
|   88,dPba,,adPba,  ,adPPYYba, 888888888  ,adPPYba,   |
|   88P'  "88"   "8a ""     `Y8      a8P" a8P_____88   |
|   88     88     88 ,adPPPPP88   ,d8P'   8PP"""""""   |
|   88     88     88 88,    ,88 ,d8"      "8b,         |
|   88     88     88 `"8bbdP"Y8 888888888  `"Ybbd8"'   |
|                                                      |
+------------------------------------------------------+
'''

infos = [
    'This console application simulates the simple maze game.\n',
    'The application was developed as part of the examination in 2021',
    'for the course "Operating Systems and Computer Networks"\n',
    'Frankfurt University of Applied Sciences\n',
    'Maksim Lukianov\n'
]
info = "\n".join(infos)


def print_art():
    print(art)


def print_info():
    print(info)
