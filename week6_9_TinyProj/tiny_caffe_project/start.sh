#!/usr/bin/env sh
set -e

BACKBONE=solver

CAFFE_ROOT=F:/caffe/scripts/build/tools/Release
SOLVER_ROOT=F:/Tiny_project/tiny_caffe_project

TRAIN=${CAFFE_ROOT}/caffe.exe
SOLVER=${SOLVER_ROOT}/brand_${BACKBONE}.prototxt
LOG=${SOLVER_ROOT}/${BACKBONE}_log/${BACKBONE}_log.log

echo ${TRAIN}
echo ${SOLVER}
echo ${LOG}

${TRAIN} train --solver=${SOLVER}| tee ${LOG}