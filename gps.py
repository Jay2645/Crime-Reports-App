from plyer import gps

class GPS(gps):
	_coordinates = None
	_callback = None

	def _init_(self, callback, minTime=10000, minDistance=1):
		super()._init_() #Plyer should wrap this to a gps handler appropriate to the operating system
		self.configure(on_location=update_loc) #Configs gps object to use update_loc function as a callback
		self.start(minTime, minDistance) #Polls every 10 seconds by default
		self._callback = callback #Allows an additional custom function besides plyers default callback
		
	def update_loc(self, **kwargs):
		if kwargs["lat"] is not None and kwargs["lng"] is not None:
			_self._coordinates = {"lat":kwargs["lat"],"lng":kwargs["lng"]}
		if self._callback is not None: self._callback()
