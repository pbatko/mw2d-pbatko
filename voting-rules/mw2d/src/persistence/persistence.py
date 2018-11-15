from electionmodel.result import  ElectionResult
from new_experiment import  OutputFilePathsGetter
from new_experiment import  ElectionsExperiment
from new_experiment import  Histogram

import pathlib2
import visualize


class ElectionExperimentResultsFileWriter:

    def __init__(self, elections_experiment, output_file_path_getter):
        # type: (ElectionsExperiment, OutputFilePathsGetter) -> None
        self.elections_experiment = elections_experiment
        self.output_file_path_getter = output_file_path_getter

        self.histogram = Histogram.fromElectionResults(
            election_results=elections_experiment.election_results
        )

    def writeResults_Text(self):
        election_results = self.elections_experiment.getElectionResults()

        for i, election_result in enumerate(election_results):
            output_path = self.output_file_path_getter.pathForSingleElection_Text(election_index=i)

            NewExperimentFileWriter \
                .writeToTextFile(election_result, output_path)

        return self

    def writeResults_Images(self):
        election_results = self.elections_experiment.getElectionResults()

        for i, election_result in enumerate(election_results):
            output_path = self.output_file_path_getter.pathForSingleElection_Image(election_index=i)

            NewExperimentFileWriter \
                .writeToImageFile(election_result, output_path)

        return self

    def writeHistogram_Text(self):
        output_path = self.output_file_path_getter.pathForHistogram_Text()
        self.histogram.writeToTextFile(output_path)

        return self

    def writeHistogram_Image(self):
        output_path = self.output_file_path_getter.pathForHistogram_Image()
        self.histogram.writeToImageFile(output_path)

        return self

    pass


class NewExperimentFileWriter:

    @staticmethod
    def writeToTextFile(election_result, path):
        # type: (ElectionResult, pathlib2.Path) -> None

        W = election_result.committee
        C = election_result.candidates_2d
        V = election_result.voters_2d
        k = election_result.committee_size
        m = election_result.number_of_candidates
        n = election_result.number_of_voters
        P = election_result.voter_preferences

        with open(str(path), 'w') as output_file:

            print >> output_file, m, n, k

            for p in C:
                x = p[0]
                y = p[1]
                print >> output_file, x, y

            for i in range(n):
                x = V[i][0]
                y = V[i][1]
                preferences_string = " ".join([str(p) for p in (P[i])])
                print >> output_file, x, y, preferences_string

            for i in W:
                candidate = C[i]
                print >> output_file, candidate[0], candidate[1]

        pass

    @staticmethod
    def writeToImageFile(election_result, path):
        # type: (ElectionResult, pathlib2.Path) -> None

        winner_points = election_result.committee_2d
        C = election_result.candidates_2d
        V = election_result.voters_2d
        k = election_result.committee_size
        rule_name = election_result.rule_class.getName()

        visualize.drawVisualizationSane(
            C=C,
            V=V,
            Winner=winner_points,
            img_file_output_path=path,
            rule_name=rule_name + "_" + str(k))

        pass


