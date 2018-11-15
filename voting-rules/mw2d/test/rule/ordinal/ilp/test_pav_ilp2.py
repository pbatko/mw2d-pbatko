import unittest

from rules.ordinal.ilp.pav_ilp import PAV_ILP_ordinal, PAV_ILP_ordinal2
from rules.ordinal.pav import PAV_BruteForce
from rules.ordinal.single_committee_value import CommitteeScore
from test_commons.brute_force import OrdinalBruteForceTestTemplate_CV12_k4, OrdinalBruteForceTestTemplate_CV4_k2


class PAV_ILP_Test2(unittest.TestCase):

    def test_with_brute_force_cv12_k4(self):
        OrdinalBruteForceTestTemplate_CV12_k4(
            testcase=self
        ).testOnSampleElections(
            testedRuleFun=PAV_ILP_ordinal2.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
        pass

    def test_with_brute_force_cv4_k2(self):
        OrdinalBruteForceTestTemplate_CV4_k2(
            testcase=self
        ).testOnSampleElections(
            testedRuleFun=PAV_ILP_ordinal2.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
        pass