from math import *
from ROOT import *

ROOT.gStyle.SetPalette(51)

def rd(rad):
  return 180*rad/pi




class geom:
  def c(a,b):
    return sqrt(a*a + b*b)

  #define the tpc plane positions (p) and unit normal directions (d)
  planesp = [(0.0,0.0,0.0) for x in xrange(6)]  
  planesd = [(0.0,0.0,0.0) for x in xrange(6)] 
  
  tpcdims = ((0,-116.5,0),(256.35,116.5,1036.8)) #two corners define the volume
  tpcboxdims=((0,256.35),(-116.5,116.5),(0,1036.8)) #tpc dims formatted like the boxdims
  label =""
  pl3ds=[]
  drawinit=0
  drawcount=0
  tpclines=[TPolyLine3D(5) for x in xrange(4)]
  boxlines=[]
  
  def __init__(self,inlabel=""):
    
    #tpc planes and surface normals
    #xz
    self.planesp[0]=(0,116.5,0)
    self.planesd[0]=(0,1,0)
    self.planesp[1]=(0,-116.5,0)
    self.planesd[1]=(0,1,0)
    #yz
    self.planesp[2]=(0,0,0)
    self.planesd[2]=(1,0,0)
    self.planesp[3]=(256.35,0,0)
    self.planesd[3]=(1,0,0)
    #xy
    self.planesp[4]=(0,0,0)
    self.planesd[4]=(0,0,1)
    self.planesp[5]=(0,0,1036.8)
    self.planesd[5]=(0,0,1)    
  
    self.label=inlabel
    self.tpcdims
    self.pl3ds=[]
    self.drawinit=0
    self.drawcount=0
    self.tpclines=[TPolyLine3D(5) for x in xrange(4)]
    self.boxlines=[]
    
  def lpIntersection(self,lp,ld,pp,pd):
    #inputs are line position, line direction, plane position, plane direction (normal)
    if not (pd[0]*ld[0] + pd[1]*ld[1] + pd[2]*ld[2])==0:
      intfound=1
      t=-(pd[0]*lp[0] - pd[0]*pp[0] + pd[1]*lp[1] - pd[1]*pp[1] + pd[2]*lp[2] - pd[2]*pp[2])/(pd[0]*ld[0] + pd[1]*ld[1] + pd[2]*ld[2])
      return (lp[0] + ld[0]*t,lp[1] + ld[1]*t,lp[2] + ld[2]*t, 1)
    else:
      return (0,0,0,0)
  
  def OutOfRange(self, x,xrange):
    #check if x outside of xrange while being flexible with the ordering of xrange
    if xrange[1]>xrange[0]:
      return (x<xrange[0] or x>xrange[1])
    else:
      return (x>xrange[0] or x<xrange[1])
  
  def boxints(self, lp,ld,bIncludeUpper,planesp, planesd,boxdims=None):
    #using defined 6 planes, find where or if this line intersects two or none of them
    #parallel lines not handled currently...
    intps=[]
    if bIncludeUpper:
      lowrange=0
    else:
      lowrange=1
    for i in range(lowrange,6):
      pos=self.lpIntersection(lp,ld,planesp[i],planesd[i])
      #print pos
      if(pos[3]==1):
        if boxdims is not None:
          #only keep if it's within the box boundaries
          keep=True
          #print pos
          for dim in xrange(3):
              if self.OutOfRange(pos[dim],boxdims[dim]):
                #print pos[dim],"not in", boxdims[dim]
                keep=False
                break
          if keep: intps.append(pos[0:3])
        else:
          intps.append(pos[0:3])
      #if ints==2: break
    #print intps
    return intps
  
  def firstBoxIntersection(self, lp,ld,bIncludeUpper,planesp, planesd,boxdims):
    intps=self.boxints(lp,ld,bIncludeUpper,planesp, planesd,boxdims)
    #self.drawpoint(intps,len(intps),kBlue)
    if len(intps)>0:
      #find interception with highest y
      maxy=-999.
      keepi=-1
      for i in xrange(len(intps)):
          if intps[i][1]>maxy:
            maxy=intps[i][1]
            keepi=i
      return intps[keepi],True
    else:
      return (-999.,-999.,-999.),False
  
  def tpcendpoint(self,lp,ld):
    #use box ints to find all tpc intersections, then return first one with all dimensions in or on tpc
    intps=self.boxints(lp,ld,True,self.planesp,self.planesd)
    
    for intp in intps:
      #print intp
      #print self.tpcdims
      #print intp[0]>=self.tpcdims[0][0]-1e-12 , intp[0]<=self.tpcdims[1][0]+1e-12 , intp[1]>=self.tpcdims[0][1]-1e-12 , intp[1]<self.tpcdims[1][1] , intp[2]>=self.tpcdims[0][2]-1e-12 , intp[2]<self.tpcdims[1][2]+1e-12
      #note this is < for y so entering point (from top of tpc) isnt considered
      #also added in an epsilon value of 1e-12 to catch rare edge cases (except for top y)
      if(intp[0]>=self.tpcdims[0][0]-1e-12 and intp[0]<=self.tpcdims[1][0]+1e-12 and intp[1]>=self.tpcdims[0][1]-1e-12 and intp[1]<self.tpcdims[1][1] and intp[2]>=self.tpcdims[0][2]-1e-12 and intp[2]<self.tpcdims[1][2]+1e-12):
        #print "found it:", intp
        return intp
    
    #if no intersections are found, then return -999,-999,-999
    return (-999.,-999.,-999.)

  def tpcintersections(self,x,y,z,theta, phi):
    #use box ints to find all tpc intersections, then return all of them
    ld=self.getDirectionVector(theta,phi)
    lp=[x,y,z]
    #print lp, ld
    intps=self.boxints(lp,ld,True,self.planesp,self.planesd)
    
    tpcintersections=[]
    for intp in intps:
      #print intp
      #print self.tpcdims
      #print intp[0]>=self.tpcdims[0][0]-1e-12 , intp[0]<=self.tpcdims[1][0]+1e-12 , intp[1]>=self.tpcdims[0][1]-1e-12 , intp[1]<=self.tpcdims[1][1]+1e-12 , intp[2]>=self.tpcdims[0][2]-1e-12 , intp[2]<self.tpcdims[1][2]+1e-12
      #also added in an epsilon value of 1e-12 to catch rare edge cases
      if(intp[0]>=self.tpcdims[0][0]-1e-12 and intp[0]<=self.tpcdims[1][0]+1e-12 and intp[1]>=self.tpcdims[0][1]-1e-12 and intp[1]<=self.tpcdims[1][1]+1e-12 and intp[2]>=self.tpcdims[0][2]-1e-12 and intp[2]<self.tpcdims[1][2]+1e-12):
        #print "found it:", intp
        tpcintersections.append(intp)
    
    if len(tpcintersections)==2:
      #print tpcintersections
      return (True, tpcintersections)
    else:
      return (False, ((-999.,-999.,-999.),(-999.,-999.,-999.)))


  def initdraw(self):
    self.drawcanv = TCanvas("tdview"+self.label, "",0 ,0,750,750)
    self.view = TView.CreateView(1)
    self.view.ShowAxis()
    self.drawtpc()
    self.drawinit=1
  
  
  
  def drawpoint(self, inBoxPs, nlines, linecolor=0, drawopt="",linewidth=1):
    if self.drawinit==0:
      self.initdraw()
    self.drawcanv.cd()
    
    
    self.pl3ds.append(TPolyLine3D(nlines))
    self.pl3ds[-1].SetLineWidth(linewidth)
    #print len(self.pl3ds)
    for i in xrange(nlines):
      #print inBoxPs[i]
      #don't draw invalid points (-999.0)
      #if inBoxPs[i][0]!=-999.0: self.pl3ds[self.drawcount].SetPoint(i,inBoxPs[i][0],inBoxPs[i][2],inBoxPs[i][1])
      if inBoxPs[i][0]!=-999.0: self.pl3ds[self.drawcount].SetPoint(i,inBoxPs[i][0],inBoxPs[i][1],inBoxPs[i][2])   
      
    if linecolor>0: self.pl3ds[self.drawcount].SetLineColor(linecolor)
    self.pl3ds[self.drawcount].Draw(drawopt+" same")
    self.drawcount+=1
    #c1.Update()



  def drawValidPoints(self,inBoxPs,linecolor=0):
    pts=[]
    for i in xrange(len(inBoxPs)):
      if inBoxPs[i][0]!=-999.0: pts.append(inBoxPs[i])
      
    self.drawpoint(pts,len(pts),linecolor)



  
  def drawtpc(self):
    self.drawcanv.cd()

    #xy faces
    self.tpclines[0].SetPoint(0,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[0][2])
    self.tpclines[0].SetPoint(1,self.tpcdims[1][0],self.tpcdims[0][1],self.tpcdims[0][2])
    self.tpclines[0].SetPoint(2,self.tpcdims[1][0],self.tpcdims[1][1],self.tpcdims[0][2])
    self.tpclines[0].SetPoint(3,self.tpcdims[0][0],self.tpcdims[1][1],self.tpcdims[0][2])
    self.tpclines[0].SetPoint(4,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[0][2])
    
    self.tpclines[1].SetPoint(0,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[1][2])
    self.tpclines[1].SetPoint(1,self.tpcdims[1][0],self.tpcdims[0][1],self.tpcdims[1][2])
    self.tpclines[1].SetPoint(2,self.tpcdims[1][0],self.tpcdims[1][1],self.tpcdims[1][2])
    self.tpclines[1].SetPoint(3,self.tpcdims[0][0],self.tpcdims[1][1],self.tpcdims[1][2])
    self.tpclines[1].SetPoint(4,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[1][2])
    
    #xz faces
    self.tpclines[2].SetPoint(0,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[0][2])
    self.tpclines[2].SetPoint(1,self.tpcdims[1][0],self.tpcdims[0][1],self.tpcdims[0][2])
    self.tpclines[2].SetPoint(2,self.tpcdims[1][0],self.tpcdims[0][1],self.tpcdims[1][2])
    self.tpclines[2].SetPoint(3,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[1][2])
    self.tpclines[2].SetPoint(4,self.tpcdims[0][0],self.tpcdims[0][1],self.tpcdims[0][2])
    
    self.tpclines[3].SetPoint(0,self.tpcdims[0][0],self.tpcdims[1][1],self.tpcdims[0][2])
    self.tpclines[3].SetPoint(1,self.tpcdims[1][0],self.tpcdims[1][1],self.tpcdims[0][2])
    self.tpclines[3].SetPoint(2,self.tpcdims[1][0],self.tpcdims[1][1],self.tpcdims[1][2])
    self.tpclines[3].SetPoint(3,self.tpcdims[0][0],self.tpcdims[1][1],self.tpcdims[1][2])
    self.tpclines[3].SetPoint(4,self.tpcdims[0][0],self.tpcdims[1][1],self.tpcdims[0][2])
    
    #that's enough to get the idea across...
    for l in self.tpclines: 
      l.SetLineColor(4)
      l.Draw("same")
  
  def drawSquareOnX(self, xpos, starty, endy, startz, endz, color=2, lw=2):
    if self.drawinit==0:
      self.initdraw()
    self.boxlines.append(TPolyLine3D(5))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,xpos,starty,startz)
    self.boxlines[i].SetPoint(1,xpos,starty,endz)
    self.boxlines[i].SetPoint(2,xpos,endy,endz)
    self.boxlines[i].SetPoint(3,xpos,endy,startz)
    self.boxlines[i].SetPoint(4,xpos,starty,startz)    
    self.boxlines[i].SetLineColor(color)
    self.boxlines[i].SetLineWidth(lw)
    self.boxlines[i].Draw("same")     
    
  def drawCrossOnX(self, xpos, starty, endy, startz, endz, color=2, lw=2):
    if self.drawinit==0:
      self.initdraw()    
    self.boxlines.append(TPolyLine3D(2))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,xpos,starty,startz)
    self.boxlines[i].SetPoint(1,xpos,endy,endz)   
    self.boxlines[i].SetLineColor(color)
    self.boxlines[i].SetLineWidth(lw)
    self.boxlines[i].Draw("same")   
    
    self.boxlines.append(TPolyLine3D(2))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,xpos,starty,endz)
    self.boxlines[i].SetPoint(1,xpos,endy,startz)     
    self.boxlines[i].SetLineColor(color)
    self.boxlines[i].SetLineWidth(lw)
    self.boxlines[i].Draw("same")       
  
  def drawbox(self, box):
    if self.drawinit==0:
      self.initdraw()

    #xy faces
    self.boxlines.append(TPolyLine3D(5))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,box[0][0],box[1][0],box[2][0])
    self.boxlines[i].SetPoint(1,box[0][1],box[1][0],box[2][0])
    self.boxlines[i].SetPoint(2,box[0][1],box[1][0],box[2][1])
    self.boxlines[i].SetPoint(3,box[0][0],box[1][0],box[2][1])
    self.boxlines[i].SetPoint(4,box[0][0],box[1][0],box[2][0])    
    self.boxlines[i].SetLineColor(2)
    self.boxlines[i].Draw("same")
    		
    self.boxlines.append(TPolyLine3D(5))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,box[0][0],box[1][1],box[2][0])
    self.boxlines[i].SetPoint(1,box[0][1],box[1][1],box[2][0])
    self.boxlines[i].SetPoint(2,box[0][1],box[1][1],box[2][1])
    self.boxlines[i].SetPoint(3,box[0][0],box[1][1],box[2][1])
    self.boxlines[i].SetPoint(4,box[0][0],box[1][1],box[2][0])
    self.boxlines[i].SetLineColor(2)
    self.boxlines[i].Draw("same")
     
    #xz faces
    self.boxlines.append(TPolyLine3D(5))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,box[0][0],box[1][0],box[2][0])
    self.boxlines[i].SetPoint(1,box[0][1],box[1][0],box[2][0])
    self.boxlines[i].SetPoint(2,box[0][1],box[1][1],box[2][0])
    self.boxlines[i].SetPoint(3,box[0][0],box[1][1],box[2][0])
    self.boxlines[i].SetPoint(4,box[0][0],box[1][0],box[2][0])    
    self.boxlines[i].SetLineColor(2)
    self.boxlines[i].Draw("same")
    
    self.boxlines.append(TPolyLine3D(5))
    i=len(self.boxlines)-1
    self.boxlines[i].SetPoint(0,box[0][0],box[1][0],box[2][1])
    self.boxlines[i].SetPoint(1,box[0][1],box[1][0],box[2][1])
    self.boxlines[i].SetPoint(2,box[0][1],box[1][1],box[2][1])
    self.boxlines[i].SetPoint(3,box[0][0],box[1][1],box[2][1])
    self.boxlines[i].SetPoint(4,box[0][0],box[1][0],box[2][1])
    self.boxlines[i].SetLineColor(2)
    self.boxlines[i].Draw("same")
    
  
  
  def close(self,tfout):
    #write canvas
    tfout.cd()
    #self.view.SetRange(-200,-100,-1000,500,1100,1000)
    self.drawcanv.Modified()
    self.drawcanv.Update()
    self.drawcanv.Write()
    #self.view.Write("tdviewrange")
    
   # self.drawcanv.SaveAs("tdview_test.png")

  def getThetaPhiFromThetas(self,qxy,qyz):
    tqxy=tan(qxy)
    tqyz=tan(qyz)
    theta=-pi/2+acos(((1+tqxy**-2+tqyz**-2)**-0.5))
    phi=atan2(sin(theta)/tan(qyz),sin(theta)/tan(qxy))
    return theta,phi

  def getThetaPhiFromLD(self,ld):
    return asin(ld[1]),atan2(ld[2],ld[0])

  def getThetaPhiLDFromLine(self,lstart,lend):
    #lstart and lend are start and end positions of vector
    llen=sqrt(pow(lstart[0]-lend[0],2)+pow(lstart[1]-lend[1],2)+pow(lstart[2]-lend[2],2))
    ld=((lstart[0]-lend[0])/llen,(lstart[1]-lend[1])/llen,(lstart[2]-lend[2])/llen) #get line direction
    theta=asin(ld[1])
    #phi=acos(ld[0]/cos(-theta))
    phi=atan2(ld[2],ld[0])
    return theta,phi,ld

  def getDirectionVector(self,theta,phi):
    #return (abs(cos(theta))*cos(phi),sin(-theta),abs(cos(theta))*sin(phi)) #this get the sign wrong on x and z components
    return ((cos(theta))*cos(phi),sin(theta),(cos(theta))*sin(phi))
    
  def getNewPos(self,x,y,z,theta, phi, newy):
    #propogate position back to height newy
    #newx=x+(newy+116.5-y)*cos(-theta)/tan(-phi)
    #newz=z+(newy+116.5-y)*sin(-theta)/tan(-phi)
    #print ""
    #print "newx,newz",newx,newz
    #return(newx,newy,newz)
    
    #print "x,y,z,theta,phi,newy: ",x,y,z,theta,phi,newy
    #direction vector, abs is to fix problem with definition of theta
    ld=self.getDirectionVector(theta,phi)
    #ld=[abs(cos(theta))*cos(phi),sin(-theta),abs(cos(theta))*sin(phi)]
    #print "len:", sqrt(ld[0]*ld[0]+ld[1]*ld[1]+ld[2]*ld[2])
    #ld=[theta,phi,sin(theta)*sin(phi)]
    #print "true ld:",ld
    #distance (hypoten.) to bottom of tpc
    d=(newy-y)/ld[1]
    #print "d:",d
    #update positions
    newpos=[x+d*ld[0], y+d*ld[1], z+d*ld[2]]
    #print "newpos:",newpos
        
    return(newpos[0],newpos[1],newpos[2])    

  def getNewPosFromld(self,x,y,z,ld, newy):
    d=(newy-y)/ld[1]
    newpos=[x+d*ld[0], y+d*ld[1], z+d*ld[2]]
    return(newpos[0],newpos[1],newpos[2])   
    
    
  def getNewPos_tpcendpoint(self,x,y,z,theta, phi, newy):
    #propogate position back to height newy
    #if this is outside the tpc x,z dimensions, find the intersection with the x,z wall

    #direction vector
    ld=self.getDirectionVector(theta,phi)
    #ld=[abs(cos(theta))*cos(phi),sin(-theta),abs(cos(theta))*sin(phi)]
    #distance (hypoten.) to bottom of tpc
    d=(newy-y)/ld[1]
    #update positions
    newpos=[x+d*ld[0], y+d*ld[1], z+d*ld[2]]
    
    if(newpos[0]<self.tpcdims[0][0] or newpos[0]>self.tpcdims[1][0]):
      #print "out of bounds x, newpos:",newpos
      #form line start and direction
      ls=[x,y,z]
      #ld=[sin(-theta-pi/2)*cos(phi),cos(-theta-pi/2),sin(-theta-pi/2)*sin(phi)]
      #print "theta, phi:", rd(theta), rd(phi)
      #print "true: formed start/dir for line:", ls, ld
      newpos=self.tpcendpoint(ls,ld)
      #print "geometry intercept:", newpos

    return(newpos[0],newpos[1],newpos[2])
    
  def getNewPos_tpcendpoint_dcos(self,x,y,z,qx,qz,newy):
    #get third direction angle using cos^2(qz)+cos^2(qx)+cos^2(qy)=1
    if (1-cos(qx)*cos(qx)-cos(qz)*cos(qz))<0.:
      print "Invalid set of angles:"
      print "   (1-cos(qx)*cos(qx)-cos(qz)*cos(qz))=",(1-cos(qx)*cos(qx)-cos(qz)*cos(qz))
      print "   qx=",qx,"   qz=",qz
      return(-999.,-999.,-999.)
    qy=acos(sqrt(1-cos(qx)*cos(qx)-cos(qz)*cos(qz)))
    #print "qs: ",qx,qy,qz
    #direction vector
    ld=[cos(qx),-cos(qy),cos(qz)]
    #print "ld:",ld
    #print "len:", sqrt(ld[0]*ld[0]+ld[1]*ld[1]+ld[2]*ld[2])
    d=(newy-y)/ld[1]
    #update positions
    newpos=[x+d*ld[0], y+d*ld[1], z+d*ld[2]]
    
    if(newpos[0]<self.tpcdims[0][0] or newpos[0]>self.tpcdims[1][0]):
      #print "out of bounds x, newpos:",newpos
      #form line start and direction
      ls=[x,y,z]
      #ld=[sin(-theta-pi/2)*cos(phi),cos(-theta-pi/2),sin(-theta-pi/2)*sin(phi)]
      #print "theta, phi:", rd(theta), rd(phi)
      #print "reco: formed start/dir for line:", ls, ld
      newpos=self.tpcendpoint(ls,ld)
      #print "geometry intercept:", newpos

    return(newpos[0],newpos[1],newpos[2])
    
  def posinbox(self,box,pos, dim1, dim2):
    #print pos[dim1]>box[dim1][0] and pos[dim1]<box[dim1][1], pos[dim1], box[dim1][0],  box[dim1][1]
    #print pos[dim2]>box[dim2][0] and pos[dim2]<box[dim2][1], pos[dim2], box[dim2][0],  box[dim2][1]
    #print ""
    #print box, pos
    if pos[dim1]>box[dim1][0] and pos[dim1]<box[dim1][1] and pos[dim2]>box[dim2][0] and pos[dim2]<box[dim2][1]:
      return True
    else:
      return False

  #def getNewPosInBox(self, ev, bshortcircuit, bs, bangles_in=False, theta_in=0, phi_in=0):
  #  #bshortcircuit=true returns as soon as one position is outside of a box
  #  posinbox1=posinbox2=posinbox3=posinbox4=bintersectsTPC=False
  #  if bangles_in:
  #    theta=theta_in
  #    phi=phi_in
  #  else:
  #    theta=ev.theta
  #    phi=ev.phi
  #
  #  posb1=self.getNewPos((ev.StartPointx_tpcFV), ev.StartPointy_tpcFV, ev.StartPointz_tpcFV, theta, phi, bs[0][1][0])
  #  posinbox1=self.posinbox(bs[0],posb1,0,2)
  #  if not posinbox1 and bshortcircuit:
  #    return False,(0,0,0,0,0,0),(posinbox1,posinbox2,posinbox3,posinbox4,bintersectsTPC)
  #      
  #  posb2=self.getNewPos((ev.StartPointx_tpcFV), ev.StartPointy_tpcFV, ev.StartPointz_tpcFV, theta, phi, bs[1][1][0])
  #  posinbox2=self.posinbox(bs[1],posb2,0,2)
  #  if not posinbox2 and bshortcircuit:
  #    return False,(posb1,0,0,0,0,0),(posinbox1,posinbox2,posinbox3,posinbox4,bintersectsTPC)
  #        
  #  if len(bs)>2:
  #    posb3=self.getNewPos((ev.StartPointx_tpcFV), ev.StartPointy_tpcFV, ev.StartPointz_tpcFV, theta, phi, bs[2][1][0])
  #    posinbox3=self.posinbox(bs[2],posb3,0,2)
  #    if not posinbox3 and bshortcircuit:
  #      return False,(posb1,posb2,0,0,0,0),(posinbox1,posinbox2,posinbox3,posinbox4,bintersectsTPC)
  #      
  #    posb4=self.getNewPos((ev.StartPointx_tpcFV), ev.StartPointy_tpcFV, ev.StartPointz_tpcFV, theta, phi, bs[3][1][0])
  #    posinbox4=self.posinbox(bs[3],posb4,0,2)
  #    if not posinbox4 and bshortcircuit:
  #      return False,(posb1,posb2,posb3,0,0,0),(posinbox1,posinbox2,posinbox3,posinbox4,bintersectsTPC)
  #  else:
  #    posb3=posb1
  #    posb4=posb2
  #    posinbox3=posinbox4=True
  #    
  #  (bintersectsTPC,tpcints)=self.tpcintersections(ev.StartPointx_tpcFV, ev.StartPointy_tpcFV, ev.StartPointz_tpcFV, theta, phi)
  #  
  #  #return tpc positions ordered in descending y
  #  if tpcints[0][1]>tpcints[1][1]:
  #    i=0
  #    j=1
  #  else:
  #    i=1
  #    j=0
  #  #print "tpcints:", tpcints[i], tpcints[j]
  #  return (posinbox1 and posinbox2 and posinbox3 and posinbox4),(posb1,posb2,posb3,posb4,tpcints[i],tpcints[j]),(posinbox1,posinbox2,posinbox3,posinbox4,bintersectsTPC)

  def getNewPosInBox3d(self, ev, bs, bangles_in=False, theta_in=0, phi_in=0):
    #similiar to above, but use 3d implementions of intersection algs
    if type(ev) is dict:
      start=(ev['StartPointx_tpcFV'], ev['StartPointy_tpcFV'], ev['StartPointz_tpcFV'])
      theta=ev['theta']
      phi=ev['phi']
    else:
      #read from ttree event
      start=(ev.StartPointx_tpcFV, ev.StartPointy_tpcFV, ev.StartPointz_tpcFV)
      if bangles_in:
        theta=theta_in
        phi=phi_in
      else:
        theta=ev.theta
        phi=ev.phi
      
      
    posinbox1=posinbox2=posinbox3=posinbox4=bintersectsTPC=False

    
    lp=start
    ld=self.getDirectionVector(theta,phi)

    #check box interceptions
    posb=[]
    posinbox=[]
    binallboxes=True
    for b in xrange(bs.nboxes):
      tposb,tposinbox=self.firstBoxIntersection(lp,ld,True,bs.planesp[b], bs.planesd[b], bs[b])
      posb.append(tposb)
      posinbox.append(tposinbox)
      binallboxes=(binallboxes and posinbox[-1])
      
    #check tpc intersections
    (bintersectsTPC,tpcints)=self.tpcintersections(start[0], start[1], start[2], theta, phi)
      
    #return tpc positions ordered in descending y
    if tpcints[0][1]>tpcints[1][1]:
      i=0
      j=1
    else:
      i=1
      j=0
    #print "tpcints:", tpcints[i], tpcints[j]
    posb.append(tpcints[i])
    posb.append(tpcints[j])
    posinbox.append(bintersectsTPC)
    return binallboxes,posb,posinbox

  def getNewPosInBox3d_noEvent(self,start,bs,theta_in, phi_in):
    #wrapper for getNewPosInBox3d to create the ev dict
    ev = {'StartPointx_tpcFV':start[0],'StartPointy_tpcFV':start[1],'StartPointz_tpcFV':start[2],'theta':theta_in,'phi':phi_in}
    return self.getNewPosInBox3d(ev,bs)
  

  def getNewRecoPosInBox(self,xstart, zstart, xangle, zangle, bs):
    #return reco positions at each box using reco position of first box, and reco angles
    posba=(xstart,bs[0][1][0],zstart)
    posbb=(xstart+(-bs[0][1][0]+bs[1][1][0])/tan(xangle),bs[1][1][0],zstart+(-bs[0][1][0]+bs[1][1][0])/tan(zangle))
    posbc=(xstart+(-bs[0][1][0]+bs[2][1][0])/tan(xangle),bs[2][1][0],zstart+(-bs[0][1][0]+bs[2][1][0])/tan(zangle)) 
    posbd=(xstart+(-bs[0][1][0]+bs[3][1][0])/tan(xangle),bs[2][1][0],zstart+(-bs[0][1][0]+bs[3][1][0])/tan(zangle)) 

    postpctop=self.getNewPos_tpcendpoint_dcos(xstart,bs[0][1][0],zstart,xangle,zangle,self.tpcdims[1][1])
    postpcbottom=self.getNewPos_tpcendpoint_dcos(xstart,bs[0][1][0],zstart,xangle,zangle,self.tpcdims[0][1])
    
    return {'posba':posba, 'posbb':posbb, 'posbc':posbc, 'posbd':posbd, 'postpctop':postpctop, 'postpcbottom':postpcbottom}
  


