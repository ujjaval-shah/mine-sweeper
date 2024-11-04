# from game import *


# if __name__ == '__main__':
#     g = Game()


### To experiment with CSS
from pyscript.web import page, div, input_, button, img, span, wrap_dom_element


root_node = page["#root"][0]

mines_field = input_(id="mines-field", type="text", size="3", value="000")
time_field = input_(id="time-field", type="text", size="3", value="000")
restart_button = button(img(src=r".\assets\slightly-smiling-face.png"), id="restart-button")
topbar = div(
    id="topbar",
    children=[time_field, restart_button, mines_field]
)

root_node.append(topbar)

def on_cell_click(e):
    cell = wrap_dom_element(e.target)
    cell.style["background-color"] = "rgb(184, 207, 229)"
    i, j = cell.id.split("_")[1:]
    data = int(i)*16 + int(j)
    if data % 9:
        cell.append(span(data % 9, classes="celldata"))
    else:
        # cell.append(span(img(src=r".\assets\red-flag.png"), classes="celldata"))
        cell.append(img(src=r".\assets\mine.png"))

grid_node = div(
    id="grid",
    children=[
        div(
            classes = "row",
            children = [
            div(
                id = f"cell_{i}_{j}",
                classes = "cell",
                onclick = on_cell_click,
                style = {
                    "background-color": "white"
                }
            ) for j in range(16)
        ]) for i in range(16)
    ]
)
root_node.append(grid_node)
