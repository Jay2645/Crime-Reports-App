from tkinter import *
from datetime import *
from plyer import gps
from tkinter import ttk

from CrimeAPI import GetCrime
from googlemap_utils import getMap, get_lat_lng

#Window
window = Tk()
crime_api = GetCrime()

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

#GPS Update Callback
def update_loc(**kwargs):
	global my_loc
	global mapImage
	global mapLabel
	if kwargs["lat"] is not None and kwargs["lng"] is not None:
		my_loc = {"lat":kwargs["lat"],"lng":kwargs["lng"]}
		getMap(my_loc["lat"], my_loc["lng"], zoom=15, width=110, height=400, format="png")
		mapImage = PhotoImage(file="map.png")
		mapLabel.configure(image=mapImage)
		mapLabel.image = mapImage
		mapLabel.pack()
#GPS functionality if applicable - mobile only (should support both iphone and android)
try:
	gps.configure(on_location=update_loc) #Configs gps object to use update_loc function as a callback
	gps.start(minTime=10000, minDistance=1) #Poll every 10 seconds
except: pass
my_loc = {}
#Default location to CSUF
my_loc["lat"]=33.8813416
my_loc["lng"]=-117.8866257

#Crime Refresher Function
def crime_refresh():
	global counter
	global time1
	global crime_api
	global my_loc
	global location
	
	crime_api.update_query(my_loc["lat"], my_loc["lng"], 10, 2)
	all_crimes = crime_api.get_crimes()

	for crime_report in all_crimes:
		crime = Label(reportFrame, bg="LightSteelBlue3", fg="dark slate gray", font = ("verdana", 8), relief = "groove", pady = 5)
		print(crime_report)

		#Get current time
		time2 = datetime.now().strftime('%H : %M : %S : %f')

		#Update time
		if time2 != time1:
			time1 = time2
			crime.config(text = "Type: " + crime_report['type'] + ", Lat: " + str(crime_report['lat']) + "/long: " + str(crime_report['lon']) + ", time: " + crime_report['timestamp'] + ", location: " + crime_report['location'])

		crime.grid(row = counter, column = 0, ipady = 6, sticky = N+W+E+S, padx = 10, ipadx = 35)
		counter += 1

#Frame for map
mapFrame = ttk.Frame(crimeFrameUI)
mapFrame.grid_columnconfigure(0, weight=1)
mapFrame.grid(row = 1, column = 0, sticky = "news")
mapFrame.configure(height = 400, width = 110)
#mapImage = Label(mapFrame, text = "MAP WILL BE DISPLAYED HERE", bg = "green")
getMap(lat=my_loc["lat"], lng=my_loc["lng"],zoom=15,width=110,height=400,format="png")
mapImage = PhotoImage(file="map.png") #this variable needs to stay so the reference to the image stays alive
mapLabel = Label(mapFrame, image=mapImage)
mapLabel.pack()
#Location Button callback to download a new map
def refresh_map():
	global mapImage
	global mapLabel
	if location.get() != ("" or None):
		new_loc = get_lat_lng(location.get())
		if new_loc is not None:
			my_loc = new_loc
			getMap(my_loc["lat"], my_loc["lng"], zoom=15, width=110, height=400, format="png")
			mapImage = PhotoImage(file="map.png")
			mapLabel.configure(image=mapImage)
			mapLabel.image = mapImage
			mapLabel.pack()

#Frame for buttons
buttonFrame = ttk.Frame(crimeFrameUI)
buttonFrame.grid_columnconfigure(0, weight = 1)
buttonFrame.grid(row = 0, column = 1, sticky = "news")
buttonFrame.configure(height = 50, width = 100)
location = Entry(buttonFrame, font = ("verdana", 10))
location.insert(0, "") #Location box needs to be empty b/c the gps poller only runs if it is
locationBtn = Button(buttonFrame, command=refresh_map, text = "Location", fg = "dark slate gray", bg = "LightSteelBlue3", width = 8, font = ("verdana", 10, "bold"))

#Frame for reports
reportFrame = ttk.Frame(crimeFrameUI)
reportFrame.grid_columnconfigure(1, weight=1)
reportFrame.grid(row = 1, column = 1, sticky = "news")
reportFrame.configure(height = 600, width = 110)
refreshBtn = Button(reportFrame, text = "Refresh Crime List", fg = "dark slate gray", bg = "LightSteelBlue3", width = 8, command = crime_refresh, font = ("verdana", 10, "bold"))

#Format for window
location.grid(row = 0, column = 0, pady = 5, padx = 5, ipady = 6, ipadx = 100)
locationBtn.grid(row = 0, column = 1, pady = 5, padx = 5, ipadx = 14, ipady = 4)
refreshBtn.grid(row = 0, column = 2, pady = 5, ipadx = 14, ipady = 4, padx = 5)
#mapLabel.grid(row = 0, column = 0, ipadx = 160, ipady = 250)

window.mainloop()
