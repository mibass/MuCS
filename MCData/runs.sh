#!/bin/bash

outdir=/uboone/data/users/mibass/cosmics/MuCS/MCData/
crymcfile=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs20-25_not21.root
crymcfilebs21=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs21.root
crymcfilebs30=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs30.root

tfgoutdir=/uboone/data/users/mibass/cosmics/MuCS/MCDataTFG/

#python MCData.py $outdir 25 700000 $crymcfile 0 $tfgoutdir -b&
#python MCData.py $outdir 21 20000 $crymcfilebs21 0 $tfgoutdir -b&
#python MCData.py $outdir 20 1200000 $crymcfile 0 $tfgoutdir -b&

python MCData.py $outdir 30 200000 $crymcfilebs30 0 $tfgoutdir -b
#python MCData.py ${outdir}Draw 30 1000 $crymcfilebs30 0 $tfgoutdir -b&


#TFG input generation
#python MCData.py ${outdir}/TFG 30 10000 $crymcfilebs30 1 $tfgoutdir -b

wait


