#!/bin/bash

#######################################
# paths
#######################################
LV2SRC="$(pwd)/"
LV2DATE="$(date +'%y%m%d-%H%M%S')"  # level 2 output
LV2OUT="${LV2SRC}../data/${LV2DATE}/"  # level 2 output
LV1="${LV2SRC}/lv1.sh"  # level 1 script
AISO=3e-23


#######################################
# prepare output
#######################################
mkdir -p $LV2OUT
cp $0 $LV2OUT


#######################################
# run level 1
#######################################
for i in {0..8}.{0..9..2}; do 
  LV1LABEL="-${i/\./}/";  # level 1 name tag
  DMI1=${i}e-22;
  source $LV1;
done
