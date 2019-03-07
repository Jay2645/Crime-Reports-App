# Import UI elements
from tkinter import *
from tkinter import ttk

# Import GPS stuff
from plyer import gps

# Import APIs
from CrimeAPI import GetCrime
from googlemap_utils import get_map, get_lat_lng

CSUF_LAT = 33.8813416
CSUF_LNG = -117.8866257

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1200

MAP_HEIGHT = 400
MAP_WIDTH = 400
MAP_FILENAME = "map"
MAP_EXTENSION = "png"

BUTTON_FOREGROUND = "dark slate gray"
BUTTON_BACKGROUND = "LightSteelBlue3"

LABEL_FONT = ("verdana", 8)
BUTTON_FONT = ("verdana", 10, "bold")

class CrimeUI(object):
	def __init__(self, address = "", radius = 10, in_days = 2):
		self.address = address
		self.crime_radius = radius
		self.crime_days_filter = in_days
		self.crime_count = 0

		# GPS functionality if applicable - mobile only (should support both iPhone and android)
		try:
			gps.configure(on_location=self._update_loc) # Configs gps object to use update_loc function as a callback
			gps.start(minTime=10000, minDistance=1) # Poll every 10 seconds
			self.use_gps = True
		except:
			self.use_gps = False
			print("No GPS configured, disabling GPS queries")

		# Get latitude and longitude of passed-in address
		self.my_loc = get_lat_lng(self.address)
		if self.my_loc == None:
			self.my_loc = {}
			if not self.use_gps:
				# If no GPS, default location to CSUF
				self.my_loc["lat"]= CSUF_LAT
				self.my_loc["lng"]= CSUF_LNG
				print("Not using GPS, default location set to " + str(self.my_loc))
		
		self.window = Tk()

		#Configuration for window GUI
		self.window.title("Crime Reports")
		self.window.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
		self.window.configure(bg = "ivory3")

		self.crime_api = GetCrime()
		self.location = Entry()

		#Scrollbar
		self.scrollbar = Scrollbar(self.window)
		self.scrollbar.pack(side = RIGHT, fill = Y)

		#Frame for window
		self.crimeFrameUI = Frame(self.window)
		self.crimeFrameUI.pack(fill = BOTH, expand = 1)
		self.crimeFrameUI.configure(height = WINDOW_HEIGHT, width = WINDOW_WIDTH)

		#Frame for map
		self.mapFrame = ttk.Frame(self.crimeFrameUI)
		self.mapFrame.grid_columnconfigure(0, weight=1)
		self.mapFrame.grid(row = 1, column = 0, sticky = "news")
		self.mapFrame.configure(height = MAP_HEIGHT, width = MAP_WIDTH)

		# Map image
		get_map(lat=self.my_loc["lat"], lng=self.my_loc["lng"],zoom=15,width=MAP_WIDTH,height=MAP_HEIGHT,format=MAP_EXTENSION)
		mapImage = PhotoImage(file=MAP_FILENAME + "." + MAP_EXTENSION) #this variable needs to stay so the reference to the image stays alive
		self.mapLabel = Label(self.mapFrame, image=mapImage)
		self.mapLabel.pack()

		#Frame for buttons
		self.buttonFrame = ttk.Frame(self.crimeFrameUI)
		self.buttonFrame.grid_columnconfigure(0, weight = 1)
		self.buttonFrame.grid(row = 0, column = 1, sticky = "news")
		self.buttonFrame.configure(height = 50, width = 100)
		self.location = Entry(self.buttonFrame, font = BUTTON_FONT)
		self.location.insert(0, self.address)

		self.locationBtn = Button(self.buttonFrame, command=self._refresh_map, text = "Location", fg = BUTTON_FOREGROUND, bg = BUTTON_BACKGROUND, width = 8, font = BUTTON_FONT)

		#Frame for reports
		self._create_report_frame()

		#Format for window
		self.location.grid(row = 0, column = 0, pady = 5, padx = 5, ipady = 6, ipadx = 100)
		self.locationBtn.grid(row = 0, column = 1, pady = 5, padx = 5, ipadx = 14, ipady = 4)

	# Create report frame
	# This gets run whenever we poll for new crime events, to prevent duplicate entries
	def _create_report_frame(self):
		self.reportFrame = ttk.Frame(self.crimeFrameUI)
		self.reportFrame.grid_columnconfigure(1, weight=1)
		self.reportFrame.grid(row = 1, column = 1, sticky = "news")
		self.reportFrame.configure(height = 600, width = 110)
		self.refreshBtn = Button(self.reportFrame, text = "Refresh Crime List", fg = BUTTON_FOREGROUND, bg = BUTTON_BACKGROUND, width = 8, command = self._crime_refresh, font = BUTTON_FONT)
		self.refreshBtn.grid(row = 0, column = 2, pady = 5, ipadx = 14, ipady = 4, padx = 5)
		
	#GPS Update Callback
	def _update_loc(self, **kwargs):
		if not self.use_gps:
			return
		if kwargs["lat"] is not None and kwargs["lng"] is not None:
			self._create_map_image({"lat":kwargs["lat"],"lng":kwargs["lng"]})

	#Crime Refresher Function
	def _crime_refresh(self):
		self.crime_api.update_query(self.my_loc["lat"], self.my_loc["lng"], self.crime_radius, self.crime_days_filter)
		all_crimes = self.crime_api.get_crimes()
		self.update_crimes(all_crimes)


	#Location Button callback to download a new map
	def _refresh_map(self):
		print("Refreshing map!")
		try:
			self.address = self.location.get()
		except NameError:
			# Use cached location
			pass
			
		if self.address == "":
			new_loc = self.my_loc
		else:
			new_loc = get_lat_lng(self.address)

		self._create_map_image(new_loc)
		self._crime_refresh()

	def _create_map_image(self, new_loc):
		if new_loc is not None:
			print("Creating an image at: " + str(new_loc))
			self.my_loc = new_loc
			if get_map(self.my_loc["lat"], self.my_loc["lng"], zoom=15, width=MAP_WIDTH, height=MAP_HEIGHT, format=MAP_EXTENSION):
				mapImage = PhotoImage(file=MAP_FILENAME + "." + MAP_EXTENSION)
				self.mapLabel.configure(image=mapImage)
				self.mapLabel.image = mapImage
				self.mapLabel.pack()
			else:
				print("Could not load map for " + self.location.get())
		else:
			print("Passed in a null location!")

	# Removes all crime data from the list and resets the crime count
	def remove_crime_list(self):
		self._create_report_frame()		
		self.crime_count = 0

	# Updates the list of crimes with the given list
	def update_crimes(self, crimes_list):
		self.remove_crime_list()

		# Re-create the frame holding all the crime reports
		for crime_report in crimes_list:
			crime = Label(self.reportFrame, bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, font = LABEL_FONT, relief = "groove", pady = 5)
			crime.config(text = crime_report['type'] + " at " + crime_report['timestamp'] + ". Location: " + crime_report['location'])

			crime.grid(row = self.crime_count, column = 0, ipady = 6, sticky = N+W+E+S, padx = 10, ipadx = 35)
			self.crime_count += 1

		print("Found " + str(self.crime_count) + " crimes.")

	def create_window(self):
		self._refresh_map()
		self.window.mainloop()