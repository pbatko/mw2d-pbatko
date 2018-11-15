import collections
import operator
import sys

from rules._base import ApprovalBasedRuleBase


# OK
class Annealing_Meta():

    @classmethod
    def apply(clazz, V, number_of_candidates, k, compute_committee_score_fun):
        # type: (list[list[int]], int, int, callable) -> list[int]

        if k == number_of_candidates:
            return range(k)

        candidates = range(number_of_candidates)
        ApprovalBasedRuleBase.randomUtils.shuffle(candidates)
        committee = candidates[:k]
        candidates = list(set(candidates).difference(committee))

        T = 2000
        p0 = 0.02
        q = 0.999

        p = p0

        def swap(committee_idx, candidates_idx):
            # type: (int, int) -> None
            tmp = committee[committee_idx]
            committee[committee_idx] = candidates[candidates_idx]
            candidates[candidates_idx] = tmp
            pass

        score = compute_committee_score_fun(committee)

        best_score = score
        best_committee = list(committee)  # make a copy

        for i in range(T):
            p *= q

            committee_idx = ApprovalBasedRuleBase.randomUtils.randint(0, k - 1)
            candidates_idx = ApprovalBasedRuleBase.randomUtils.randint(0, number_of_candidates - k - 1)
            committee_tmp = list(committee)
            committee_tmp[committee_idx] = candidates[candidates_idx]
            tmp_score = compute_committee_score_fun(committee_tmp)

            if tmp_score > score or ApprovalBasedRuleBase.randomUtils.random() < p:
                score = tmp_score
                swap(committee_idx=committee_idx,
                     candidates_idx=candidates_idx)
                if score > best_score:
                    best_score = score
                    best_committee = list(committee)

        return best_committee