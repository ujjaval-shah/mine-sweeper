import os
from pyscript.web import div, img, span
from settings import *
from pyscript import display



class GridCell:
    PRESSED_COLOR = "rgb(184, 207, 229)"
    FALSE_POSITIVE_COLOR = "rgb(255, 160, 160)"

    INITIAL = 0
    FLAGGED = 1
    FALSE_POSITIVE = 2
    REVEALED = 3
    BLAST = 4

    FLAG_IMAGE = os.path.join('.', 'assets', 'red-flag.png')
    MINE_IMAGE = os.path.join('.', 'assets', 'mine.png')

    def __init__(self, x, y, data, grid):
        self.x = x
        self.y = y
        self.data = data
        self.parent_ = grid
        self.image_tag = img()

        self.node = div(
            self.image_tag,
            id = f"cell_{x}_{y}",
            classes = "cell",
            style = {"background-color": "white"},
            onclick = self.onLeftClick,
            oncontextmenu = self.onRightClick
        )

        self.state = GridCell.INITIAL
    
    def setState(self, state):
        if self.state == state:
            return
        self.state = state
        self.updateDisplay()
    
    def updateDisplay(self):
        if self.state == GridCell.INITIAL:
            self.image_tag.src = ""
        elif self.state == GridCell.FLAGGED:
            self.image_tag.src = GridCell.FLAG_IMAGE
        elif self.state == GridCell.FALSE_POSITIVE:
            self.node.style["background-color"] = GridCell.FALSE_POSITIVE_COLOR
        elif self.state == GridCell.REVEALED:
            self.node.style["background-color"] = GridCell.PRESSED_COLOR
            self.image_tag.src = ""
            if 0 < self.data < INF:
                self.node.append(span(
                    self.data,
                    classes="celldata",
                    style = {"color": CELL_TEXT_COLOR[self.data]}
                ))
            elif self.data >= INF:
                self.image_tag.src = GridCell.MINE_IMAGE
        elif self.state == GridCell.BLAST:
            self.node.style["background-color"] = "red"
            self.image_tag.src = GridCell.MINE_IMAGE

    def onRightClick(self, e):
        e.preventDefault()
        if not self.parent_.parent_.isGameEnded():
            self.parent_.parent_.setState(STARTED)
            if self.state in [GridCell.INITIAL, GridCell.FLAGGED]:
                if self.state == GridCell.INITIAL:
                    self.setState(GridCell.FLAGGED)
                    self.parent_.increaseFlagCount()
                elif self.state == GridCell.FLAGGED:
                    self.setState(GridCell.INITIAL)
                    self.parent_.decreaseFlagCount()

    def onLeftClick(self, e):
        if not self.parent_.parent_.isGameEnded():
            self.parent_.parent_.setState(STARTED)
            if self.state == GridCell.INITIAL:
                if self.data == 0:
                    self.setState(GridCell.REVEALED)
                    self.parent_.bfs((self.x, self.y))
                    self.parent_.checkIfIsAVictory()
                    return
                
                if self.data < INF:
                    self.setState(GridCell.REVEALED)
                    self.parent_.checkIfIsAVictory()
                else:
                    self.setState(GridCell.BLAST)
                    self.parent_.parent_.setState(GAME_OVER)
    
    def bfsClick(self):
        if self.state != GridCell.REVEALED:
            self.setState(GridCell.REVEALED)
    
    def onVictory(self):
        if self.state == GridCell.INITIAL:
            self.setState(GridCell.FLAGGED)
    
    def onGameOver(self):
        if self.state == GridCell.FLAGGED:
            if self.data < INF:
                self.setState(GridCell.FALSE_POSITIVE)
        if self.state == GridCell.INITIAL:
            if self.data >= INF:
                self.setState(GridCell.REVEALED)
