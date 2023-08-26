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
# Global variables (played positions dict, winning combinations etc)
# --------------------------------------------------

played_positions = {key: False for key in range(1, 10)}

# winning combinations

row_positions = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
column_positions = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
diagonal_positions = [[1, 5, 9], [3, 5, 7]]

winning_combinations = row_positions + column_positions + diagonal_positions

turn_of_player = True  # false meaning it is the turn of the engine

playing_grid = create_grid()

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


# --------------------------------------------------
# Place the input (both from user and engine) into the grid, update the grid and the played positions
# --------------------------------------------------

# if turn of player then, symbol: "O" and if turn of engine symbol: "X"


def place_input_on_the_playing_grid(symbol_to_place: str, pos_to_place_symbol_on: int):
    global playing_grid, played_positions
    playing_grid = playing_grid.replace(f"{pos_to_place_symbol_on}", symbol_to_place)
    # we also need to update the played_positions dictionary
    played_positions.update({pos_to_place_symbol_on: symbol_to_place})
    return playing_grid


# --------------------------------------------------
# Check whether the game is ("Draw", "") | ("Player", winning_combo) | ("Engine", winning_combo) | ("Continue", "")
# --------------------------------------------------

# but before we move on we need to check if the game is drawn or
# whether anyone has already won (someone has won if any of the winning combinations
# has the same value at all positions i.e, either "X" or, "O"
# in all 3 positions of a combination)


def check_if_draw(played_positions_dict):
    # if anyone hasn't won and all the positions are occupied
    """
    Returns True | False (bool)
    """
    if list(played_positions_dict.values()).count(False) == 0:
        return True

    return False


def check_who_won(played_positions_dict):
    """
    Returns ("Player", winning_combo) | ("Engine", winning_combo) | None (nonetype)
    """
    global winning_combinations

    for ith_combo in winning_combinations:
        if [played_positions_dict[pos] for pos in ith_combo].count("O") == 3:
            return ("Player", ith_combo)
        elif [played_positions_dict[pos] for pos in ith_combo].count("X") == 3:
            return ("Engine", ith_combo)

    return None


def check_whether_to_continue_playing(played_positions_dict):
    """
    Returns ("Draw", "") | ("Player", winning_combo) | ("Engine", winning_combo) | ("Continue", "")
    """
    # if there hasn't been at least 5 rounds we don't need to check if there's a winner or not
    if list(played_positions_dict.values()).count(False) >= 5:
        return ("Continue", "")

    # if no one has won check if draw
    who_won = check_who_won(played_positions_dict)
    if who_won == None:
        if check_if_draw(played_positions_dict) == True:
            return ("Draw", "")
        else:
            return ("Continue", "")
    else:
        return who_won


# --------------------------------------------------
# Novice engine
# --------------------------------------------------


def novice_engine_chooses(played_positions_dict):
    # place at any empty position
    return random.choice(
        [key for key, value in played_positions_dict.items() if value == False]
    )


# --------------------------------------------------
# Beginner engine
# --------------------------------------------------


def beginner_engine_chooses(played_positions_dict):
    global winning_combinations

    # place where the player's winning combination can be blocked else choose randomly
    for ith_combo in winning_combinations:
        vals_in_combo = [played_positions_dict[pos] for pos in ith_combo]
        if vals_in_combo.count("O") == 2 and vals_in_combo.count(False) == 1:
            # if there's no empty position in that combo then no need to panic
            return [pos for pos in ith_combo if played_positions[pos] == False][0]

    return random.choice(
        [key for key, value in played_positions_dict.items() if value == False]
    )


# --------------------------------------------------
# Competent engine
# --------------------------------------------------


def competent_engine_chooses(played_positions_dict):
    global winning_combinations

    # first priority: choose where the engine has a winning combo
    for ith_combo in winning_combinations:
        vals_in_combo = [played_positions_dict[pos] for pos in ith_combo]
        if vals_in_combo.count("X") == 2 and vals_in_combo.count(False) == 1:
            # if there's no empty position in that combo then no need to panic
            return [pos for pos in ith_combo if played_positions[pos] == False][0]

    # second priority: block players winning
    for ith_combo in winning_combinations:
        vals_in_combo = [played_positions_dict[pos] for pos in ith_combo]
        if vals_in_combo.count("O") == 2 and vals_in_combo.count(False) == 1:
            # if there's no empty position in that combo then no need to panic
            return [pos for pos in ith_combo if played_positions[pos] == False][0]

    # third priority: choose where the engine has a winning chance in the next round
    # i.e, when only 1 "X" and 0 "O" in a winning combo
    for ith_combo in winning_combinations:
        vals_in_combo = [played_positions_dict[pos] for pos in ith_combo]
        if vals_in_combo.count("X") == 1 and vals_in_combo.count("O") == 0:
            return random.choice(
                [pos for pos in ith_combo if played_positions[pos] == False]
            )

    # else, choose randomly
    return random.choice(
        [key for key, value in played_positions_dict.items() if value == False]
    )


# --------------------------------------------------
# Choose engine to play against
# --------------------------------------------------

available_engines = {
    1: novice_engine_chooses,
    2: beginner_engine_chooses,
    3: competent_engine_chooses,
}


def choose_engine_to_play_against():
    global available_engines

    engine = input("Please choose the engine to play against (1-3): \t")
    if engine == "":
        engine = "2"
    if engine in ["1", "2", "3"]:
        return available_engines[int(engine)]
    else:
        print("Invalid input.")
        choose_engine_to_play_against()
