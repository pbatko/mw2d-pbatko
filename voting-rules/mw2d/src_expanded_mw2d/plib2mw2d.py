#!/usr/bin/env python
import sys


def convert_preferences(path_from, path_to="2mw2d_converted.out"):
    file_from = open(path_from, 'r')
    file_to = open(path_to, 'w')

    for line_num, line in enumerate(file_from):
        if line_num == 0:
            cand_num = int(line)
        elif line_num == cand_num + 1:
            nvoters = int(line.split(',')[0])
            nvotes = int(line.split(',')[1])
            file_to.write(str(cand_num) + " " + str(nvotes) + "\n")
            for c_number in xrange(cand_num):
                file_to.write(str(c_number) + " 0 0 #\n")
        elif line_num > cand_num + 1:
            splitted_line = [segment.strip() for segment in line.split(',')]
            weight = int(splitted_line[0])
            for _ in xrange(weight):
                file_to.write(" ".join([str(int(c) - 1) for c in splitted_line[1:]]) + " 0 0#\n")
    file_from.close()
    file_to.close()


if __name__ == '__main__':
    path_from = sys.argv[1]
    path_to = sys.argv[2]
    convert_preferences(path_from, path_to)
