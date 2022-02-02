from utilities.json_opener import read


def first_contact():
    presets = read('./data/search_data.json')['topics']

    keys = []
    while True:
        print("scegli una categoria di ricerca scrivendo il numero corrispondente:")
        for i, pre in enumerate(presets):
            keys.append(pre)
            print(f"{i + 1}) {pre}")

        selection = int(input())-1
        if 0 <= selection < len(presets):
            break
        else:
            print('Input errato, riprova')

    print("Scrivi il modello che vuoi cercare: ")
    model = str(input())

    return selection, model, presets[keys[selection]]+model
