#!/bin/bash
outfolder=/uboone/data/users/mibass/cosmics/MuCS/Rates

cryfile=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs20-25_not21.root
cryfile26=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs26.root
cryfile27=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs27.root
cryfile28=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs28.root
cryfile30=/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs30.root


#python rates.py $outfolder/testbs23 23 1000 $cryfile -b  
#python rates.py $outfolder/testbs26 26 1000 $cryfile26 -b
#python rates.py $outfolder/testbs27 27 1000 $cryfile27 -b
#python rates.py $outfolder/testbs28 28 1000 $cryfile28 -b
python rates.py $outfolder/testbs30 30 1000 $cryfile30 -b

