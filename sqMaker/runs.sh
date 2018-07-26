#!/bin/bash
mclibpath=/uboone/data/users/mibass/cosmics/MuCS/MClib
dboutpath=/uboone/data/users/mibass/cosmics/MuCS/sqMaker

#rm MClib_bs30.sqlite; python sqMaker.py $mclibpath/angular_nom_bs30_MERGED.root MClib_bs30.sqlite -b
#mv MClib_bs30.sqlite $dboutpath

rm MClib_bs32.sqlite
python sqMaker.py $mclibpath/angular_nom_bs32_MERGED.root MClib_bs32.sqlite -b
mv MClib_bs32.sqlite $dboutpath

#rm MClib_bs33.sqlite
#python sqMaker.py $mclibpath/angular_nom_bs33_MERGED.root MClib_bs33.sqlite -b
#mv MClib_bs33.sqlite $dboutpath

#rm MClib_bs34.sqlite
#python sqMaker.py $mclibpath/angular_nom_bs34_MERGED.root MClib_bs34.sqlite -b
#mv MClib_bs34.sqlite $dboutpath

#rm MClib_bs35.sqlite
#python sqMaker.py $mclibpath/angular_nom_bs35_MERGED.root MClib_bs35.sqlite -b
#mv MClib_bs35.sqlite $dboutpath
