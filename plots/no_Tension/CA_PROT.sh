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
       cp ../CA.ndx .
       if [ -e index.ndx ]; then
          for CA in {1..18}
          do
             echo $CA
             groupN=$(( $CA + 27 ));
             echo "48
                   ${groupN}" | gmx density -s  ENTH_MEMB.tpr -f ENTH_MEMB.xtc -o CA_${CA}.xvg -center -sl 2000 -n CA.ndx; 
          done
          echo "25
                48" | gmx density -s  ENTH_MEMB.tpr -f ENTH_MEMB.xtc -n CA.ndx -o Phos.xvg -center -sl 2000;
       fi
       cd ..
    fi
done
