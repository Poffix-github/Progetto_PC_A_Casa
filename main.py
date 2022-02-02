from asyncio import run
import clerk
from data_retirever import data_retriever
from archiver import archiver


def main():
    print('Benvenuto a Progetto PC a Casa')

    cond = True
    while cond:
        command = input()
        if command == 'help' or command == 'h':
            print("'quit' or 'q':    end session\n"
                  "'new' or 'n':    search for new product")
        elif command == 'quit' or command == 'q':
            cond = False
            print("Ciao")
        elif command == 'new' or command == 'n':
            topic, model, file_name = clerk.first_contact()

            data = run(data_retriever(topic, model))

            new_products = []
            new_num = archiver(file_name, data, new_products)

            # pretty printing
            print(f"ricerca per: {file_name}\n"
                  f"numero di prodotti nuovi: {new_num}")
            for (site, items) in new_products:
                if items:
                    print(site + ":")
                    for product in items:
                        print('    ' + str(product))
                    print()
        else:
            print('unknown command')


if __name__ == '__main__':
    main()
