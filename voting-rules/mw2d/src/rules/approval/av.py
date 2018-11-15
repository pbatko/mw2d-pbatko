from rules._base import ApprovalBasedRules, ApprovalBasedRuleBase


def register():
    ApprovalBasedRules.add(AV)


# OK
class AV(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V, number_of_candidates, k):
        # type: (list[list[int]], int) -> list[int]

        number_of_votes_per_candidate = [0] * number_of_candidates

        for vote in V:
            for c in vote:
                number_of_votes_per_candidate[c] += 1

        candidates = range(number_of_candidates)
        clazz.randomUtils.shuffle(candidates)
        candidates_best_to_worst = sorted(candidates, key=lambda c: -number_of_votes_per_candidate[c])
        committee = candidates_best_to_worst[:k]
        return committee

