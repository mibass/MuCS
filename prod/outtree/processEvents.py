#!/bin/env python
# -*- coding: utf-8 -*-
import os,sys,string
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile, TChain, TGraph, TBox, TLegend, TColor
from math import *
from timeit import default_timer as timer
from array import array
sys.path.insert(0, '/uboone/app/users/mibass/cosmics/MuCS/common/')
from boxsetups import *
from geom import *
from flatttree import *
sys.path.insert(0, '/uboone/app/users/mibass/cosmics/MuCS/preselected/')
from dataHelper import *

print "Parsing arguments..."
argANAfile=sys.argv[1] #input data file
argMCANAfile=sys.argv[2] #input data file
argARTfile=sys.argv[3] #name of input art file
argN=int(sys.argv[4]) #number of events to process
argNStart=int(sys.argv[5]) #event to start on (0 based)
argoutputFile=sys.argv[6] #outputdirectory
argbs=int(sys.argv[7]) #box setup
argpmtonly=True if int(sys.argv[8])==1 else False #pmtonly

bs=boxsetup3d(argbs,False)
tfout=TFile(argoutputFile, "recreate")
dh=dataHelper("",False)
#xrecooffset=-23.58 #computed by looking at difference between MuCS_Start_TPC and Tagged_Start
xrecooffset=0

#defualts are:
#dh.hitmap72=(57,58,60,62,64,52,56,41,43,46,35,36,40,25,30,24,9,11,13,1,3,5,7,8)
#dh.hitmap31=(8,7,5,3,1,13,11,9,24,30,25,40,36,35,46,43,41,56,52,64,62,60,58,57)
#dh.hitmap72=(8,7,5,3,1,13,11,9,24,30,25,40,36,35,46,43,41,56,52,64,62,60,58,57)
#dh.hitmap31=(57,58,60,62,64,52,56,41,43,46,35,36,40,25,30,24,9,11,13,1,3,5,7,8)
#dh.refilldicts()

print "ANA file:",argANAfile
print "MCANA file:",argMCANAfile
print "ART file:",argARTfile
print "entries to look at in input file:",argN

fANA=TFile(argANAfile)
fART=TFile(argARTfile)
anatree=fANA.Get('analysistree/anatree')
events=fART.Get('Events')


#The mc anatree needs to be flexible so that if it's not ready yet (None) it can be skipped
mcanatree=None
mcentries=0
if os.path.isfile(argMCANAfile):
  fMCANA=TFile(argMCANAfile)
  mcanatree=fMCANA.Get('analysistree/anatree')
  mcentries=mcanatree.GetEntries()

print "data, MC, events tree has %d,%d,%d entries"%(anatree.GetEntries(),mcentries,events.GetEntries())
#setup the MuCS libraries/objects
ROOT.gSystem.Load("libuboonecode_uboone_MuCS")
ROOT.gInterpreter.GenerateDictionary("MuCS::MuCSRecoData","MuCSRecoData.h")
ROOT.gInterpreter.GenerateDictionary("MuCS::MuCSData","MuCSData.h")

def av(v):
  #return anatree variable with name v
  global anatree
  return anatree.__getattr__(v)

def avt(v,tlbl):
  #return anatree track variable with name v
  return av("%s_%s"%(v,tlbl))

def mcav(v):
  #return anatree variable with name v
  global mcanatree
  return mcanatree.__getattr__(v)

def mcavt(v,tlbl):
  #return anatree track variable with name v
  return mcav("%s_%s"%(v,tlbl))
  
def drawBoxHits(mdhits,geo):
  #draw line inside boxes for each hit
  avgxsum=avgysum=avgzsum=0.
  avgxcount=avgycount=avgzcount=0
  p1=(0.,0.,0.)
  p2=(0.,0.,0.)
  hitlist=((7,mdhits.Hits7()),(3,mdhits.Hits3()),(2,mdhits.Hits2()),(1,mdhits.Hits1()))
  for hitset in hitlist:
    pmt=hitset[0]
    for hit in hitset[1]:
      
      (layer,strip)=dh.getStripNumberFromPMTHit(pmt,hit)
      strip=strip-1 # switch from 1 based counting to 0 based
      if abs(bs.stripDirection[layer][0])==1: #xdirection
        xavg=bs.getStripDims(layer,0,strip)[1] #avg value
        xs=(xavg,xavg)
        zs=bs[layer][2]      
        avgxsum+=xavg
        avgxcount+=1
      elif abs(bs.stripDirection[layer][2])==1: #zdirection
        zavg=bs.getStripDims(layer,2,strip)[1] #avg value
        zs=(zavg,zavg)
        xs=bs[layer][0]
        avgzsum+=zavg
        avgzcount+=1
      else:
        raise ValueError('invalid strip direction; not implemented;')
       
      ys=((bs[layer][1][0]+bs[layer][1][1])/2,(bs[layer][1][0]+bs[layer][1][1])/2)
      print "\t","pmt=",pmt, ", layer=",layer, ", hit=",hit,", strip=",strip,":",(xs[0],ys[0],zs[0]),",",(xs[1],ys[1],zs[1])
      geo.drawpoint(((xs[0],ys[0],zs[0]),(xs[1],ys[1],zs[1])), 2, 0,"",2)
      
     
            
    if pmt==3: #form first hit
      p1=(avgxsum/avgxcount,(bs[0][1][0]+bs[0][1][1])/2,avgzsum/avgzcount)
      avgxsum=avgysum=avgzsum=0.
      avgxcount=avgycount=avgzcount=0
    if pmt==1: #form second hit
      p2=(avgxsum/avgxcount,(bs[4][1][0]+bs[4][1][1])/2,avgzsum/avgzcount)
      avgxsum=avgysum=avgzsum=0.
      avgxcount=avgycount=avgzcount=0

  
  #project to top of tpc:
  p3=geo.getNewPosFromld(p1[0],p1[1],p1[2],[a_i - b_i for a_i, b_i in zip(p1, p2)], 116.5)
  theta_xy=atan2(-(p1[1]-p2[1]),-(p1[0]-p2[0]))
  theta_yz=atan2(-(p1[1]-p2[1]),-(p1[2]-p2[2]))
  #p3=(p1[0] + cos(theta_xy)*(p1[1]-116.5),116.5,p1[2] + cos(theta_yz)*(p1[1]-116.5))
  geo.drawpoint((p1,p2,p3),3,0,"",1)
  print "***Drawing box hits"
  print "\tp1,p2:",p1,p2
  print "\tp3:",p3
  print "\ttheta_xy:",theta_xy
  print "\ttheta_yz:",theta_yz
  print "***"

  return (p1,p3)


def getLinesTuple(md,geo):
  
  #start
  p1=(md.x(),md.y(),md.z())
  theta,phi=geo.getThetaPhiFromThetas(md.theta_xy(),md.theta_yz())
  
  p2= geo.getNewPos(p1[0],p1[1],p1[2],theta, phi, 116.5)
  tpcints=geo.tpcintersections(p1[0],p1[1],p1[2],theta, phi)
  tpclen=0.
  print tpcints
  if tpcints[0]:
    tpclen=dist(tpcints[1][0],tpcints[1][1])
    
  
  #middle line
  theta1,phi1=geo.getThetaPhiFromThetas(md.theta_xy()-md.theta_xy_rms(),md.theta_yz())
  theta2,phi2=geo.getThetaPhiFromThetas(md.theta_xy()+md.theta_xy_rms(),md.theta_yz())
  theta3,phi3=geo.getThetaPhiFromThetas(md.theta_xy(),md.theta_yz()-md.theta_yz_rms())
  theta4,phi4=geo.getThetaPhiFromThetas(md.theta_xy(),md.theta_yz()+md.theta_yz_rms())
  theta5,phi5=geo.getThetaPhiFromThetas(md.theta_xy()+md.theta_xy_rms(),md.theta_yz()-md.theta_yz_rms())
  theta6,phi6=geo.getThetaPhiFromThetas(md.theta_xy()+md.theta_xy_rms(),md.theta_yz()+md.theta_yz_rms())
  theta7,phi7=geo.getThetaPhiFromThetas(md.theta_xy()-md.theta_xy_rms(),md.theta_yz()+md.theta_yz_rms())
  theta8,phi8=geo.getThetaPhiFromThetas(md.theta_xy()-md.theta_xy_rms(),md.theta_yz()-md.theta_yz_rms())
  
  xs=(geo.getNewPos(p1[0],p1[1],p1[2],theta1, phi1, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta2, phi2, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta3, phi3, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta4, phi4, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta5, phi5, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta6, phi6, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta7, phi7, 116.5)[0],
      geo.getNewPos(p1[0],p1[1],p1[2],theta8, phi8, 116.5)[0]
    )
  zs=(geo.getNewPos(p1[0],p1[1],p1[2],theta1, phi1, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta2, phi2, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta3, phi3, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta4, phi4, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta5, phi5, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta6, phi6, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta7, phi7, 116.5)[2],
      geo.getNewPos(p1[0],p1[1],p1[2],theta8, phi8, 116.5)[2]
    ) 
  
  p3=(min(xs),116.5,min(zs))
  p4=(min(xs),116.5,max(zs))
  p5=(max(xs),116.5,min(zs))
  p6=(max(xs),116.5,max(zs))

  #pb=(md.x() + cos(md.theta_xy())*(md.y()-320.051),320.051,md.z() + cos(md.theta_yz())*(md.y()-320.051))
  pb= geo.getNewPos(p1[0],p1[1],p1[2],theta, phi, 320.051)
  print "***Getting lines tuples..."
  print "\tp1:",p1
  print "\tpb:",pb
  print "\tp2:",p2
  print "\ttheta_xy:",md.theta_xy()
  print "\ttheta_yz:",md.theta_yz()
  print "\ttpcints:", tpcints
  print "\ttpclen:", tpclen
  print "***"
  return (p1,p2,p1,p3,p1,p4,p1,p5,p1,p6),p1,md.theta_xy(),md.theta_yz(),p2,tpclen,md.theta_xy_rms(),md.theta_yz_rms()
  #return (p1,pb,p2),p1,md.theta_xy(),md.theta_yz(),p2,tpclen


def dist(p1,p2):
  return sqrt(pow(p1[0]-p2[0],2)+pow(p1[1]-p2[1],2)+pow(p1[2]-p2[2],2))

def checkTrkMuCSIntersection(inp1,inp2,liberalize=0):
  if inp1[1]>inp2[1]: #make sure top point is p1
    p1=inp1
    p2=inp2
  else:
    p1=inp2
    p2=inp1

  p0=geo.getNewPosFromld(p1[0],p1[1],p1[2],[a_i - b_i for a_i, b_i in zip(p1, p2)], bs[0][1][0])
  p4=geo.getNewPosFromld(p1[0],p1[1],p1[2],[a_i - b_i for a_i, b_i in zip(p1, p2)], bs[4][1][0])
  
  intersects0=(bs[0][0][0]-liberalize<p0[0]<bs[0][0][1]+liberalize and bs[0][2][0]-liberalize<p0[2]<bs[0][2][1]+liberalize)
  intersects4=(bs[4][0][0]-liberalize<p4[0]<bs[4][0][1]+liberalize and bs[4][2][0]-liberalize<p4[2]<bs[4][2][1]+liberalize)
  return intersects0,intersects4
 
def checkMuCSTagMC(trk,tl):
  return checkMuCSTag(trk,tl,favt=mcavt)

def checkMuCSTag(trk,tl,favt=avt):
  startx=favt("trkstartx",tl)[trk]
  starty=favt("trkstarty",tl)[trk]
  endx=favt("trkendx",tl)[trk]
  endy=favt("trkendy",tl)[trk]
  if favt("trkcosmictype_tagger",tl)[trk]==-1 and favt("trkcosmicscore_tagger",tl)[trk]== -999.0 and startx>0 and startx<279 and starty>-130 and starty<130 and endx>0 and endx<279 and  endy>-130 and endy<130:
    return True
  else:
    return False


def GetTaggedInfoMC(trk,tl):
  return GetTaggedInfo(trk,tl,mcavt)

def GetTaggedInfo(trk,tl,favt=avt):
  global xrecooffset
  start=(0.,0.,0.)
  theta_xy=0.
  theta_yz=0.
  
  if favt("trkstarty",tl)[trk]>favt("trkendy",tl)[trk]:
    start=(favt("trkstartx",tl)[trk]+xrecooffset,favt("trkstarty",tl)[trk],favt("trkstartz",tl)[trk])
    end=(favt("trkendx",tl)[trk]+xrecooffset,favt("trkendy",tl)[trk],favt("trkendz",tl)[trk])
    theta_xy=atan2(favt("trkstartdcosy",tl)[trk],favt("trkstartdcosx",tl)[trk])
    theta_yz=atan2(favt("trkstartdcosy",tl)[trk],favt("trkstartdcosz",tl)[trk])
  else:
    start=(favt("trkendx",tl)[trk]+xrecooffset,favt("trkendy",tl)[trk],favt("trkendz",tl)[trk])
    end=(favt("trkstartx",tl)[trk]+xrecooffset,favt("trkstarty",tl)[trk],favt("trkstartz",tl)[trk])
    theta_xy=atan2(favt("trkenddcosy",tl)[trk],favt("trkenddcosx",tl)[trk])
    theta_yz=atan2(favt("trkenddcosy",tl)[trk],favt("trkenddcosz",tl)[trk])  
  
  return start,end, theta_xy, theta_yz, favt("trklen",tl)[trk]


def getTop(p1,p2):
  if p1[1]>p2[1]:
    return p1
  else:
    return p2

def drawFlashes(g, anatree, ismc):
  a=anatree
  ret_time=ret_pe=ret_ycenter=ret_ywidth=ret_zcenter=ret_zwidth=totpe=0.
  flashesdrawn=0
  if a is None:
    return flashesdrawn,ret_time,ret_pe,ret_ycenter,ret_ywidth,ret_zcenter,ret_zwidth, 0, totpe
  for i in xrange(a.no_flashes):
    t=a.flash_time[i] - (1. if ismc else 0.) #include offset to match mc flash times to data flash times
    if(t>-2 and t<2):
      if t<-0.8:
        col=ROOT.kRed
      elif t<0:
        col=ROOT.kBlue
      elif t<1:
        col=8
      else:
        col=ROOT.kGray
      
      #col=TColor.GetColorBright(int(a.flash_pe[i]))
      if ismc:
        g.drawCrossOnX(0,a.flash_ycenter[i]-a.flash_ywidth[i],a.flash_ycenter[i]+a.flash_ywidth[i],a.flash_zcenter[i]-a.flash_zwidth[i],a.flash_zcenter[i]+a.flash_zwidth[i],col,3)
      else:
        g.drawSquareOnX(0,a.flash_ycenter[i]-a.flash_ywidth[i],a.flash_ycenter[i]+a.flash_ywidth[i],a.flash_zcenter[i]-a.flash_zwidth[i],a.flash_zcenter[i]+a.flash_zwidth[i],col,3)
      #print "Drew flash",a.flash_ycenter[i]-a.flash_ywidth[i],a.flash_ycenter[i]+a.flash_ywidth[i],a.flash_zcenter[i]-a.flash_zwidth[i],a.flash_zcenter[i]+a.flash_zwidth[i]
      flashesdrawn+=1  
    
    if t<-0.8 and t >-1.1:
      #store this flashes info to return
      ret_time=a.flash_time[i]
      ret_pe=a.flash_pe[i]
      ret_ycenter=a.flash_ycenter[i]
      ret_ywidth=a.flash_ywidth[i]
      ret_zcenter=a.flash_zcenter[i]
      ret_zwidth=a.flash_zwidth[i]
    
    totpe+=a.flash_pe[i]
  
  print ("MC" if ismc else ""),"FLASH:",flashesdrawn,ret_time,ret_pe,ret_ycenter,ret_ywidth,ret_zcenter,ret_zwidth
  return flashesdrawn,ret_time,ret_pe,ret_ycenter,ret_ywidth,ret_zcenter,ret_zwidth, a.no_flashes, totpe


def GetEntries(i):
  global events, anatree, mcanatree
  events.GetEntry(i)
  ret1=anatree.GetEntry(i)
  if mcanatree is not None:
    #ret2=mcanatree.GetEntry(anatree.event-1)
    ret2=mcanatree.GetEntry(i)
    if anatree.event != mcanatree.event:
      print "Data:%d, MC:%d"%(anatree.event , mcanatree.event)
      raise ValueError("ERROR! Mismatched event numbers!")
  return anatree.event



def DoEventsList(tl):
  #do events list loop for track label tl
  ftreelist=["evt_number/I", "evt_time/I", "MuCS_Start[3]/F", "MuCS_theta_xy/F", "MuCS_theta_xy_rms/F", "MuCS_theta_yz/F", "MuCS_theta_yz_rms/F", "MuCS_Start_TPC[3]/F", "MuCS_NHitsX/I","MuCS_NHitsZ/I", "MuCS_TPC_len/F", "Tagged_Start[3]/F", "Tagged_End[3]/F", "Tagged_theta_xy/F", "Tagged_theta_yz/F", "Tagged_len/F", "MinD_Start[3]/F","MinD_End[3]/F", "MinD_theta_xy/F" , "MinD_theta_yz/F" , "MinD_dist/F", "MinD_len/F", "MCTagged_Start[3]/F", "MCTagged_End[3]/F", "MCTagged_theta_xy/F", "MCTagged_theta_yz/F", "MCTagged_len/F", "flash_time/F", "flash_pe/F", "flash_ycenter/F","flash_ywidth/F","flash_zcenter/F","flash_zwidth/F", "nflashes/I","totpe/F","MCflash_time/F","MCflash_pe/F", "MCflash_ycenter/F","MCflash_ywidth/F","MCflash_zcenter/F","MCflash_zwidth/F","MCnflashes/I","MCtotpe/F"]
  etree=flatttree("events_%s"%(tl),ftreelist)


  for i in range(argNStart,argN):
    eventnumber=GetEntries(i)
    print "Entry: %d, Event:%d"%(i,eventnumber)
    
    #for some reason, this gets the MuCS::MuCSRecoData object
    #the try/excepts are to handle different era's of variable names automagically
    try:
    #md=events.__getattr__("MuCS::MuCSRecoDatas_mucsreco__MuCSExtrapolate.obj.ftheta_xy") 
    #mdhits=events.__getattr__("MuCS::MuCSDatas_merger__MuCSMerger.obj.ft0")
      md=events.__getattr__("MuCS::MuCSRecoDatas_MuCSReco__MuCSMerge.obj.ftheta_xy") 
      mdhits=events.__getattr__("MuCS::MuCSDatas_MuCSMerger__MuCSMerge.obj.ft0")
    except:
      try:
        md=events.__getattr__("MuCS::MuCSRecoDatas_MuCSReco__MuCSMETAL.obj.ftheta_xy") 
        mdhits=events.__getattr__("MuCS::MuCSDatas_MuCSMerger__MuCSMETAL.obj.ft0")
      except:
        raise
    
    mind=1e6
    geo=geom("%s_%d"%(tl,eventnumber))

    Tagged_Start=(0.,0.,0.)
    Tagged_End=(0.,0.,0.)
    Tagged_theta_xy=Tagged_theta_yz=0.
    MuCS_Start=MuCS_Start_TPC=(0.,0.,0.)
    MuCS_theta_xy=MuCS_theta_yz=MuCS_theta_xy_rms=MuCS_theta_yz_rms=0.
    MinD_Start=(0.,0.,0.)
    MinD_End=(0.,0.,0.)
    MinD_dist=0.
    MinD_theta_xy=MinD_theta_yz=0.
    MuCS_NHitsX=MuCS_NHitsZ=0
    MuCS_TPC_len=Tagged_len=MinD_len=0.
    MCTagged_Start=(0.,0.,0.)
    MCTagged_End=(0.,0.,0.)
    MCTagged_theta_xy=MCTagged_theta_yz=MCTagged_len=0.  
    
    for b in bs: geo.drawbox(b)
    if md.z()!=0.: 
      mucstrks=drawBoxHits(mdhits,geo) #draw MuCS hits and projected track v1
      mucstrks,MuCS_Start,MuCS_theta_xy,MuCS_theta_yz,MuCS_Start_TPC, MuCS_TPC_len,MuCS_theta_xy_rms,MuCS_theta_yz_rms=getLinesTuple(md,geo)
      geo.drawpoint(mucstrks,len(mucstrks),4,"f",4) #draw projected track from MuCSExtrapolate

    if not argpmtonly:
      print "ntracks=",avt("ntracks",tl)
      for trk in xrange(avt("ntracks",tl)):
        p1=(avt("trkstartx",tl)[trk]+xrecooffset,avt("trkstarty",tl)[trk],avt("trkstartz",tl)[trk])
        p2=(avt("trkendx",tl)[trk]+xrecooffset,avt("trkendy",tl)[trk],avt("trkendz",tl)[trk])
        print p1,p2
        if checkMuCSTag(trk,tl) and avt("trklen",tl)[trk]>Tagged_len:
          geo.drawpoint((p1,p2), 2, 2,"",4)
          Tagged_Start, Tagged_End, Tagged_theta_xy,Tagged_theta_yz,Tagged_len=GetTaggedInfo(trk,tl)
        else:
          geo.drawpoint((p1,p2), 2, 11,"",2)
          
        #find closest track to MuCS TPC projection
        if md.z()!=0:
          pTop,pBot,t1,t2,tlen=GetTaggedInfo(trk,tl)
          d=dist(pTop,MuCS_Start_TPC)
          if d<mind:
            mind=d
            MinD_dist=d
            MinD_Start, MinD_End,MinD_theta_xy,MinD_theta_yz,MinD_len=GetTaggedInfo(trk,tl)
        
    #get number of hits that went into the MuCS track
    if md.z()!=0:
      MuCS_NHitsZ=len(mdhits.Hits7())+len(mdhits.Hits2())
      MuCS_NHitsX=len(mdhits.Hits3())+len(mdhits.Hits1())
      print "Hits Z,X:", MuCS_NHitsZ,",", MuCS_NHitsX
    
    #get mc track info
    if mcanatree is not None:
      for trk in xrange(mcavt("ntracks",tl)):
        p1=(mcavt("trkstartx",tl)[trk]+xrecooffset,mcavt("trkstarty",tl)[trk],mcavt("trkstartz",tl)[trk])
        p2=(mcavt("trkendx",tl)[trk]+xrecooffset,mcavt("trkendy",tl)[trk],mcavt("trkendz",tl)[trk])
        if checkMuCSTagMC(trk,tl) and mcavt("trklen",tl)[trk]>MCTagged_len:
          geo.drawpoint((p1,p2), 2, 9,"",4)
          MCTagged_Start, MCTagged_End, MCTagged_theta_xy,MCTagged_theta_yz,MCTagged_len=GetTaggedInfoMC(trk,tl)
        else:
          geo.drawpoint((p1,p2), 2, 46,"",2)
      
    #draw and get flash info
    nflashes,flash_time,flash_pe,flash_ycenter,flash_ywidth,flash_zcenter,flash_zwidth,ntotflashes,totpe=drawFlashes(geo, anatree, False)
    MCnflashes,MCflash_time,MCflash_pe,MCflash_ycenter,MCflash_ywidth,MCflash_zcenter,MCflash_zwidth,MCntotflashes,MCtotpe=drawFlashes(geo, mcanatree, True)
    
    print "Drew %d data flashes and %d mc flashes" %(nflashes,MCnflashes)
    
    #fill tree
    etree.fill((eventnumber,int(anatree.evttime), MuCS_Start, MuCS_theta_xy, MuCS_theta_xy_rms, MuCS_theta_yz, MuCS_theta_yz_rms, MuCS_Start_TPC, MuCS_NHitsX, MuCS_NHitsZ,MuCS_TPC_len, Tagged_Start, Tagged_End, Tagged_theta_xy, Tagged_theta_yz, Tagged_len, MinD_Start, MinD_End, MinD_theta_xy, MinD_theta_yz, MinD_dist, MinD_len, MCTagged_Start, MCTagged_End, MCTagged_theta_xy, MCTagged_theta_yz, MCTagged_len, flash_time, flash_pe,flash_ycenter,flash_ywidth,flash_zcenter,flash_zwidth, ntotflashes, totpe, MCflash_time, MCflash_pe,MCflash_ycenter,MCflash_ywidth,MCflash_zcenter,MCflash_zwidth,MCntotflashes,MCtotpe))
    geo.close(tfout)
    del geo
    print "finished event", eventnumber
    #if i>10: exit(0)
    
  etree.close(tfout)


DoEventsList("trackkalmanhit")
if not argpmtonly:
  DoEventsList("stitchkalmanhit")
  DoEventsList("pmtrack")
  DoEventsList("pandoraCosmicKHit")
  DoEventsList("pandoraCosmic")

tfout.Close()
