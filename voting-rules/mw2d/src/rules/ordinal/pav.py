from rules.bruteforcetemplate import BruteForceRule
from rules.ordinal.single_committee_value import CommitteeScore


class PAV_BruteForce:

    @classmethod
    def apply(clazz, V, number_of_candidates, k):
        # type: (list[list[int]], int, int) -> (list[list[int]], float)

        return BruteForceRule.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            scoreCommitteeFun=CommitteeScore.PAV
        )