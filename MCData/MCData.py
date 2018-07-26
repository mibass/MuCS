#make data tree, from cry mc, that mimics data 
import os,sys,string
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile, TChain, TGraph, TBox, TLegend
from math import *
from array import array
sys.path.insert(0, '../common/')
from flatttree import *
from geom import *
from boxsetups import *


outfilePrefix=sys.argv[1]
argbs=int(sys.argv[2])
nfoundlimit=int(sys.argv[3])
filecry=sys.argv[4]
btfgoutput=(sys.argv[5]=="1")
tfgoutputdir=sys.argv[6]
if nfoundlimit>0: print "Limiting found entries to:", nfoundlimit

foutstr=outfilePrefix+"MCDataOutput_b"+str(argbs)+".root"
print "Puttting output into", foutstr
tfout=TFile(foutstr, "recreate")

#filecry="/uboone/data/users/mibass/cosmics/cry/onlymuons/genroot_1.root"
#filecry="/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_onlymuons_bs20-25_not21.root"

anatree=TChain('anatree')
anatree.Add(filecry)
entries=anatree.GetEntries()
print "total cry entries: ", entries

geo=geom()
bs=boxsetup3d(argbs,False)

#variables for tfg output
lc=0
linesPerEvent=1
eventsPerFile=500
tfgouttemplate=tfgoutputdir+"/MuCSMuons_bs%s_%d.txt"
tfgfilecount=1
if btfgoutput: tfgfile=open(tfgouttemplate%(argbs,tfgfilecount),'w')
lbuffer=[]
eventCount=0

def writeLine(line):
  global tfgfile, tfgouttemplate, tfgfilecount, maxlinesperevent, lbuffer, eventCount
  #tfgfile.write(line)
  lbuffer.append(line)
  if len(lbuffer)==linesPerEvent:
    #write lbuffer to file, prepending the event number and linecount
    writeLinesToFile(eventCount, len(lbuffer), lbuffer)
    lbuffer[:]=[]
    eventCount+=1
    if eventCount%eventsPerFile==0 and eventCount>0:
      tfgfilecount+=1
      #eventCount=0

def writeLinesToFile(eventNumber, particleCount, lines):
  global tfgouttemplate
  fname=tfgouttemplate%(argbs,tfgfilecount)
    
  with open(fname, 'a') as f:
    f.write("%d %d\n"%(eventNumber, particleCount))
    for line in lines:
      f.write("%s" % line)
    f.close()
    
def writeTFG(ev):
  ##TextFileGen Output: status code << PDG code << first mother << second mother << first daughter << second daughter << Px << Py << Pz << energy << mass << x << y << z << time of particle production
  #1 -13 0 0 0 0 -0.0661634 -0.406499 -0.380253 0.570417 0.10566 -73.015 1800 2009.14 2.04924e+06
  
  line="1" #status code
  line+=" "+str(ev.cry_pdg)
  line+=" 0" #first mother
  line+=" 0" #second mother
  line+=" 0" #first daughter
  line+=" 0" #second daughter
  line+=" "+"%f"%ev.cry_Px
  line+=" "+"%f"%ev.cry_Py
  line+=" "+"%f"%ev.cry_Pz
  line+=" "+"%f"%ev.cry_Eng
  line+=" "+"%f"%ev.cry_mass
  line+=" "+"%f"%ev.StartPointx_tpcFV
  line+=" "+"%f"%ev.StartPointy_tpcFV
  line+=" "+"%f"%ev.StartPointz_tpcFV
  line+=" "+"%f\n"%(fmod(ev.cry_t,4.8e-3)-1.6e-3)
  
  writeLine(line)



found=0
ncur=0
for b in bs: geo.drawbox(b)
ftree=flatttree("preselected",["s1[12]/I","s2[12]/I","s3[12]/I","s4[12]/I","s5[12]/I","s6[12]/I","s7[12]/I","s8[12]/I",
"true_theta/D", "true_phi/D","true_thetaxy/D","true_thetayz/D", "true_cry_Eng/D", "true_cry_pdg/I","true_cry_t/D","true_Start[3]/D","true_TPCStart[3]/D","true_TPCEnd[3]/D"])

def ba(bx):
  #build hit list
  l=[]
  for i in xrange(12):
    if i>len(bx)-1:
      l.append(-1)
    else:
      l.append(bx[i])
  return l

for ev in anatree:
  #fix angles coming out of cry  
  thistheta,thisphi=geo.getThetaPhiFromLD((ev.cry_Px/ev.cry_P,ev.cry_Py/ev.cry_P,ev.cry_Pz/ev.cry_P))
  #thisphi+=pi
  #binallboxes,posb,posinbox=geo.getNewPosInBox3d(ev,bs)
  binallboxes,posb,posinbox=geo.getNewPosInBox3d(ev,bs,True,thistheta,thisphi)



  if not binallboxes: 
    ncur+=1
    continue
  found+=1
  print "Found ",found," coincidences at t=", ev.cry_t, "(%0.2f Hz)"%(found/ev.cry_t)
  
  if nfoundlimit<=1000:
    if binallboxes and posinbox[8]:
      geo.drawpoint(posb, 10, ROOT.kGray)
    else:
      geo.drawpoint(posb, 8, ROOT.kRed)
  
  
  #find out which strips these points go through
  bhits,trigger=bs.getHitPatternAndTrigger(posb[0:8])
  ld=geo.getDirectionVector(thistheta,thisphi)
  theta_xy=atan2(ld[1],ld[0])
  theta_yz=atan2(ld[1],ld[2])
  
  
  #print "reco top tpc pos", recoPs['postpctop']
  #print "reco bottom tpc pos", recoPs['postpcbottom']
  if btfgoutput: writeTFG(ev)
  ftree.fill([ba([bhits[0]]),ba([bhits[1]]),ba([bhits[2]]),ba([bhits[3]]),ba([bhits[4]]),ba([bhits[5]]),ba([bhits[6]]),ba([bhits[7]]),
    thistheta,thisphi,theta_xy,theta_yz,ev.cry_Eng,ev.cry_pdg,ev.cry_t,
    posb[0],posb[8],posb[9]])
    
  if nfoundlimit>0 and found>=nfoundlimit: break
  
  ncur+=1
#store output hists
ftree.close(tfout)
tfout.cd()
geo.close(tfout)
tfout.Close()
#write remaining lbuffer to txt output file
if btfgoutput: writeLinesToFile(eventCount, len(lbuffer), lbuffer)
