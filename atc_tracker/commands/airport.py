from FlightRadar24 import FlightRadar24API
from colorama import init, Fore, Back
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import time
import sys
import keyboard
from datetime import datetime
import pytz

api = FlightRadar24API()
init(autoreset=True)

def airport_details(airport_iata_icao: str = None):
    try:
        airport = api.get_airport(airport_iata_icao)
        airport.set_airport_details(api.get_airport_details(airport_iata_icao))
    except ValueError:
        print(f"{Fore.RED}[!] Invalid code")
        sys.exit(1)

    print("-"*int(len(airport.name))+"-"*int(len(airport.name)/3)+"-"*int(len(airport.name)/3))
    print(int(len(airport.name)/3)*" " + f"{airport.name}")
    print("-"*int(len(airport.name))+"-"*int(len(airport.name)/3)+"-"*int(len(airport.name)/3))

    print(f"""IATA/ICAO code: {airport.iata}/{airport.icao}
City: {airport.city}
Country: {airport.country}
Time zone: {airport.timezone_abbr} (UTC {airport.timezone_offset_hours if "-" in airport.timezone_offset_hours else "+"+airport.timezone_offset_hours})
Local time: {datetime.now(pytz.timezone(airport.timezone_name)).strftime("%Y-%m-%d %H:%M:%S")}
Elevation: {airport.altitude}ft
Latitude: {airport.latitude}
Longitude: {airport.longitude}
Runways: {len(airport.runways)}
Rating: {airport.average_rating} {Fore.YELLOW}★{Fore.RESET} ({airport.total_rating} ratings)
Website: {airport.website}
Wikipedia: {airport.wikipedia}
Weather: 
    - Temperature: {airport.weather["temp"]["celsius"]}°C / {airport.weather["temp"]["fahrenheit"]}°F
    - Sky condition: {airport.weather["sky"]["condition"]["text"]}
    - Visibility: {airport.weather["sky"]["visibility"]["mi"]}mi
    - Wind: {airport.weather["wind"]["direction"]["degree"]}° ({airport.weather["wind"]["direction"]["text"]}) / Speed: {airport.weather["wind"]["speed"]["kts"]}kts
    - Metar: {airport.weather["metar"]}
""")
    print(f"{Back.WHITE}{Fore.BLACK}                          Runways details                           ")
    print(f"{'Name/number':<15} {'Length':<20} {'Surface':<30}")
    print("=" * 15 + " " + "=" * 20 + " " + "=" * 30 + " ")

    for runway in airport.runways:
        print(f"""{runway['name']:<15} {f"{runway['length']['ft']}ft/{runway['length']['m']}m":<20} {f"{runway['surface']['name']} ({runway['surface']['code']})":<30}""")

    print(f"\n{Back.WHITE}{Fore.BLACK}                             Departures                             ")
    print(f"{'Flight Number':<14} {'Callsign':<10} {'Airline code':<12} {'Destination':<13} {'ETD (Local)':<12} {'Status':<22} {'Model':<6} {'Registration':<13} {'Gate':<7}")
    print("=" * 14 + " " + "=" * 10 + " " + "=" * 12 + " " + "=" * 13 + " " + "=" * 12 + " " + "=" * 22 + " " + "=" * 6 + " " + "=" * 13 + " " + "=" * 7)

    for departure in airport.departures["data"]:
        flight_number = departure["flight"]["identification"]["number"]["default"] if departure["flight"]["identification"]["number"]["default"] != None else ""
        callsign = departure["flight"]["identification"]["callsign"] if departure["flight"]["identification"]["callsign"] != None else ""
        airline = "" if departure["flight"]["airline"] == None else f"""{departure["flight"]["airline"]["code"]["iata"]}/{departure["flight"]["airline"]["code"]["icao"]}"""
        destination = f"""{departure["flight"]["airport"]["destination"]["code"]["iata"]}/{departure["flight"]["airport"]["destination"]["code"]["icao"]}"""
        etd = datetime.fromtimestamp(departure["flight"]["time"]["scheduled"]["departure"]).strftime("%m/%d %H:%M")
        status = departure["flight"]["status"]["text"]
        model = departure["flight"]["aircraft"]["model"]["code"]
        registration = departure["flight"]["aircraft"]["registration"]
        terminal = "" if departure["flight"]["airport"]["origin"]["info"]["terminal"] == None else "T"+departure["flight"]["airport"]["origin"]["info"]["terminal"]+"-"
        gate = "" if departure["flight"]["airport"]["origin"]["info"]["gate"] == None else departure["flight"]["airport"]["origin"]["info"]["gate"]


        print(f"""{flight_number:<14} {callsign:<10} {airline:<12} {destination:<13} {etd:<12} {status:<22} {model:<6} {registration:<13} {f"{terminal}{gate}":<7}""")

    print(f"\n{Back.WHITE}{Fore.BLACK}                              Arrivals                              ")
    print(f"{'Flight Number':<14} {'Callsign':<10} {'Airline code':<12} {'Origin':<13} {'ETA (Local)':<12} {'Status':<22} {'Model':<6} {'Registration':<13} {'Gate':<7}")
    print("=" * 14 + " " + "=" * 10 + " " + "=" * 12 + " " + "=" * 13 + " " + "=" * 12 + " " + "=" * 22 + " " + "=" * 6 + " " + "=" * 13 + " " + "=" * 7)

    for departure in airport.arrivals["data"]:
        flight_number = departure["flight"]["identification"]["number"]["default"] if departure["flight"]["identification"]["number"]["default"] != None else ""
        callsign = departure["flight"]["identification"]["callsign"] if departure["flight"]["identification"]["callsign"] != None else ""
        airline = "" if departure["flight"]["airline"] == None else f"""{departure["flight"]["airline"]["code"]["iata"]}/{departure["flight"]["airline"]["code"]["icao"]}"""
        origin = f"""{departure["flight"]["airport"]["origin"]["code"]["iata"]}/{departure["flight"]["airport"]["origin"]["code"]["icao"]}"""
        eta = datetime.fromtimestamp(departure["flight"]["time"]["scheduled"]["arrival"]).strftime("%m/%d %H:%M")
        status = departure["flight"]["status"]["text"]
        model = departure["flight"]["aircraft"]["model"]["code"]
        registration = departure["flight"]["aircraft"]["registration"]
        terminal = "" if departure["flight"]["airport"]["destination"]["info"]["terminal"] == None else "T"+departure["flight"]["airport"]["destination"]["info"]["terminal"]+"-"
        gate = "" if departure["flight"]["airport"]["destination"]["info"]["gate"] == None else departure["flight"]["airport"]["destination"]["info"]["gate"]


        print(f"""{flight_number:<14} {callsign:<10} {airline:<12} {origin:<13} {eta:<12} {status:<22} {model:<6} {registration:<13} {f"{terminal}{gate}":<7}""")
