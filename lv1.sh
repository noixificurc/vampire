#!/bin/bash

########################################
# configuration
########################################
NCPU=$(nproc --ignore=6)  # number of slaves
if [ -z "${ISO1+x}" ]; then
  ISO1=-3e-21
fi 
if [ -z "${DMI1+x}" ]; then
  DMI1=7e-22
fi 
if [ -z "${AISO+x}" ]; then
  AISO=-3e-23
fi


########################################
## paths
########################################
SRC="$(pwd)/"
DATE="$(date +'%y%m%d-%H%M%S')-$(date +%N | cut -c1-6)"  ## date
OUT="${SRC}../data/${LV2OUT}${DATE}${LV1LABEL}/"  ## path output directory
CNFSRC="${SRC}conf/"
CNFOUT="${OUT}conf/"
VAMP="vampire-parallel"
EXCSRC="${SRC}${VAMP}"  # Vampire executable in source directory
EXCOUT="${OUT}${VAMP}"  # Vampire executable in source directory
VDC="${SRC}util/vdc/vdc"  # Vampire to povray converter
META="${OUT}meta/"  # meta data 


#######################################
# prepare input and output
#######################################
mkdir -p "$META" "$CNFOUT"
cp $0 $OUT
cp $EXCSRC $EXCOUT
prepCnf $CNFSRC      \
        $CNFOUT      \
        "ISO1=$ISO1" \
        "DMI1=$DMI1" \
        "AISO=$AISO"


#######################################
# run
#######################################
cd $OUT
# run simulation
mpirun -n $NCPU $EXCOUT --input-file "${CNFOUT}input" --output-file "result"
# create povray file
$VDC --povray --input-file "atoms-coords"
# render spin configuration
NFRAME=$(find . -name 'spins-*.inc' -printf '%f\n' |
         sed 's/spins-\([0-9]*\)\.inc/\1/' |
         sort -n |
         tail -1)  # number of frames
povray +KFI0 +KFF${NFRAME} -W2000 -H1500 +Ometa/conf-.png spins.pov


#######################################
# clean
#######################################
rm $EXCOUT
cd $SRC
