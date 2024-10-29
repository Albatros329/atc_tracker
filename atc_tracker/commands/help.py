from colorama import init, Fore, Back

init(autoreset=True)

def help():
    print(f"{Back.WHITE}{Fore.BLACK} Available commands: ")
    print("├── flights - List all flights (filters available, see the documentation)")
    print("├── airport - Obtain information on a specific airport")
    print("└── about - About the project")