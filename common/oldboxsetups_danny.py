from math import *
from ROOT import *
import random
import copy

class boxsetup3d:
  #boxdims= [[(0.0,0.0) for y in xrange(3)] for x in xrange(4)]
  __boxdims= []
  scanangles = [(0.0,0.0) for y in xrange(3)] #range of angles (radians) that cover this box in acos(px,py,pz/p) (py not needed)
  scanangles3d = [(0.0,0.0) for y in xrange(3)] #ditto, but for 3d scan (simultaneous in x,z)
  #normals = [(0.0,0.0,0.0) for y in xrange(4)] #surface normals for boxes
  normals = [] #surface normals for boxes
  planesp=[]
  planesd=[]
  #moving towards doing everything in theta,phi
  thetas=(0.,0.)
  phis=(0.,0.)
  dh=0
  dhstrip=1.0 #height of strip
  dw=4. #width of a strip (cm)
  dz=0. #needs to be a multiple of dw (strip width, cm)  
  boxset=0
  nboxes=0
  sigma_abs=(1.,1.,1.) #uncertainties (absolute) in x,y,z positions
  sigma_rel=(1.,1.,1.) #uncertainties (relative) in x,y,z positions of the bottom two boxes wrt to top two boxes
  __throwndims=[] #stores throw positions
  alignErrors=False
  __rng = random.Random() #local rng stream to avoid affecting other rng streams
  
  
  def updatePositions(self):
    if not self.alignErrors: 
      print "Not using alignment errors!"
      exit(1)
    #throw a new set of positions to augment the __boxdim positions
    #self.__throwndims=list(self.__boxdims) #reset to centers
    #print "ar:",self.__throwndims[0][0][0],self.__boxdims[0][0][0]
    for dim in xrange(3):
      offset=self.__rng.gauss(0,self.sigma_abs[dim]) #compute offset for each dimension (same across all boxes)
      #print offset
      for box in xrange(self.nboxes):
        for edge in xrange(2): 
          self.__throwndims[box][dim][edge]=self.__boxdims[box][dim][edge]+offset
    
    if self.nboxes==8: #apply relative errors by shifting bottom box positions (index 2 and 3)
      for dim in xrange(3):
        offset=self.__rng.gauss(0,self.sigma_rel[dim]) #compute offset for each dimension (same across two bottom boxes)
        for box in range(4,8):
          for edge in xrange(2): 
            self.__throwndims[box][dim][edge]=self.__throwndims[box][dim][edge]+offset    
            
    self.SetPlanes() #update planes and surface normals
  
  def __getitem__(self,index):
    #overloaded getitem
    if self.alignErrors: #return thrown positions for boxes
      return self.__throwndims[index]
    else: #return default positions
      return self.__boxdims[index]
      
  def __init__(self,n,bloadsmearing,inAlignErrors=False):
    self.alignErrors=inAlignErrors
    self.boxset=n
    if bloadsmearing: self.loadSmearFiles()
    if(n==1):
      self.dw=4.0 #width of a strip (cm)
      self.dz=48.0 #needs to be a multiple of dw (strip width, cm)
      self.dh=50.0 #separation between the boxes (cm)
      self.scanangles[2]=(-1.8,-0.2)
      self.scanangles[0]=(-2.5,-0.5)
      self.thetas=(-1.57,-0.4)
      self.phis=(-3.2,-0.0)
      self.nboxes=4
      self.__boxdims=[[[0.0,0.0] for y in xrange(3)] for x in xrange(self.nboxes)]
      self.normals=[(0.0,0.0,0.0) for y in xrange(self.nboxes)] #surface normals for boxes
      #top box position, tpc coordinates, other box is positioned relative to this
      self.__boxdims[0][0]=[208.35,256.35]
      self.__boxdims[0][1]=[403.15,403.15-self.dhstrip] #189 cm (top of tpc to platform) + 163.15 (top of tpc) + 50 (box sep) + 1 (strip depth)
      self.__boxdims[0][2]=[-48,0]
      self.normals[0]=(0,1,0)
      
      self.__boxdims[1][0]=[self.__boxdims[0][0][0]-self.dw/2,self.__boxdims[0][0][1]-self.dw/2]
      self.__boxdims[1][1]=[self.__boxdims[0][1][0]-self.dhstrip,self.__boxdims[0][1][1]-self.dhstrip]
      self.__boxdims[1][2]=[self.__boxdims[0][2][0]-self.dw/2,self.__boxdims[0][2][1]-self.dw/2] 
      self.normals[1]=(0,1,0)      
      
      self.__boxdims[2][0]=self.__boxdims[0][0]
      self.__boxdims[2][1]=[self.__boxdims[0][1][0]-self.dh,self.__boxdims[0][1][1]-self.dh]
      self.__boxdims[2][2]=[self.__boxdims[0][2][0]+self.dz,self.__boxdims[0][2][1]+self.dz]
      self.normals[2]=(0,1,0)
 
      self.__boxdims[3][0]=[self.__boxdims[2][0][0]-self.dw/2,self.__boxdims[2][0][1]-self.dw/2]
      self.__boxdims[3][1]=[self.__boxdims[2][1][0]-self.dhstrip,self.__boxdims[2][1][1]-self.dhstrip]
      self.__boxdims[3][2]=[self.__boxdims[2][2][0]-self.dw/2,self.__boxdims[2][2][1]-self.dw/2] 
      self.normals[3]=(0,1,0)
      
      self.SetPlanes()

    if(n==2):
      self.dh=812. #vertical separation between the boxes (cm), (going downward since first box is assumed to be the topmost box)
      self.scanangles[2]=(-1.15,-1.0) #range of angles (radians) that cover this box in acos(pz/p)
      self.scanangles[0]=(-1.4,-1.25) #range of angles (radians) that cover this box in acos(pz/p)
      self.scanangles3d[2]=(-1.15,-1.0) 
      self.scanangles3d[0]=(-1.4,-1.25)
      self.dz=450.8
      
      #top box position, tpc coordinates, other box is positioned relative to this
      self.__boxdims[0][0]=[0.,48.]
      self.__boxdims[0][1]=[353.15,353.15-self.dhstrip] #189 cm (top of tpc to platform) + 163.15 (top of tpc) + 1 (strip depth)
      self.__boxdims[0][2]=[538.,586.]
      
      self.__boxdims[1][0]=[self.__boxdims[0][0][0]-self.dw/2,self.__boxdims[0][0][1]-self.dw/2]
      self.__boxdims[1][1]=[self.__boxdims[0][1][0]-self.dhstrip,self.__boxdims[0][1][1]-self.dhstrip]
      self.__boxdims[1][2]=[self.__boxdims[0][2][0]-self.dw/2,self.__boxdims[0][2][1]-self.dw/2] 
 
      #self.__boxdims[2][0]=self.__boxdims[0][0]
      self.__boxdims[2][0]=[208.35,256.35]
      self.__boxdims[2][1]=[self.__boxdims[0][1][0]-self.dh,self.__boxdims[0][1][1]-self.dh]
      self.__boxdims[2][2]=[self.__boxdims[0][2][0]+self.dz,self.__boxdims[0][2][1]+self.dz] 

 
      self.__boxdims[3][0]=[self.__boxdims[2][0][0]-self.dw/2,self.__boxdims[2][0][1]-self.dw/2]
      self.__boxdims[3][1]=[self.__boxdims[2][1][0]-self.dhstrip,self.__boxdims[2][1][1]-self.dhstrip]
      self.__boxdims[3][2]=[self.__boxdims[2][2][0]-self.dw/2,self.__boxdims[2][2][1]-self.dw/2] 

    if(n==3):
      #both on top, aligned, 0.5 m separation
      self.dw=4.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.dh=50.0 #separation between the boxes (cm)
      self.scanangles[2]=(-2.6,-0.5)
      self.scanangles[0]=(-2.6,-0.5) 
      self.scanangles3d[2]=(-2.6,-0.5) 
      self.scanangles3d[0]=(-2.6,-0.5)  
      
      #top box position, tpc coordinates, other box is positioned relative to this
      self.__boxdims[0][0]=[208.35,256.35]
      self.__boxdims[0][1]=[403.15,403.15-self.dhstrip] #189 cm (top of tpc to platform) + 163.15 (top of tpc) + 50 (box sep) + 1 (strip depth)
      self.__boxdims[0][2]=[538.,586.]
      
      self.__boxdims[1][0]=[self.__boxdims[0][0][0]-self.dw/2,self.__boxdims[0][0][1]-self.dw/2]
      self.__boxdims[1][1]=[self.__boxdims[0][1][0]-self.dhstrip,self.__boxdims[0][1][1]-self.dhstrip]
      self.__boxdims[1][2]=[self.__boxdims[0][2][0]-self.dw/2,self.__boxdims[0][2][1]-self.dw/2] 
 
      self.__boxdims[2][0]=self.__boxdims[0][0]
      self.__boxdims[2][1]=[self.__boxdims[0][1][0]-self.dh,self.__boxdims[0][1][1]-self.dh]
      self.__boxdims[2][2]=[self.__boxdims[0][2][0]+self.dz,self.__boxdims[0][2][1]+self.dz] 

 
      self.__boxdims[3][0]=[self.__boxdims[2][0][0]-self.dw/2,self.__boxdims[2][0][1]-self.dw/2]
      self.__boxdims[3][1]=[self.__boxdims[2][1][0]-self.dhstrip,self.__boxdims[2][1][1]-self.dhstrip]
      self.__boxdims[3][2]=[self.__boxdims[2][2][0]-self.dw/2,self.__boxdims[2][2][1]-self.dw/2] 

    if(n==4):
      #both on top, aligned, 1 m separation
      self.dw=4.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.dh=100.0 #separation between the boxes (cm)
      self.scanangles[2]=(-2.1,-1.0) 
      self.scanangles[0]=(-2.1,-1.0) 
      self.scanangles3d[2]=(-2.1,-1.0) 
      self.scanangles3d[0]=(-2.1,-1.0) 
            
      #top box position, tpc coordinates, other box is positioned relative to this
      self.__boxdims[0][0]=[208.35,256.35]
      self.__boxdims[0][1]=[403.15,403.15-self.dhstrip] #189 cm (top of tpc to platform) + 163.15 (top of tpc) + 50 (box sep) + 1 (strip depth)
      self.__boxdims[0][2]=[538.,586.]
      
      self.__boxdims[1][0]=[self.__boxdims[0][0][0]-self.dw/2,self.__boxdims[0][0][1]-self.dw/2]
      self.__boxdims[1][1]=[self.__boxdims[0][1][0]-self.dhstrip,self.__boxdims[0][1][1]-self.dhstrip]
      self.__boxdims[1][2]=[self.__boxdims[0][2][0]-self.dw/2,self.__boxdims[0][2][1]-self.dw/2] 
 
      self.__boxdims[2][0]=self.__boxdims[0][0]
      self.__boxdims[2][1]=[self.__boxdims[0][1][0]-self.dh,self.__boxdims[0][1][1]-self.dh]
      self.__boxdims[2][2]=[self.__boxdims[0][2][0]+self.dz,self.__boxdims[0][2][1]+self.dz] 

 
      self.__boxdims[3][0]=[self.__boxdims[2][0][0]-self.dw/2,self.__boxdims[2][0][1]-self.dw/2]
      self.__boxdims[3][1]=[self.__boxdims[2][1][0]-self.dhstrip,self.__boxdims[2][1][1]-self.dhstrip]
      self.__boxdims[3][2]=[self.__boxdims[2][2][0]-self.dw/2,self.__boxdims[2][2][1]-self.dw/2] 

    if(n==5):
      #Full veto with 1 boxes
      #1 big at 7m
      self.dw=5.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.scanangles[2]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(pz/p)
      self.scanangles[0]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(px/p)    
      self.nboxes=1
      self.__boxdims=[[[0.0,0.0] for y in xrange(3)] for x in xrange(self.nboxes)]
      self.normals=[(0.0,0.0,0.0) for y in xrange(self.nboxes)] #surface normals for boxes
             
      self.__boxdims[0][0]=[-375.0,615.0]
      self.__boxdims[0][1]=[700.,700.-self.dhstrip] #189 cm (top of tpc to platform) + 163.15 (top of tpc) + 272.8 (dy to free space)
      self.__boxdims[0][2]=[0.,1065.]  
      self.normals[0]=(0,1,0)
      
      self.SetPlanes()

    if(n==6):
      #Full veto with 5 boxes
      #1 big at 7m
      #4 angled around tpc within dimensions from Martin Auger
      self.dw=5.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.scanangles[2]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(pz/p)
      self.scanangles[0]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(px/p)    
      self.nboxes=11
      self.__boxdims=[[[0.0,0.0] for y in xrange(3)] for x in xrange(self.nboxes)]
      self.normals=[(0.0,0.0,0.0) for y in xrange(self.nboxes)] #surface normals for boxes
             
      self.__boxdims[0][0]=[-375.0,615.0]
      self.__boxdims[0][1]=[700.,700.-self.dhstrip]
      self.__boxdims[0][2]=[0.,1065.]  
      self.normals[0]=(0,1,0)

      #vertical modules
      self.__boxdims[1][0]=[-100.,-100.-self.dhstrip]
      self.__boxdims[1][1]=[-81.25,81.25] 
      self.__boxdims[1][2]=[0.,1065.]  
      self.normals[1]=(1,0,0)

      self.__boxdims[2][0]=[256.35+100.,256.35+100.-self.dhstrip]
      self.__boxdims[2][1]=[-81.25,81.25] 
      self.__boxdims[2][2]=[0.,1065.]  
      self.normals[2]=(1,0,0)

      #slanted modules split into steps x<0 side
      self.__boxdims[3][0]=[-100.,-100.+57.5]
      self.__boxdims[3][1]=[81.25,81.25-self.dhstrip] 
      self.__boxdims[3][2]=[0.,1065.]  
      self.normals[3]=(0,1,0)

      self.__boxdims[4][0]=[-100.+57.5,-100.+57.5+self.dhstrip]
      self.__boxdims[4][1]=[81.25,81.25+57.5] 
      self.__boxdims[4][2]=[0.,1065.]  
      self.normals[4]=(1,0,0)
      
      self.__boxdims[5][0]=[-100.+57.5,-100.+57.5+57.5]
      self.__boxdims[5][1]=[81.25+57.5,81.25+57.5+self.dhstrip] 
      self.__boxdims[5][2]=[0.,1065.]  
      self.normals[5]=(0,1,0) 
      
      self.__boxdims[6][0]=[-100.+57.5+57.5,-100.+57.5+57.5+self.dhstrip]
      self.__boxdims[6][1]=[81.25+57.5,81.25+57.5+57.5] 
      self.__boxdims[6][2]=[0.,1065.]  
      self.normals[6]=(0,1,0) 
 
       #slanted modules split into steps x>0 side
      self.__boxdims[7][0]=[256.35+100.,256.35+100.-57.5]
      self.__boxdims[7][1]=[81.25,81.25-self.dhstrip] 
      self.__boxdims[7][2]=[0.,1065.]  
      self.normals[7]=(0,1,0)

      self.__boxdims[8][0]=[256.35+100.-57.5,256.35+100.-57.5+self.dhstrip]
      self.__boxdims[8][1]=[81.25,81.25+57.5] 
      self.__boxdims[8][2]=[0.,1065.]  
      self.normals[8]=(1,0,0)
      
      self.__boxdims[9][0]=[256.35+100.-57.5,256.35++100.-57.5-57.5]
      self.__boxdims[9][1]=[81.25+57.5,81.25+57.5+self.dhstrip] 
      self.__boxdims[9][2]=[0.,1065.]  
      self.normals[9]=(0,1,0) 
      
      self.__boxdims[10][0]=[256.35+100.-57.5-57.5,256.35+100.-57.5-57.5+self.dhstrip]
      self.__boxdims[10][1]=[81.25+57.5,81.25+57.5+57.5] 
      self.__boxdims[10][2]=[0.,1065.]  
      self.normals[10]=(0,1,0) 
           
      self.SetPlanes()
      
    if(n==7):
      #Full veto with 7 boxes
      #1 big at 7m
      #4 angled around tpc within dimensions from Martin Auger
      #2 angled upstream and downstream
      self.dw=5.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.scanangles[2]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(pz/p)
      self.scanangles[0]=(-2.1,-1.0) #range of angles (radians) that cover this box in acos(px/p)    
      self.nboxes=13
      self.__boxdims=[[[0.0,0.0] for y in xrange(3)] for x in xrange(self.nboxes)]
      self.normals=[(0.0,0.0,0.0) for y in xrange(self.nboxes)] #surface normals for boxes
             
      self.__boxdims[0][0]=[-375.0,615.0]
      self.__boxdims[0][1]=[700.,700.-self.dhstrip]
      self.__boxdims[0][2]=[0.,1065.]  
      self.normals[0]=(0,1,0)

      #vertical modules
      self.__boxdims[1][0]=[-100.,-100.-self.dhstrip]
      self.__boxdims[1][1]=[-81.25,81.25] 
      self.__boxdims[1][2]=[0.,1065.]  
      self.normals[1]=(1,0,0)

      self.__boxdims[2][0]=[256.35+100.,256.35+100.-self.dhstrip]
      self.__boxdims[2][1]=[-81.25,81.25] 
      self.__boxdims[2][2]=[0.,1065.]  
      self.normals[2]=(1,0,0)

      #slanted modules split into steps x<0 side
      self.__boxdims[3][0]=[-100.,-100.+57.5]
      self.__boxdims[3][1]=[81.25,81.25-self.dhstrip] 
      self.__boxdims[3][2]=[0.,1065.]  
      self.normals[3]=(0,1,0)

      self.__boxdims[4][0]=[-100.+57.5,-100.+57.5+self.dhstrip]
      self.__boxdims[4][1]=[81.25,81.25+57.5] 
      self.__boxdims[4][2]=[0.,1065.]  
      self.normals[4]=(1,0,0)
      
      self.__boxdims[5][0]=[-100.+57.5,-100.+57.5+57.5]
      self.__boxdims[5][1]=[81.25+57.5,81.25+57.5+self.dhstrip] 
      self.__boxdims[5][2]=[0.,1065.]  
      self.normals[5]=(0,1,0) 
      
      self.__boxdims[6][0]=[-100.+57.5+57.5,-100.+57.5+57.5+self.dhstrip]
      self.__boxdims[6][1]=[81.25+57.5,81.25+57.5+57.5] 
      self.__boxdims[6][2]=[0.,1065.]  
      self.normals[6]=(0,1,0) 
 
       #slanted modules split into steps x>0 side
      self.__boxdims[7][0]=[256.35+100.,256.35+100.-57.5]
      self.__boxdims[7][1]=[81.25,81.25-self.dhstrip] 
      self.__boxdims[7][2]=[0.,1065.]  
      self.normals[7]=(0,1,0)

      self.__boxdims[8][0]=[256.35+100.-57.5,256.35+100.-57.5+self.dhstrip]
      self.__boxdims[8][1]=[81.25,81.25+57.5] 
      self.__boxdims[8][2]=[0.,1065.]  
      self.normals[8]=(1,0,0)
      
      self.__boxdims[9][0]=[256.35+100.-57.5,256.35++100.-57.5-57.5]
      self.__boxdims[9][1]=[81.25+57.5,81.25+57.5+self.dhstrip] 
      self.__boxdims[9][2]=[0.,1065.]  
      self.normals[9]=(0,1,0) 
      
      self.__boxdims[10][0]=[256.35+100.-57.5-57.5,256.35+100.-57.5-57.5+self.dhstrip]
      self.__boxdims[10][1]=[81.25+57.5,81.25+57.5+57.5] 
      self.__boxdims[10][2]=[0.,1065.]  
      self.normals[10]=(0,1,0) 

      #vertical modules up/down stream
      self.__boxdims[11][0]=[0.-50.,256.35+50.]
      self.__boxdims[11][1]=[-116.5-50.,116.5+50.] 
      self.__boxdims[11][2]=[0.-100.,0.-100+self.dhstrip]  
      self.normals[11]=(0,0,1)

      self.__boxdims[12][0]=[0.-50.,256.35+50.]
      self.__boxdims[12][1]=[-116.5-50.,116.5+50.] 
      self.__boxdims[12][2]=[1036.8+100.,1036.8+100+self.dhstrip]  
      self.normals[12]=(0,0,1)  
               
      self.SetPlanes()
      
    if(n==20 or n==21 or n==22 or n==23 or n==24 or n==25):
      #both on top, aligned(20) or offset in x (21), 0.735 m separation
      self.dw=4.0 #width of a strip (cm)
      self.dz=0 #needs to be a multiple of dw (strip width, cm)
      self.dh=74. #table height
      if n==22: self.dh=20
      if n==23: self.dh=300
      if n==24: self.dh=0
      if n==25: self.dh=4

      self.thetas=(-pi/2,-0.8)
      self.phis=(-pi,pi)
      if n==21:
        self.thetas=(-pi/2,-0.6)
        #self.phis=(-1.6,+1.6)   
      if n==22: self.thetas=(-pi/2,-0.2)  
      if n==25: 
        self.thetas=(-pi/2,-0.0)
        self.sigma_rel=(0.1,0.1,0.1) #1 mm relative error when the boxes are on top of each other
      self.nboxes=8
      self.__boxdims=[[[0.0,0.0] for y in xrange(3)] for x in xrange(self.nboxes)]
      self.normals=[(0.0,0.0,0.0) for y in xrange(self.nboxes)] #surface normals for boxes
      
      topboxoffset_x=0
      if n==21:
        topboxoffset_x=48.
        
      #x-bilayer 1 (top box)
      self.__boxdims[0][0]=[208.35+topboxoffset_x,208.35+12*self.dw+topboxoffset_x]
      self.__boxdims[0][1]=[403.15,403.15-self.dhstrip]
      self.__boxdims[0][2]=[538.,538.+12*self.dw]
      self.normals[0]=(0,1,0)
      
      refb=self.__boxdims[0]
      
      self.__boxdims[1][0]=[refb[0][0]+self.dw/2,refb[0][1]+self.dw/2]
      self.__boxdims[1][1]=[refb[1][0]-self.dhstrip,refb[1][1]-self.dhstrip]
      self.__boxdims[1][2]=[refb[2][0],refb[2][1]] 
      self.normals[1]=(0,1,0)

      #z-bilayer 1 (top box)
      self.__boxdims[2][0]=[refb[0][0],refb[0][1]]
      self.__boxdims[2][1]=[refb[1][0]-2.*self.dhstrip,refb[1][1]-2.*self.dhstrip]
      self.__boxdims[2][2]=[refb[2][0],refb[2][1]] 
      self.normals[2]=(0,1,0)

      self.__boxdims[3][0]=[refb[0][0],refb[0][1]]
      self.__boxdims[3][1]=[refb[1][0]-3.*self.dhstrip,refb[1][1]-3.*self.dhstrip]
      self.__boxdims[3][2]=[refb[2][0]+self.dw/2,refb[2][1]+self.dw/2] 
      self.normals[3]=(0,1,0)


      #x-bilayer 2 (bottom box)
      self.__boxdims[4][0]=[refb[0][0]-topboxoffset_x,refb[0][1]-topboxoffset_x]
      self.__boxdims[4][1]=[refb[1][0]-self.dh,refb[1][1]-self.dh]
      self.__boxdims[4][2]=[refb[2][0],refb[2][1]] 
      self.normals[4]=(0,1,0)
      
      refb=self.__boxdims[4] #change reference box for following boxes
      
      self.__boxdims[5][0]=[refb[0][0]+self.dw/2,refb[0][1]+self.dw/2]
      self.__boxdims[5][1]=[refb[1][0]-self.dhstrip,refb[1][1]-self.dhstrip]
      self.__boxdims[5][2]=[refb[2][0],refb[2][1]] 
      self.normals[5]=(0,1,0)     

      #z-bilayer 2 (bottom box)
      self.__boxdims[6][0]=[refb[0][0],refb[0][1]]
      self.__boxdims[6][1]=[refb[1][0]-2.*self.dhstrip,refb[1][1]-2.*self.dhstrip]
      self.__boxdims[6][2]=[refb[2][0],refb[2][1]] 
      self.normals[6]=(0,1,0)

      self.__boxdims[7][0]=[refb[0][0],refb[0][1]]
      self.__boxdims[7][1]=[refb[1][0]-3.*self.dhstrip,refb[1][1]-3.*self.dhstrip]
      self.__boxdims[7][2]=[refb[2][0]+self.dw/2,refb[2][1]+self.dw/2] 
      self.normals[7]=(0,1,0)

     
      self.SetPlanes()

    self.__throwndims=copy.deepcopy(self.__boxdims) #after if statement, deepcopy boxdims to throwndims
                      
  def SetPlanes(self):
    self.planesp=[]
    self.planesd=[]
    #Set 6 plane positions and directions for each box
    for bs in xrange(len(self[:])):
      self.planesp.append([])
      self.planesd.append([])
      #xz
      self.planesp[bs].append((0.5*(self[bs][0][0]+self[bs][0][1]),self[bs][1][0],0.5*(self[bs][2][0]+self[bs][2][1])))
      self.planesp[bs].append((0.5*(self[bs][0][0]+self[bs][0][1]),self[bs][1][1],0.5*(self[bs][2][0]+self[bs][2][1])))
      self.planesd[bs].append(self.normals[bs])
      self.planesd[bs].append(self.normals[bs])
      #xy
      self.planesp[bs].append((0.5*(self[bs][0][0]+self[bs][0][1]),0.5*(self[bs][1][0]+self[bs][1][0]),self[bs][2][0]))
      self.planesp[bs].append((0.5*(self[bs][0][0]+self[bs][0][1]),0.5*(self[bs][1][0]+self[bs][1][0]),self[bs][2][1]))
      rotnormalyz=(self.normals[bs][0],-self.normals[bs][2],self.normals[bs][1]) #rotate normal in yz
      self.planesd[bs].append(rotnormalyz)
      self.planesd[bs].append(rotnormalyz)
      #yz
      self.planesp[bs].append((self[bs][0][0],0.5*(self[bs][1][0]+self[bs][1][0]),0.5*(self[bs][2][0]+self[bs][2][1])))
      self.planesp[bs].append((self[bs][0][1],0.5*(self[bs][1][0]+self[bs][1][0]),0.5*(self[bs][2][0]+self[bs][2][1])))
      rotnormalxy=(-self.normals[bs][1],self.normals[bs][0],self.normals[bs][2]) #rotate normal in xy
      self.planesd[bs].append(rotnormalxy)
      self.planesd[bs].append(rotnormalxy)      
      #print self.planesp[bs]
      #print self.planesd[bs]
      #print ""
      
  def whichStrip(self, bz, lay, dim):
    #strip numbers (low[0] to high[1]) from 0 to dz/dw
    #print bz, lay, dim, self[lay][dim][0]
    #print bz, lay,self[lay][dim][0],self[lay][dim][1],
    if bz<self[lay][dim][0] or bz>self[lay][dim][1]:
      #print -1
      return -1
    else:
      #print int((bz-self[lay][dim][0])/self.dw)
      #if lay==0: print bz, int((bz-self[lay][dim][0])/self.dw)
      if bz==self[lay][dim][1]: #this happens when the muon intersects the edge of the last strip
        return int((bz-self[lay][dim][0]-1e-8)/self.dw)
      else:
        return int((bz-self[lay][dim][0])/self.dw)
      

  def getHitPatternAndTrigger(self,p):
    #assumes 8 boxes
    if len(p)!=8: 
      print "wrong number of positions passed for hit pattern finding..."
      exit(1)
    bx=[]
    bz=[]
    trigger=True #8-fold coincidence?
    for xlayer in (0,1,4,5):
      bx.append(self.whichStrip(p[xlayer][0],xlayer,0))
      bz.append(self.whichStrip(p[xlayer+2][2],xlayer+2,2))
      if bx[-1]>=0 and bx[-1]<=11 and bz[-1]>=0 and bz[-1]<=11 and trigger:
        trigger=True
      else:
        trigger=False
        
    return bx,bz,trigger

  def getStripDims(self, lay, dim, i):
    #In layer lay, dimension dim, return position range and mean
    low=self[lay][dim][0] + self.dw*i
    high=self[lay][dim][0] + self.dw*(i+1)    
    mean=(high+low)/2
    return (low,high),mean

  filesloaded=0
  def loadSmearFiles(self):
    if self.filesloaded==0:
      #load smearing files for current boxset
      self.fsmear0="angular_bs%d_dim0.root"%self.boxset
      self.fsmear2="angular_bs%d_dim2.root"%self.boxset
      print "Loading smearing file %s" % self.fsmear0
      self.tfsmear0=TFile(self.fsmear0,"r")
      print "Loading smearing file %s" % self.fsmear2
      self.tfsmear2=TFile(self.fsmear2,"r")
      if self.tfsmear0.IsOpen() and self.tfsmear2.IsOpen():
        self.filesloaded=1
      else:
        print "Error loading smearing files..."
        exit(1)
    
  
  def getDistsForStrips(self,xStrips,zStrips):
    #pull angular distributions for this strip from the appropriate file
    #print "q%d_%d_%d_%d"%(xStrips[0],xStrips[1],xStrips[2],xStrips[3])
    #print "q%d_%d_%d_%d"%(zStrips[0],zStrips[1],zStrips[2],zStrips[3])
    thxSmear=self.tfsmear0.Get("q%d_%d_%d_%d"%(xStrips[0],xStrips[1],xStrips[2],xStrips[3]))
    thzSmear=self.tfsmear2.Get("q%d_%d_%d_%d"%(zStrips[0],zStrips[1],zStrips[2],zStrips[3]))
    thxPos=self.tfsmear0.Get("xa%d_%d_%d_%d"%(xStrips[0],xStrips[1],xStrips[2],xStrips[3]))
    thzPos=self.tfsmear2.Get("xa%d_%d_%d_%d"%(zStrips[0],zStrips[1],zStrips[2],zStrips[3]))
    #make new 2d dist from these
    #qxzhist=TH2F("qxzhist","", thxSmear.GetNbinsX(),thxSmear.GetBinLowEdge(0),thxSmear.GetBinLowEdge(thxSmear.GetNbinsX()+1), thzSmear.GetNbinsX(),thzSmear.GetBinLowEdge(0),thzSmear.GetBinLowEdge(thzSmear.GetNbinsX()+1))
    #for i in xrange(thxSmear.GetNbinsX()):
    #  for j in xrange(thzSmear.GetNbinsX()):
    #    qxzhist.Fill(thxSmear.GetBinCenter(i),thzSmear.GetBinCenter(j),thxSmear.GetBinContent(i)*thzSmear.GetBinContent(j))
    #qxzhist.Scale(1/qxzhist.Integral())
    
    return (thxSmear,thzSmear,thxPos,thzPos)
      
      
   
