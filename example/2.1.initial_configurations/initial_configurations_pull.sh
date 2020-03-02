#!/bin/bash

# Use . as the decimal separator
export LC_NUMERIC=en_US.UTF-8

# Rang and spacing of the reaction coordinate
MIN_WINDOW=0.1
MAX_WINDOW=3.8
WINDOW_STEP=0.1

for window in $(seq ${MIN_WINDOW} ${WINDOW_STEP} ${MAX_WINDOW})
do

#  mkdir $window

#  cp *.mdp $window

  cd $window

#  sed "s/POS1/$window/g" -i pull.mdp
#  sed "s/POS1/$window/g" -i em.mdp 
#  sed "s/POS1/$window/g" -i em2.mdp 
#  sed "s/POS1/$window/g" -i eq.mdp

#  gmx grompp -f pull.mdp -c ../start.gro -p ../../2.0.parameters/topol.top -o pull.tpr
  gmx mdrun -nt 1 -deffnm pull -v &> pullrun.log

#  gmx grompp -f em.mdp -c pull.gro -p ../../2.0.parameters/topol.top  -o em.tpr
#  gmx mdrun -nt 1 -deffnm em -v  &> emrun.log

#  gmx grompp -f em2.mdp -c em.gro -p ../../2.0.parameters/topol.top  -o em2.tpr
#  gmx mdrun -nt 1 -deffnm em2 -v &> em2run.log

#  gmx grompp -f eq.mdp -c em2.gro -p ../../2.0.parameters/topol.top  -o eq.tpr
#  gmx mdrun -nt 1 -deffnm eq -v -px eq_x -pf eq_f &> eqrun.log

  cd ../

done
