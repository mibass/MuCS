#!/bin/bash

version=v05_08_00
trackalg=trackkalmanhit

makeTFGSet () {
  run=$1
  group=$2
  N=$3
  Nperfile=$4

  infile=/pnfs/uboone/scratch/users/mibass/MuCS/$version/outtree/MuCSRun${run}_Group${group}/*.root
  outtfgfolder=/uboone/data/users/mibass/MuCS/$version/TFGOutputs/MuCSRun${run}_Group${group}_$trackalg
  
  mkdir -p $outtfgfolder
  rm -rf $outtfgfolder/*.txt
  
  python OutTreeToTFG.py "$infile" $outtfgfolder ${outtfgfolder}_TFGtesttree.root $N $Nperfile $trackalg -b
  
}


#makeTFGSet 3702 158 17200 30
