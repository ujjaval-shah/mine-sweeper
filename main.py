# from game import *


# if __name__ == '__main__':
#     g = Game()


### To experiment with CSS
from pyscript.web import page, div, input_, button, img


root_node = page["#root"][0]

mines_field = input_(id="mines-field", type="text", size="3", value="000")
time_field = input_(id="time-field", type="text", size="3", value="000")
restart_button = button(img(src=r".\assets\slightly-smiling-face.png"), id="restart-button")
topbar = div(
    id="topbar",
    children=[time_field, restart_button, mines_field]
)

root_node.append(topbar)

root_node.append(div(id="grid"))
