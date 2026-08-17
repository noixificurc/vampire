#!/bin/bash

#-----------------------
# configuration
#-----------------------
VAMP=./vampire-parallel
NCPU=$(nproc --ignore=6)
VDC=./util/vdc/vdc



#-----------------------
# clealing
#-----------------------
rm spins-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]\.* spins\.pov  spins[0-9]*\.png


#-----------------------
# run
#-----------------------
mpirun -n $NCPU $VAMP
$VDC --povray
povray +KFI0 +KFF20 -W2000 -H1500 spins.pov

