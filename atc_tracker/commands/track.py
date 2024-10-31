from colorama import init, Fore, Back, Style
from FlightRadar24 import FlightRadar24API
from pynput import keyboard
import time
from datetime import datetime

api = FlightRadar24API()
init(autoreset=True)

q_pressed = False

def on_press(key):
    global q_pressed
    try:
        if key.char == 'q':  # Vérifie si la touche 'q' est pressée
            q_pressed = True
    except AttributeError:
        pass

def start_listener():
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

start_listener()

def track_flight(registration: str = None):
    """
    Tracks the flight information for a given aircraft registration.
    This function continuously fetches and displays real-time flight data for an aircraft
    identified by its registration number. The data includes flight status, altitude, 
    ground speed, vertical speed, heading, squawk code, departure and destination airports, 
    and estimated arrival times. The function updates the information every 3 seconds until 
    the 'q' key is pressed.
    Args:
        registration (str, optional): The registration number of the aircraft to track. 
                                      Defaults to None.
    Displays:
        - Flight Information: Callsign, Airline, Aircraft Model, Registration.
        - Flight Status: Status, Latitude, Longitude, Altitude, Ground Speed, Vertical Speed, 
                         Heading, ICAO 24bit Address, Squawk.
        - Route Information: Departure Airport, Destination Airport, Scheduled Departure Time, 
                             Real Departure Time, Scheduled Arrival Time, Estimated Arrival Time.
        - Flight Progress: A progress bar indicating the percentage of the flight completed.
    Notes:
        - The function will print an error message if the flight does not exist or has not 
          switched on its transponder.
        - The function uses ANSI escape codes to clear the terminal screen and update the 
          displayed information.
    """

    altitude_last = 0
    ground_speed_last = 0

    if not len(api.get_flights(registration=registration)) == 0:
        while not q_pressed:
            flight_data = api.get_flights(registration=registration)[0]
            flight_details = api.get_flight_details(flight_data)
            
            callsign = flight_data.callsign
            airline = flight_details["airline"]["name"] if flight_details["airline"]["name"] != None else ""
            aircraft_model = f'{flight_details["aircraft"]["model"]["text"]} ({flight_details["aircraft"]["model"]["code"]})' if flight_details["aircraft"]["model"]["text"] != None else ""
            registration = flight_data.registration
            status = 'In flight' if flight_details['status']['live'] else 'On ground'

            if int(flight_data.altitude) > altitude_last:
                altitude = f"{flight_data.altitude} ft {Style.BRIGHT}⇗{Style.RESET_ALL}"
            elif int(flight_data.altitude) < altitude_last:
                altitude = f"{flight_data.altitude} ft {Style.BRIGHT}⇘{Style.RESET_ALL}"
            elif int(flight_data.altitude) == altitude_last:
                altitude = f"{flight_data.altitude} ft {Style.BRIGHT}⇒{Style.RESET_ALL}"

            if int(flight_data.ground_speed) > ground_speed_last:
                ground_speed = f"{flight_data.ground_speed} kts {Style.BRIGHT}⇗{Style.RESET_ALL}"
            elif int(flight_data.ground_speed) < ground_speed_last:
                ground_speed = f"{flight_data.ground_speed} kts {Style.BRIGHT}⇘{Style.RESET_ALL}"
            elif int(flight_data.ground_speed) == ground_speed_last:
                ground_speed = f"{flight_data.ground_speed} kts {Style.BRIGHT}⇒{Style.RESET_ALL}"
            
            vertical_speed = f"{flight_data.vertical_speed} fpm"
            heading = flight_data.heading
            squawk = flight_data.squawk

            departure_airport = f'{flight_data.origin_airport_iata} ({flight_details["airport"]["origin"]["name"]})' if flight_data.origin_airport_iata else "N/A"
            destination_airport = f'{flight_data.destination_airport_iata} ({flight_details["airport"]["destination"]["name"]})' if flight_data.destination_airport_iata else "N/A"
            scheduled_departure = datetime.utcfromtimestamp(flight_details['time']['scheduled']['departure']).strftime('%Y-%m-%d %H:%M UTC') if flight_details['time']['scheduled']['departure'] and flight_details['time']['scheduled']['departure'] != 0 else ""
            real_departure_time = datetime.utcfromtimestamp(flight_details['time']['real']['departure']).strftime('%Y-%m-%d %H:%M UTC') if flight_details['time']['real']['departure'] and flight_details['time']['real']['departure'] != 0 else ""
            scheduled_arrival = datetime.utcfromtimestamp(flight_details['time']['scheduled']['arrival']).strftime('%Y-%m-%d %H:%M UTC') if flight_details['time']['scheduled']['arrival'] and flight_details['time']['scheduled']['arrival'] != 0 else ""
            estimated_arrival = datetime.utcfromtimestamp(flight_details['time']['estimated']['arrival']).strftime('%Y-%m-%d %H:%M UTC') if flight_details['time']['estimated']['arrival'] and flight_details['time']['estimated']['arrival'] != 0 else ""



            print("\033[2J\033[H", end="")

            print(f"{'Flight Information':<18}")
            print("="*19)

            print(f"""{'Callsign:':<26} {callsign:<10}
{'Airline:':<26} {airline:<20}
{'Aircraft Model:':<26} {aircraft_model:<80}
{'Registration:':<26} {registration:<20}
        """)
            
            print(f"{'Flight Status':<13}")
            print("="*14)

            print(f"""{'Status:':<26} {status:<10}
{'Latitude:':<26} {flight_data.latitude:<20}
{'Longitude:':<26} {flight_data.longitude:<20}
{'Altitude:':<26} {altitude:<20}
{'Ground Speed:':<26} {ground_speed:<20}
{'Vertical Speed:':<26} {vertical_speed:<20}
{'Heading:':<26} {str(heading)+"°":<20}
{'ICAO 24bit Address:':<26} {flight_data.icao_24bit:<20}
{'Squawk:':<26} {squawk:<20}
        """)

            print(f"{'Route Information':<17}")
            print("="*18)

            print(f"""{'Departure Airport:':<26} {departure_airport:<80}
{'Destination Airport:':<26} {destination_airport:<80}
{'Scheduled Departure Time:':<26} {scheduled_departure:<20}
{'Real Departure Time:':<26} {real_departure_time:<20}
{'Scheduled Arrival Time:':<26} {scheduled_arrival:<20}
{'Estimated Arrival Time:':<26} {estimated_arrival:<20}
        """)
            
            if flight_details['time']['real']['departure'] and flight_details['time']['estimated']['arrival']:
                total_flight_time = flight_details['time']['estimated']['arrival'] - flight_details['time']['real']['departure']
                elapsed_time = time.time() - flight_details['time']['real']['departure']
                progress = (elapsed_time / total_flight_time) * 100

                bar_length = 40
                filled_length = int(bar_length * progress // 100)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f"{'Flight Progress:':<26} |{bar}| {progress:.2f}%")
            else:
                progress = 0

            altitude_last = flight_data.altitude
            ground_speed_last = flight_data.ground_speed
            time.sleep(3)
    else:
        print(f"{Fore.RED}[!] This flight does not exist or has not switched on its transponder.")