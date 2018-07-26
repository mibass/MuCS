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


gStyle.SetPalette(51)
gROOT.ForceStyle()


outfilePrefix=sys.argv[1]
argbs=int(sys.argv[2])
iFindAllBoxesMode=int(sys.argv[3]) #0 - store all, 1 - store coincidences, 2 - store missed
if iFindAllBoxesMode==0:
  bStoreFound=True
  bStoreNotFound=True
  bFakeRate=False
elif iFindAllBoxesMode==1:
  bStoreFound=True
  bStoreNotFound=False
  bFakeRate=False
elif iFindAllBoxesMode==2:
  bStoreFound=False
  bStoreNotFound=True
  bFakeRate=False
   
nfoundlimit=int(sys.argv[4]) #total limit on found muons
nlimit=int(sys.argv[5]) #total limit number of events to process
iorboxes=int(sys.argv[6]) #0 - AND of boxes, 1- OR of boxes, 2 TPC muons (store all muons going through tpc)
bOrBoxes=(True if iorboxes==1 else False)
bTPCmuons=(True if iorboxes==2 else False)
file=sys.argv[7]
inmuons=sys.argv[8]

if inmuons!="0":
  #load muons with jentry, ngeant, pdg, Mother, TrackId, processname, Eng, Mother_ngeant, Mother_pdg, Mother_eng, Primary_ngeant, Primary_pdg, Primary_Eng, lastDaughterStartx, lastDaughterStarty, lastDaughterStartz from inmuons txt file
  muonslist=[line.split(' ') for line in open(inmuons)]
  
geo=geom()
bs=boxsetup3d(argbs,False)

outfile=outfilePrefix+"DannyTheVeto_b"+str(argbs)+".root"
print "Putting output in",outfile
tfout=TFile(outfile, "recreate")

plotext=".png"

def drawMuon(inBoxPoints):
  global geo
  geo.drawValidPoints(inBoxPoints)
  
def drawMuonWithDict(inBoxPoints,thisev):
  antipoints=[]
  antipoints.append(geo.getNewPos(thisev['StartPointx_tpcFV'], thisev['StartPointy_tpcFV'], thisev['StartPointz_tpcFV'],thisev['theta'],thisev['phi'],700))
  antipoints.append((thisev['StartPointx_tpcFV'], thisev['StartPointy_tpcFV'], thisev['StartPointz_tpcFV']))
  #print antipoints
  geo.drawValidPoints(antipoints)


def drawShowers(ne):
  global anatree
  nepoints=((anatree.StartPointx[ne], anatree.StartPointy[ne], anatree.StartPointz[ne]),(anatree.EndPointx[ne], anatree.EndPointy[ne], anatree.EndPointz[ne]))
  #print nepoints
  geo.drawValidPoints(nepoints,2)


anatree=TChain('analysistree/anatree')
anatree.Add(file)
entries=anatree.GetEntries()
anatree.SetBranchStatus("*",0)
for b in ("StartPointx", "StartPointy", "StartPointz","EndPointx", "EndPointy", "EndPointz", "StartPointx_tpcAV", "StartPointy_tpcAV", "StartPointz_tpcAV","pdg","TrackId","Mother","processname"):
  anatree.SetBranchStatus(b,1)

#tree to store nue-like bgs in
nueliketree=flatttree("nuelikes",["jentry/I","ngeant/I","pdg/I", "Mother/I", "TrackId/I", "iscomp/I", "isconv/I","Eng/F", "Mother_ngeant/I", "Mother_pdg/I", "Mother_Eng/F", "Primary_ngeant/I", "Primary_pdg/I", "Primary_Eng/F","muon_inTPCActive/I","muon_inMTG/I","StartPointx_tpcAV/F", "StartPointy_tpcAV/F", "StartPointz_tpcAV/F"])

print "Total anatree entries: ", entries
anatree.GetEntry(anatree.GetEntries()-1)
print "Total muonslist entries: ", len(muonslist)


#draw boxes
for b in bs: geo.drawbox(b)

ntotal=len(muonslist)
nMTG=0 #muons in MTG
nentries=0 #number of entries processed in muonslist
tpccount=0 #muons in tpc
#loop over events
totalEvents=0 #total number of events processed

if nfoundlimit>0 or nlimit>0:
  for imi in xrange(len(muonslist)):
    if imi==0 or muonslist[imi][0]!=muonslist[imi-1][0]: #only load next event if it's not already loaded
      anatree.GetEntry(int(muonslist[imi][0]))
      totalEvents+=1
    ngeant=int(muonslist[imi][10]) #ngeant entry of primary causing this nuelike 
    ne=int(muonslist[imi][1]) #ngeat of nuelike
    muon_inTPCActive=0
    muon_inMTG=0

    if abs(anatree.pdg[ngeant])==13:
      if anatree.inTPCActive[ngeant]==1: # use start and tpc start
        #get angles from vector between startpoint and tpc startpoint
        thistheta,thisphi,ld=geo.getThetaPhiLDFromLine((anatree.StartPointx[ngeant], anatree.StartPointy[ngeant], anatree.StartPointz[ngeant]),(anatree.StartPointx_tpcAV[ngeant], anatree.StartPointy_tpcAV[ngeant], anatree.StartPointz_tpcAV[ngeant]))
        #make a dict to pass to getNewPosInBox3d
        thisev={'StartPointx_tpcFV':anatree.StartPointx_tpcAV[ngeant],'StartPointy_tpcFV':anatree.StartPointy_tpcAV[ngeant], 'StartPointz_tpcFV':anatree.StartPointz_tpcAV[ngeant],'theta':thistheta,'phi':thisphi}
      else: # use start and start from daughters start position in muonslist
        thistheta,thisphi,ld=geo.getThetaPhiLDFromLine((anatree.StartPointx[ngeant], anatree.StartPointy[ngeant], anatree.StartPointz[ngeant]),(float(muonslist[imi][13]), float(muonslist[imi][14]), float(muonslist[imi][15])))
        #make a dict to pass to getNewPosInBox3d
        thisev={'StartPointx_tpcFV':float(muonslist[imi][13]),'StartPointy_tpcFV':float(muonslist[imi][14]), 'StartPointz_tpcFV':float(muonslist[imi][15]),'theta':thistheta,'phi':thisphi}      
      (bAllBoxes,inBoxPoints,posinboxes)=geo.getNewPosInBox3d(thisev,bs)
      


      #is in tpc?
      if posinboxes[-1]:
        tpccount+=1
        muon_inTPCActive=1
        
      #is in MTG?
      bMTG=False
      for box in xrange(len(posinboxes)-1):
        bMTG=bMTG or posinboxes[box]      
      if bMTG: 
        muon_inMTG=1
        nMTG+=1
      
      #muon drawing
      if bStoreFound and bMTG and nfoundlimit<=1000 and nlimit<=1000: #make sure we don't draw too much
        drawMuon(inBoxPoints)
        if nlimit<=5: drawShowers(ne)
        
      if bStoreNotFound and not bMTG and nentries<=1000 and nlimit<=1000:
        drawMuonWithDict(inBoxPoints,thisev)
        if nlimit<=10: drawShowers(ne)
        

          
      nentries+=1
    
    #fill nueliketree for this row
    #nueliketree.fill((int(muonslist[imi][0]),int(muonslist[imi][1]),int(muonslist[imi][2]), int(muonslist[imi][3]), int(muonslist[imi][4]), int(muonslist[imi][5]=="compt"), int(muonslist[imi][5]=="conv"),float(muonslist[imi][6]), int(muonslist[imi][7]), int(muonslist[imi][8]), float(muonslist[imi][9]), int(muonslist[imi][10]), int(muonslist[imi][11]), float(muonslist[imi][12]),int(muon_inTPCActive),int(muon_inMTG),anatree.StartPointx_tpcAV[ne],anatree.StartPointy_tpcAV[ne],anatree.StartPointz_tpcAV[ne]))
    
    if (nMTG>=nfoundlimit and nfoundlimit>0) or (totalEvents>=nlimit and nlimit>0): 
      break  
    if totalEvents%100==0: 
      print "Event ", totalEvents,"\r",
      sys.stdout.flush()                  
  

if iFindAllBoxesMode%3==0:
  print "Looking for all"
elif iFindAllBoxesMode%3==1:
  print "Looking for Coincidence"
elif iFindAllBoxesMode%3==2:
  print "Looking for Anticoincidence" 
  
#print "Through",("either box" if bOrBoxes else "both boxes")
#print "found ", found, " in ", ncur, "(",float(found)/ncur,")"

print "Number nuelikes with muon in MTG:", nMTG
print "Number nuelikes with muon in TPC:", tpccount
if tpccount>0: print "Nuelikes Tagged Rate:", float(nMTG)/tpccount
totalEventTime=totalEvents*6.4e-3
print "total number of events looked at:", totalEvents
print "total time elapsed:", totalEventTime
if totalEventTime>0: print "tpc rate:", float(tpccount)/totalEventTime
print "looked at", nentries, "entries in muonslist"

#store output hists
geo.close(tfout)
nueliketree.close(tfout)
tfout.Close()



        

