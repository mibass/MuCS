import os,sys,string
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile, TChain, TGraph, TBox, TLegend
from math import *
from timeit import default_timer as timer
from array import array
sys.path.insert(0, '/uboone/app/users/mibass/cosmics/MuCS/common/')
from boxsetups import *
from geom import *
from flatttree import *
sys.path.insert(0, '/uboone/app/users/mibass/cosmics/MuCS/preselected/')
from dataHelper import *
from random import *

arginfile=sys.argv[1] #input data file
argTFGOutputFolder=sys.argv[2] #folder to put tfg inputs into
argtfoutfile=sys.argv[3] #root file output
argN=int(sys.argv[4]) #number of events to process
argbs=int(sys.argv[5]) #box setup to use
argEventsPerFile=int(sys.argv[5]) #box setup to use
argtrackalg=sys.argv[6] #which track algorithm to use



#fin = TFile(arginfile)
#events = fin.Get('events')
events = TChain("events_%s"%argtrackalg)
events.Add(arginfile)
evtFile=TFile("EvsTheta.root", "r")
hevt=evtFile.Get("evt")

qbins=50
xbins=50
geo=geom()
bs=boxsetup3d(argbs,False)
for b in bs: geo.drawbox(b)
seed(0)

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
    
  return 10


lc=0
linesPerEvent=1
eventsPerFile=argEventsPerFile
tfgouttemplate=argTFGOutputFolder+"/MuCSMuons_bs%s_%05d.txt"
tfgfilecount=1
tfgfile=open(tfgouttemplate%(argbs,tfgfilecount),'w')
lbuffer=[]

def writeLine(line, noparticles=False):
  global tfgfile, tfgouttemplate, tfgfilecount, maxlinesperevent, lbuffer, evtnumber
  if noparticles:
    lbuffer=[]
  else:
    lbuffer.append(line)
  if len(lbuffer)==linesPerEvent or noparticles:
    #write lbuffer to file, prepending the event number and linecount
    writeLinesToFile(evtnumber, len(lbuffer), lbuffer)
    lbuffer[:]=[]
    if evtnumber%eventsPerFile==0 and evtnumber>0:
      tfgfilecount+=1

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

  
tf=TFile(argtfoutfile, "recreate")

#diagnostic histograms to make sure things are behaving correctly
xzhist=TH2F("z vs x","",xbins,bs[0][0][0],bs[0][0][1],xbins,bs[0][2][0],bs[0][2][1])
thetaphihist=TH2F("phivstheta","Phi vs Theta",qbins,bs.thetas[0],bs.thetas[1],qbins,bs.phis[0],bs.phis[1])

NHistWarning=10
evtnumber=0 #number of triggers found
nHitTPC=0
bdrawpoints=True

evtnumber=1
entrynumber=0
while evtnumber<argN: #loop until we find the specified number of triggers
  events.GetEntry(entrynumber)
  print "On evtnumber",evtnumber, " and entrynumber", entrynumber, " found:", events.evt_number
  if events.evt_number!=evtnumber or events.MuCS_Start[1]==0.:
    if events.evt_number<evtnumber: 
      entrynumber+=1
    else:
      #writeLine("",True)
      evtnumber+=1
    continue
  
  theta,phi=geo.getThetaPhiFromThetas(events.MuCS_theta_xy,events.MuCS_theta_yz)
  
  print theta,phi
  p=[]
  p.append((events.MuCS_Start[0],events.MuCS_Start[1],events.MuCS_Start[2]))
  print p
  for i in range(1,8):
    p.append(geo.getNewPos(p[0][0],p[0][1],p[0][2],theta,phi,bs[i][1][0]))
  
  
  
  xzhist.Fill(p[0][0],p[0][2])
  thetaphihist.Fill(theta,phi)
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
  
  ld=geo.getDirectionVector(theta,phi)
  writeTFG(p[0],ld,theta)
  evtnumber+=1
  entrynumber+=1
    

xzhist.Write()
thetaphihist.Write()

print "Done! Found",evtnumber,"events (", nHitTPC," in TPC [", 0. if evtnumber==0 else float(nHitTPC)/evtnumber,"]"


print "Closing tdview..."
geo.close(tf)
print "Closing TFile..."
tf.Close()
#write remaining lbuffer to txt output file
writeLinesToFile(evtnumber, len(lbuffer), lbuffer)
  
