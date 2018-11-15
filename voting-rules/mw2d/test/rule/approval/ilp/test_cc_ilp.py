import unittest

from rules.approval.cc import CC_BruteForce
from rules.approval.ilp.owa import CC_ILP
from rules.approval.single_committee_value import CommitteeScore
from test_commons.brute_force import ApprovalBruteForceTestTemplate


class CC_ILP_Test(unittest.TestCase):

    def test_with_brute_force(self):
        ApprovalBruteForceTestTemplate(self).testOnSampleElections(
            testedRuleFun=CC_ILP.apply,
            committeeScoreFun=CommitteeScore.CC,
            bruteForceRuleFun=CC_BruteForce.apply)
