from os import listdir
from asyncio import run
from os.path import isfile
from data_retirever import data_retriever
from archiver import archiver
import clerk


def main():
    print('Benvenuto a Progetto PC a Casa (digita "help" per la lista dei comandi)')

    cond = True
    while cond:
        command = input()
        # list of all commands
        if command == 'help' or command == 'h':
            print("'quit' or 'q':    end session\n"
                  "'new' or 'n':    search for new product\n"
                  "'list':    lists all files currently available\n"                  
                  "'open name_of_file':    opens the file if it exists")
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
            topic, model, file_name = clerk.first_contact()

            data = run(data_retriever(topic, model))

            new_products = []
            new_num = archiver(file_name, data, new_products)

            # new products pretty printing
            print(f"ricerca per: {file_name}\n"
                  f"numero di prodotti nuovi: {new_num}")
            for (site, items) in new_products:
                if items:
                    print(site + ":")
                    for product in items:
                        print('    ' + str(product))
                    print()
        else:
            print('comando sconosciuto')


if __name__ == '__main__':
    main()
