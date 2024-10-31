from java.awt import Color



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
    1: Color.BLUE,
    # Green
    2: Color(0, 128, 0),
    3: Color.RED,
    # Indigo
    4: Color(75, 0, 130),
    # Maroon
    5: Color(128, 0, 0),
    # Baby Blue
    6: Color(137, 207, 240),
    7: Color.BLACK,
    8: Color.GRAY
}

