import collections
import unittest


class ApprovalBasedRules_Test(unittest.TestCase):
    RuleInput = collections.namedtuple('RuleInput', ['V', 'number_of_candidates', 'k'], verbose=False)

    input_params_sets = [
        RuleInput(
            k=3,
            number_of_candidates=4,
            V=[
                [0],
                [1],
                [1, 2],
                [0, 1, 2],
                [3]
            ]),
        RuleInput(
            k=4,
            number_of_candidates=4,
            V=[
                [0],
                [1],
                [1, 2],
                [0, 1, 2],
                [3]
            ])

    ]

    def test_approvalBasedRules_basicTest(self):
        import rules._base

        rule_classes = rules._base.ApprovalBasedRules.getList()

        for rule_class in rule_classes:
            for input_params in self.input_params_sets:
                # given
                k = input_params.k
                number_of_candidates = input_params.number_of_candidates
                V = input_params.V

                print(rule_class)

                # when
                actual_committee = rule_class.apply(
                    V=V,
                    number_of_candidates=number_of_candidates,
                    k=k)

                # then

                actual_k = len(actual_committee)
                msg = "Actual size of the committee: '{0}', expected: '{1}'".format(actual_k, k)
                self.assertEqual(actual_k, k, msg=msg)

        pass

    def test_approvalCC(self):
        # given
        import rules.approval.cc
        slowCC = rules.approval.cc.CC_ReverseGreedy_Slow
        fastCC = rules.approval.cc.CC_ReverseGreedy

        k = 3
        V = [
            [0],
            [1],
            [2],
            [3],
            [4],
            [5],
            [6]
        ]
        number_of_candidates = 7

        # TODO bad hack to disable randomness
        import rules._base
        rules._base.ApprovalBasedRuleBase.randomUtils = rules._base.RandomUtils_Const()

        # when
        import copy
        slowResult = slowCC.apply(
            V=copy.deepcopy(V),
            number_of_candidates=number_of_candidates,
            k=k
        )
        fastResult = fastCC.apply(
            V=copy.deepcopy(V),
            number_of_candidates=number_of_candidates,
            k=k
        )

        # then
        self.assertListEqual(slowResult, fastResult)

    pass
