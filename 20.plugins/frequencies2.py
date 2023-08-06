import operator, collections

def top25(word_list):
    counts = collections.Counter(word_list)
    return counts.most_common(25)
