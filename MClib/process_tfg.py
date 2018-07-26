#Generate muons that start randomly at 2d position of top box
#Throw angles over ranges that will reach the bottom box
#50/50 muon/antimuon mix
#Uniform E dist (for now, later get a pdf from a corsika or cry sim, or use a parameterization)
#ROOT OUTPUT:Store angles, hit pattern, xz's at each panel
#TextFileGen Output: status code << PDG code << first mother << second mother << first daughter << second daughter << Px << Py << Pz << energy << mass << x << y << z << time of particle production
  #not Px,Py,Pz should be computed with muon's energy & mass in mind (not just a direction)
  #don't forget that first entry of tfg event is eventnumber, number of particles in event
  


import os,sys,string
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile, TChain
from math import *
from array import array
from random import *
sys.path.insert(0, '../common/')
from boxsetups import *
from geom import *
import itertools
from flatttree import *


argbs=int(sys.argv[1]) #box setup to use
argoutput=sys.argv[2] #name of outputfile
arginputlist=sys.argv[3] #name of input list file

def ScaleAndWriteHist(h):
  if h.Integral()>0:
    h.Scale(1/h.Integral())
    h.Write()
  else:
    print h.GetName()," has 0 entries. Skipping..."
 

qbins=50
xbins=50
geo=geom()
bs=boxsetup3d(argbs,False)
for b in bs: geo.drawbox(b)

ttree=TChain("MCSMuons/MCSMuons")
files=0
for line in file(arginputlist):
  ttree.Add(line[:-1])
  files+=1

print "Found",ttree.GetEntries(),"entries in",files,"files"

tf=TFile(argoutput, "recreate")

#diagnostic histograms to make sure things are behaving correctly
xzhist=TH2F("z vs x","",xbins,bs[0][0][0],bs[0][0][1],xbins,bs[0][2][0],bs[0][2][1])
thetaphihist=TH2F("phivstheta","Phi vs Theta",qbins,bs.thetas[0],bs.thetas[1],qbins,bs.phis[0],bs.phis[1])

#this needs to match MClibrary.py exactly
ftree=flatttree("boxevents",["strips[8]/I","true_Start[3]/F","true_theta/F","true_phi/F","true_thetaxy/F","true_thetayz/F","true_TPCStart[3]/F","true_TPCEnd[3]/F","inTPCActive/I"])


tcount=0 #number of triggers found
N=ttree.GetEntries()

skipped=0
for muon in ttree:

  #get position at each box
  p=[]
  for i in xrange(8):
    if muon.LevelPointx[i]==-999. or muon.LevelPointy[i]==-999. or muon.LevelPointz[i]==-999.:
      print "Muon missing level point", i
      break
    p.append((muon.LevelPointx[i],muon.LevelPointy[i],muon.LevelPointz[i]))
  
  if len(p)<8:
    print "Skipping muon start/end: (",muon.StartPointx,",",muon.StartPointy,",",muon.StartPointz,")", "(",muon.EndPointx,",",muon.EndPointy,",",muon.EndPointz,")"
    skipped+=1
    continue


  #generate direction vector and make projections onto XY and YZ
  theta,phi,ld=geo.getThetaPhiLDFromLine(p[7],p[0])
  #ld=geo.getDirectionVector(theta,phi) #get ld this way to match silly scheme used for these simulationss
  theta_xy=(atan2((ld[1]),(ld[0])))
  theta_yz=(atan2((ld[1]),(ld[2])))


  #get hit pattern for this muon using above positions
  bx,bz,trigger=bs.getHitPatternAndTrigger(p)

  #populate hists for triggers
  if trigger:
    xzhist.Fill(p[0][0],p[0][2])
    thetaphihist.Fill(theta,phi)
    if muon.inTPCActive==1:
      p.append((muon.StartPointx_tpcAV,muon.StartPointy_tpcAV,muon.StartPointz_tpcAV))
      p.append((muon.EndPointx_tpcAV,muon.EndPointy_tpcAV,muon.EndPointz_tpcAV))
      #geo.drawpoint(p, 6)  #only enable for small runs because it takes forever to save
    else:    
      #geo.drawpoint(p, 4)  #only enable for small runs because it takes forever to save
      p.append((-999.,-999.,-999.))
      p.append((-999.,-999.,-999.))
    
    ftree.fill(((bx[0],bx[1],bx[2],bx[3],bz[0],bz[1],bz[2],bz[3]),
            p[0],theta,phi,theta_xy,theta_yz,p[8],p[9],muon.inTPCActive))
                
    tcount+=1

xzhist.Write()
thetaphihist.Write()

print "Done! Found",tcount,"triggers"
print "skipped",skipped,"out of",muon.GetEntries()
print "Closing tdview..."
geo.close(tf)
ftree.close(tf)
print "Closing TFile..."
tf.Close("")




exit(0)



    


