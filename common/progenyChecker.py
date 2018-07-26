from math import *
from ROOT import *


class progenyChecker:


  #def __init__(self):
    
  #  print "test" 
  
  def checkForShowers(self, ev,i):
    print "finding daughters for ev ",i,
    daughters=self.findDaughters(ev,ev.TrackId[i],i,True)
    #print daughters
    #for d in daughters:
    #  print ev.pdg[d], ev.processname[d], (ev.processname[d]=="compt" or ev.processname[d]=="conv")
    print len(daughters)
    
 # def isShower(self, ev,i):
 #   #check to see if this was created by pair production or compton scattering
 #   print "is:",ev.processname[i]
 #   if ev.processname[i]=="compt" or ev.processname[i]=="conv":
 #     print "found a shower!"
 #     return True
 #   else: return False
     
  def findDaughters(self, ev, TrackId, starti, noFollowShowers=False):
    #find daughters of TrackId
    l=[]
    #print TrackId
    for i in range(starti,ev.geant_list_size):
      if(ev.Mother[i]==TrackId):
        l.append(i)
        if noFollowShowers and (ev.processname[i]=="compt" or ev.processname[i]=="conv"): #only count top particle for a shower
          continue
        else:
          l.extend(self.findDaughters(ev,ev.TrackId[i],i))
    #print l
    return l


