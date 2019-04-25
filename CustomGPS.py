from plyer import gps

#A wrapper for plyer's global gps object - plyer should pick a proxy appropriate to the operating system
class CustomGPS():
	coordinates = None
	_callback = None

	#This wrapper allows us to add an additional callback from other scripts
	def __init__(self, callback=None, minTime=10000, minDistance=1):
		gps.configure(on_location=self.update_loc) #Configs gps object to use update_loc function as a callback
		gps.start(minTime, minDistance) #Polls every 10 seconds by default
		self._callback = callback #Allows an additional custom function besides plyers default callback
		
	def update_loc(self, **kwargs):
		if kwargs["lat"] is not None and kwargs["lng"] is not None:
			self.coordinates = {"lat":kwargs["lat"],"lng":kwargs["lng"]}
		if self._callback is not None: self._callback()
		
	#Get plyer's gps object for whatever reason
	def get_gps(): return gps
