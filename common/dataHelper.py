import os,sys,string
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TH2F, TFile, TChain, TGraph, TBox
from math import *
from array import array
import sqlite3


class dataHelper:

  #note: i swapped 31 and 72 here so that strip numbers would increase in the appropriate directions (relative to Leo's diagram)
  hitmap72=(57,58,60,62,64,52,56,41,43,46,35,36,40,25,30,24,9,11,13,1,3,5,7,8)
  hitmap31=(8,7,5,3,1,13,11,9,24,30,25,40,36,35,46,43,41,56,52,64,62,60,58,57)
  adcmap = (8, 7, 5, 3, 1, 13, 11, 9, 24, 30, 25, 40, 36, 35, 46, 43, 41, 56, 52, 64, 62, 60, 58, 57)
  dict72={}
  dict31={}
  dictadcmap={}
  MCFile=""
  distsTree=TChain()
  last_sFilter=""#stores the most recent sFilter that was generated
  histcount=0
  filters={}#stores dictionary of hits , arranged by strip number
  swapBoxes=False
  
  def __init__(self,mcfile="",swapBoxes=False):
    self.refilldicts()

    if mcfile!="":
      self.MCFile=mcfile
      self.distsTree=TChain("boxevents")
      self.distsTree.Add(mcfile)
      if self.distsTree.GetEntries()<1:
        print "Problem with input MC tree"
        exit(1)
        
    self.filters={i:[] for i in xrange(8)}
    self.swapBoxes=swapBoxes
    
  def reset(self):
    self.filters={i:[] for i in xrange(8)}

  def refilldicts(self):
    self.dict72={self.hitmap72[i]:i+1 for i in xrange(len(self.hitmap72))}
    self.dict31={self.hitmap31[i]:i+1 for i in xrange(len(self.hitmap31))}    
    self.dictadcmap={i:self.adcmap[i] for i in xrange(len(self.adcmap))}
  
  def close(self):
    #need to reset entry list before ending otherwise python can't seem to cleanup the ttree
    self.distsTree.SetEntryList(0)
    
  def getStripNumberFromPMTHit(self,pmt,hit):
    #map from PMT number and hit number to strips and numbers used in MC
    #pmt's are ordered 7,3,2,1 moving down in tpc y (starting at top box)

    baselayer=0
    ldict=None
    if pmt==7:
      baselayer=0 if not self.swapBoxes else 4
      ldict=self.dict72
    elif pmt==3:
      baselayer=2 if not self.swapBoxes else 6
      ldict=self.dict31
    elif pmt==2:
      baselayer=4 if not self.swapBoxes else 0
      ldict=self.dict72
    elif pmt==1:
      baselayer=6 if not self.swapBoxes else 2
      ldict=self.dict31
    else:
      print "ERROR: Invalid pmt number, exiting!"
      exit(1)
 
    layer=baselayer+(1 if ldict[hit]>12 else 0)
    strip=ldict[hit]-(12 if ldict[hit]>12 else 0)
    return layer,strip

  def buildFilterString(self,hits):
    #build filter string from hits (tuple of four tuples each with pmtnumber,hits vector)

    sFilter=""
    lfilters={i:[] for i in xrange(8)} #set of filters only for this set of hits, the self.filters gets appended with ALL filters for an event
    for i in xrange(len(hits)):
      pmt=hits[i][0]
      for j in xrange(len(hits[i][1])):
        strip,num=self.getStripNumberFromPMTHit(pmt,hits[i][1][j])
        if len(hits)==2: self.filters[strip].append(num) #only append to filters in the 2 hits case to keep from appending twice
        lfilters[strip].append(num)
        #print "pmt=%d,chan=%d -> strip=%d,num=%d"%(pmt,hits[i][1][j],strip,num)
    
    isFirst=True
    for stripi in xrange(len(lfilters)):
      if(len(lfilters[stripi])>0):
        if not isFirst:
          sFilter+=" && "
        else:
          isFirst=False
        sFilter+="("
        for i in xrange(len(lfilters[stripi])):
          sFilter+=" strips[%d]==%d " % (stripi,lfilters[stripi][i]-1) #note strip indices in MC library start at 0, not 1
          if i<len(lfilters[stripi])-1 and len(lfilters[stripi])>1:
            sFilter+="||"
        sFilter+=")"
    
    
    #print sFilter
    self.last_sFilter=sFilter.replace("strips","")
    return sFilter

  def buildFilterStringFromMC(self,ps,layer):
    #for an mc preselected tree, the hits are stored in 8 arrays with 12 entries each
    #a number >-1 represents the hit strip number (and the indices match the MC indices)
     #copy hits into dictionary, arrange by strip number
    if layer=="z": #note, this was x when I thought the x layers were on top
      hitsArrays=(ps.s1,ps.s2,ps.s5,ps.s6)
      stripmap=(1,2,5,6)
    elif layer=="ztop":
      hitsArrays=(ps.s1,ps.s2) #only want topmost bilayer to match with data
      stripmap=(1,2)
    else:
      hitsArrays=(ps.s3,ps.s4,ps.s7,ps.s8)
      stripmap=(3,4,7,8)
    sFilter=""
    for i in xrange(len(hitsArrays)):
      if i>0:
        sFilter+=" && "
      sFilter+="("
      for j in xrange(len(hitsArrays[i])):
        if hitsArrays[i][j]>-1:
          self.filters[stripmap[i]-1].append(hitsArrays[i][j])
          sFilter+=" strips[%d]==%d " % (stripmap[i]-1,hitsArrays[i][j])
          if i<len(hitsArrays[i])-1 and hitsArrays[i][j+1]!=-1: #if it's not the last element, and there is another hit in this layer
            sFilter+="||"        
      sFilter+=")"
    
    self.last_sFilter=sFilter.replace("strips","")
    return sFilter

  def getHist(self,var,histname,histTitle,bins=50,addFilter=""):
    thisHistname=histname+str(self.histcount) #give each hist a unique name
    nbins=int(self.nResults/10)
    if nbins<5: nbins=1 #sometimes hists don't seem to work with such low bins numbers (between 1 and 5?)
    hDist=TH1F(thisHistname,"",nbins,0.,0.)
    self.distsTree.Draw(var+">>"+thisHistname,addFilter,"goff")
    hDist.SetTitle(histTitle)
  
    self.histcount+=1
    return hDist

  def CleanHit(self,isData,isARTData,ps):
    cleanhit=0
    if isData:
      #hit is clean if there is only two hits per bilayer
      cleanhit=1 if (len(ps.hits1)==2 and len(ps.hits2)==2 and len(ps.hits3)==2 and len(ps.hits7)==2) else 0
    elif isARTData:
      md=ps.__getattr__("MuCS::MuCSDatas_merger__MuCSMerger.obj.ft0")
      cleanhit=1 if (len(md.Hits1())==2 and len(md.Hits2())==2 and len(md.Hits3())==2 and len(md.Hits7())==2) else 0
    else:
      #hit is clean if there is only one entry per layer
      cleanhit=1 if ps.s1[1]==-1 and ps.s2[1]==-1 and ps.s3[1]==-1 and ps.s4[1]==-1 and ps.s5[1]==-1 and ps.s6[1]==-1 and ps.s7[1]==-1 and ps.s8[1]==-1 else 0
    return cleanhit

  def setEntryList(self,hits,layer,isData=True):
    if isData:
      sFilter=self.buildFilterString(hits) #get filter string to query the MC library with
    else:
      sFilter=self.buildFilterStringFromMC(hits,layer) #hits is a preselected MC tree
    self.distsTree.SetEntryList(0)
    self.nResults=self.distsTree.Draw(">>alist",sFilter,"entrylistarray")
    
    #print "nResults=",self.nResults
    if self.nResults>0:
      self.EList=ROOT.gROOT.FindObject("alist")
      if not self.EList:
        print "unable to retrieve entry list!"
        exit(1)
      else:
        self.distsTree.SetEntryList(self.EList)
        #print "limited entries: from", self.distsTree.GetEntries(), "to",self.distsTree.GetSelectedRows()
      return True
    else:
      return False
    
