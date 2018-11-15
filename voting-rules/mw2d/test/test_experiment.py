import unittest

import ballot_2d2
import new_experiment


# class EuclideanElectionDatapointsGenerator_Test(unittest.TestCase):
#
#     def test_dataPointGeneration(self):
#         # given
#         distribution_descriptor = new_experiment.EuclideanDistributionDescriptor(
#             commands=['candidates',
#                       'circle 0 0 3 200',
#                       'voters',
#                       'circle 0 0 3 200'
#                       ],
#             label="label")
#
#         # when
#         actual = new_experiment \
#             .EuclideanElectionDatapointsGenerator \
#             .fromDistributionDescriptor(distribution_descriptor)
#
#         # then
#         self.assertTrue(
#             isinstance(actual, new_experiment.EuclideanElectionDatapoints))
#
#         self.assertEqual(len(actual.C), 200)
#         self.assertEqual(len(actual.V), 200)
#
#         self.assertEqual(type(actual.C[0]), tuple)
#         self.assertEqual(type(actual.V[0]), tuple)
#
#         self.assertEqual(type(actual.V[0][0]), float)
#         self.assertEqual(type(actual.V[0][1]), float)
#
#         self.assertEqual(type(actual.C[0][0]), float)
#         self.assertEqual(type(actual.C[0][1]), float)
#
#         pass


class ElectionInstance_Test(unittest.TestCase):

    def test_ElectionInstance(self):
        # given
        datapoints = new_experiment.EuclideanElectionDatapoints(
            V=[(0, 10), (0, 0)],
            C=[(0, 1), (0, 2), (0, 11), (0, 12)]
        )

        # when
        actual = new_experiment.ElectionInstance. \
            fromEuclideanDatapoints(
            euclidean_election_datapoints=datapoints,
            ballot_calc=ballot_2d2.ApprovalBallotCalc_NearestUniform(min=2, max=2)
        )

        # then
        self.assertEqual(actual.C, [(0, 1), (0, 2), (0, 11), (0, 12)])
        self.assertEqual(actual.V, [(0, 10), (0, 0)])
        self.assertEqual(actual.P, [[2, 3], [0, 1]])

        pass

