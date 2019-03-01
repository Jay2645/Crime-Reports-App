from plyer import gps

my_gps = None
my_loc = None

def start_gps_poll():
	my_gps = gps() #Plyer should wrap this to a gps handler appropriate to the operating system
	my_gps.configure(on_location=update_loc) #Configs gps object to use update_loc function as a callback
	my_gps.start(minTime=10000, minDistance=1) #Poll every 10 seconds
	
def stop_gps_poll():
	if my_gps is not None:
		my_gps.stop()
		
def update_loc(**kwargs):
	if kwargs["lat"] is not None and kwargs["lng"] is not None:
		my_loc = {"lat":kwargs["lat"],"lng":kwargs["lng"]}

def get_gps():
	return my_gps
def get_loc():
	return my_loc