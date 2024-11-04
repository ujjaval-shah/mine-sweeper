# from java.awt import Color



GRID_SIZE = 16
TOTAL_MINES = 40
INF = 1000 # Indicates a mine

MARGIN = (6, 6, 6, 6)
TOPBAR_HEIGHT = 100
MINE_WIDTH = 45
LENGTH = GRID_SIZE*MINE_WIDTH
RESTART_BTN_DIMENSIONS = (78, 78)

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
    # Baby Blue
    6: "rgb(137, 207, 240)",
    7: "black",
    8: "gray"
}

