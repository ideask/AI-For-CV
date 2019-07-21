#!/usr/bin/env sh
#export CUDA_VISIBLE_DEVICES=1
set -e
STATE=train


CAFFE_ROOT=F:/caffe/scripts/build/tools/Release
SOLVER_ROOT=F:/Tiny_project/tiny_caffe_project

TRAIN=${CAFFE_ROOT}/caffe.exe
SOLVER=${SOLVER_ROOT}/brand_solver.prototxt
TESTER=${SOLVER_ROOT}/brand_network.prototxt
LOG=${SOLVER_ROOT}/network_log/$STATE.log
WEIGH=${SOLVER_ROOT}/models/_iter_1000.caffemodel
echo ${TRAIN}
echo ${SOLVER}
echo ${LOG}
if $STATE == train; then
  ${TRAIN} $STATE --solver=${SOLVER} --gpu=0 2>&1 | tee $LOG
else
  ${TRAIN} $STATE --model=${TESTER} --weights=${WEIGH} --iterations=100 --gpu=0 2>&1 | tee $LOG
fi
