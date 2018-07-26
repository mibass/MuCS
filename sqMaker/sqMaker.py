#script to make sqlite3 MC library based on root input
#searches all possible hit patterns and outputs theta, position in x and z
#outputs them, with pmt hit numbers, to sqlite db for use by MuCSMerger module

import os,sys,string
import ROOT
from math import *
from ROOT import TTree, TH1F, TCanvas, gROOT, TGaxis, gStyle, TColor, TLegend, THStack, TChain
from ROOT import *
from array import array
import sqlite3
sys.path.insert(0, '../common/')
sys.path.insert(0, '../preselected/')
from boxsetups import *
from dataHelper import *

argmcfile=sys.argv[1]
argoutputdbname=sys.argv[2]


#blank preselected class to pass to dataHelper's setEntryList
class ps:
  s1=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s2=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s3=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s4=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s5=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s6=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s7=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
  s8=[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

dh = dataHelper(argmcfile)

#create sqlite db
conn = sqlite3.connect(argoutputdbname)
curs=conn.cursor()
curs.execute('''CREATE TABLE hitmap13x (hita1 int, hita2 int, hitb1 int, hitb2 int, nentries int, q float, q_rms float, p float, p_rms float)''')
curs.execute('''CREATE TABLE hitmap27z (hita1 int, hita2 int, hitb1 int, hitb2 int, nentries int, q float, q_rms float, p float, p_rms float)''')

#the mcs mclib will have hits in terms of strips, s1-8, labelled 1-12
#the mcs data will have hits in terms of hits on each pmt
#to map between them, use the dataHelper's hitmap lists

#loop over all possible hit patterns:
for a in xrange(12):
  for b in xrange(12):
    for c in xrange(12):
      for d in xrange(12):
        #make object to match preselected tree variables in x
        ps.s3[0]=a
        ps.s4[0]=b
        ps.s7[0]=c
        ps.s8[0]=d
        
        if dh.setEntryList(ps,"x",False):
          htrue_thetaxy=dh.getHist("true_thetaxy","true_thetaxy","")
          htrue_pxy=dh.getHist("true_Start[0]","true_StartX","")
          print "x:",dh.last_sFilter,htrue_thetaxy.GetMean(), htrue_thetaxy.GetRMS(), htrue_thetaxy.GetEntries()
          #x hits are on pmts 1,3, so use that hitmap to convert a,b,c,d to pmt hits
          hit1a=dh.hitmap31[a]
          hit1b=dh.hitmap31[b+12]
          hit3a=dh.hitmap31[c]
          hit3b=dh.hitmap31[d+12]
          curs.execute("INSERT INTO hitmap13x VALUES (%d,%d,%d,%d,%d,%f,%f,%f,%f)"%(hit1a,hit1b,hit3a,hit3b,htrue_thetaxy.GetEntries(),htrue_thetaxy.GetMean(),htrue_thetaxy.GetRMS(),htrue_pxy.GetMean(), htrue_pxy.GetRMS()))
          print hit1a,hit1b,hit3a,hit3b, htrue_pxy.GetMean(), htrue_pxy.GetRMS()
        else:
          print "no data",dh.last_sFilter


        #make object to match preselected tree variables in z
        ps.s1[0]=a
        ps.s2[0]=b
        ps.s5[0]=c
        ps.s6[0]=d
        
        if dh.setEntryList(ps,"z",False):
          htrue_thetayz=dh.getHist("true_thetayz","true_thetayz","")
          htrue_pyz=dh.getHist("true_Start[2]","true_StartZ","")
          print "z:",dh.last_sFilter,htrue_thetayz.GetMean(), htrue_thetayz.GetRMS(), htrue_thetayz.GetEntries()
          #z hits are on pmts 2,7, so use that hitmap to convert a,b,c,d to pmt hits
          hit2a=dh.hitmap72[a]
          hit2b=dh.hitmap72[b+12]
          hit7a=dh.hitmap72[c]
          hit7b=dh.hitmap72[d+12]
          print hit2a,hit2b,hit7a,hit7b, htrue_pyz.GetMean(), htrue_pyz.GetRMS()
          curs.execute("INSERT INTO hitmap27z VALUES (%d,%d,%d,%d,%d,%f,%f,%f,%f)"%(hit2a,hit2b,hit7a,hit7b,htrue_thetayz.GetEntries(),htrue_thetayz.GetMean(),htrue_thetayz.GetRMS(),htrue_pyz.GetMean(), htrue_pyz.GetRMS()))
        else:
          print "no data",dh.last_sFilter


conn.commit()

conn.close()



