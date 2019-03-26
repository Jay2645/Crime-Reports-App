import toga
from toga.style.pack import *

window = toga.MainWindow('id-window', title='This is a window!')
#window.show()

def button_handler(widget):
    print("hello")


def locationbutton_handler(widget):
    print("Location Button has been selected")


def refreshbutton_handler(widget):
    print("Refresh Button has been selected")


def build(app):
    box = toga.Box()

#make children boxes for different sections of layout
    box_a = toga.Box('box_a')
    box_b = toga.Box('box_b')

    #box = toga.Box('box', children=[box_a, box_b])

#Scrollbar stuff
    #content = toga.WebView()

    #container = toga.ScrollContainer(content=content, horizontal=True)

    #container.vertical = True

    locationBut = toga.Button('Location', on_press=locationbutton_handler)
    refreshBut = toga.Button('Refresh Crime List', on_press=refreshbutton_handler)
    locationInput = toga.TextInput()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1

    locationBut.style.padding = (0, 0, 50, 50)
    locationBut.style.flex = 0
    refreshBut.style.padding = (0, 0, 100, 100)
    refreshBut.style.flex = 0

    locationInput.style.update(flex=1, padding_bottom=0)

    box_b.add(locationBut)
    box_b.add(refreshBut)
    box_b.add(locationInput)

    split = toga.SplitContainer()

    split.content = [box_a, box_b]

    return split


def main():
    return toga.App('Crime Busters', 'dummy', startup=build)


if __name__ == '__main__':
    main().main_loop()
