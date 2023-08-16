#!/usr/bin/env python3

import re
import sys
import operator
import queue
import threading
word_space = queue.Queue()
freq_space = queue.Queue()

stopwords = set(open("stop_words.txt").read().split(","))


def process_words():
    word_freqs = {}
    while True:
        try:
            word = word_space.get(timeout=1)
        except queue.Empty:
            break
        if not word in stopwords:
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    freq_space.put(word_freqs)


for word in re.findall(r"[a-z]{2,}", open(sys.argv[1]).read().lower()):
    word_space.put(word)

workers = []
for i in range(5):
    workers.append(threading.Thread(target=process_words))

[t.start() for t in workers]

[t.join() for t in workers]

word_freqs = {}
while not freq_space.empty():
    freqs = freq_space.get()
    for (k, v) in freqs.items():
        if k in word_freqs:
            count = sum(item[k] for item in [freqs, word_freqs])
        else:
            count = freqs[k]
        word_freqs[k] = count
for (w, c) in sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)[:25]:
    print(w, '-', c)
