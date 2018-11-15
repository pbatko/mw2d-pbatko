import pathlib2


class EuclideanElectionDatapoints:

    @classmethod
    def fromFile(cls, datapoints_file_path):
        # type: (pathlib2.Path) -> EuclideanElectionDatapoints
        with open(str(datapoints_file_path), mode='r') as input_file:
            lines = input_file.readlines()
            lines_orig_len = len(lines)
            number_of_voters = int(lines[0])
            lines = lines[1:]
            V_str = lines[:number_of_voters]
            lines = lines[number_of_voters:]
            number_of_candidates = int(lines[0])
            lines = lines[1:]
            C_str = lines

            V = [cls.__toFloatPair(x) for x in V_str]
            C = [cls.__toFloatPair(x) for x in C_str]

            assert lines_orig_len == (2 + number_of_candidates + number_of_voters)

            return EuclideanElectionDatapoints(V=V, C=C)
        pass

    @classmethod
    def __toFloatPair(cls, str):
        a, b = str.split(",")
        return float(a), float(b)

    def __FloatPairToStr(cls, pair):
        a, b = pair
        return str(a) + "," + str(b)

    def __init__(self, V, C):
        # type: (list[(float, float)], list[(float, float)]) -> None
        self.V = V
        self.C = C

    def toFile(self, output_file_path):
        # type: (pathlib2.Path) -> None
        V = self.V
        C = self.C

        V_str = [self.__FloatPairToStr(x) for x in V]
        C_str = [self.__FloatPairToStr(x) for x in C]

        l = [len(V)] + V_str + [len(C)] + C_str

        with open(str(output_file_path), mode='w') as output_file:
            for line in l:
                print >> output_file, line
        pass

    pass
