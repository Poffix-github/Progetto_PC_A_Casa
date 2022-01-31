# TODO: delete notes.txt from github
from asyncio import run
from data_retirever import data_retriever
from archiver import archiver


def main():
    topics = ["", "nvidia geforce rtx ", "intel core "]
    topic = 2
    model = "i5-12"

    data = run(data_retriever(topic, model))

    new_products = []
    file_name = topics[topic] + model
    new_num = archiver(file_name, data, new_products)

    # pretty printing
    print(f"ricerca per: {file_name}\nnumero di prodotti nuovi: {new_num}")
    for (site, items) in new_products:
        if items:
            print(site + ":")
            for product in items:
                print('    ' + str(product))
            print()


if __name__ == '__main__':
    main()
