import pickle
import ast
from StallModule import Stall

with open('stall.txt', 'r') as data:
    with open('stall', 'wb') as f:
        lines = data.readlines()

        for line in lines:
            # split based on '/' which separates each piece of information when we saved it
            line = line.split('/')

            # dictionary was stored as string; this changes it to dictionary again
            line[4] = ast.literal_eval(line[4])

            # corresponds to Stall(name, _open, close, days, menu)
            stall = Stall(line[0], line[1], line[2], line[3], line[4])
            pickle.dump(stall, f)