# Rote - a tiny python library for writing human in the loop apps

Write apps that require human input, and are failsafe with the data
being processed.

## Example

```
from rote import Rote
import json

app = Rote()

names = [
    'Jeremy',
    'Erin',
    'Tyrone',
    'Cthulhu',
]  # more realistically, import from a file


@app.setup
def setup():
    try:
        with open('labels.json', 'r') as infile:
            data = json.load(infile)
    except:
        data = {
            'female': [],
            'male': [],
            'other': [],
        }

    print("Classify the following names as male, female, or don't know:\n\n")
    return data


@app.newdata
def newdata(existing_data):
    all_names = set(x for k in existing_data for x in existing_data[k])
    return [x for x in names if x not in all_names]


@app.teardown
def write(data):
    with open('labels.json', 'w') as outfile:
        outfile.write(json.dumps(data))


@app.foreach
def process(item, data):
    print('Name: ' + item)
    choice = input("male, female, or other? (m/f/o) ")
    choice = (choice or 'o')[0].lower()

    subset = data['other']
    if choice == 'm':
        subset = data['male']
    elif choice == 'f':
        subset = data['female']

    subset.append(item)


app.run()
```


Output:

```
Classify the following names as male, female, or don't know:


Name: Jeremy
male, female, or other? (m/f/o) m
Name: Erin
male, female, or other? (m/f/o) f
Name: Tyrone
male, female, or other? (m/f/o) ^C

Quitting after teardown...
```

Partial results are handled by `teardown`, skipped by filtering in `newdata`.
