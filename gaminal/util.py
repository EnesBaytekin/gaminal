from os import system, name

if name == 'nt':
    def clear_terminal():
        system('cls')
else:
    def clear_terminal():
        system('clear')


def change_dir_to_main_dir():
    from sys import argv
    from os.path import dirname, abspath
    from os import chdir

    chdir(dirname(abspath(argv[0])))
