from os import system, name

if name == 'nt':
    def clear_terminal():
        system('cls')
else:
    def clear_terminal():
        system('clear')

