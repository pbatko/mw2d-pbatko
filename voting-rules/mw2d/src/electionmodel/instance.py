

class ElectionInstance:

    def __init__(self, V, C, P):
        self.V = V
        self.C = C
        self.P = P
        pass

    def getNumberOfCandidates(self):
        # type: () -> int
        return len(self.C)

    @staticmethod
    def fromEuclideanDatapoints(euclidean_election_datapoints, ballot_calc):
        # type: (EuclideanElectionDatapoints, ballot_2d2.BallotCalc) -> ElectionInstance

        P = ballot_calc.calculateFrom2dPoints(
            V=euclidean_election_datapoints.V,
            C=euclidean_election_datapoints.C
        )

        return ElectionInstance(
            V=euclidean_election_datapoints.V,
            C=euclidean_election_datapoints.C,
            P=P
        )

    pass