#
#
from itertools import chain, combinations


# https://stackoverflow.com/questions/20297154/python-create-iterator-through-subsets-of-a-set-for-a-loop
def powersetFromSize1(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def scoreCommittee_tmajThreshold(S, V):

    def tMajThreshold(S):
        return len(S) / 2

    def isApproved(S, vote):
        number_of_approved_candidates_in_S = len(set(S).intersection(set(vote)))
        return number_of_approved_candidates_in_S >= tMajThreshold(S=S)

    score = 0
    for vote in V:
        if isApproved(S=S, vote=vote):
            score += 1
    return score

def scoreCommittee_NAV(S, V):
    S_len = len(S)
    S = set(S)
    score = 0
    for vote in V:
        vote = set(vote)
        approvedInS = len(vote.intersection(S))
        dissprovedInS = S_len - approvedInS
        s = approvedInS - dissprovedInS
        score += s

    return score


def findWinners(C, V, scoreCommitteeFun):
    max_score = -1
    best_committees = []
    for S in powersetFromSize1(C):
        score = scoreCommitteeFun(S=S, V=V)
        if score > max_score:
            max_score = score
            best_committees = [S]
        elif score == max_score:
            best_committees.append(S)
    print "Best score: {}".format(max_score)
    print "Winners:"
    for S in best_committees:
        print S


def main():
    # C = [1, 2, 3, 4, 5]
    # a, b, c, d, e = C
    # V = [
    #     [a, b],
    #     [a, b],
    #     [a, b],
    #     [c, d],
    #     [c, e],
    #     [d, e]
    # ]
    # findWinners(C=C, V=V, scoreCommitteeFun=scoreCommittee_tmajThreshold)

    # print "=========="
    # print "=========="
    # print "=========="
    #
    # C = [1, 2]
    # a, b = C
    # V = [
    #     [a, b]
    # ]
    # findWinners(C=C, V=V, scoreCommitteeFun=scoreCommittee_tmajThreshold)



    C = [1, 2, 3]
    a, b, c = C
    V = [
        [a],
        [b],
        [c],
    ]
    findWinners(C=C, V=V, scoreCommitteeFun=scoreCommittee_NAV)




    pass

if __name__ == '__main__':
    main()
