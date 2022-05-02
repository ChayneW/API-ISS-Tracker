import requests
from datetime import datetime
import smtplib

MY_LAT = # int your location lat
MY_LONG = #int your location long

'''Function to track ISS through ISS API:
  - Parse through JSON data to locate ISS Lat and Long, then convert data into a float for accurate positioning.
  - Conditional statement to compare ISS location to user's location. 
  - Function return's True of False.
  '''
def iss_overhead():

# ISS Data:
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
# print(response)

    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_longitude = float(iss_data['iss_position']['longitude'])
    iss_latitude = float(iss_data['iss_position']['latitude'])
    
    iss_position = (iss_longitude, iss_latitude)
    print(f"the ISS is at: {iss_position}")

    # Your position is within +5/-5 degrees of iss position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

      
'''Function that tracks daylight through a sunrise/sunset website API:
  - Parse through JSON data from API request to retreive sunrise/sunset time.
  - Format then assign variables to check user's location based on API to see if daylight or night time. 
  - Function return's True or False. 
  '''      
def is_night():

    parameters = {
        # "lat": MY_LAT,
        # "lng": MY_LONG,
        "formatted": 0, # used to change time to universal time
    }
    # Sun Data:

    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    # print(response)
    sun_data = sun_response.json()
    # print(data)

    # Returns same result as previous changes
    sunrise = int(sun_data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(sun_data['results']['sunset'].split('T')[1].split(':')[0])

    print(f"sunrise is at {sunrise} am")
    print(f"sunset is at {sunset} pm")

    time_now = datetime.now().hour
    print(time_now)

    if time_now >= sunset or time_now <= sunrise:
        return True

'''MAIN PROGRAM STARTS HERE:
  - Ties both functions: 'is_overhead()' and 'is_night' to check if the current conditions are met for you to optimally see the ISS.
  - Uses SMTPLIB module to allow email to be sent on status of ISS if near location.
  '''
if iss_overhead() and is_night():
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        MY_EMAIL = 'YOUR EMAIL'
        PASSWORD = 'YOUR EMAIL PASSWORD'
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg='Subject: LOOK UP!\n\n ISS is above you!!')
