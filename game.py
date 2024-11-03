import os
# from javax.swing import (
#     JFrame, JPanel, JTextField,
#     JButton, BorderFactory, ImageIcon,
#     Timer,
# )
# from java.awt import (
#     BorderLayout, Dimension, 
#     Color, Font, Insets,
# )
# from java.awt.event import ActionListener
# from java.io import File
from grid import Grid
from settings import *


class TopbarWrapper(JPanel):
    
    def __init__(self):
        super(JPanel, self).__init__()
        self.setLayout(BorderLayout())
        self.setBorder(BorderFactory.createEmptyBorder(*MARGIN))

    def getPreferredSize(self):
        return Dimension(LENGTH, TOPBAR_HEIGHT)


class TextDisplayWrapper(JPanel):
    margin = (2, 2, 2, 2)

    def __init__(self, child, where):
        super(JPanel, self).__init__()
        self.setLayout(BorderLayout())
        self.setBorder(BorderFactory.createEmptyBorder(*TextDisplayWrapper.margin))
        self.add(child, where)


class TimerListener(ActionListener):
    
    def __init__(self, game):
        super(ActionListener, self).__init__()
        self.game = game
    
    def actionPerformed(self, e):
        self.game.incrementTimeField()


class restartBtnListener(ActionListener):
    
    def __init__(self, game):
        super(ActionListener, self).__init__()
        self.game = game

    def actionPerformed(self, e):
        self.game.restart()


class Game:
    INITIAL_IMAGE = os.path.join(os.getcwd(), 'assets', 'slightly-smiling-face.png')
    VICTORY_IMAGE = os.path.join(os.getcwd(), 'assets', 'smiling-face-with-sunglasses.png')
    GAME_OVER_IMAGE = os.path.join(os.getcwd(), 'assets', 'face-with-head-bandage.png')
    TEXTFIELD_FONT_FILE = File(os.path.join(os.getcwd(), 'assets', 'Digital7Mono.ttf'))
    TEXTFIELD_FONT = Font.createFont(Font.TRUETYPE_FONT, TEXTFIELD_FONT_FILE).deriveFont(80.0)

    def __init__(self):
        self.state = YET_TO_START
        self.time_taken = 0

        self.frame = JFrame("Minesweeper")
        self.frame.setResizable(False)
        self.frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.frame.setLayout(BorderLayout())


        topbar = TopbarWrapper()
        
        # Mines count field
        self.mines_field = JTextField("000")
        self.mines_field.setEditable(False)
        self.mines_field.setBackground(Color.WHITE)
        self.mines_field.setFont(Game.TEXTFIELD_FONT)
        topbar.add(TextDisplayWrapper(self.mines_field, BorderLayout.WEST), BorderLayout.WEST)

        # Smiley Button
        self.restartBtn = JButton()
        
        restart_wrap = JPanel()
        self.restartBtn.setMargin(Insets(0,0,0,0))
        
        self.restartBtn.setIcon(ImageIcon(Game.INITIAL_IMAGE))
        self.restartBtn.setFocusPainted(False)
        self.restartBtn.setPreferredSize(Dimension(*RESTART_BTN_DIMENSIONS))
        self.restartBtn.setBackground(Color.WHITE)
        self.restartBtn.addActionListener(restartBtnListener(self))
        restart_wrap.add(self.restartBtn)

        topbar.add(restart_wrap, BorderLayout.CENTER)

        # timer display field
        self.time_field = JTextField("000")
        self.time_field.setEditable(False)
        self.time_field.setBackground(Color.WHITE)
        self.time_field.setFont(Game.TEXTFIELD_FONT)
        topbar.add(TextDisplayWrapper(self.time_field, BorderLayout.EAST), BorderLayout.EAST)

        self.frame.getContentPane().add(topbar, BorderLayout.NORTH)

        # grid
        self.grid = Grid(self)
        self.frame.getContentPane().add(self.grid, BorderLayout.CENTER)

        
        self.frame.pack()
        self.frame.setVisible(True)
    
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
            self.frame.remove(self.grid)
            self.grid = Grid(self)
            self.frame.getContentPane().add(self.grid, BorderLayout.CENTER)
            self.frame.revalidate()
            self.frame.pack()
            # print "timer field reset"
            self.resetTimeField()
            # print "mines field reset"
            self.updateMinesField(TOTAL_MINES)
            # print "restart button icon updated"
            self.restartBtn.setIcon(ImageIcon(Game.INITIAL_IMAGE))
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
            self.restartBtn.setIcon(ImageIcon(Game.VICTORY_IMAGE))
        elif self.state == GAME_OVER:
            # print "timer stopped"
            self.stopTimer()
            # print "reveal all mines"
            # print "falsely flagged cells color"
            self.grid.onGameOver()
            # print "restart button icon updated"
            self.restartBtn.setIcon(ImageIcon(Game.GAME_OVER_IMAGE))
    
    def restart(self):
        self.setState(YET_TO_START)
    
    def startTimer(self):
        self.timer = Timer(ONE_SECOND, TimerListener(self))
        self.timer.start()
    
    def stopTimer(self):
        self.timer.stop()

    def resetTimeField(self):
        if self.timer:
            self.timer.stop()
        self.time_taken = 0
        self.updateTimeField(self.time_taken)
    
    def incrementTimeField(self):
        self.time_taken += 1
        self.updateTimeField(self.time_taken)
    
    def updateTimeField(self, time_seconds):
        time_seconds = min(time_seconds, TIMER_FIELD_LIMIT)
        text = str(time_seconds)
        self.time_field.setText((3 - len(text))*'0' + text)

    def updateMinesField(self, remaining_mines):
        remaining_mines = max(remaining_mines, MINES_FIELD_LIMIT)
        text = str(remaining_mines)
        self.mines_field.setText((3 - len(text))*'0' + text)
