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
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile
from math import *
from array import array
from random import *
sys.path.insert(0, '../common/')
from boxsetups import *
from geom import *
import itertools
from flatttree import *

argbs=int(sys.argv[1]) #box setup to use
argmode=int(sys.argv[2]) #mode: 1=nominal, 2=tfgoutput, 3=alignment
argN=int(sys.argv[3]) #number of triggers to find
argoutput=sys.argv[4] #name of outputfile
argseed=int(sys.argv[5])
argTFGOutputFolder=sys.argv[6] #folder to put tfg inputs into

seed(argseed)
qbins=50
xbins=50
geo=geom()
if argmode==3:
  bs=boxsetup3d(argbs,False,True)
else:
  bs=boxsetup3d(argbs,False)
for b in bs: geo.drawbox(b)
for b in bs: print b
#exit()
#print bs.scanangles3d

#load EvsTheta muon distribution created with (/uboone/data/uboonepro/sowjanya/cosmogenics/merged_cosmicnew_noOB.root):
#TFile f("EvsTheta.root","recreate")
#TH2F *evt=new TH2F("evt","",50,0,1,200,0,200)
#anatree.Draw("Eng:cos(theta-pi/2)>>evt","process_primary==1 && abs(pdg)==13 && inTPCActive==1","colz",40000)
#evt.Write()
evtFile=TFile("EvsTheta.root", "r")
hevt=evtFile.Get("evt")

def getE(costheta):
  #return energy in this range
  xbin=hevt.GetXaxis().FindBin(costheta)
  #print costheta,xbin
  hproj=hevt.ProjectionY("evt_py",xbin,xbin)
  if hproj.GetEntries()>0:
    E= hproj.GetRandom()
  else:
    E=uniform(50,100) #since these will be high angles, they should have high energies
    
  if E<0.10566: #don't return Es less than the muon mass
    E+=0.10566
    
  return E


lc=0
linesPerEvent=100
eventsPerFile=100
tfgouttemplate=argTFGOutputFolder+"/MCSMuons_bs%s_%d.txt"
tfgfilecount=1
if argmode==2: tfgfile=open(tfgouttemplate%(argbs,tfgfilecount),'w')
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
    

def writeTFG(startp,ld,theta):
  ##TextFileGen Output: status code << PDG code << first mother << second mother << first daughter << second daughter << Px << Py << Pz << energy << mass << x << y << z << time of particle production
  #1 -13 0 0 0 0 -0.0661634 -0.406499 -0.380253 0.570417 0.10566 -73.015 1800 2009.14 2.04924e+06
  pdg = "13" if uniform(0,1)>0.5 else "-13"
  AngerIsAnEnergy=getE(cos(theta)) #in GeV
  mass=0.10566 #in GeV
  #Energy = sqrt(P_x*P_x + P_y*P_y + P_z*P_z + mass*mass);
  Ptot=sqrt(pow(AngerIsAnEnergy,2)-pow(mass,2))
  P_x=ld[0]*Ptot
  P_y=ld[1]*Ptot
  P_z=ld[2]*Ptot
  
  line="1" #status code
  line+=" "+pdg
  line+=" 0" #first mother
  line+=" 0" #second mother
  line+=" 0" #first daughter
  line+=" 0" #second daughter
  line+=" "+"%f"%P_x
  line+=" "+"%f"%P_y
  line+=" "+"%f"%P_z
  line+=" "+"%f"%AngerIsAnEnergy
  line+=" "+"%f"%mass
  line+=" "+"%f"%startp[0]
  line+=" "+"%f"%startp[1]
  line+=" "+"%f"%startp[2]
  line+=" 0\n" #time
  
  writeLine(line)
  
#tf=TFile("angular_tfg_bs"+str(argbs)+".root", "recreate")
tf=TFile(argoutput, "recreate")

#diagnostic histograms to make sure things are behaving correctly
xzhist=TH2F("z vs x","",xbins,bs[0][0][0],bs[0][0][1],xbins,bs[0][2][0],bs[0][2][1])
thetaphihist=TH2F("phivstheta","Phi vs Theta",qbins,bs.thetas[0],bs.thetas[1],qbins,bs.phis[0],bs.phis[1])

ftree=flatttree("boxevents",["strips[8]/I","true_Start[3]/F","true_theta/F","true_phi/F","true_thetaxy/F","true_thetayz/F","true_TPCStart[3]/F","true_TPCEnd[3]/F","inTPCActive/I","bbox_Start[3]/F"])


NHistWarning=10
tcount=0 #number of triggers found
nHitTPC=0
bdrawpoints=True

while tcount<argN: #loop until we find the specified number of triggers
  #print bs[:]
  if argmode==3: 
    bs.updatePositions() #throw new positions for boxes
    if bdrawpoints:
      for b in bs: geo.drawbox(b)
  #print bs[:]
  
  #throw theta and phi
  theta=uniform(bs.thetas[0],bs.thetas[1])
  phi=uniform(bs.phis[0],bs.phis[1])

  #compute position at each box
  p=[]
  p.append((uniform(bs[0][0][0],bs[0][0][1]),bs[0][1][0],uniform(bs[0][2][0],bs[0][2][1]))) #distribute uniformly across topmost box
  for i in range(1,8):
    p.append(geo.getNewPos(p[0][0],p[0][1],p[0][2],theta,phi,bs[i][1][0]))
  
  
  #generate direction vector and make projections onto XY and YZ
  theta,phi,ld=geo.getThetaPhiLDFromLine(p[7],p[0]) #makes things consinstent for all angles
  theta_xy=(atan2((ld[1]),(ld[0])))
  theta_yz=(atan2((ld[1]),(ld[2])))
  
  #get hit pattern for this muon using above positions
  bhits,trigger=bs.getHitPatternAndTrigger(p)
    
  #populate hists for triggers
  if trigger:
    xzhist.Fill(p[0][0],p[0][2])
    thetaphihist.Fill(theta,phi)
    #add on projections to tpc
    binallboxes,posb,posinbox=geo.getNewPosInBox3d_noEvent(p[0],bs,theta, phi)
    if posinbox[8]: #hits tpc
      p.append(posb[8])
      p.append(posb[9])
      if bdrawpoints: geo.drawpoint(p, 10)  #only enable for small runs because it takes forever to save
      nHitTPC+=1
    else:
      if bdrawpoints:
        p.append(geo.getNewPos(p[0][0],p[0][1],p[0][2],theta,phi,geo.tpcdims[1][1]))
        p.append(geo.getNewPos(p[0][0],p[0][1],p[0][2],theta,phi,geo.tpcdims[0][1]))
        geo.drawpoint(p, 10, 2)
      p.append((-999.,-999.,-999.))
      p.append((-999.,-999.,-999.))
    tcount+=1
    if argmode==2: writeTFG(p[0],ld,theta)
    ftree.fill(((bhits[0],bhits[1],bhits[2],bhits[3],bhits[4],bhits[5],bhits[6],bhits[7]),
                p[0],theta,phi,theta_xy,theta_yz,p[8],p[9],int(posinbox[4]),p[4]))

xzhist.Write()
thetaphihist.Write()

print "Done! Found",tcount,"triggers (", nHitTPC," in TPC [", 0. if tcount==0 else float(nHitTPC)/tcount,"]"


print "Closing tdview..."
geo.close(tf)
ftree.close(tf)
print "Closing TFile..."
tf.Close()
#write remaining lbuffer to txt output file
if argmode==2: writeLinesToFile(eventCount, len(lbuffer), lbuffer)
  

    


