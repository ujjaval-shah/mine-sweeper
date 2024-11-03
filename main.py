# from game import *


# if __name__ == '__main__':
#     g = Game()


### To experiment with CSS
from pyscript.web import page, div, input_, button


root_node = page["#root"][0]

mines_field, time_field = input_(id="mines-field"), input_(id="time-field")
restart_button = button(id="restart-button")
topbar = div(
    id="topbar",
    children=[time_field, restart_button, mines_field]
)

root_node.append(topbar)

root_node.append(div(id="grid"))
