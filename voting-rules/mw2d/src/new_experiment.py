import pathlib2

import ballot_2d2
import experiment
import histogram
import histogram_draw
import rules.approval
import utils.utils
import visualize
import winner

from electionmodel.euclidean import EuclideanElectionDatapoints
from electionmodel.result import ElectionResult
from electionmodel.instance import ElectionInstance






class EuclideanElectionDatapointsGenerator:
    """
    Generates 2D points representing voters and candidates according to specified data distributions

    Delagates calculations to `OldExperiment`
    """

    @staticmethod
    def fromDistributionDescriptor(distribution_descriptor):
        # type: (DistributionDescriptor) -> list[EuclideanElectionDatapoints]
        # delegate to legacy `OldExperiment`

        if isinstance(distribution_descriptor, EuclideanDistributionDescriptor):
            number_of_distributions = distribution_descriptor.getNumberOfDistributions()
            ret = []
            for _ in range(number_of_distributions):
                old = experiment.OldExperiment.fromCommandList(commands=distribution_descriptor.getCommands(),
                                                               ballot_calc=None,
                                                               output_dir_path=None)
                old.run()
                x = EuclideanElectionDatapoints(
                    V=old.V,
                    C=old.C)
                ret.append(x)

            return ret

        if isinstance(distribution_descriptor, DistributionDescriptorFromFs):
            number_of_distributions = distribution_descriptor.number_of_distributions

            ret = []
            for idx in range(number_of_distributions):
                datapoints_file = distribution_descriptor.src_dir_path / str(idx)
                x = EuclideanElectionDatapoints.fromFile(datapoints_file_path=datapoints_file)
                ret.append(x)

            return ret

    pass


class NewExperiment:

    @staticmethod
    def computeElectionResult(election_instance, rule_class, committee_size):
        # type: (ElectionInstance, rules.rule_approval.ApprovalBasedRuleBase, int, str) -> ElectionResult

        W = winner.calculateWinnerSane(
            V=election_instance.P,
            number_of_candidates=election_instance.getNumberOfCandidates(),
            k=committee_size,
            rule_class=rule_class
        )

        return ElectionResult(
            election_instance=election_instance,
            committee=W,
            rule_class=rule_class
        )

    pass



class Histogram:

    def __init__(self, old_histogram):
        # type: (histogram.OldHistogram) -> None
        self.old_histogram = old_histogram
        pass

    @staticmethod
    def fromElectionResults(election_results):
        # type: (list[ElectionResult]) -> Histogram

        h = histogram.OldHistogram(number_of_experiments=None,
                                   input_dir_path=None,
                                   rule_name_with_committee_size=None)

        for election_result in election_results:
            h.computeHistogramIncrementallySane(election_result.committee_2d)

        return Histogram(h)

    def writeToTextFile(self, path):
        # type: (pathlib2.Path) -> None

        self \
            .old_histogram \
            .writeHistFileSaner(output_path=path)

    pass

    def writeToImageFile(self, path, TRADITIONAL=True, threshold=0.004, col_r=1.0, col_g=0.8, col_b=0.8):
        # type: (pathlib2.Path) -> None

        W = self.old_histogram.W
        H = self.old_histogram.H
        HISTOGRAM = self.old_histogram.HISTOGRAM

        histogram_draw.drawHistogramSaner2(
            output_file_path=path,
            W=W,
            H=H,
            HISTOGRAM=HISTOGRAM,
            TRADITIONAL=TRADITIONAL,
            threshold=threshold,
            col_r=col_r,
            col_g=col_g,
            col_b=col_b)

        pass


class ElectionInstancesContainer:

    def serializeToString(self):

        ballot_calc_dict = self.ballot_calc.to_dict()

        serialized_distribution_descriptor = self.distribution_descriptor.serializeToString()
        number_of_serialized_instances = len(self.election_instances)
        serialized_instances = "\n".join([x.serializeToString() for x in self.election_instances])

        """{0}
{1}
{2}
{3}""".format(serialized_ballot_calc,
              serialized_distribution_descriptor,
              str(number_of_serialized_instances),
              serialized_instances)

        pass

    @classmethod
    def deserializeFromString(clazz, s):
        lines = s.splitlines()
        number_of_elections = int(lines[0])
        lines = lines[1:]

        ballot_calc, lines = ballot_2d2.BallotCalc.deserializeFromLines(lines)
        distribution_descriptor, lines = EuclideanDistributionDescriptor.deserializeFromLines(s)

        number_of_instances = int(lines[0])
        lines = lines[1:]

        deserialized_instances = []
        for _ in range(number_of_instances):
            deserialized_instance, lines = ElectionInstance.deserializeFromLines(lines)
            deserialized_instances.append(deserialized_instance)

        return ElectionInstancesContainer(
            election_instances=deserialized_instances,
            ballot_calc=ballot_calc,
            distribution_descriptor=distribution_descriptor
        )

    def __init__(self, election_instances, ballot_calc, distribution_descriptor):
        # type: (list[ElectionInstance], int, ballot_2d2.BallotCalc, EuclideanDistributionDescriptor) -> None
        self.election_instances = election_instances
        self.ballot_calc = ballot_calc
        self.distribution_descriptor = distribution_descriptor

        pass

    def getBallotCalcLabel(self):
        # type: () -> str
        return self.ballot_calc.getShortName()

    @staticmethod
    def fromDistribution(distribution_descriptor, ballot_calcs, list_of_datapoints):
        # type: (EuclideanDistributionDescriptor, list[ballot_2d2.BallotCalc], list[EuclideanElectionDatapoints]) -> list[ElectionInstancesContainer]
        election_instances_list = ElectionInstancesContainer.__generateElectionInstances(
            ballot_calcs=ballot_calcs,
            list_of_datapoints=list_of_datapoints)

        result = []
        for ballot_calc, election_instances in election_instances_list:
            result.append(ElectionInstancesContainer(
                election_instances=election_instances,
                ballot_calc=ballot_calc,
                distribution_descriptor=distribution_descriptor
            ))
        return result

    @staticmethod
    def __generateElectionInstances(ballot_calcs, list_of_datapoints):
        # type: (list[ballot_2d2.BallotCalc], list[EuclideanElectionDatapoints]) -> list[ballot_2d2.BallotCalc, list[ElectionInstance]] # TODO use better result type!

        def convertToElectionInstance(euclidean_election_datapoints, ballot_calc):
            # type: (EuclideanElectionDatapoints) -> ElectionInstance

            return ElectionInstance.fromEuclideanDatapoints(
                euclidean_election_datapoints=euclidean_election_datapoints,
                ballot_calc=ballot_calc)

        euclidean_election_datapoints_list = list_of_datapoints

        election_instances_list = []
        for ballot_calc in ballot_calcs:
            tuple = (
                ballot_calc, [convertToElectionInstance(x, ballot_calc) for x in euclidean_election_datapoints_list])
            election_instances_list.append(tuple)

        return election_instances_list


pass


class ElectionsExperimentParameters:

    def __init__(self, rule_class, committee_size):
        # type: (rules.rule_approval.ApprovalBasedRuleBase, int) -> None
        self.committee_size = committee_size
        self.rule_class = rule_class

    def mkString(self):
        # type: () -> str

        return "committee_size {0}, rule_name: {1}".format(self.committee_size, self.rule_class.getName())

    pass


class ElectionsExperiment:

    def __init__(self, election_instances, elections_experiment_parameters):
        # type: (ElectionInstancesContainer, ElectionsExperimentParameters) -> None

        self.election_instances = election_instances.election_instances  # TODO
        self.elections_experiment_parameters = elections_experiment_parameters

        self.election_results = None

        pass

    def getElectionResults(self):
        # type: () -> list[ElectionResult]
        if self.election_results is None:
            raise Exception("Elections results not available - experiment hasn't been run!")

        return self.election_results

    def runExperiment(self):
        # type: () -> None

        election_instances = self.election_instances
        rule_class = self.elections_experiment_parameters.rule_class
        committee_size = self.elections_experiment_parameters.committee_size

        election_results = []
        for election_instance in election_instances:
            election_result = NewExperiment.computeElectionResult(
                election_instance=election_instance,
                rule_class=rule_class,
                committee_size=committee_size)
            election_results.append(election_result)

        self.election_results = election_results

        pass

    pass


class OutputFilePathsGetter:

    def __init__(self,
                 base_work_dir_path,
                 election_experiment_parameters,
                 distribution_label,
                 ballot_calc_label):
        # type: (pathlib2.Path, ElectionsExperimentParameters, str, str) -> None

        utils.utils.PathValidator(base_work_dir_path, "Election experiment base work dir path") \
            .exists() \
            .is_dir()

        self.base_dir_path = base_work_dir_path
        self.election_experiment_parameters = election_experiment_parameters
        self.distribution_label = distribution_label
        self.ballot_calc_label = ballot_calc_label

        pass

    def pathForSingleElection_Text(self, election_index):
        # type: (int) -> pathlib2.Path
        return self.__pathForSingleElection(election_index).with_suffix(".txt")

    def pathForSingleElection_Image(self, election_index):
        # type: (int) -> pathlib2.Path
        return self.__pathForSingleElection(election_index).with_suffix(".png")

    def pathForHistogram_Text(self):
        # type: () -> pathlib2.Path
        return self.__pathForHistogram(suffix="_hist.txt")

    def pathForHistogram_Image(self):
        # type: () -> pathlib2.Path
        return self.__pathForHistogram(suffix="_hist.png")

    # PRIVATE

    def __pathForSingleElection(self, election_index):
        # type: (int) -> pathlib2.Path

        rule_name = self.election_experiment_parameters.rule_class.getName()
        committee_size = self.election_experiment_parameters.committee_size

        election_result_bare_file_name = "{0}_k{1}_{2}".format(rule_name, committee_size, election_index)

        return self.__baseDirPathForSingleElections() / election_result_bare_file_name

    def __pathForHistogram(self, suffix):
        # type: (str) -> pathlib2.Path
        dir_path = self.base_dir_path / "histogram"
        dir_path.mkdir(parents=False, exist_ok=True)

        return dir_path / (self.__makeElectionName() + suffix)

    def __baseDirPathForSingleElections(self):
        # type: () -> pathlib2.Path
        dir_path = self.base_dir_path / self.__makeElectionName()
        dir_path.mkdir(parents=False, exist_ok=True)

        return dir_path

    def __makeElectionName(self):
        # type: () -> str
        distribution_label = self.distribution_label
        ballot_calc_label = self.ballot_calc_label
        rule_name = self.election_experiment_parameters.rule_class.getName()
        committee_size = self.election_experiment_parameters.committee_size
        elections_results_dir_name = "elections_{0}_{1}_{2}_k{3}".format(distribution_label, rule_name,
                                                                         ballot_calc_label, committee_size)
        return elections_results_dir_name

    pass





class DistributionDescriptor(object):
    pass


class DistributionDescriptorFromFs(DistributionDescriptor):

    def __init__(self, src_dir_path, distribution_label, number_of_distributions):
        # type: (pathlib2.Path) -> None
        self.src_dir_path = src_dir_path
        self.distribution_label = distribution_label
        self.number_of_distributions = number_of_distributions
        pass

    def getLabel(self):
        return self.distribution_label

    pass



class EuclideanDistributionDescriptor(DistributionDescriptor):

    @classmethod
    def getGauss1(clazz, number_of_voters_and_candidates, number_of_datapoint_distributions):
        # type: () -> EuclideanDistributionDescriptor
        return EuclideanDistributionDescriptor(
            commands=clazz.get2dGaussianElectionDistributionCommands(0, 0, 1, number_of_voters_and_candidates),
            label='gauss1',
            number_of_datapoint_distributions=number_of_datapoint_distributions
        )

    @classmethod
    def getGauss4(clazz, number_of_voters_and_candidates, number_of_datapoint_distributions):
        assert number_of_voters_and_candidates % 4 == 0
        c = number_of_voters_and_candidates / 4
        # type: () -> EuclideanDistributionDescriptor
        commands = (clazz.get2dGaussianElectionDistributionCommands(-1, 0, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(1, 0, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(0, -1, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(0, 1, 0.5, c))
        return EuclideanDistributionDescriptor(
            commands=commands,
            label='gauss4',
            number_of_datapoint_distributions=number_of_datapoint_distributions
        )

    def __init__(self, commands, label, number_of_datapoint_distributions):
        # type: (list[str], str) -> None
        self.__label = label
        self.__commands = commands
        self.__number_of_datapoint_distributions = number_of_datapoint_distributions
        pass

    def getCommands(self):
        # type: () -> list[str]
        return self.__commands

    def getLabel(self):
        # type: () -> str
        return self.__label

    def getNumberOfDistributions(self):
        # type: () -> int
        return self.__number_of_datapoint_distributions

    @staticmethod
    def get2dGaussianElectionDistributionCommands(x, y, sigma, n):
        distribution_str = 'gauss {0} {1} {2} {3}'.format(x, y, sigma, n)

        return ['candidates',
                distribution_str,
                'voters',
                distribution_str,
                ]

        pass


class EuclideanDistributionDescriptorContainer():
    # TODO simplify

    def __init__(self, descriptors):
        # type: (list[EuclideanDistributionDescriptor]) -> None
        self.__descriptors = descriptors
        pass

    def getDescriptorList(self):
        return self.__descriptors

    @classmethod
    def toDir(cls, output_dir_path, list_of_descriptors_and_list_of_datapoints):
        # type: (pathlib2.Path, list((EuclideanDistributionDescriptor, list[EuclideanElectionDatapoints]))) -> None

        info_file_content = []

        output_dir_path.mkdir(exist_ok=False, parents=True)

        for idx, (descriptor, datapoint_sets) in enumerate(list_of_descriptors_and_list_of_datapoints):
            info_file_content.append(
                str(idx) + ", " + descriptor.getLabel() + ", " + str(descriptor.getNumberOfDistributions()))

            datapoints_dir = output_dir_path / str(idx)
            datapoints_dir.mkdir(parents=False, exist_ok=False)

            for dpidx, datapoint_set in enumerate(datapoint_sets):
                output_file_path = datapoints_dir / str(dpidx)
                datapoint_set.toFile(output_file_path=output_file_path)

        with open(str(output_dir_path / "info.txt"), 'w') as info_file:
            for line in info_file_content:
                print >> info_file, line
        pass

    @classmethod
    def fromDir(cls, input_dir_path):
        # type: (pathlib2.Path) -> EuclideanDistributionDescriptorContainer
        info_file_path = input_dir_path / "info.txt"

        list_of_distribution_descriptors = []
        with open(str(info_file_path), 'r') as info_file:
            lines = info_file.readlines()
            for line in lines:
                distribution_dir_name, label, number_of_distributions = [x.strip() for x in line.split(",")]
                list_of_distribution_descriptors.append(
                    DistributionDescriptorFromFs(
                        src_dir_path=input_dir_path / distribution_dir_name,
                        distribution_label=label,
                        number_of_distributions=int(number_of_distributions)
                    )
                )

        return EuclideanDistributionDescriptorContainer(list_of_distribution_descriptors)

    @classmethod
    def getByNames(clazz, names, number_of_voters_and_candidates, number_of_datapoint_distributions):
        # type: (list[str]) -> EuclideanDistributionDescriptorContainer
        ds = [d for d in clazz.getDefault(
            number_of_voters_and_candidates=number_of_voters_and_candidates,
            number_of_datapoint_distributions=number_of_datapoint_distributions).getDescriptorList() if
              d.getLabel() in names]
        return EuclideanDistributionDescriptorContainer(ds)

    @classmethod
    def getDefault(clazz, number_of_voters_and_candidates, number_of_datapoint_distributions):
        # type: () -> EuclideanDistributionDescriptorContainer
        distributions = {
            'unisqua': ['candidates',
                        'uniform -3 -3 3 3 {0}'.format(number_of_voters_and_candidates),
                        'voters',
                        'uniform -3 -3 3 3 {0}'.format(number_of_voters_and_candidates),
                        ],
            'unidisc': ['candidates',
                        'circle 0 0 3 {0}'.format(number_of_voters_and_candidates),
                        'voters',
                        'circle 0 0 3 {0}'.format(number_of_voters_and_candidates)
                        ]
        }

        descriptors = []
        for label, commands in distributions.iteritems():
            descriptors.append(
                EuclideanDistributionDescriptor(
                    commands=commands,
                    label=label,
                    number_of_datapoint_distributions=number_of_datapoint_distributions
                )
            )

        descriptors.append(
            EuclideanDistributionDescriptor.getGauss1(number_of_voters_and_candidates,
                                                      number_of_datapoint_distributions))
        descriptors.append(
            EuclideanDistributionDescriptor.getGauss4(number_of_voters_and_candidates,
                                                      number_of_datapoint_distributions))

        return EuclideanDistributionDescriptorContainer(descriptors)
