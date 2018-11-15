import itertools


class BruteForceRule:

    @classmethod
    def apply(clazz, V, number_of_candidates, k, scoreCommitteeFun):
        # type: (list[list[int]], int, int, callable) -> (list[list[int]], float)
        """
        :param scoreCommitteeFun: (V, committee) -> float
        """

        def subsetsIter(S, m):
            # S - set
            # m - size of a subsets
            # return set(itertools.combinations(S, m))
            return itertools.combinations(S, m)

        best_committees = []
        best_score = -1

        for committee in subsetsIter(S=range(number_of_candidates), m=k):
            committee = list(committee)
            score = scoreCommitteeFun(V, committee)
            if score > best_score:
                best_score = score
                best_committees = [committee]
            elif score == best_score:
                best_committees.append(committee)

        return best_committees, best_score

