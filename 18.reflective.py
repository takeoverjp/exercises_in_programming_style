#!/usr/bin/env python3
import sys, re, operator, string, os

stops = set(open('stop_words.txt').read().split(',') + list(string.ascii_lowercase))

def frequencies_imp(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

if len(sys.argv) > 1:
    extract_words_func = "lambda name : [x.lower() for x in re.split(r'[^a-zA-Z]+', open(name).read()) if len(x) > 0 and x.lower() not in stops]"
    frequencies_func = "lambda wl : frequencies_imp(wl)"
    sort_func = "lambda word_freq: sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)"
    filename = sys.argv[1]
else:
    extract_words_func = "lambda x: []"
    frequencies_func = "lambda x: []"
    sort_func = "lambda x: []"
    filename = os.path.basename(__file__)

exec('extract_words = ' + extract_words_func)
exec('frequencies = ' + frequencies_func)
exec('sort = ' + sort_func)

word_freqs = locals()['sort'](locals()['frequencies'](locals()['extract_words'](filename)))
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)
