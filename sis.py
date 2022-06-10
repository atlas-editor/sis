import os
import sys
from cmd_loop import MainLoop
import data_access

if __name__ == '__main__':
    print('S(imple)IS 0.1\nType help for more information.')
    if not os.path.exists('data/main.db'):
        user_input = input(f'No database found, do you wish to create one (y/n)? ')
        if user_input == 'y':
            data_access.init_db()
            data_access.create_hw_table()
        else:
            sys.exit(0)
    MainLoop().start()