import random

""" what to do?

1. show the welcome screen
2. the user plays first

3. playing Steps

# see if any one has already won (if not continue if yes then show who has won with what combination)
# take user input (see if it's a valid input, if yes then place it on the board, show the grid)
# see if someone has already won (if not continue if yes then show who has won with what combination)
# computers turn (see if there are any winning combinations and if it can be blocked. 
if yes place input there otherwise choose a random empty space or if in intelligent mode try to use one 
of the winning combinations)
# continue playing until one wins or it's a draw (when no winning combination is matched and also all 
9 spaces are occupied)

"""
# --------------------------------------------------
# create initial grid
# --------------------------------------------------

def create_grid():
    init_grid = """
            =====    =====    =====
              1        2        3
            =====    =====    =====
              4        5        6
            =====    =====    =====
              7        8        9
            =====    =====    =====
"""

    return init_grid

# --------------------------------------------------
# prompt the human player until a valid input is provided
# --------------------------------------------------

def prompt_human_player(invalid=False):
    if invalid:
        print("Invalid input. Try again.")

    input_from_user = input(
        "Please choose a position between (1-9) and be sure to choose an empty space: \t"
    )
    return input_from_user

# check if user input is valid
# invalid if 
# 1) not a number 
# 2) the input is not a valid key to the played positions dict
# 3) the position is not empty


def is_input_valid(user_input):
    global played_positions
    try:
        user_input = int(user_input)
    except:
        return False

    if (played_positions.get(user_input) is False) and (
        played_positions.get(user_input) is not None
    ):
        return user_input
    else:
        return False
    
# take input from the player
# prompt until a valid input is chosen

def human_player_input():
    input_from_user = prompt_human_player()

    while is_input_valid(input_from_user) is False:
        input_from_user = prompt_human_player(True)

    return int(input_from_user)

