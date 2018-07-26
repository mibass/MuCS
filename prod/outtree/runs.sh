#!/bin/bash

anatype=MuCSPTAL
#anatype=MuCSMPTAL
#anatype=MuCSMETAL

dataversion=v05_08_00
mcversion=v05_08_00
DAGHeader () {
  echo "<parallel>" > $1
}

DAGFooter () {
  echo "</parallel>" >> $1
}


FindMCFile () {
  #echo $1
  tbn=$1
  IFS='-' read -r -a array <<< "$tbn"
  run=${array[2]}
  subruna=${array[3]}
  IFS='_' read -r -a array <<< "$subruna"
  subrun=${array[0]}
#  echo "found run=$run and subrun=$subrun"
  
  #find the right mc file
  afile=`find $2/*/*.root |grep ${run}-${subrun}`
  #find it's directory
  bdir=$(dirname "${afile}")
  if [[ -z "${afile// }" ]]; then
    echo NONE
  else
    echo $bdir/MuCSMETA_anatree.root
  fi
}


DoRunSet () {
  #$1 = run number
  #$2 = group number
  run=$1
  group=$2
  bs=$3
  pmtonly=$4
  nevents=$5
  suffix=$6 #output suffix
  mcsuffix=$7
  
  USAGE_MODEL="DEDICATED,OPPORTUNISTIC"
  #USAGE_MODEL="OPPORTUNISTIC"
  #$the rest are parameters to DoARun
  outputfilename=""
  dagoutputfile=./Runs_$1_$2${suffix}.dag
  echo "making dag file $dagoutputfile"
  
  
  #MuCSRecoPath=/pnfs/uboone/scratch/users/mibass/MuCS/$version/MuCSReco/Run${run}_Group${group}
  #AnaPath=/pnfs/uboone/scratch/users/mibass/MuCS/$version/ana/Run${run}_Group${group}
  MuCSRecoPath=/pnfs/uboone/scratch/users/mibass/MuCS/${dataversion}/${anatype}/MuCSRun${run}_Group${group}/*
  MCFILEDIR="/pnfs/uboone/scratch/users/mibass/MuCS/${mcversion}/mcana${mcsuffix}/MuCSRun${run}_Group${group}/"
  #OutTreePath=/uboone/data/users/mibass/MuCS/$version/outtree/Run${run}_Group${group}
  OutTreePath=/pnfs/uboone/scratch/users/mibass/MuCS/${mcversion}/outtree/MuCSRun${run}_Group${group}${suffix}
  mkdir -p $OutTreePath
  
  DAGHeader $dagoutputfile
  
  #for f in $MuCSRecoPath/*MuCSMETA.root
  for f in $(find $MuCSRecoPath/*MuCSMETA.root)
  do
    bn=${f##*/}
    bdir=$(dirname "${f}")
    MCfile=$(FindMCFile $bn $MCFILEDIR)
#    echo "Found MC File $MCfile, looking for $bn, in $MCFILEDIR"
    #anafile=$AnaPath/${bn/.root/}_ana.root
    anafile=$bdir/MuCSMETA_anatree.root
    outfile=$OutTreePath/${bn/.root/}_outtree.root
    rm -f $outfile
    
    #python processEvents.py $anafile $MCFILE $f $nevents 0 $outfile -b
    echo jobsub -n -G uboone --OS=SL5,SL6 --resource-provides=usage_model=$USAGE_MODEL --memory=4000MB file://`pwd`/grid_runOne.sh ${mcversion} ${anafile} ${MCfile} ${f} ${nevents} ${outfile} ${bs} ${pmtonly} `pwd`/processEvents.py >> $dagoutputfile
    #break
  done    
  
  DAGFooter $dagoutputfile
  echo "wrote dag file $dagoutputfile"
  jobsub_submit_dag -G uboone file://$dagoutputfile
}


MergeSet () {
  run=$1
  group=$2
  suffix=$3
  
  ubdatapath=/uboone/data/users/mibass/MuCS/$mcversion/outtree/MuCSRun${run}_Group${group}${suffix}
  rm -rf $ubdatapath
  mkdir -p $ubdatapath
  OutTreePath=/pnfs/uboone/scratch/users/mibass/MuCS/$mcversion/outtree/MuCSRun${run}_Group${group}${suffix}
  ifdh cp -D $OutTreePath/ $ubdatapath/
  
  #MergedOutTreePath=/pnfs/uboone/scratch/users/mibass/MuCS/$mcversion/MergedOuttree/MuCSRun${run}_Group${group}
  MergedOutTreePath=/uboone/data/users/mibass/MuCS/MuCS/$mcversion/MergedOuttree/MuCSRun${run}_Group${group}${suffix}
  mkdir -p $MergedOutTreePath
  outfile=${MergedOutTreePath}_MergedTree.Root
  rm -f $outfile
  
  find $ubdatapath/*.root > /tmp/mib_tmp.txt
  hadd -f -k $outfile @/tmp/mib_tmp.txt
  
  #cleanup
  rm $ubdatapath/*.root
  
}

#anatype=MuCSPTAL
anatype=MuCSMPTAL
#anatype=MuCSMETAL

#DoRunSet 3702 158 30 0 50
#DoRunSet 3702 158Deconv 30 0 50
#DoRunSet 3702 158_pdfreco 30 0 50
#DoRunSet 3702 158 30 0 50 500MeV 500MeV
#DoRunSet 3702 158_pdfreco 30 0 50 BigExtension BigExtension
#DoRunSet 3702 158 30 0 50 CORSIKA CORSIKA
#DoRunSet 3678 153 30 0 50
#DoRunSet 3355to3360 144 30 0 50
#DoRunSet 6268to6269 166 32 0 50
#DoRunSet 7106 167_pdfreco 30 0 50
#DoRunSet 7263 180 33 0 50
#DoRunSet 7264 180 33 0 50
#DoRunSet 7265 180 33 0 50
#DoRunSet 7347 181 34 0 50
#DoRunSet 7348 181 34 0 50
#DoRunSet 7702 182 35 0 50
#DoRunSet 7703 183 35 0 50

#pmtonly runs
#DoRunSet 7177 169 30 1 1000
#DoRunSet 7180 170 30 1 1000
#DoRunSet 7186 171 30 1 1000
#DoRunSet 7191 172 30 1 1000 #????????????????
#DoRunSet 7193 173 30 1 1000

#MergeSet 3702 158
#MergeSet 3702 158Deconv
#MergeSet 3702 158_pdfreco
#MergeSet 3702 158_pdfreco BigExtension
#MergeSet 3702 158 CORSIKA
#MergeSet 3702 158 500MeV
#MergeSet 3678 153  
#MergeSet 6268to6269 166
#MergeSet 7106 167_pdfreco
#MergeSet 7177 169
#MergeSet 7180 170
#MergeSet 7186 171
#MergeSet 7191 172
#MergeSet 7193 173
#MergeSet 7263 180
#MergeSet 7264 180
#MergeSet 7265 180
#MergeSet 7347 181
#MergeSet 7348 181
#MergeSet 7702 182
#MergeSet 7703 183

#test run
#ana=/pnfs/uboone/scratch/users/mibass/MuCS/v05_08_00/MuCSMPTAL/MuCSRun3702_Group158_pdfreco/11074247_0/MuCSMETA_anatree.root
##mcana=/pnfs/uboone/scratch/users/mibass/MuCS/v05_08_00/mcana/MuCSRun6268to6269_Group166//10100867_81/MuCSMETA_anatree.root
#mcana=NULL
#art=/pnfs/uboone/scratch/users/mibass/MuCS/v05_08_00/MuCSMPTAL/MuCSRun3702_Group158_pdfreco/11074247_0/BeamOff-2015_11_12_10_55_48-0003702-00032_20160614T003158_rawprescale_20160614T071402_reco1_20160614T174334_reco2_MuCSDT_MuCSMETA.root
#outfile=t.root

#python ./processEvents.py $ana $mcana $art 50 0 $outfile 30 -b



