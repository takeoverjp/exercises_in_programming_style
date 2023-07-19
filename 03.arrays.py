#!/usr/bin/env python3

import sys
import numpy as np

characters = np.array([' '] + list(open(sys.argv[1]).read()) + [' '])
characters[~np.char.isalpha(characters)] = ' '
characters = np.char.lower(characters)
sp = np.where(characters == ' ')
sp2 = np.repeat(sp, 2)
w_ranges = np.reshape(sp2[1:-1], (-1, 2))
w_ranges = w_ranges[np.where(w_ranges[:, 1] - w_ranges[:, 0] > 2)]
words = list(map(lambda r: characters[r[0]:r[1]], w_ranges))
swords = np.array(list(map(lambda w: ''.join(w).strip(), words)))
stop_words = np.array(list(set(open('stop_words.txt').read().split(','))))
ns_words = swords[~np.isin(swords, stop_words)]
uniq, counts = np.unique(ns_words, axis=0, return_counts=True)
wf_sorted = sorted(zip(uniq, counts), key=lambda t: t[1], reverse=True)

for w, c in wf_sorted[:25]:
    print(w, '-', c)
