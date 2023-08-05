#!/usr/bin/env python3

import sys, re, operator, string, time

def extract_words(path_to_file):
    with open(path_to_file) as f:
        str_data = f.read()
    pattern = re.compile(r'[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if w not in stop_words]

def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)

def profile(f):
    def profilewrapper(*arg, **kw):
        start_time = time.time()
        ret_value = f(*arg, **kw)
        elapsed = time.time() - start_time
        print("%s(...) took %s secs" % (f.__name__, elapsed))
        return ret_value
    return profilewrapper

tracked_functions = [extract_words, frequencies, sort]
for func in tracked_functions:
    globals()[func.__name__] = profile(func)

word_freqs = sort(frequencies(extract_words(sys.argv[1])))
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)
