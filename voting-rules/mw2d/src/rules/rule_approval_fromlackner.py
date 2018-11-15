import core
import lackner_approval
import lackner_preference
import lackner_profile
import rule_approval

core.RULES += [("RAV_Lackner"), ""]
core.RULES += [("seqMaxPhragmen_Lackner"), ""]


class RAV_Lackner(rule_approval.ApprovalBasedRuleBase):

    @staticmethod
    def apply(V, number_of_candidates, k):
        def getDP(votes):
            return lackner_preference.DichotomousPreference(votes, number_of_candidates)

        profile = lackner_profile.Profile(number_of_candidates)
        for votes in V:
            dp = getDP(votes)
            profile.add_preference(dp)

        committee = lackner_approval.compute_seqpav(
            profile=profile,
            committeesize=k,
            tiebreaking=True)

        return list(committee[0])


class SeqMaxPhragmen_Lackner(rule_approval.ApprovalBasedRuleBase):

    @staticmethod
    def apply(V, number_of_candidates, k):
        # todo pass exact number of candidates!
        index_of_biggest_candidate = max([max(v) for v in V])
        n = index_of_biggest_candidate + 1  # approximate number of candidates

        def getDP(votes):
            return lackner_preference.DichotomousPreference(votes, n)

        profile = lackner_profile.Profile(n)
        for votes in V:
            dp = getDP(votes)
            profile.add_preference(dp)

        committee = lackner_approval.compute_seqphragmen(
            profile=profile,
            committeesize=k
        )

        return list(committee[0])
