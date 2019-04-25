# Import Kivy stuff
from kivy.app import App
from kivy.uix.button import *
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.loader import Loader

# Import GPS stuff
from plyer import gps

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
        return FloatLayout()

class CrimeUI(Widget):
    def __init__(self, address="", radius=10, in_days=2):
        super().__init__()
        self.address = address
        self.crime_radius = radius
        self.crime_days_filter = in_days
        self.crime_count = 0

        self.crime_api = GetCrime()

        # GPS functionality if applicable - mobile only (should support both iPhone and android)
        print("TEST TEST TEST")
        try:
            gps.configure(on_location=self._update_loc)  # Configs gps object to use update_loc function as a callback
            gps.start(minTime=10000, minDistance=1)  # Poll every 10 seconds
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
                self.my_loc["lat"] = CSUF_LAT
                self.my_loc["lng"] = CSUF_LNG
                print("Not using GPS, default location set to " + str(self.my_loc))

    # GPS Update Callback
    def _update_loc(self, **kwargs):
        if not self.use_gps:
            return
        if kwargs["lat"] is not None and kwargs["lng"] is not None:
            self._create_map_image({"lat": kwargs["lat"], "lng": kwargs["lng"]})

    # Crime Refresher Function
    def _crime_refresh(self, source_button=None):
        self.crime_api.update_query(self.my_loc["lat"], self.my_loc["lng"], self.crime_radius, self.crime_days_filter)
        all_crimes = self.crime_api.get_crimes()
        self.update_crimes(all_crimes)

    # Location Button callback to download a new map
    def _refresh_map(self, source_button=None):
        print("Refreshing map!")
        try:
            self.address = self.window.get_current_address()
        except NameError:
            # Use cached location
            pass

        if self.address == "":
            new_loc = self.my_loc
        else:
            new_loc = get_lat_lng(self.address)

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
