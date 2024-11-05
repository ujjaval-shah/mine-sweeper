import os
from grid import Grid
from settings import *
from pyscript.web import page, div, input_, button, img, span, wrap_dom_element
from pyodide.ffi.wrappers import set_interval, clear_interval



class Game:
    INITIAL_IMAGE = os.path.join('.', 'assets', 'slightly-smiling-face.png')
    VICTORY_IMAGE = os.path.join('.', 'assets', 'smiling-face-with-sunglasses.png')
    GAME_OVER_IMAGE = os.path.join('.', 'assets', 'face-with-head-bandage.png')

    def __init__(self):
        self.state = None
        self.time_taken = 0
        self.timer = None
        self.game_mode = None
        
        self.bindGameModeInput()

        self.root_node = page["#root"][0]

        self.mines_field = input_(id="mines-field", type="text", size="3", value="000")
        self.time_field = input_(id="time-field", type="text", size="3", value="000")
        self.restart_btn_img = img()
        self.restart_button = button(
            self.restart_btn_img,
            id="restart-button",
            onclick=lambda e: self.restart()
        )
        self.top_bar = div(
            id="topbar",
            children=[self.time_field, self.restart_button, self.mines_field]
        )
        
        self.root_node.append(self.top_bar)

        self.grid_node = div(id="grid")
        self.root_node.append(self.grid_node)

        self.setState(YET_TO_START)

    def isGameEnded(self):
        return self.state == VICTORY or self.state == GAME_OVER
    
    def setState(self, state):
        if self.state == state:
            return

        self.state = state
        self.updateGame()
    
    def updateGame(self):
        if self.state == YET_TO_START:
            # print "new grid"
            self.grid_node.innerHTML = ""
            self.grid = Grid(self, self.grid_node, self.game_mode)
            # print "timer field reset"
            self.resetTimeField()
            # print "mines field reset"
            self.updateMinesField(TOTAL_MINES[self.game_mode])
            # print "restart button icon updated"
            self.restart_btn_img.src = Game.INITIAL_IMAGE
        elif self.state == STARTED:
            # print "timer started"
            self.startTimer()
        elif self.state == VICTORY:
            # print "timer stopped"
            self.stopTimer()
            # print "mines filed 0"
            self.updateMinesField(0)
            # print "flag remaining mines"
            self.grid.onVictory()
            # print "restart button icon updated"
            self.restart_btn_img.src = Game.VICTORY_IMAGE
        elif self.state == GAME_OVER:
            # print "timer stopped"
            self.stopTimer()
            # print "reveal all mines"
            # print "falsely flagged cells color"
            self.grid.onGameOver()
            # print "restart button icon updated"
            self.restart_btn_img.src = Game.GAME_OVER_IMAGE
    
    def restart(self):
        self.setState(YET_TO_START)

    def bindGameModeInput(self):
        for radiobtn in page["input[type=radio]"]:
            if radiobtn.checked:
                self.game_mode = radiobtn.value
            radiobtn.onchange = self.onGameModeChange

    def onGameModeChange(self, e):
        self.game_mode = e.target.value
        self.state = None
        self.restart()

    def startTimer(self):
        self.timer = set_interval(self.incrementTimeField, 1000)
    
    def stopTimer(self):
        if self.timer:
            clear_interval(self.timer)

    def resetTimeField(self):
        self.stopTimer()
        self.time_taken = 0
        self.updateTimeField(self.time_taken)
    
    def incrementTimeField(self):
        self.time_taken += 1
        self.updateTimeField(self.time_taken)
    
    def updateTimeField(self, time_seconds):
        time_seconds = min(time_seconds, TIMER_FIELD_LIMIT)
        text = str(time_seconds)
        self.time_field.value = (3 - len(text))*'0' + text

    def updateMinesField(self, remaining_mines):
        remaining_mines = max(remaining_mines, MINES_FIELD_LIMIT)
        text = str(remaining_mines)
        self.mines_field.value = (3 - len(text))*'0' + text
