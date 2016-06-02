from itertools import cycle
import random

def make_rotator(data):
    # Shuffle
    random.shuffle(data)

    # Cycled iterator
    return cycle(data)

def read_file(filename):
    data = []

    with open(filename, 'rb') as f:
        for line in f.readlines():
            if line:
                data += line.strip()

    return data
