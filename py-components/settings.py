BEGINNER = "BEGINNER"
INTERMEDIATE = "INTERMEDIATE"
EXPERT = "EXPERT"

GRID_SIZE = {
    BEGINNER: [9, 9],
    INTERMEDIATE: [16, 16],
    EXPERT: [16, 30]
}
TOTAL_MINES = {
    BEGINNER: 10,
    INTERMEDIATE: 40,
    EXPERT: 99
}

INF = 1000 # Indicates a mine

ONE_SECOND = 1000

TIMER_FIELD_LIMIT = 999
MINES_FIELD_LIMIT = -99

# states of game component
YET_TO_START = 0
STARTED = 1
VICTORY = 2
GAME_OVER = 3

CELL_TEXT_COLOR = {
    1: "blue",
    2: "green",
    3: "red",
    4: "indigo",
    5: "maroon",
    6: "mediumpurple",
    7: "black",
    8: "gray"
}
