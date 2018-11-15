import main_app2
import utils.testutils
import pathlib2


def my_args(time_name_str):
    time_name = time_name_str
    argv = [
        # "--rules", "PhragmenMax_Seq",
        "--rules",
        # "PhragmenMax_ILP",
        # "PhragmenVar_ILP",
        # "Monroe_ILP",
        # "PAV_ILP",
        # "CC_ILP",
        # "PAV_SinglePeaked_ILP",
        # "PAV_ILP_ordinal",
        # "CC_Banzhaf",
        # "CC_ReverseGreedy_Slow",
        # "CC_ReverseGreedy",
        # "CC_Greedy",
        # "CC_Annealing",
        # "PAV_Annealing",
        "PAV_ReverseGreedy",
        "PAV_Greedy",
        # "PAV_Genetic",
        # "PhragmenMax_Seq",
        # "PhragmenVar_Seq",

        # "--rules", "PhragmenMax_ILP",
        # "PhragmenMax_ILP_2", # "PAV_Annealing", # "PhragmenMax_ILP", # "CC_ILP", "PAV_ILP", # "PhragmenMax_ILP"
        "--committee-size", "10",
        "--output-dir-name", "new_exp_2_" + time_name + "_py_PAV_ReverseGreedy",
        "--base-working-dir-name", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-experiments",

        # single gauss distribution, 12 voters and candidates

        # "--datapoints-dir-path-src",
        # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_20181015-195053_py_phragmen",

        "--number-of-elections", "1000",
        "--distributions", "unidisc",  # "gauss1",  # , "unisqua", "gauss4",
        "--number-voters-and-candidates", "100",
        # "--datapoints-dir-path-dst", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_cv100_k10_x10__" + time_name,
        # "--datapoints-dir-path-dst", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/ordinal_cv4__" + time_name,

        "--ballot-calc-params", "ApprovalBallotCalc_NearestUniform", "10.0", "10.0",
        # "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "1.05", "1.05"
    ]
    for arg in argv:
        print arg

    return argv

def my_args_bigMaxPhragmen():
    time_name = main_app2.getDateTimeFileName()
    argv = [
        "--rules", "PhragmenMax_ILP",

        "--committee-size", "10",
        "--output-dir-name", "new_exp_2_" + time_name + "_py_bigMaxPhragmen",
        "--base-working-dir-name", "/home/pbatko/src/code-misc/python/voting-rules/mw2d-experiments",

        # "--datapoints-dir-path-src",
        # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_py_bigMaxPhragmen",

        "--number-of-elections", "1000",
        "--distributions", "unidisc",  # "gauss1",  # , "unisqua", "gauss4",
        "--number-voters-and-candidates", "100",

        # "--datapoints-dir-path-dst",
        # "/home/pbatko/src/code-misc/python/voting-rules/mw2d-datapoints/datapoints_py_bigMaxPhragmen",

        # "--ballot-calc-params", "ApprovalBallotCalc_NearestUniform", "1", "10"
        "--ballot-calc-params", "ApprovalBallotCalc_RadiusUniform", "1.05", "1.05"
    ]
    return argv

if __name__ == '__main__':

    import random

    random.seed(1)
    # numpy.random.seed(1)

    time_name = main_app2.getDateTimeFileName()

    # utils.testutils.TEST_UTIL_HOOK = utils.testutils.SaveElectionInstance(
    #     baseOutputDir=pathlib2.Path("/home/pbatko/src/code-misc/python/voting-rules/mw2d/test-input/ordinal-cv4_{0}".format(time_name))
    # )

    main_app2.main(
        my_args(time_name_str = main_app2.getDateTimeFileName())
    )
    # main_app2.main(my_args_bigMaxPhragmen())


