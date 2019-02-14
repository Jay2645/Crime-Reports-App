from tkinter import *
from datetime import *
from tkinter import ttk

#Window
window = Tk()

#Entry for Location
location = Entry()

#Configuration for window of GUI
window.title("Crime Reports")
window.geometry("1000x600")
window.configure(bg = "ivory3")

#Variables
counter = 0
scrollCount = 0
time1 = ""

#Scrolling Bar
scrollbar = Scrollbar(window)
scrollbar.pack(side = RIGHT, fill = Y)

#Frame for window
crimeFrameUI = Frame(window)
crimeFrameUI.pack(fill = BOTH, expand = 1)
crimeFrameUI.configure(height = 600, width = 1000)

#Crime Refresher Function
def crime_refresh():
    global counter
    global time1

    crime = Label(reportFrame, text="crime", bg="LightSteelBlue3", fg="dark slate gray", font = ("verdana", 10), relief = "groove", pady = 5)

    #Get current time
    time2 = datetime.now().strftime('%H : %M : %S : %f')

    #Update time
    if time2 != time1:
        time1 = time2
        crime.config(text = "lat/long " + time2 + ", crime type" )

    crime.grid(row = counter, column = 0, ipady = 6, sticky = N+W+E+S, padx = 10, ipadx = 35)
    counter += 1

#Frame for map
mapFrame = ttk.Frame(crimeFrameUI)
mapFrame.grid_columnconfigure(0, weight=1)
mapFrame.grid(row = 1, column = 0, sticky = "news")
mapFrame.configure(height = 400, width = 110)
mapImage = Label(mapFrame, text = "MAP WILL BE DISPLAYED HERE", bg = "green")

#Frame for buttons
buttonFrame = ttk.Frame(crimeFrameUI)
buttonFrame.grid_columnconfigure(0, weight = 1)
buttonFrame.grid(row = 0, column = 1, sticky = "news")
buttonFrame.configure(height = 50, width = 100)
location = Entry(buttonFrame, font = ("verdana", 10))
location.insert(0, "Enter location...")
locationBtn = Button(buttonFrame, text = "Location", fg = "dark slate gray", bg = "LightSteelBlue3", width = 8, font = ("verdana", 10, "bold"))

#Frame for reports
reportFrame = ttk.Frame(crimeFrameUI)
reportFrame.grid_columnconfigure(1, weight=1)
reportFrame.grid(row = 1, column = 1, sticky = "news")
reportFrame.configure(height = 600, width = 110)
refreshBtn = Button(reportFrame, text = "Refresh", fg = "dark slate gray", bg = "LightSteelBlue3", width = 8, command = crime_refresh, font = ("verdana", 10, "bold"))

#Format for window
location.grid(row = 0, column = 0, pady = 5, padx = 5, ipady = 6, ipadx = 100)
locationBtn.grid(row = 0, column = 1, pady = 5, padx = 5, ipadx = 14, ipady = 4)
refreshBtn.grid(row = 0, column = 2, pady = 5, ipadx = 14, ipady = 4, padx = 5)
mapImage.grid(row = 0, column = 0, ipadx = 160, ipady = 250)

window.mainloop()