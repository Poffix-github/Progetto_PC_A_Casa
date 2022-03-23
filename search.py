from asyncio import run

import archiver
import data_retriever


def search(lock, topic, model, full_name, path):
    data = run(data_retriever.data_retriever(topic, model))

    lock.acquire()
    try:
        new_products = []
        # save products on file
        new_num = archiver.products_dump(full_name, data, new_products)

        # save search on log file
        archiver.add(model, topic, path)

        # new products pretty printing
        print(f"ricerca per: {full_name}\n"
              f"numero di prodotti nuovi: {new_num}")
        for (site, items) in new_products:
            if items:
                print(site + ":")
                for product in items:
                    print('    ' + str(product))
                print()
    finally:
        lock.release()
