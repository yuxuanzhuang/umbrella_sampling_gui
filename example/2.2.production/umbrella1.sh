#!/bin/bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

# Rang and spacing of the reaction coordinate
MIN_WINDOW=0.0
MAX_WINDOW=1.9
WINDOW_STEP=0.1

for window in $(seq ${MIN_WINDOW} ${WINDOW_STEP} ${MAX_WINDOW})
do

  mkdir $window

  cp md.mdp $window

  cd $window

  sed "s/POS1/$window/g" -i md.mdp

  gmx grompp -f md.mdp -c ../../2.1.initial_configurations/$window/eq.gro -p ../../2.0.parameters/topol.top -o md.tpr
  gmx mdrun -nt 6 -deffnm md  -v -px md_x -pf md_f -cpi md.cpt &> mdrun.log

  cd ../

done
