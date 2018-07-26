#!/bin/bash
#process output from MCSMuons larsoft module
outfolder=/uboone/data/users/mibass/cosmics/MuCS/MClib

#make input file list
#find /pnfs/uboone/scratch/users/mibass/MCS/v04_08_01/MCSMuons/MCSmuons_bs20/*|grep standard_reco_hist.root >$outfolder/inputlist_processtfg_bs20.txt
#find /pnfs/uboone/scratch/users/mibass/MCS/v04_08_01/MCMuons/MCSmuons_bs21/* |grep standard_reco_hist.root >$outfolder/inputlist_processtfg_bs21.txt

#python process_tfg.py 20 ${outfolder}/angular_mcs_bs20_MERGED.root $outfolder/inputlist_processtfg_bs20.txt -b
#python process_tfg.py 21 ${outfolder}/angular_mcs_bs21_MERGED.root $outfolder/inputlist_processtfg_bs21.txt -b
