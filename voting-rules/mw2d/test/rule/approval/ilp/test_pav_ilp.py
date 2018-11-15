import unittest

from rules.approval.ilp.owa import PAV_ILP
from rules.approval.pav import PAV_BruteForce
from rules.approval.single_committee_value import CommitteeScore
from test_commons.brute_force import ApprovalBruteForceTestTemplate


class PAV_ILP_Test(unittest.TestCase):

    def test_with_brute_force(self):
        ApprovalBruteForceTestTemplate(self).testOnSampleElections(
            testedRuleFun=PAV_ILP.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
