#!/usr/bin/env python3
import json
from io import BytesIO
from tkinter import PhotoImage
#import plyer #use this to get gps coords later
import requests

#Downloads a static png of the map with the given parameters. Returns true or false based on success
def getMap(lat=0,lng=0,zoom=16,width=400,height=500,format='png'):
	with open("google_maps_api_key.txt", "r") as fh:
		api_key = fh.readline()
		fh.close()
		params = {}
		params["key"]=api_key
		params["center"]=f"{lat},{lng}"
		params["zoom"]=zoom
		params["size"]=f"{width}x{height}"
		params["format"]=format
		'''note: can add "markers" separated by pipes to params to add typical google teardrop markers to the map. Consider doing this for the crime spots'''
		res = requests.get("https://maps.googleapis.com/maps/api/staticmap", params=params)
		with open("map." + format, "wb") as fh:
			fh.write(res.content)
			fh.close()
			return True
		#return PhotoImage(res.content)
	return False
	
def get_lat_lng(address):
	with open("google_maps_api_key.txt", "r") as fh:
		api_key = fh.readline()
		fh.close()
		params = {}
		params["address"]=address
		params["key"]=api_key
		res = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
		res = json.loads(res.text)
		try:
			return {"lat":res["results"][0]["geometry"]["location"]["lat"],"lng":res["results"][0]["geometry"]["location"]["lng"]}
		except:
			return None

#if __name__ == "__main__":
	#map_img = Image.open(getMap(33.8813416,-117.8866257,15))
	#map_img.show()
	#getMap(33.8813416,-117.8866257,15)
	