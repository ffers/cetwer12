import json

def load_processed():
    try:
        with open("reg_ref_list.json", "r") as file:
            return list(json.load(file))
    except FileNotFoundError:
        return list()

def list_f():
    data = []
    refs = load_processed()
    refs_all = ''.join(refs)
    print(refs_all)

list_f()