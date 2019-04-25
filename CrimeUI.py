# Import Kivy stuff
from kivy.app import App
from kivy.uix.button import *
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.loader import Loader

# Import GPS stuff
from gps import GPS

# Import APIs
from CrimeAPI import GetCrime
from googlemap_utils import get_map, get_lat_lng

#import os

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

'''		if my_loc is not None:
			if get_map(my_loc["lat"], my_loc["lng"], zoom=15, width=MAP_WIDTH, height=MAP_HEIGHT, format=MAP_EXTENSION):
				image_path = "../" + MAP_FILENAME + "." + MAP_EXTENSION
				self.map_image = toga.Image(image_path)
				self.map_view.image = self.map_image
				print("Updating image at " + str(my_loc) + " using image at " + image_path)
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
	def _gps = None #GPS object
	def _use_gps = False
	def address #An address/location in text format
	def coordinates = {} #{"Lat","Lng"} of current location
	def radius #For SpotCrime
	def in_days #For SpotCrime (how recent are crimes we care about)
	
	#Methods
	def __init__(self, address="", radius=10, in_days=2):
		super().__init__()
		self.address = address

		# GPS functionality if applicable - mobile only (should support both iPhone and android)
		try:
			self._gps = GPS(_update_location)
			self.use_gps = True
		except:
			self._use_gps = False
			print("No GPS configured, disabling GPS queries")

		# Get latitude and longitude of passed-in address
		if address != "":
			self.coordinates = get_lat_lng(address)
		else if not self._use_gps:
			# If no GPS or text address, default to CSUF
			self.coordinates["lat"] = CSUF_LAT
			self.coordinates["lng"] = CSUF_LNG
			print("Default location set to " + str(self.my_loc))
				
		self.crime_api = GetCrime(self.coordinates["lat"], self.coordinates["lng"], radius, in_days)
		
	#_update_location will get called by the gps (if used) and update the list of crimes and the map image
	def _update_location(self):
		#if an address has been typed in the text box, however, then don't update
		if self.ids.txt_loc != "":
			_crime_refresh()
			_update_map()
			
	# Crime Refresher Function
	def _crime_refresh(self):
		self.crime_api.update_query(self.my_loc["lat"], self.my_loc["lng"], self.crime_radius, self.crime_days_filter)
		all_crimes = self.crime_api.get_crimes()
		self.update_crimes(all_crimes)

	# Location Button callback to download a new map
	def _update_map(self, location):
		print("Refreshing map!")
		if(location != "")
		self.window.create_map_image(new_loc)
		self._crime_refresh()

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
