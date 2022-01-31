from os.path import isfile


def archiver(name, data, new_products):
    # transform file into a list
    old_data = []
    file_name = './info storage/' + name + '.txt'

    if not isfile(file_name):
        f = open(file_name, 'w')
        f.close()

    with open(file_name, 'r') as f:
        # site
        line1 = f.readline()
        while line1 != '':
            old_items = []
            # products
            line2 = f.readline()
            while line2 != '' and line2[0:5] == '    (':
                old_items += [line2[4:-1]]
                line2 = f.readline()
            old_data += [old_items]
            line1 = line2

    # compare the new list and the file just retrieved
    new_tot = 0
    for (site, products), old_products in zip(data, old_data):
        per_site = []
        for prod in products:
            if str(prod) not in old_products:
                per_site += [prod]
        new_tot += len(per_site)
        new_products += [(site, per_site)]

    # put new data in file
    new_data = []
    for (site, items) in data:
        new_data += [site + '\n']
        for item in items:
            new_data += ['    ' + str(item) + '\n']
    with open(file_name, 'w') as f:
        f.writelines(new_data)

    return new_tot
