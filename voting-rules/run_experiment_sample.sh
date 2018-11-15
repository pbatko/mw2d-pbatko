#!/bin/bash


PWD="$(pwd)"
MW2D_SRC_PATH=${PWD}/voting-rules/mw2d/src
MW2D_DATAPOINTS_PATH=${PWD}/mw2d-datapoints
MW2D_EXPERIMENTS_PATH=${PWD}/mw2d-experiments


NOW_DATE_TIME="$(date +"%Y-%m-%d_%H-%M-%S")"

EXPERIMENT_NAME="experiment_cv100_k10_x200__AV"

export PYTHONPATH="$MW2D_SRC_PATH":"$PYTHONPATH"

echo "PYTHONPATH: $PYTHONPATH"

# some probably available rules:
# --rules PAV_ILP CC_ILP AV CC_Banzhaf CC_ReverseGreedy CC_Greedy PAV_ReverseGreedy PAV_Greedy PhragmenMax_Seq PhragmenVar_Seq \
# CC_Banzhaf CC_ReverseGreedy CC_Greedy PAV_ReverseGreedy PAV_Greedy PhragmenMax_Seq PhragmenVar_Seq

python2  mw2d/src/main_app2.py \
--committee-size 10 \
--rules AV \
--output-dir-name ${EXPERIMENT_NAME}__${NOW_DATE_TIME} \
--base-working-dir-name ${MW2D_EXPERIMENTS_PATH} \
--ballot-calc-params ApprovalBallotCalc_RadiusUniform 1.05 1.05 \
--ballot-calc-params ApprovalBallotCalc_NearestUniform 10.0 10.0 \
--number-of-elections 200 \
--number-voters-and-candidates 100 \
--distribution unidisc \
--datapoints-dir-path-dst ${MW2D_DATAPOINTS_PATH}/${EXPERIMENT_NAME}__${NOW_DATE_TIME}

# you can also read datapoints from a file
# --datapoints-dir-path-src $USER_HOME_DIR/python/voting-rules/mw2d-datapoints/experiment_cv100_k10_x2000__2018-10-21_15-59-18

