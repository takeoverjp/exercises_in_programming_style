#!/usr/bin/env python3
import sys, os

def touchopen(filename, *args, **kwargs):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, "a").close()
    return open(filename, *args, **kwargs)
    
data = []

f = open('stop_words.txt')
data = [f.read(1024).split(',')]
f.close()

data.append([])
data.append(None)
data.append(0)
data.append(False)
data.append('')
data.append('')
data.append(0)

word_freqs = touchopen('word_freqs', 'rb+')
f = open(sys.argv[1], 'r')
while True:
    data[1] = [f.readline()]
    if data[1] == ['']:
        break
    if data[1][0][len(data[1][0])-1] != '\n':
        data[1][0] = data[1][0] + '\n'
    data[2] = None
    data[3] = 0
    for c in data[1][0]:
        if data[2] is None:
            if c.isalnum():
                data[2] = data[3]
        else:
            if not c.isalnum():
                data[4] = False
                data[5] = data[1][0][data[2]:data[3]].lower()

                if len(data[5]) >= 2 and data[5] not in data[0]:
                    while True:
                        data[6] = str(word_freqs.readline().strip(), 'utf-8')
                        if data[6] == '':
                            break
                        data[7] = int(data[6].split(',')[1])
                        data[6] = data[6].split(',')[0].strip()
                        if data[5] == data[6]:
                            data[7] += 1
                            data[4] = True
                            break
                    if not data[4]:
                        word_freqs.seek(0, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], 1), 'utf-8'))
                    else:
                        word_freqs.seek(-26, 1)
                        word_freqs.write(bytes("%20s,%04d\n" % (data[5], data[7]), 'utf-8'))
                    word_freqs.seek(0, 0)
                data[2] = None
        data[3] += 1
f.close()
word_freqs.flush()


del data[:]

data = data + [[]] * (25 - len(data))
data.append('')
data.append(0)

while True:
    data[25] = str(word_freqs.readline().strip(), 'utf-8')
    if data[25] == '':
        break
    data[26] = int(data[25].split(',')[1])
    data[25] = data[25].split(',')[0].strip()
    for i in range(25):
        if data[i] == [] or data[i][1] < data[26]:
            data.insert(i, [data[25], data[26]])
            del data[26]
            break

for tf in data[0:25]:
    if len(tf) == 2:
        print(tf[0], '-', tf[1])

word_freqs.close()
                        