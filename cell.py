import os
from javax.swing import BorderFactory, JPanel, JLabel, ImageIcon, SwingUtilities
from java.awt import Color, Font
from java.awt.event import MouseListener
from settings import *



class GridCell(JPanel):
    PRESSED_COLOR = (184, 207, 229)
    FALSE_POSITIVE_COLOR = (255, 160, 160)

    INITIAL = 0
    FLAGGED = 1
    FALSE_POSITIVE = 2
    REVEALED = 3
    BLAST = 4

    FLAG_IMAGE = os.path.join(os.getcwd(), 'assets', 'red-flag.png')
    MINE_IMAGE = os.path.join(os.getcwd(), 'assets', 'mine.png')

    def __init__(self, id, data, mines):
        super(JPanel, self).__init__()
        self.id = id
        self.data = data
        self.state = GridCell.INITIAL
        self.flagged = False
        self.pressed = False
        self.parent_ = mines
        self.label = JLabel()
        self.setBackground(Color.WHITE)
        self.setBorder(BorderFactory.createLineBorder(Color.BLACK, 1))
        self.label.setFont(Font("Arial", Font.BOLD, 30))
        self.add(self.label)
        self.addMouseListener(self.MineActionListener(self))

    class MineActionListener(MouseListener):
        
        def __init__(self, btn):
            super(MouseListener, self).__init__()
            self.btn = btn

        def mouseEntered(self, mouse_event): pass
        def mouseExited(self, mouse_event): pass
        def mousePressed(self, mouse_event): pass
        def mouseReleased(self, mouse_event): pass

        def mouseClicked(self, mouse_event):
            if SwingUtilities.isLeftMouseButton(mouse_event):
                self.btn.onLeftClick()
            if SwingUtilities.isRightMouseButton(mouse_event):
                self.btn.onRightClick()
    
    def setState(self, state):
        if self.state == state:
            return
        self.state = state
        self.updateDisplay()
    
    def updateDisplay(self):
        if self.state == GridCell.INITIAL:
            self.label.setIcon(None)
        elif self.state == GridCell.FLAGGED:
            self.label.setIcon(ImageIcon(GridCell.FLAG_IMAGE))
        elif self.state == GridCell.FALSE_POSITIVE:
            self.setBackground(Color(*GridCell.FALSE_POSITIVE_COLOR))
        elif self.state == GridCell.REVEALED:
            self.setBackground(Color(*GridCell.PRESSED_COLOR))
            self.label.setIcon(None)
            if 0 < self.data < INF:
                self.label.setForeground(CELL_TEXT_COLOR[self.data])
                self.label.setText(str(self.data))
            elif self.data >= INF:
                self.label.setIcon(ImageIcon(GridCell.MINE_IMAGE))
        elif self.state == GridCell.BLAST:
            self.setBackground(Color.RED)
            self.label.setIcon(ImageIcon(GridCell.MINE_IMAGE))

    def onRightClick(self):
        if not self.parent_.parent_.isGameEnded():
            self.parent_.parent_.setState(STARTED)
            if self.state in [GridCell.INITIAL, GridCell.FLAGGED]:
                if self.state == GridCell.INITIAL:
                    self.setState(GridCell.FLAGGED)
                    self.parent_.increaseFlagCount()
                elif self.state == GridCell.FLAGGED:
                    self.setState(GridCell.INITIAL)
                    self.parent_.decreaseFlagCount()

    def onLeftClick(self):
        if not self.parent_.parent_.isGameEnded():
            self.parent_.parent_.setState(STARTED)
            if self.state == GridCell.INITIAL:
                if self.data == 0:
                    self.setState(GridCell.REVEALED)
                    self.parent_.bfs(self.id)
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
