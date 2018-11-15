import pathlib2

class BaseTestUtil(object):

    def apply(self, V, k, number_of_candidates):
        raise NotImplementedError()

class NoOpHook(BaseTestUtil):

    def apply(self, V, k, number_of_candidates):
        pass

TEST_UTIL_HOOK = NoOpHook()

class SaveElectionInstance:

    def __init__(self, baseOutputDir):
        # type: (pathlib2.Path) -> None
        self.baseOutputDir = baseOutputDir
        self.i = 0

    def apply(self, V, k, number_of_candidates):
        # type: (list[list], int, int) -> None
        self.i += 1

        if not self.baseOutputDir.exists():
            self.baseOutputDir.mkdir()

        with open(str(self.baseOutputDir / str(self.i)), "w") as file:
            print >> file, str(len(V))
            print >> file, str(number_of_candidates)
            # print >> file, str(k)
            for votes in V:
                print >> file, " ".join([str(x) for x in votes])
        pass


