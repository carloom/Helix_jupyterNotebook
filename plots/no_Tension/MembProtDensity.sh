#!/bin/bash
#SBATCH -J DenPlot
#SBATCH -o DenPlot.o%j
#SBATCH -t 150:00:00
#SBATCH -n 1 -N 1

#SBATCH --mail-type=ALL

#SBATCH --mail-user=carlosomerea89@gmail.com

module add   GROMACS

for file in $(ls)
do
    if [ -d $file ]; then
       cd $file
       if [ -e ENTH_MEMB.tpr ]; then
          echo "48 
                1" | gmx density -s  ENTH_MEMB.tpr -f ENTH_MEMB.xtc -n index.ndx -o protDen.xvg -center -sl 2000; 
          echo "48
                25" | gmx density -s  ENTH_MEMB.tpr -f ENTH_MEMB.xtc -n index.ndx -o Memb.xvg -center -sl 2000;
       fi
       cd ..
    fi
done
