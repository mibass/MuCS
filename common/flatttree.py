from math import *
from ROOT import *
from array import array


class flatttree:
  farrays=[]
  t= TTree()
  
  def __init__(self,name,fields):
    #fields is a list of fields for the flat ttree with /I or /D appended to indicate int or double
    self.t = TTree( name, 'generated as a flatttree' )
    print "Building tree:",name
    #init fields
    self.farrays=[]
    for f in fields:
      if f.find(']')>-1:
        n=int(f[f.find('[')+1:f.find(']')])
      else:
        n=1
      if(f.endswith('/D')):
        self.farrays.append(array('d',[ 0. ]*n))
      elif(f.endswith('/F')):
        self.farrays.append(array('f',[ 0. ]*n))
      elif(f.endswith('/I')):
        self.farrays.append(array('i',[ 0 ]*n))
      else:
        print "invalid type for tree field!"
        exit(1)
      if f.find('[')==-1:
        fname=f[:f.find('/')]
      else:
        fname=f[:f.find('[')]
      print "Adding field", fname,f
      self.t.Branch(fname,self.farrays[-1],f)
      
    #print self.farrays
    
  def fill(self,fields):
    if(len(self.farrays) != len(fields)):
      print "wrong number of fields passed for this tree, expected", len(self.farrays)
      exit(1)
     
    for i in xrange(len(fields)):
      #print self.farrays[i][0]
      #print self.farrays[i][0], type(self.farrays[i][0]), fields[i], type(fields[i])
      if isinstance(fields[i], tuple) or isinstance(fields[i], list):
        for j in xrange(len(fields[i])):
          self.farrays[i][j]=fields[i][j]
      else:
        #print fields[i]
        self.farrays[i][0]=fields[i]

    self.t.Fill()
    
  def close(self,tfile):
    tfile.cd()
    self.t.Write()
    self.farrays=[]
    self.t=None
    
  def Scan(self):
    self.t.Scan()
    
  def Scan(self,opt):
    self.t.Scan(opt)
    
