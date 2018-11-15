import unittest

import pathlib2

from test_commons.election_test_data import ApprovalElectionTestDataSource
from test_commons.election_test_data import ElectionTestDataSource
from test_commons.election_test_data import OrdinalElectionTestDataSource
from utils.utils import pluck


class BruteForceTestTemplate(object):

    def __init__(self, testcase, dataSource):
        # type: (unittest.TestCase, ElectionTestDataSource) -> None
        self.testcase = testcase
        self.dataSource = dataSource

    def testOnSampleElections(self, testedRuleFun, committeeScoreFun, bruteForceRuleFun):
        # type: (callable, callable, callable) -> None
        """
        :param testedRuleFun: (V, ?number_of_candidates, k) -> list[int]
        :param committeeScoreFun: (V, actualCommittee) -> float
        :param bruteForceRuleFun:  (V, ?number_of_candidates, k) -> list[list[int]], float
        """
        for electionDataDict in self.dataSource.getSampleElections():
            # given
            V, number_of_candidates, k = pluck(electionDataDict, 'V', 'number_of_candidates', 'k')

            # expected
            expectedCommittees, expectedScore = bruteForceRuleFun(V=V, number_of_candidates=number_of_candidates, k=k)

            # when
            actualCommittee = testedRuleFun(V=V, number_of_candidates=number_of_candidates, k=k)
            actualScore = committeeScoreFun(V=V, committee=actualCommittee)

            # then
            self.testcase.assertIn(
                member=actualCommittee,
                container=expectedCommittees,
                msg="{0} with score {1} not in {2} with score {3}".format(
                    actualCommittee,
                    actualScore,
                    expectedCommittees,
                    expectedScore)
            )
            self.testcase.assertEqual(expectedScore, actualScore)

    pass


class ApprovalBruteForceTestTemplate(BruteForceTestTemplate):

    def __init__(self, testcase):
        # type: (unittest.TestCase) -> None
        super(ApprovalBruteForceTestTemplate, self).__init__(
            testcase=testcase,
            dataSource=ApprovalElectionTestDataSource()
        )


# TODO duplication with OrdinalBruteForceTestTemplate_CV12
class OrdinalBruteForceTestTemplate_CV4_k2(BruteForceTestTemplate):

    def __init__(self, testcase):
        # type: (unittest.TestCase) -> None
        dataSource = OrdinalElectionTestDataSource(
            data_dir=pathlib2.Path("../test-input/ordinal-cv4_20181104-213844"),
            # file_names=[str(x) for x in range(1, 11)]
            file_names=[str(x) for x in [1]],
            k=2
        )
        super(OrdinalBruteForceTestTemplate_CV4_k2, self).__init__(
            testcase=testcase,
            dataSource=dataSource
        )


class OrdinalBruteForceTestTemplate_CV12_k4(BruteForceTestTemplate):

    def __init__(self, testcase):
        # type: (unittest.TestCase) -> None
        dataSource = OrdinalElectionTestDataSource(
            data_dir=pathlib2.Path("../test-input/ordinal-cv12_20181104-212147"),
            # file_names=[str(x) for x in range(1, 11)]
            file_names=[str(x) for x in [1]],
            k=4
        )
        super(OrdinalBruteForceTestTemplate_CV12_k4, self).__init__(
            testcase=testcase,
            dataSource=dataSource
        )
