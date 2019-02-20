#!/usr/bin/env python3
from io import BytesIO
from PIL import Image
#import plyer #use this to get gps coords later
import requests

#Returns a static image
def getMap(lat=0,lng=0,zoom=16,width=400,height=500):
    with open("google_maps_api_key.txt", "r") as fh:
        api_key = fh.readline()
        fh.close()
        params = {}
        params["key"]=api_key
        params["center"]=f"{lat},{lng}"
        params["zoom"]=zoom
        params["size"]=f"{width}x{height}"
        '''todo: can add "markers" separated by pipes to params to add typical google teardrop markers to the map. Consider doing this for the crime spots'''
        return BytesIO(requests.get("https://maps.googleapis.com/maps/api/staticmap", params=params).content)

if __name__ == "__main__":
    map_img = Image.open(getMap(33.8813416,-117.8866257,15))
    map_img.show()
    
