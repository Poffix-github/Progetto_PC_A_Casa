from os import listdir
from os.path import isfile
import clerk
import search
from utilities import json_opener, get_full_name

# GLOBAL VARIABLES
search_data_path = './data/search_data.json'
search_log_path = './data/search_log.json'


def main():
    print('Benvenuto a Progetto PC a Casa (digita "help" per la lista dei comandi)')

    cond = True
    while cond:
        command = input()
        # list of all commands
        if command == 'help' or command == 'h':
            print("'quit' or 'q':          end session\n"
                  "'new' or 'n':           search for new product\n"
                  "'list':                 lists all files currently available\n"                  
                  "'open name_of_file':    opens the file if it exists\n"
                  "'src all':              launches all searches ever done")
        # end of session
        elif command == 'quit' or command == 'q':
            cond = False
            print("Ciao ( ´ ▽ ` )/")
        # lists all files currently available
        elif command == 'list':
            for f in listdir('./info storage/'):
                print(f)
        # opens the file if it exists
        elif command[0:5] == 'open ':
            file = './info storage/'+command[5:]+'.txt'
            if isfile(file):
                with open(file, 'r') as f:
                    print(f.read())
        elif command == 'new' or command == 'n':
            topic, model, full_name = clerk.first_contact(search_data_path)
            search.search(topic, model, full_name, search_log_path)
        elif command == 'src all':
            searches = json_opener.read(search_log_path)

            for key in searches:
                full_name = get_full_name.full_name(search_data_path, key, searches[key])
                search.search(searches[key], key, full_name, search_log_path)
            print("All done! (◕‿◕)")
        else:
            print('comando sconosciuto')


if __name__ == '__main__':
    main()
