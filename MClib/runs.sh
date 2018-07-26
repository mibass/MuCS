#!/bin/bash
#generate MC libraries for MuCS configurations
#see ../common/boxsetups.py for box configurations
outfolder=/uboone/data/users/mibass/cosmics/MuCS/MClib
tfginputsfolder=/uboone/data/users/mibass/cosmics/MuCS/MClib/TextFileGenInputs

#testrun to get tdviews out of
#python MClibrary.py 20 1 1000 ${outfolder}/angular_tdviews_bs20_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 20 3 1000 ${outfolder}/angular_tdviews_bs20_ali.root 1 $tfginputsfolder -b
#python MClibrary.py 21 1 1000 ${outfolder}/angular_tdviews_bs21_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 26 1 1000 ${outfolder}/angular_tdviews_bs26_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 27 1 1000 ${outfolder}/angular_tdviews_bs27_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 28 1 1000 ${outfolder}/angular_tdviews_bs28_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 30 1 1000 ${outfolder}/angular_tdviews_bs30_nom.root 1 $tfginputsfolder -b
#python MClibrary.py 30 3 10 ${outfolder}/angular_tdviews_bs30_ali.root 1 $tfginputsfolder -b
#python MClibrary.py 32 1 1000 ${outfolder}/angular_tdviews_bs32_ali.root 1 $tfginputsfolder -b

#align and nominal: split into seperate runs
N=500000
#N=5000
#for i in {00001..00002};do
##  python MClibrary.py 21 1 $N ${outfolder}/angular_nom_bs21_$i.root $i $tfginputsfolder -b&
##  python MClibrary.py 21 3 $N ${outfolder}/angular_ali_bs21_$i.root $i $tfginputsfolder -b&
##  wait
##  python MClibrary.py 20 1 $N ${outfolder}/angular_nom_bs20_$i.root $i $tfginputsfolder -b&
##  python MClibrary.py 20 3 $N ${outfolder}/angular_ali_bs20_$i.root $i $tfginputsfolder -b&
##  wait
##  python MClibrary.py 22 1 $N ${outfolder}/angular_nom_bs22_$i.root $i $tfginputsfolder -b&
##  python MClibrary.py 22 3 $N ${outfolder}/angular_ali_bs22_$i.root $i $tfginputsfolder -b
##  wait
#  #python MClibrary.py 25 1 $N ${outfolder}/angular_nom_bs25_$i.root $i $tfginputsfolder -b&
#  #python MClibrary.py 25 3 $N ${outfolder}/angular_ali_bs25_$i.root $i $tfginputsfolder -b&
#  #wait
#  python MClibrary.py 30 1 $N ${outfolder}/angular_nom_bs30_$i.root $i $tfginputsfolder -b&
#  #python MClibrary.py 30 3 $N ${outfolder}/angular_ali_bs30_$i.root $i $tfginputsfolder -b&  
#  wait
#  #python MClibrary.py 31 1 $N ${outfolder}/angular_nom_bs31_$i.root $i $tfginputsfolder -b&
#   python MClibrary.py 32 1 $N ${outfolder}/angular_nom_bs32_$i.root $i $tfginputsfolder -b&
#  python MClibrary.py 33 1 $N ${outfolder}/angular_nom_bs33_$i.root $i $tfginputsfolder -b&
#  python MClibrary.py 34 1 $N ${outfolder}/angular_nom_bs34_$i.root $i $tfginputsfolder -b&
#  python MClibrary.py 35 1 $N ${outfolder}/angular_nom_bs35_$i.root $i $tfginputsfolder -b&
#done
#wait

#merge them together:
#hadd -f -k ${outfolder}/angular_nom_bs21_MERGED.root ${outfolder}/angular_nom_bs21_????[1].root
#hadd -f -k ${outfolder}/angular_ali_bs21_MERGED.root ${outfolder}/angular_ali_bs21_????[1].root 
#hadd -f -k ${outfolder}/angular_nom_bs20_MERGED.root ${outfolder}/angular_nom_bs20_????[1].root
#hadd -f -k ${outfolder}/angular_ali_bs20_MERGED.root ${outfolder}/angular_ali_bs20_????[1].root 
#hadd -f -k ${outfolder}/angular_nom_bs22_MERGED.root ${outfolder}/angular_nom_bs22_????[1].root
#hadd -f -k ${outfolder}/angular_ali_bs22_MERGED.root ${outfolder}/angular_ali_bs22_????[1].root 
#hadd -f -k ${outfolder}/angular_nom_bs25_MERGED.root ${outfolder}/angular_nom_bs25_????[1].root
#hadd -f -k ${outfolder}/angular_ali_bs25_MERGED.root ${outfolder}/angular_ali_bs25_????[1].root 
#hadd -f -k ${outfolder}/angular_nom_bs30_MERGED.root ${outfolder}/angular_nom_bs30_????[1].root
#hadd -f -k ${outfolder}/angular_ali_bs30_MERGED.root ${outfolder}/angular_ali_bs30_????[1].root
hadd -f -k ${outfolder}/angular_nom_bs32_MERGED.root ${outfolder}/angular_nom_bs32_????[1].root
#hadd -f -k ${outfolder}/angular_nom_bs33_MERGED.root ${outfolder}/angular_nom_bs33_????[1].root
#hadd -f -k ${outfolder}/angular_nom_bs34_MERGED.root ${outfolder}/angular_nom_bs34_????[1].root
#hadd -f -k ${outfolder}/angular_nom_bs35_MERGED.root ${outfolder}/angular_nom_bs35_????[1].root

#mcs: one single run generates the full input list for prodatfg_bs??.xml
#N=1000000 #--> 100*14776300/101=14,630,000 muons, 146300 events
#python MClibrary.py 20 2 $N ${outfolder}/angular_MCSin_bs20_0.root 1 $tfginputsfolder -b
#python MClibrary.py 21 2 $N ${outfolder}/angular_MCSin_bs21_0.root 1 $tfginputsfolder -b
#move the last file of this to a name that won't be put into input list:
#mv $tfginputsfolder/MCSMuons_bs21_1464.txt $tfginputsfolder/NOTUSED_MCSMuons_bs21_1464.txt 

#generate input list:
#ls $tfginputsfolder/MCSMuons_bs21_*.txt > $tfginputsfolder/inputlist_bs21.txt # remove the last entry of this
#get number of events via `wc $tfginputsfolder/MCSMuons_bs21_*.txt`
#put this number into xml file










