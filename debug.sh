#!/bin/bash

#########################################
## slurm
#########################################
#SBATCH --job-name=mn3sn
#SBATCH --output=./proc.log
#SBATCH --partition=all  
##SBATCH --nodelist=r3 
##SBATCH --exclude=r2,r3,r4,r5
#SBATCH --ntasks=1       
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --array=0-0:1  ## start and end indices are included


#########################################
## configuration
#########################################
STEP=500000
INCR=$(echo "${STEP} / 5000" | bc)
TEMP=0.0
ISO1=0.0
DMI1=1e-22
ISO2=0.0
DMI2=0.0
ISO3=$(awk -v x="$ISO1" 'BEGIN{print -0 * x}')
AISO=0.0
DAMP=1.0
## Gamma 5x
ISD1="-1,-1,0"
ISD2="-1,+1,0"
ISD3="1,0,0"
## Gamma 3x
##ISD1="-1,+1,0"
##ISD2="-1,-1,0"
##ISD3="1,0,0"
## coordinate axes
##ISD1="1,0,0"
##ISD2="0,1,0"
##ISD3="0,0,1"
## random
##ISD1="random"
##ISD2="random"
##ISD3="random"


########################################
## paths
########################################
SRC="$(pwd)/"
DATE="$(date +'%y%m%d-%H%M%S')-$(date +%N | cut -c1-6)"  ## date
OUT="${SRC}../../data/${SLURM_ARRAY_JOB_ID}/${DATE}-${DMI1/\./}/"  ## path output directory
CNFSRC="${SRC}conf/ws/"  # source of configuration files
CNFOUT="${OUT}conf/"  # destination of configuration files
VAMP="vampire-cuda"  # Vampire file base name
EXCSRC="${SRC}${VAMP}"  ## Vampire executable in source directory
EXCOUT="${OUT}${VAMP}"  ## Vampire executable in source directory
VDC="${SRC}util/vdc/vdc"  ## Vampire to povray converter
META="${OUT}meta/"  ## meta data 
LOG="${OUT}proc.log"  ## logfile with std output


########################################
## prepare input and output
########################################
mkdir -p "$META" "$CNFOUT"
cp $EXCSRC ${BASH_SOURCE[0]} $OUT
cp $EXCSRC $EXCOUT
prepCnf $CNFSRC      \
        $CNFOUT      \
        "STEP=$STEP" \
        "INCR=$INCR" \
        "TEMP=$TEMP" \
        "ISO1=$ISO1" \
        "DMI1=$DMI1" \
        "ISO2=$ISO2" \
        "DMI2=$DMI2" \
        "ISO3=$ISO3" \
        "AISO=$AISO" \
        "DAMP=$DAMP" \
        "ISD1=$ISD1" \
        "ISD2=$ISD2" \
        "ISD3=$ISD3"


########################################
## run
########################################
cd $OUT
## run simulation
srun --output="$LOG"                       \
     $EXCOUT --input-file "${CNFOUT}input" \
             --output-file "result"
## create povray file
$VDC --povray                    \
     --input-file "atoms-coords" \
     --vector-z 1,1,0            \
     --slice 0,1,0,1,0,1
## render spin configuration
NFRAME=$(find ${OUT} -name 'spins-*.inc' -printf '%f\n' |
         sed 's/spins-\([0-9]*\)\.inc/\1/' |
         sort -n |
         tail -1)  ## number of frames
povray -W2000              \ 
       -H1500              \
       -D                  \
       +KFI0               \
       +KFF${NFRAME}       \
       +O${META}/conf-.png \
       ${OUT}spins.pov 


########################################
## clean
########################################
rm $EXCOUT
##cd $SRC
