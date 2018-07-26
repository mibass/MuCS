import os,sys,string
import ROOT
from math import *
from ROOT import TTree, TH1F, TCanvas, gROOT, TGaxis, gStyle, TColor, TLegend, THStack, TChain, TEntryList, TLine, TView
from ROOT import *
from array import array
sys.path.insert(0, '../common/')
from flatttree import *
from geom import *
from boxsetups import *


argfile=sys.argv[1]
argall=int(sys.argv[2])

nuelikes=TChain('nuelikes')
nuelikes.Add(argfile)

nEvents=nuelikes.GetMaximum("jentry")+1
totalTime=nEvents*6.4e-3
ScaleToTime=211
ScaleFactor=ScaleToTime/totalTime

print "Number of events:",nEvents
print "Using scalefactor:",ScaleFactor

#fv cut, plus only look at electrons (pair production energy cut is on mother's energy, so it's sufficient to only count electrons)
#FVCut="StartPointx_tpcAV>25 && StartPointx_tpcAV<231.5 && StartPointy_tpcAV>91.5 && StartPointy_tpcAV>-91.5 && StartPointz_tpcAV>30 && StartPointz_tpcAV<986.8 && pdg==11"
FVCut="pdg==11"


if argall==1:
  r1=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==0 && Eng>0.2 && muon_inTPCActive==1 && %s"% FVCut,"goff")
  r2=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==1 && Mother_Eng>0.2 && muon_inTPCActive==1 && %s"% FVCut,"goff")
  r3=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==0 && Eng>0.2 && muon_inTPCActive==0 && %s"% FVCut,"goff")
  r4=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==1 && Mother_Eng>0.2 && muon_inTPCActive==0 && %s"% FVCut,"goff")
else:
  r1=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==0 && Eng>0.2 && muon_inTPCActive==1 && muon_inMTG==1 && %s"% FVCut,"goff")
  r2=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==1 && Mother_Eng>0.2 && muon_inTPCActive==1 && muon_inMTG==1 && %s"% FVCut,"goff")
  r3=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==0 && Eng>0.2 && muon_inTPCActive==0 && muon_inMTG==1 && %s"% FVCut,"goff")
  r4=nuelikes.Draw("1","abs(Primary_pdg)==13 && isconv==1 && Mother_Eng>0.2 && muon_inTPCActive==0 && muon_inMTG==1 && %s"% FVCut,"goff")


rates=(r1,r2,r3,r4)

def nscaled(r,scale):
  err=sqrt(r)
  return scale*r,scale*err


for r in rates:
  rs,err=nscaled(r,ScaleFactor)
  
  print int(rs),"+-",int(err),"      ",nscaled(r,1.)
