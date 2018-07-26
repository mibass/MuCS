#!/grid/fermiapp/products/larsoft/python/v2_7_8/Linux64bit+2.6-2.12/bin/python
import os,sys,string
import ROOT
from math import *
from ROOT import TTree, TH1F, TCanvas, gROOT, TGaxis, gStyle, TColor, TLegend, THStack, TChain, TEntryList, TLine, TView
from ROOT import *
from array import array
sys.path.insert(0, '../common/')
from boxsetups import *
from geom import *
from flatttree import *

#gROOT.SetStyle("astyle")
gStyle.SetPalette(51)
gROOT.ForceStyle()


outfilePrefix=sys.argv[1]
argbs=int(sys.argv[2])
nfoundlimit=int(sys.argv[3])
argcryfile=sys.argv[4]
if nfoundlimit>0: print "Limiting found entries to:", nfoundlimit

geo=geom()
#bs=boxsetup3d(argbs,True)
bs=boxsetup3d(argbs,False)

tfout=TFile(outfilePrefix+"_ratesAndStuffOut_b"+str(argbs)+".root", "recreate")

qbins=1000
plotext=".png"
#cryfile="/uboone/data/users/mibass/cosmics/MuCS/cry_mc/genroot_1.root"

anatree=TChain('anatree')
anatree.Add(argcryfile)
entries=anatree.GetEntries()
print "total entries: ", entries
   

found=0
#draw boxes
for b in bs: geo.drawbox(b)
ftree=flatttree("boxevents",["strips[8]/I",
"reco_anglex_mean/D","reco_anglex_rms/D", "reco_anglez_mean/D","reco_anglez_rms/D",
"reco_tpc_track_length/D", "reco_tpc_start[3]/D", "reco_tpc_end[3]/D", "reco_start_x_mean/D","reco_start_x_rms/D", "reco_start_z_mean/D", "reco_start_z_rms/D",
"true_tpc_track_length/D", "true_tpc_start[3]/D", "true_tpc_end[3]/D", "true_start[3]/D",
"true_theta/D", "true_phi/D", "true_cry_Eng/D", "true_cry_pdg/I","true_cry_t/D",
"true_anglex/D", "true_anglez/D",
"cosq_TrueToReco/D"])

ntotal=anatree.GetEntries()
ncur=0
tpccount=0
#loop over events
for ev in anatree:
  #generate propogated positions, in each box, from TPC, only continue if it goes through all four
  #print "Event ", ncur, "\r",
  
  thistheta,thisphi=geo.getThetaPhiFromLD((ev.cry_Px/ev.cry_P,ev.cry_Py/ev.cry_P,ev.cry_Pz/ev.cry_P))
  #thisphi+=pi
  #binallboxes,posb,posinbox=geo.getNewPosInBox3d(ev,bs)
  binallboxes,posb,posinbox=geo.getNewPosInBox3d(ev,bs,True,thistheta,thisphi)
  if ncur%10000==0: print "Event ", ncur,"(",ncur/ntotal,"%)" ,"\r",
  sys.stdout.flush()
  #if posinboxes[0] and posinboxes[1]: geo.drawpoint(inBoxPoints, 6)
  if not binallboxes: 
    ncur+=1
    continue
  found+=1
  print "Found ",found," coincidences at t=", ev.cry_t, "(%0.2f Hz)"%(found/ev.cry_t)
  
  if nfoundlimit<=1000:
    if binallboxes and posinbox[8]:
      geo.drawpoint(posb, 10, ROOT.kGray)
    else:
      del posb[-1]
      del posb[-1]
      posb.append(geo.getNewPos(posb[0][0],posb[0][1],posb[0][2],thistheta,thisphi,geo.tpcdims[1][1]))
      posb.append(geo.getNewPos(posb[0][0],posb[0][1],posb[0][2],thistheta,thisphi,geo.tpcdims[0][1]))
      
      geo.drawpoint(posb, 10, ROOT.kRed)
    
  
  #find out which strips these points go through
  bhits,trigger=bs.getHitPatternAndTrigger(posb[0:8])
  
  #get smearing hist for this collection of strip hits, and make 2d dist from them
  #(thxSmear,thzSmear,txpos,tzpos)=bs.getDistsForStrips(xStrips,zStrips)

  #true tpc track length
  if posinbox[8]: #in tpc
    tpccount+=1
    tpctracklength=sqrt(pow(posb[8][0]-posb[9][0],2)+pow(posb[8][1]-posb[9][1],2)+pow(posb[8][2]-posb[9][2],2))
    tpcs=posb[8]
    tpce=posb[9]
  else:
    tpctracklength=0
    tpcs=(-999,-999,-999)
    tpce=(-999,-999,-999)
  
  #calculate reco tpc start/end/length
  #reco_qx=thxSmear.GetMean()
  #reco_qz=thzSmear.GetMean()
  #reco_bxa=txpos.GetMean()
  #reco_bza=tzpos.GetMean()
  #reco_bxa_rms=txpos.GetRMS()
  #reco_bza_rms=tzpos.GetRMS()
  #recoPs=geo.getNewRecoPosInBox(reco_bxa, reco_bza, reco_qx, reco_qz, bs)
  #reco_tpctracklength=sqrt(pow(recoPs['postpctop'][0]-recoPs['postpcbottom'][0],2)+pow(recoPs['postpctop'][1]-recoPs['postpcbottom'][1],2)+pow(recoPs['postpctop'][2]-recoPs['postpcbottom'][2],2))
  
  #if recoPs['postpctop'][0] and recoPs['postpcbottom'][0]!=-999.0:
  #  reco_theta,reco_phi,reco_ld=geo.getThetaPhiLDFromLine(recoPs['postpctop'],recoPs['postpcbottom'])
  #  true_theta,true_phi,true_ld=geo.getThetaPhiLDFromLine(inBoxPoints[4],inBoxPoints[5])
  #  cosq_TrueToReco=true_ld[0]*reco_ld[0]+true_ld[1]*reco_ld[1]+true_ld[2]*reco_ld[2]
  #else:
  #  cosq_TrueToReco=-1.
  
  #print "reco top tpc pos", recoPs['postpctop']
  #print "reco bottom tpc pos", recoPs['postpcbottom']
  
  ftree.fill([(bhits[2],bhits[3],bhits[6],bhits[7],bhits[0],bhits[1],bhits[4],bhits[5]),
    0,0,0,0,
    0,
    (0,0,0),(0,0,0), 0, 0, 0, 0,
    tpctracklength,
    tpcs,tpce,
    posb[0],
    ev.theta, ev.phi, ev.cry_Eng, ev.cry_pdg, ev.cry_t,
    -acos((cos(ev.theta))*cos(ev.phi)),-acos((cos(ev.theta))*sin(ev.phi)),
    0.])
    

  if nfoundlimit>0 and found>=nfoundlimit: break
  
  ncur+=1
#store output hists
#ftree.Scan("*")
print "Done! Found",found,"triggers (", tpccount," in TPC [", 0. if found==0 else float(tpccount)/found,"]"
ftree.close(tfout)
tfout.cd()
geo.close(tfout)
tfout.Close()

