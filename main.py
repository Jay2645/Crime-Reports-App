from getcrime import GetCrime

# Create crime object, with latitude, longitude, radius, and days
# This gets all crime within 300 miles of CSUF in the past 10 days
crime_module = GetCrime(33.7214127465601, -118.00509452819823, 300, 10)
# Print all incidents
crime_module.get_crime()