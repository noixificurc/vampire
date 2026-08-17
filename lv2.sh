#!/bin/bash

#######################################
# paths
#######################################
LV2OUT="$(date +'%y%m%d-%H%M%S')/"  # level 2 output
LV1="$(pwd)/lv1.sh"  # level 1 script


#######################################
# prepare output
#######################################
mkdir -p $LV2OUT
cp $0 $LV2OUT


#######################################
# run level 1
#######################################
for i in 7.{0..9}{0..5..5}; do 
  LV1LABEL="-${i/\./}/";  # level 1 name tag
  DMI1=${i}e-22;
  source $LV1;
done
