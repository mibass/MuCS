#!/bin/sh

N=10000

outdir=/uboone/data/users/mibass/cosmics/MuCS/DannyTheVeto/plots

#ingeantfile=/uboone/data/uboonerd/cosmogenics/cosmics_newgeom_noOB_10MeVcut_merged_anahist.root
ingeantfile=/uboone/data/users/mibass/corsika/corsikaTFG/anatree_corsikaF_CMC_20k_NoXCorrection_noOB_10MeV_v04_14_00.root

muonslist=$outdir/nuelikes.dat


wait



doSet() {
  bs=$1
  #python rates_DannyTheVeto.py $outdir/devito_draw $bs 2 0 0 0 $ingeantfile $muonslist -b &
  python rates_DannyTheVeto.py $outdir/devito_coin_OR $bs 1 0 $N 1 $ingeantfile $muonslist -b #> $outdir/devito${bs}_output_coin
  #python rates_DannyTheVeto.py $outdir/devito_anti_OR $bs 2 0 $N 1 $ingeantfile $muonslist -b > $outdir/devito${bs}_output_anti
  wait
}

for i in `seq 5 10`; do
  doSet $i
done

#doSet 10





#anatree loop to export list of conv's and compts
#echo "gROOT->LoadMacro(\"anatree.C+\");TChain t(\"analysistree/anatree\");t.Add(\"$ingeantfile\"); anatree m(t.GetTree()); m.Loop(); gSystem->Exit(0);" | root -b -l > $muonslist


#process nulikestree output

#python process_nuelikes.py $outdir/devito_coin_ORDannyTheVeto_b5.root 1 >$outdir/process_all.txt -b

doProcessSet() {
  python process_nuelikes.py $outdir/devito_coin_ORDannyTheVeto_b$1.root 0 >$outdir/process_mtg_$1 -b
}

#for i in `seq 5 14`; do
#  doProcessSet $i
#done
