import pathlib2


def _readElectionInstance(data_file_path):
    # type: (pathlib2.Path) -> (list[list[int]], int)

    import os
    cwd = os.getcwd()
    print cwd
    with open(str(data_file_path)) as f:
        lines = f.readlines()

    number_of_voters = int(lines[0])
    number_of_candidates = int(lines[1])

    assert len(lines) == (2 + number_of_voters)

    V = []
    for line in lines[2:]:
        vote = [int(x) for x in (line.split(" ")) if len(x) > 0]
        V.append(vote)

    return V, number_of_candidates


class ElectionTestDataSource(object):

    def getSampleElections(self):
        # type: () -> list[dict]
        raise NotImplementedError()

    pass


class OrdinalElectionTestDataSource(ElectionTestDataSource):

    def __init__(self, data_dir, file_names, k):
        # type: (pathlib2.Path, list[str], int) -> None
        """
        :param data_dir: Points to a directory where the files with individual election are
        """
        self.base_data_dir = data_dir
        self.file_names = file_names
        self.k = k
        pass

    def getSampleElections(self):
        for file_name in self.file_names:
            election_data_file = self.base_data_dir / file_name
            V = self.__deserializeElection(election_data_file)
            data = {
                'k': self.k,
                'V': V,
                'number_of_candidates': len(V[0]),
                'sample_name': file_name
            }
            yield data

    def __deserializeElection(self, election_data_file):
        # type: (pathlib2.Path) -> (list[list[int]])

        V, _number_of_candidates = _readElectionInstance(
            data_file_path=election_data_file
        )
        return V

    pass


class ApprovalElectionTestDataSource(ElectionTestDataSource):
    test_input_dir_path = pathlib2.Path("../test-input/_phragmen_test_data")
    test_input_file_names = [str(x) for x in range(1, 11)]  # [:1] # TODO take just first file because it's slow

    def getSampleElections(self):
        for sample_name in self.test_input_file_names:
            V, number_of_candidates, k = self.__deserializeSampleData(sample_name)
            data = {
                'V': V,
                'number_of_candidates': number_of_candidates,
                'k': k,
                'sample_name': sample_name
            }
            yield data

    def getSamplePhragmenResult(self, sample_name):
        loads, committee = self.__deserializePhragmenResult(sample_name=sample_name)
        data = {
            'loads': loads,
            'committee': committee,
        }
        return data

    def serializeCommitteeAndLoads(self, voter_loads, committee, sample_name):
        # type: (list[float], list[int], str) -> None

        committee = sorted(committee, key=lambda x: x)

        c_str = " ".join([str(x) for x in committee])
        v_str = " ".join([str(x) for x in voter_loads])

        with open(str(self.test_input_dir_path / (sample_name + "_results")), 'w') as f:
            print >> f, c_str
            print >> f, v_str

    def __deserializePhragmenResult(self, sample_name):
        # type: (str) -> (list[float], list[int])

        with open(str(self.test_input_dir_path / (sample_name + "_phragmen_results")), 'r') as f:
            lines = f.readlines()

        assert len(lines) == 2

        committee = [int(x) for x in lines[0].split(" ")]
        loads = [float(x) for x in lines[1].split(" ")]

        return loads, committee

    def __deserializeSampleData(self, sample_name):
        # type: (str) -> ((list[list[int]], int, int), (list[int], list[float]))
        election_data_file_path = self.test_input_dir_path / sample_name
        V, number_of_candidates = _readElectionInstance(
            data_file_path=election_data_file_path
        )

        # TODO hardcoded committee size
        input_data = (V, number_of_candidates, 4)

        return input_data

    pass
