from colorama import init, Fore, Back

init(autoreset=True)

def help():
    """
    Prints the available commands for the ATC tracker application.
    """

    print(f"{Back.WHITE}{Fore.BLACK} Available commands: ")
    print("├── flights - List all flights (filters available, see the documentation)")
    print("├── airport - Obtain information on a specific airport")
    print("├── track - Monitoring a flight in real time")
    print("└── about - About the project")