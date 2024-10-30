from colorama import init, Fore, Back, Style
from FlightRadar24 import FlightRadar24API
import keyboard
import time
from datetime import datetime

api = FlightRadar24API()
init(autoreset=True)

def track_flight(registration: str = None):
    altitude_last = 0
    ground_speed_last = 0

    while not keyboard.is_pressed("q"):
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