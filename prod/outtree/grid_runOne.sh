#!/bin/bash
set -x #echo on


source /grid/fermiapp/products/common/etc/setups.sh
source /grid/fermiapp/products/uboone/setup_uboone.sh

ver=$1
inputana=$2
inputMC=$3
inputMuCSReco=$4
nevents=$5
outfile=$6
bs=$7
pmtonly=$8
inputscript=$9
startevent=0

setup uboonecode $ver -q e9:prof
bnana=${inputana##*/}
bnMuCSReco=${inputMuCSReco##*/}
bnoutput=${outfile##*/}
bninputscript=${inputscript##*/}

cd $_CONDOR_SCRATCH_DIR

ifdh cp -D ${inputana} ${inputMuCSReco} ${inputscript} ./
ifdh cp ${inputMC} ./mcanatreeinput.root
ifdh cp -D /uboone/app/users/mibass/cosmics/MuCS/common/boxsetups.py /uboone/app/users/mibass/cosmics/MuCS/common/geom.py /uboone/app/users/mibass/cosmics/MuCS/common/flatttree.py /uboone/app/users/mibass/cosmics/MuCS/preselected/dataHelper.py ./

bnMC=mcanatreeinput.root

pwd
ls

echo $UBOONECODE_INC
cp $UBOONECODE_INC/uboone/MuCS/MuCSData.h ./
cp $UBOONECODE_INC/uboone/MuCS/MuCSRecoData.h ./

#do the thing
python ${bninputscript} ./$bnana ./$bnMC ./$bnMuCSReco $nevents 0 ./$bnoutput ${bs} ${pmtonly} -b

#copy output file to appropriate place
ifdh cp ./$bnoutput $outfile

