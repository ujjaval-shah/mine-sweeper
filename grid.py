from collections import deque
from threading import Thread
import random
# from javax.swing import JPanel, BorderFactory
# from java.awt import GridLayout, Dimension
from cell import GridCell
from settings import *
from pyscript.web import page, div, input_, button, img, span, wrap_dom_element



class Grid:
    
    def __init__(self, game, grid_node):
        self.parent_ = game
        self.total_flags = 0
        self.grid_node = grid_node

        self.arrangeMines()
        # self.buttons = [[GridCell(i*GRID_SIZE+j, self.cells[i][j], self) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

        self.grid_node.append([
            div(
                classes = "row",
                children = [
                    GridCell(
                        x = i, y = j,
                        data = self.cells[i][j],
                        grid = self,
                        id = f"cell_{i}_{j}",
                        classes = "cell",
                        style = {
                            "background-color": "white"
                        }
                    ) for j in range(GRID_SIZE)
                ]
            ) for i in range(GRID_SIZE)
        ])

        # self.buttons = [[GridCell(i*GRID_SIZE+j, self.cells[i][j], self) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

        # for i in range(GRID_SIZE):
        #     for j in range(GRID_SIZE):
        #         self.add(self.buttons[i][j])

    def is_valid(self, x):
        return 0 <= x[0] < GRID_SIZE and 0 <= x[1] < GRID_SIZE
    
    def arrangeMines(self):
        self.cells = [[0 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

        mines_set = set()
        while len(mines_set) < TOTAL_MINES:
            mine = random.randrange(GRID_SIZE*GRID_SIZE)
            mines_set.add(mine)
        
        for mine in mines_set:
            cell = (mine // GRID_SIZE, mine % GRID_SIZE)

            neighbours = [
                (cell[0]-1, cell[1]-1),
                (cell[0]-1, cell[1]),
                (cell[0]-1, cell[1]+1),
                (cell[0], cell[1]-1),
                (cell[0], cell[1]+1),
                (cell[0]+1, cell[1]-1),
                (cell[0]+1, cell[1]),
                (cell[0]+1, cell[1]+1),
            ]

            self.cells[cell[0]][cell[1]] = INF

            for ncell in neighbours:
                if self.is_valid(ncell):
                    self.cells[ncell[0]][ncell[1]] += 1
        
        # # DEBUG
        # print("\n")
        # for row in self.cells:
        #     print(row)

# # # method definition updated    
    def bfs(self, id):
        root = (id // GRID_SIZE, id % GRID_SIZE)
        q = deque([root])
        visited = set([root])

        while q:
            nq = deque()
            for cell in q:

                neighbours = [
                    (cell[0]-1, cell[1]-1),
                    (cell[0]-1, cell[1]),
                    (cell[0]-1, cell[1]+1),
                    (cell[0], cell[1]-1),
                    (cell[0], cell[1]+1),
                    (cell[0]+1, cell[1]-1),
                    (cell[0]+1, cell[1]),
                    (cell[0]+1, cell[1]+1),
                ]

                for ncell in neighbours:
                    if self.is_valid(ncell) and ncell not in visited:
                        if self.buttons[ncell[0]][ncell[1]].state == GridCell.FLAGGED:
                            self.decreaseFlagCount()
                        if self.cells[ncell[0]][ncell[1]] == 0:
                            Thread(target=self.buttons[ncell[0]][ncell[1]].bfsClick).start()
                            visited.add(ncell)
                            nq.append(ncell)
                        elif self.cells[ncell[0]][ncell[1]] < INF:
                            Thread(target=self.buttons[ncell[0]][ncell[1]].bfsClick).start()
                            visited.add(ncell)
                
                q = nq
        return
    
    def increaseFlagCount(self):
        self.total_flags += 1
        remaining_mines = TOTAL_MINES - self.total_flags
        self.parent_.updateMinesField(remaining_mines)
    
    def decreaseFlagCount(self):
        self.total_flags -= 1
        remaining_mines = TOTAL_MINES - self.total_flags
        self.parent_.updateMinesField(remaining_mines)

    def checkIfIsAVictory(self):
        non_revealed_cells_count = 0
        for row in self.buttons:
            for btn in row:
                non_revealed_cells_count += (btn.state != GridCell.REVEALED)
        if non_revealed_cells_count == TOTAL_MINES:
            self.parent_.setState(VICTORY)
    
    def onVictory(self):
        for row in self.buttons:
            for btn in row:
                Thread(target=btn.onVictory).start()
    
    def onGameOver(self):
        for row in self.buttons:
            for btn in row:
                Thread(target=btn.onGameOver).start()


# def on_cell_click(e):
#     cell = wrap_dom_element(e.target)
#     cell.style["background-color"] = "rgb(184, 207, 229)"
#     i, j = cell.id.split("_")[1:]
#     data = int(i)*16 + int(j)
#     if data % 9:
#         cell.append(span(data % 9, classes="celldata"))
#     else:
#         # cell.append(span(img(src=r".\assets\red-flag.png"), classes="celldata"))
#         cell.append(img(src=r".\assets\mine.png"))


# class Grid:

#     def __init__(self, game, grid_node):
#         self.parent_ = game
#         self.total_flags = 0

#         self.arrangeMines()
#         grid_node.append([
#             div(
#                 classes = "row",
#                 children = [
#                 div(
#                     id = f"cell_{i}_{j}",
#                     classes = "cell",
#                     onclick = on_cell_click,
#                     style = {
#                         "background-color": "white"
#                     }
#                 ) for j in range(16)
#             ]) for i in range(16)
#         ])

#         # self.buttons = [[GridCell(i*GRID_SIZE+j, self.cells[i][j], self) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

#         # for i in range(GRID_SIZE):
#         #     for j in range(GRID_SIZE):
#         #         self.add(self.buttons[i][j])

#     def is_valid(self, x):
#         return 0 <= x[0] < GRID_SIZE and 0 <= x[1] < GRID_SIZE
    
#     def arrangeMines(self):
#         self.cells = [[0 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

#         mines_set = set()
#         while len(mines_set) < TOTAL_MINES:
#             mine = random.randrange(GRID_SIZE*GRID_SIZE)
#             mines_set.add(mine)
        
#         for mine in mines_set:
#             cell = (mine // GRID_SIZE, mine % GRID_SIZE)

#             neighbours = [
#                 (cell[0]-1, cell[1]-1),
#                 (cell[0]-1, cell[1]),
#                 (cell[0]-1, cell[1]+1),
#                 (cell[0], cell[1]-1),
#                 (cell[0], cell[1]+1),
#                 (cell[0]+1, cell[1]-1),
#                 (cell[0]+1, cell[1]),
#                 (cell[0]+1, cell[1]+1),
#             ]

#             self.cells[cell[0]][cell[1]] = INF

#             for ncell in neighbours:
#                 if self.is_valid(ncell):
#                     self.cells[ncell[0]][ncell[1]] += 1
        
#         # DEBUG
#         print("\n")
#         for row in self.cells:
#             print(row)

#     def onVictory(self):
#         pass

#     def onGameOver(self):
#         pass
