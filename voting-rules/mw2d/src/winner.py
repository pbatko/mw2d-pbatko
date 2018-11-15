################################
# winner.py -- Winner Computation
#

import utils.testutils
import os

from core import *

# from rule_pr import *


# import rule packages

from rules.rule_proportional import *

try:
    import numpy as np
    import ilp
except:
    debug("No numeric libraries! Do not use ILP")
    raise


# read in the data in our format
# m n  (number of candidates and voters)
# m candidate names
# ...
# pref1  (n preference orders)
# ...
# return (m,n,C,V)
def readData(lines, k):
    # type: (list[str], int) -> (int, int, list[str], list[list[int]])
    V = []
    C = []

    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    for l in lines[1:m + 1]:
        s = l.rstrip()
        C += [s]

    for l in lines[m + 1:m + n + 1]:
        # skip first two numbers: they are 2d coordinates, TODO: do it in other places as well!
        s = l.split()[2:m + 2]
        s = [int(x) for x in s]
        V += [s]

    return (m, n, C, V)


def writeHeader(input_file_lines, output_file, k):
    # type: (list[str], file, int) -> None
    lines = input_file_lines

    (m, n) = lines[0].split()
    m = int(m)  # no of candidates
    n = int(n)  # no of voters
    output_file.write("{0} {1} {2}\n".format(m, n, k))

    candidates_lines = lines[1:m + 1]
    for l in candidates_lines:
        output_file.write(l.rstrip() + "\n")

    voters_lines = lines[m + 1:m + n + 1]
    for l in voters_lines:
        output_file.write(l.rstrip() + "\n")


#
# print winners
#

def writeWinners(W, C, output_file):
    # type: (list[int], list[str], file) -> None
    debug("printwinners")
    for i in W:
        output_file.write(C[i] + "\n")


def calculateWinner(input_file_path_arg, output_file_path_arg, rule_class, k):
    # type: (str, str, type, int) -> None
    input_lines = open(input_file_path_arg, 'r').readlines()
    (m, n, C, V) = readData(input_lines, k)
    number_of_candidates = len(C)

    W = calculateWinnerSane(V, number_of_candidates, k, rule_class)

    output_file = open(output_file_path_arg, 'w')
    writeHeader(input_lines, output_file, k)
    writeWinners(W, C, output_file)

import pathlib2





def calculateWinnerSane(V, number_of_candidates, k, rule_class):
    # make a copy just in case
    V = [list(vote) for vote in V]

    utils.testutils.TEST_UTIL_HOOK.apply(
        V=V,
        k=k,
        number_of_candidates=number_of_candidates
    )

    W = rule_class.apply(V, number_of_candidates, k)
    print(W)
    if len(set(W)) != k:
        print "ERROR:"
        print "k: " + str(k)
        print "len(set(W)): " + str(len(set(W)))
        print "len(W): " + str(len(W))
        print "rule_class: " + str(rule_class)
        print ""
        print ""
        print ""
        raise Exception
    # assert len(set(W)) == k  # sanity check

    return W


if __name__ == "__main__":

    # TODO restore ability to use stdin and stdout
    # data_in = stdin
    # data_out = stdout

    seed()

    if len(argv) < 3:
        print "ERROR: Required at least to arguments: input and output files"
        exit(1)

    if argv[1] == "help":
        print "This script computes election results"
        print
        print "Invocation:"
        print "  python winner.py rule k <ordinal_election.out"
        print
        print "Available rules:"
        for (rule, description) in RULES:
            l = 10
            print "%s - %s" % (rule + " " * (l - len(rule)), description)
        exit()

    input_file_path_arg = argv[1]
    output_file_path_arg = argv[2]

    if len(argv) >= 4:
        rule_function_name = argv[3]
    else:
        rule_function_name = "kborda"

    if len(argv) == 5:
        committee_size_str = argv[4]
        k = int(committee_size_str)
    else:
        k = 1

    calculateWinner(input_file_path_arg, output_file_path_arg, rule_function_name, k)
