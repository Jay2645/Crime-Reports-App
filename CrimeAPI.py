import datetime
from spotcrime import SpotCrime

class GetCrime(object):
    def __init__(self, latitude = 33.7214127465601, longitude = -118.00509452819823, radius_miles = 10, in_days = 1):
        # API request type:
        #http://api.spotcrime.com/crimes.json?lat=33.7214127465601&lon=-118.00509452819823&radius=200&callback=?&key=This-api-key-is-for-commercial-use-exclusively.Only-entities-with-a-Spotcrime-contract-May-use-this-key.Call-877.410.1607.
        self.api = "This-api-key-is-for-commercial-use-exclusively.Only-entities-with-a-Spotcrime-contract-May-use-this-key.Call-877.410.1607."
        self.update_query(latitude, longitude, radius_miles, in_days)

    def update_query(self, latitude, longitude, radius_miles, in_days):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius_miles/100 #Python-spotcrime's radius conversion: 1 mile = 0.01
        self.in_days = in_days

    def get_crimes(self):
        sc = SpotCrime((self.latitude, self.longitude), self.radius, None, ['Other'], self.api, days=self.in_days)
        return sc.get_incidents()