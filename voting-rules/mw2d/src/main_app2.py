import argparse
import sys

import pathlib2

import main_runner

parser = argparse.ArgumentParser(description='Runs series of experiments')
parser.add_argument('--rules',
                    required=True,
                    type=str,
                    metavar="RULE",
                    nargs='+',
                    help='Voting rule names')
parser.add_argument('--distributions',
                    required=False,
                    type=str,
                    metavar="NAME",
                    nargs='+',
                    help='Distribution schemes names')
parser.add_argument('--ballot-calc-params',
                    required=True,
                    type=str,
                    metavar=("NAME", "ARG1", "ARG2"),
                    nargs=3,
                    help='Parameters to instantiate ballot calc',
                    action='append'
                    )
parser.add_argument('--committee-size',
                    required=True,
                    type=int,
                    metavar='SIZE',
                    help='Committee size')
parser.add_argument('--output-dir-name',
                    required=True,
                    type=str,
                    metavar='NAME',
                    help='Output dir name')
parser.add_argument('--base-working-dir-name',
                    required=True,
                    type=str,
                    metavar='NAME',
                    help='Base dir for all output')
parser.add_argument('--number-of-elections',
                    required=False,
                    type=int,
                    metavar='NAME',
                    help='Number of elections')
parser.add_argument('--number-voters-and-candidates',
                    required=False,
                    type=int,
                    metavar='NUM',
                    help='Number candidates and number of voters (they are equal)')
parser.add_argument('--datapoints-dir-path-src',
                    required=False,
                    type=str,
                    metavar='PATH',
                    help='File path pointing to dir with file holding datapoints for 2D elections that we read from')
parser.add_argument('--datapoints-dir-path-dst',
                    required=False,
                    type=str,
                    metavar='PATH',
                    help='File path pointing to dir with file holding datapoints for 2D elections that we write to')


class CmdLineExperimentParameters():

    def __init__(self, namespace):
        # type: (argparse.Namespace) -> None
        self.distributions = namespace.distributions
        self.ballot_calcs_params = namespace.ballot_calc_params
        self.committee_size = namespace.committee_size
        self.rules = namespace.rules
        self.output_dir_name = namespace.output_dir_name
        self.base_working_dir_name = namespace.base_working_dir_name
        self.number_of_elections = namespace.number_of_elections
        self.number_voters_and_candidates = namespace.number_voters_and_candidates
        self.datapoints_dir_path_src = pathlib2.Path(
            namespace.datapoints_dir_path_src) if namespace.datapoints_dir_path_src is not None else None
        self.datapoints_dir_path_dst = pathlib2.Path(
            namespace.datapoints_dir_path_dst) if namespace.datapoints_dir_path_dst is not None else None
        pass

    pass


def timed(f):
    import time
    def g(*args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        elapsed_time = time.time() - start_time
        elapsed_time_formatted = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        print "================"
        print "Elapsed time: {0}".format(elapsed_time_formatted)

    return g


@timed
def main(argv):
    namespace = parser.parse_args(argv)
    params = CmdLineExperimentParameters(namespace)
    main_runner.main_runner(params)
    pass


def getDateTimeFileName():
    """
    :return: a datetime string, e.g. '20180716-175916'
    """
    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr

# sys.path.insert(0, '/home/pbatko/ibm/ILOG/CPLEX_Studio128/cplex/python/2.7/x86-64_linux')


if __name__ == '__main__':
    import random

#    import rules.approval._base
#
#    for r in rules.approval._base.ApprovalBasedRules.getList():
#        print '"' + str(r).split('.')[-1] + '",'
#
#    exit(1)

    random.seed(1)
    # numpy.random.seed(1)

    main(sys.argv[1:])
