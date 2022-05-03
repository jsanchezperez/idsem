"""
  Invoice JSON Token Generator
"""
import json

def create(input_fn, output_fn):
    """ ... """
    with open(input_fn, encoding="utf-8") as ifn:
        data = json.load(ifn)

    for key, value in data.items():
        data[key] = '#' + str(key) + ' ' + str(value) + ' #' + str(key)

    with open(output_fn, 'w', encoding="utf-8") as ofn:
        json.dump(data, ofn, ensure_ascii=False)
