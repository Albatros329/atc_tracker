import sys
from colorama import init, Fore, Back
from atc_tracker.commands import *
from .utils import *

init(autoreset=True)

available_filters = ["airline", "bounds", "registration", "aircraft_type"]

start_color = (0, 100, 255)
end_color = (0, 255, 100)

def main():
    text = r"""
           __          __               __          
     ___ _/ /_____    / /________ _____/ /_____ ____
    / _ `/ __/ __/   / __/ __/ _ `/ __/  '_/ -_) __/
    \_,_/\__/\__/    \__/_/  \_,_/\__/_/\_\\__/_/   
                /___/                              

       The Air traffic Control in your terminal
    """

    for line in text.splitlines():
        print(gradient_text(line, start_color, end_color))

    # Check the command and parameters
    if len(sys.argv) < 2:
        help()
    elif sys.argv[1] == "flights":
        if len(sys.argv) > 2:
            filters = {}
            for filter in sys.argv[2:len(sys.argv)]:
                if not filter.startswith("--") or len(filter.split("=")) != 2 or "\"" in filter or "'" in filter or filter.split("=")[1] == "" or not str(filter.split("=")[0])[2:] in available_filters:
                    print(f"{Fore.RED}[!] Invalid filter or filter is not available.")
                    sys.exit(1)
                elif str(filter.split("=")[0][2:]) in list(filters.keys()):
                    if not str(filter.split("=")[0][2:]) in ["airline", "registration", "aircraft_type"]:
                        print(f"{Fore.RED}[!] The \"{filter.split('=')[0]}\" filter cannot be used more than once.")
                        sys.exit(1)
                    else:
                        if not filters.get(str(filter.split("=")[0])[2:]) == str(filter.split("=")[1]):
                            filters[str(filter.split("=")[0])[2:]] = [filters.get(str(filter.split("=")[0])[2:])]
                            filters[str(filter.split("=")[0])[2:]].append(str(filter.split("=")[1]))
                else:
                    filters[str(filter.split("=")[0])[2:]] = str(filter.split("=")[1])
            print(f"{Fore.BLUE}{Back.WHITE}[tip] Hold down the q key to stop the program.{Back.RESET}\n")
            flights_list(filters=filters)
        elif len(sys.argv) == 2:
            print(f"{Fore.YELLOW}Recovering all the flights could take a long time (up to 8 minutes), so we recommend that you use the filters.\n")
            flights_list(filters={})
        else:
            print(f"{Fore.RED}[!] Invalid arguments")
            sys.exit(1)
    elif sys.argv[1] == "airport":
        if len(sys.argv) == 3:
            airport_details(sys.argv[2])
        else:
            print(f"{Fore.RED}[!] Invalid arguments")
            sys.exit(1)
    elif sys.argv[1] == "track":
        if len(sys.argv) == 3:
            print(f"{Fore.BLUE}{Back.WHITE}[tip] Hold down the q key to stop the program.{Back.RESET}\n")
            track_flight(sys.argv[2])
        else:
            print(f"{Fore.RED}[!] Invalid arguments")
            sys.exit(1)
    elif sys.argv[1] == "about":
        about()
    elif sys.argv[1] == "help":
        help()
    else:
        print(f"{Fore.RED}[!] Unknown command: {sys.argv[1]}\n")
        help()
        sys.exit(1)

if __name__ == "__main__":
    main()
