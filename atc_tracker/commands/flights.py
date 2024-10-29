from FlightRadar24 import FlightRadar24API
from colorama import init, Fore, Back
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta
import time
import sys
import keyboard

api = FlightRadar24API()
init(autoreset=True)

def get_eta(flight):
    R = 6371.0  # Radius of the Earth in km
    lat1 = radians(flight.latitude)
    lon1 = radians(flight.longitude)
    lat2 = radians(api.get_airport(flight.destination_airport_iata).latitude)
    lon2 = radians(api.get_airport(flight.destination_airport_iata).longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # in kilometers

    time_to_arrival = distance / flight.ground_speed  # in hours
    
    return (datetime.now() + timedelta(hours=time_to_arrival)).strftime('%H:%M')

def flights_list(filters: dict = {}):
    """
    Display the list of flights, based on a list of filters.

    :param filters: Filters list
    """
    k = 0

    print(f"{'Model':<6} {'Call Sign':<10} {'Status':<10} {'DEP-ARR':<8} {'ETA':<6} {'Altitude':<10} {'Ground Speed':<15} {'Heading':<8} {'Squawk':<7} {'Registration':<12}")
    print("=" * 6 + " " + "=" * 10 + " " + "=" * 10 + " " + "=" * 8 + " " + "=" * 6 + " " + "=" * 10 + " " + "=" * 15 + " " + "=" * 8 + " " + "=" * 7 + " " + "=" * 13)

    if filters == {}:
        zones = api.get_zones()
        for airline in api.get_airlines():
            for zone in zones.keys():
                if "subzones" in zones[zone]:
                    for subzone in zones[zone]["subzones"].keys():
                        bounds = f"{zones[zone]['subzones'][subzone]['tl_y']},{zones[zone]['subzones'][subzone]['br_y']},{zones[zone]['subzones'][subzone]['tl_x']},{zones[zone]['subzones'][subzone]['br_x']}"
                else:
                    bounds = f"{zones[zone]['tl_y']},{zones[zone]['br_y']},{zones[zone]['tl_x']},{zones[zone]['br_x']}"

                for flight in list(api.get_flights(bounds=bounds, airline=airline['ICAO'])):
                    model = flight.aircraft_code
                    call_sign = flight.callsign
                    status = "On ground" if flight.on_ground else "In flight"
                    departure = flight.origin_airport_iata if not str(flight.origin_airport_iata) == "" else "---"
                    arrival = flight.destination_airport_iata if not str(flight.destination_airport_iata) == "" else "---"
                    altitude = flight.altitude
                    speed = flight.ground_speed
                    heading = flight.heading
                    squawk = flight.squawk
                    registration = flight.registration
                    
                    try:
                        eta = get_eta(flight)
                    except:
                        eta = "--:--"

                    print(f"{Fore.RED if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''}{model:<6} {call_sign:<10} {status:<10} {departure}-{arrival:<4} {eta:<6} {altitude:<10} {speed:<15} {heading:<8} {Back.WHITE if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''}{squawk:<7}{Back.RESET if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''} {registration:<12}")

                    k += 1
    else:
        if isinstance(filters.get("airline"), str):
            airlines = [filters.get("airline")]
        elif isinstance(filters.get("airline"), list):
            airlines = filters.get("airline")
        else:
            airlines = []
        
        if isinstance(filters.get("registration"), str):
            registrations = [filters.get("registration")]
        elif isinstance(filters.get("registration"), list):
            registrations = filters.get("registration")
        else:
            registrations = []

        if isinstance(filters.get("aircraft_type"), str):
            aircrafttype = [filters.get("aircraft_type")]
        elif isinstance(filters.get("aircraft_type"), list):
            aircrafttype = filters.get("aircraft_type")
        else:
            aircrafttype = []

        for airline in airlines if airlines else [None]:
            for registration in registrations if registrations else [None]:
                for type in aircrafttype if aircrafttype else [None]:
                    for flight in list(api.get_flights(airline=airline, bounds=filters.get("bounds"), registration=registration, aircraft_type=type)):
                        if not keyboard.is_pressed('q'):
                            model = flight.aircraft_code
                            call_sign = flight.callsign
                            status = "On ground" if flight.on_ground else "In flight"
                            departure = flight.origin_airport_iata if not str(flight.origin_airport_iata) == "" else "---"
                            arrival = flight.destination_airport_iata if not str(flight.destination_airport_iata) == "" else "---"
                            altitude = flight.altitude
                            speed = flight.ground_speed
                            heading = flight.heading
                            squawk = flight.squawk
                            registration = flight.registration

                            try:
                                eta = get_eta(flight)
                            except:
                                eta = "--:--"

                            print(f"{Fore.RED if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''}{model:<6} {call_sign:<10} {status:<10} {departure}-{arrival:<4} {eta:<6} {altitude:<10} {speed:<15} {heading:<8} {Back.WHITE if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''}{squawk:<7}{Back.RESET if str(squawk)[0:4] in ['7500', '7600', '7700'] else ''} {registration:<12}")

                            k += 1
                        else:
                            print(f"\n{Fore.YELLOW}[!] Stopped by user.")
                            sys.exit(1)
            
    print(f"\n{Fore.BLUE}[i] {k} flights were listed.")