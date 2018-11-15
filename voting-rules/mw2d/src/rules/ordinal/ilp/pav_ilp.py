from rules._base import ApprovalBasedRuleBase
from rules._base import ApprovalBasedRules

import rules.rule_proportional as rule_proportional
# from rules.rule_proportional import



def register():
    ApprovalBasedRules.add(PAV_ILP_ordinal)


# TODO create a common class for ordinal based elections
class PAV_ILP_ordinal(ApprovalBasedRuleBase):

    # eclude from approval rules because it's an ordinal rule
    excluded = True

    @classmethod
    def apply(clazz, V, number_of_candidates, k):
        # type: (list[list[int]], int) -> list[int]

        owa = [1.0 / i for i in range(1, k + 1)]


        committee = rule_proportional.PAV(V, k)
        return committee


class PAV_ILP_ordinal2(ApprovalBasedRuleBase):

    # eclude from approval rules because it's an ordinal rule
    excluded = True

    @classmethod
    def apply(clazz, V, number_of_candidates, k):
        # type: (list[list[int]], int) -> list[int]

        owa = [1.0 / i for i in range(1, k + 1)]


        committee = rule_proportional.PAVtopk(V, k)
        return committee