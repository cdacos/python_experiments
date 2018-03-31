#!/usr/bin/env python3

import argparse
import os
import random
import sys


def is_valid_throw(s) -> bool:
    if len(s) < 5:
        print('{} too few values (expected 5)'.format(5 - len(s)))
        return False
    elif len(s) > 5:
        print('{} too many values (expected 5)'.format(len(s) - 5))
        return False
    invalid = [t for t in s if t not in '123456']
    if invalid:
        print('"{}" invalid values (expected one of "123456")'.format(''.join(invalid)))
        return False
    return True


def read_wordlist(filename) -> dict:
    path = os.path.join(dirname, filename)
    return {parts[0]: parts[1] for parts in [line.strip().split('\t') for line in open(path)]}


def pretty_print(title, pwd):
    print('')
    print('*** {}:'.format(title))
    print(pwd)
    print('len: {}'.format(len(pwd)))


parser = argparse.ArgumentParser()
parser.add_argument('size', type=int, help='''Number of words required. Arnold Reinhard writes: "6 words may be breakable by an organization with a very large budget, such as a large country's security agency. 7 words and longer are unbreakable with any known technology, but may be within the range of large organizations by around 2030. 8 words should be completely secure through 2050." http://world.std.com/~reinhold/dicewarefaq.html''')
args = parser.parse_args()

dirname, _ = os.path.split(os.path.abspath(sys.argv[0]))

permutations = []
user_throws = True

for i in range(0, args.size):
    perm = ''
    if user_throws:
        print('{}. Enter the 5 values of your dice (e.g. 14236){}:'.format(i+1, ', else blank to generate all throws' if i == 0 else ''))
        while True:
            perm = sys.stdin.readline().strip()
            if not perm and i == 0:
                print('Generating throws...')
                break
            if is_valid_throw(perm):
                break
    if not perm:
        user_throws = False
        s = []
        for j in range(0, 5):
            s.append(str(random.randint(1, 6)))
        perm = ''.join(s)
    permutations.append(perm)

reinhold_list = read_wordlist('diceware.wordlist.txt')
eff_list = read_wordlist('eff_large_wordlist.txt')

pretty_print('Diceworld', ' '.join([reinhold_list[p] for p in permutations]))
pretty_print('EFF', ' '.join([eff_list[p] for p in permutations]))
