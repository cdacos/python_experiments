import sys

param = sys.argv[1]

def LongestWord(sen):
    longest=''
    word=''
    for c in sen + ' ':
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            word+=c
        else:
            if len(word) > len(longest):
                longest = word
            word=''
    return longest

print("LongestWord: {} -> {}".format(param, LongestWord(param)))
