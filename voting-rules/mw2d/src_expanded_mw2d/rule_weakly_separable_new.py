#
# weakly separable rules
#

from core import *
from random import random
from absrule import Rule


##############################################################################
#
#     #    #  ######    ##    #    #  #        #   #
#     #    #  #        #  #   #   #   #         # #
#     #    #  #####   #    #  ####    #          #
#     # ## #  #       ######  #  #    #          #
#     ##  ##  #       #    #  #   #   #          #
#     #    #  ######  #    #  #    #  ######     #
#
#
#      ####   ######  #####     ##    #####     ##    #####   #       ######
#     #       #       #    #   #  #   #    #   #  #   #    #  #       #
#      ####   #####   #    #  #    #  #    #  #    #  #####   #       #####
#          #  #       #####   ######  #####   ######  #    #  #       #
#     #    #  #       #       #    #  #   #   #    #  #    #  #       #
#      ####   ######  #       #    #  #    #  #    #  #####   ######  ######

### NEW VERSIONS ###

def weaklySeparable2(profile, k, scoring_vector):
    m = profile.num_cand
    n = profile.voters_num()

    score = [[i, 0.1 * random()] for i in range(m)]
    for preference in profile:
        for i in range(m):
            score[preference.at_pos(i)][1] += scoring_vector[i]

    # debug(score)
    score = sorted(score, key=negsecond)[0:k]
    debug("print score")
    debug(score)
    winner = [s[0] for s in score]
    return winner


def bloc2(profile, k):
    m = profile.num_cand
    return weaklySeparable2(profile, k, ([1] * k) + ([0] * (m - k)))


def kborda2(profile, k):
    m = profile.num_cand
    return weaklySeparable2(profile, k, [m - i - 1 for i in range(m)])


def concave_kborda(profile, k):
    m = profile.num_cand
    return weaklySeparable2(profile, k, [sqrt(m - i - 1) for i in range(m)])


def convex_kborda(profile, k):
    m = profile.num_cand
    return weaklySeparable2(profile, k, [(m - i - 1) ** 2 for i in range(m)])


def sntv2(profile, k):
    m = profile.num_cand
    return weaklySeparable2(profile, k, [1] + [0] * (m - 1))


def tapproval2(profile, k, t):
    m = profile.num_cand
    return weaklySeparable2(profile, k, ([1] * t) + ([0] * (m - t)))


class Bloc2(Rule):
    def find_winners(self, profile, k):
        return bloc2(profile, k)


class KBorda2(Rule):
    def find_winners(self, profile, k):
        return kborda2(profile, k)


class SNTV2(Rule):
    def find_winners(self, profile, k):
        return sntv2(profile, k)


class TApproval2(Rule):
    def __init__(self, t):
        self.t = t

    def find_winners(self, profile, k):
        return tapproval2(profile, k, self.t)


# for i in range(1,201):
#  text = "approval_%d = lambda x,y: tapproval( x, y, %d )" % (i,i)
#  exec( text )

### OLD VERSIONS ###

def weaklySeparable(V, k, scoring_vector):
    m = len(V[0])
    n = len(V)

    score = [[i, 0.1 * random()] for i in range(m)]
    for v in V:
        for i in range(m):
            score[v[i]][1] += scoring_vector[i]

    score = sorted(score, key=negsecond)[0:k]
    debug("print score")
    debug(score)
    winner = [s[0] for s in score]
    return winner


RULES += [("bloc", "the Bloc rule (k-Approval)")]


def bloc(V, k):
    m = len(V[0])
    return weaklySeparable(V, k, ([1] * k) + ([0] * (m - k)))


RULES += [("kborda", "the k-Borda rule")]


def kborda(V, k):
    m = len(V[0])
    return weaklySeparable(V, k, [m - i - 1 for i in range(m)])


def concave_kborda(V, k):
    m = len(V[0])
    return weaklySeparable(V, k, [sqrt(m - i - 1) for i in range(m)])


def convex_kborda(V, k):
    m = len(V[0])
    return weaklySeparable(V, k, [(m - i - 1) ** 2 for i in range(m)])


RULES += [("sntv", "the SNTV rule (k-Plurality)")]


def sntv(V, k):
    m = len(V[0])
    return weaklySeparable(V, k, [1] + [0] * (m - 1))


class Bloc(Rule):
    def find_winners(self, V, k):
        return bloc(V, k)


class KBorda(Rule):
    def find_winners(self, V, k):
        return kborda(V, k)


class SNTV(Rule):
    def find_winners(self, V, k):
        return sntv(V, k)


class TApproval(Rule):
    def __init__(self, t):
        self.t = t

    def find_winners(self, V, k):
        return tapproval(V, k, self.t)


def tapproval(V, k, t):
    m = len(V[0])
    return weaklySeparable(V, k, ([1] * t) + ([0] * (m - t)))


for i in range(1, 201):
    text = "approval_%d = lambda x,y: tapproval( x, y, %d )" % (i, i)
    exec (text)
