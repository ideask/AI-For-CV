#!/usr/bin/env sh
#export CUDA_VISIBLE_DEVICES=1
set -e
STATE=train


CAFFE_ROOT=/home/kenny/caffe/build/tools
SOLVER_ROOT=${PWD}

TRAIN=${CAFFE_ROOT}/caffe
SOLVER=${SOLVER_ROOT}/brand_solver.prototxt
TESTER=${SOLVER_ROOT}/brand_network.prototxt
LOG=${SOLVER_ROOT}/network_log/$STATE.log
WEIGH=${SOLVER_ROOT}/models/brand_solver_iter_1000.caffemodel
echo ${TRAIN}
echo ${SOLVER}
echo ${LOG}
if [ $STATE = "train" ]; then
  ${TRAIN} $STATE --solver=${SOLVER} --gpu all 2>&1 | tee $LOG
else
  ${TRAIN} $STATE --model=${TESTER} --weights=${WEIGH} --iterations=100 --gpu all 2>&1 | tee $LOG
fi
