import toga


def button_handler(widget):
    print("hello")

def locationbutton_handler(widget):
    print("Location Button has been selected")

def refreshbutton_handler(widget):
    print("Refresh Button has been selected")


def build(app):
    box = toga.Box()
    
    locationBut = toga.Button('Location', on_press=locationbutton_handler)
    refreshBut = toga.Button('Refresh Crime List', on_press=refreshbutton_handler)
    locationInput = toga.TextInput()

    button = toga.Button('Hello world', on_press=button_handler)
    button.style.padding = 50
    button.style.flex = 1

    #locationBut.style.padding = (50, 50, 50, 50)
    #locationBut.style.flex = 1
    #refreshBut.style.padding = (0, 0, 100, 100)
    #refreshBut.style.flex = 1
    
    locationInput.style.update(flex=1,padding_bottom=5)
    
    box.add(locationBut)
    box.add(refreshBut)
    box.add(locationInput)

    return box


def main():
    return toga.App('Watch Dogs', 'dummy', startup=build)


if __name__ == '__main__':
    main().main_loop()
