# Import Kivy stuff
from kivy.app import App
from kivy.uix.button import *
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.loader import Loader

# Import GPS stuff
import CustomGPS

# Import APIs
from CrimeAPI import GetCrime
from googlemap_utils import get_map, get_lat_lng

#import os
from functools import partial

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

'''		if coordinates is not None:
			if get_map(coordinates["lat"], coordinates["lng"], zoom=15, width=MAP_WIDTH, height=MAP_HEIGHT, format=MAP_EXTENSION):
				image_path = "../" + MAP_FILENAME + "." + MAP_EXTENSION
				self.map_image = toga.Image(image_path)
				self.map_view.image = self.map_image
				print("Updating image at " + str(coordinates) + " using image at " + image_path)
			else:
				print("Could not load map for " + self.get_current_address())
		else:
			print("Cannot generate a map for no location!")
'''

class grid(Widget):
	pass


class crimeApp(App):
	def build(self):
		#return CrimeUI('800 N State College Blvd, Fullerton, CA 92831', 10, 2)
		return CrimeUI()

class CrimeUI(FloatLayout):
	#Properties
	crime_api = None #Reference to CrimeAPI object
	gps = None #Reference to GPS object
	_use_gps = False
	address = "" #An address/location in text format
	coordinates = {} #{"Lat","Lng"} of current location
	radius = None #For SpotCrime
	in_days = None #For SpotCrime (how recent are crimes we care about)
	map_image_src = StringProperty('map.png')
	
	#Methods
	def __init__(self, address="", radius=10, in_days=2):
		super().__init__()
		self.address = address
		#self.radius = radius
		#overwriting radius to be based on the zoom level of our google map
		#zoom level 15 is roughly 22.43 miles per pixel and our map is 400x500, so the radius should be:
		self.radius = 500/22.43
		self.in_days = in_days

		#GPS functionality if applicable - mobile only (should support both iPhone and android)
		#DISABLED BECAUSE NOT IMPLEMENTED YET BY PLYER
		'''try:
			self.gps = CustomGPS(_update_location)
			self._use_gps = True
		except:
			self._use_gps = False
			print("No GPS configured, disabling GPS queries")'''
		self._use_gps = False

		#Get latitude and longitude of passed-in address
		if address != "":
			self.coordinates = get_lat_lng(address)
		#If no GPS or text address, default to CSUF
		elif not self._use_gps:
			self.coordinates["lat"] = CSUF_LAT
			self.coordinates["lng"] = CSUF_LNG
			print("Default location set to " + str(self.coordinates))
		
		self.crime_api = GetCrime(self.coordinates["lat"],self.coordinates["lng"],self.radius,in_days)
		self._update_location()
	
	#_update_location might get called by the gps (if used) or by the user typing in an address and then pressing the "Location" button
	#updates both the list of crimes and the map image
	def _update_location(self):
		#Prioritize the user's input in the text box
		if self.ids.txt_loc.text != "":
			self.coordinates = get_lat_lng(self.ids.txt_loc.text)
			self._crime_refresh()
			self._update_map()
		#Otherwise see if the gps' location has changed
		elif self._use_gps and self.coordinates == self.gps.coordinates:
			self.coordinates = self.gps.coordinates
			self_crime_refresh()
			self._update_map()
		#Otherwise assume this function was called for good reason and refresh everything anyway
		else:
			self._crime_refresh()
			self._update_map()
	#Re-Center and calculate everything based on a new position
	def _move_to(self, lat, lng):
		self.coordinates["lat"] = lat
		self.coordinates["lng"] = lng
		print("Moving to " + str(lat) + "," + str(lng))
		self._update_location()
	# Crime Refresher Function
	def _crime_refresh(self):
		self.crime_api.update_query(self.coordinates["lat"], self.coordinates["lng"], self.radius, self.in_days)
		self.all_crimes = self.crime_api.get_crimes()
		#Delete the old crimes in the GUI
		self.ids.crime_box.clear_widgets()
		#Update the GUI list of crimes
		i=0
		for crime in self.all_crimes:
			crime_button = Button(text=str(i) + ":" + crime["type"] + " at " + crime["timestamp"], font_size='12dp', size_hint=(1,self.height/len(self.all_crimes)));
			callback = lambda x,y,o:self._move_to(x, y)
			crime_button.bind(on_press = partial(callback, crime["lat"], crime["lon"]))
			i+=1
			self.ids.crime_box.add_widget(crime_button)

	# Download a new map image - might be called by the gps or by the user typing in an address
	def _update_map(self):
		print("Refreshing map!")
		pins = None
		if self.all_crimes:
			pins = []
			i=0
			for crime in self.all_crimes:
				pins.append("color:red|label:" + str(i) + "|" + str(crime["lat"]) + "," + str(crime["lon"]))
				i+=1
		get_map(pins, self.coordinates["lat"], self.coordinates["lng"])
		#Display the map in our application's GUI
		self.ids.map_image.reload()

	''' Old Jay code - pretty sure only necessary for testing
	# Removes all crime data from the list and resets the crime count
	def remove_crime_list(self):
		self.window.create_report_frame(self._crime_refresh)
		self.crime_count = 0

	# Updates the list of crimes with the given list
	def update_crimes(self, crimes_list):
		self.remove_crime_list()

		# Re-create the frame holding all the crime reports
		for crime_report in crimes_list:
			self._create_crime_frame(crime_report)

		print("Found " + str(self.crime_count) + " crimes.")
	'''