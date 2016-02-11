import sys

filename = sys.argv[1]

with open(filename) as f:
    filename = filename + '.csv'
    target = open(filename, 'w')
    for line in f:
        s = line.split()
        target.write(s[2])
        target.write('\n')