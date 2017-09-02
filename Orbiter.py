from __future__ import division
from math import cos,sin,atan2,pi,sqrt,acos,atan,asin
from PIL import Image,ImageDraw
from random import random


def pyththe(a,b):
	return sqrt(a**2+b**2)

def dist3d(pos1,pos2):
	return pyththe(pyththe(pos2[0]-pos1[0],pos2[1]-pos1[1]),pos2[2]-pos1[2])
	
def toazimuthinclination(pos1,pos2):
	r=dist3d(pos1,pos2)
	(x,y,z)=(pos2[0]-pos1[0],pos2[1]-pos1[1],(pos2[2]-pos1[2])/r)
	print (x,y,z)
	a1=atan(y/x)
	a2=acos(z)
	return (a1,a2)
	
def step2d(posself,posother,selfmass,othermass,movementvector,distance):
	GravityConstant=100
	pull=(othermass/selfmass)/(distance+.01)*GravityConstant
	angle=atan2(posother[1]-posself[1],posother[0]-posself[0])
	return (movementvector[0]+(cos(angle)*pull),movementvector[1]+(sin(angle)*pull),movementvector[2])

class Partical:
	def __init__(self,startpos,mass,radius,velocity):
		global count
		self.num=count
		count+=1
		self.pos=startpos
		self.lastpos=startpos
		self.mass=mass
		self.volume=4*(pi*radius**3)/3
		self.density=self.volume/mass
		self.radius=radius
		self.velocity=velocity
		self.iteration=0
	def gravity(self,Particals,time):
		(x,y,z)=self.velocity
		for i in Particals:
			if not self.num==i.num:
				pos=i.lastpos if i.iteration>self.iteration else i.pos
				(x,y,z)=step2d(self.pos,pos,self.mass,i.mass,(x,y,z),dist3d(self.pos,pos))
		self.iteration +=1
		self.velocity=(x,y,z)
		self.lastpos=self.pos
		self.pos=(self.pos[0]+x*time,self.pos[1]+y*time,self.pos[2]+z*time)
		
def Orbit(Particals,Dim,Type="Trace",frames=100,time=.8):
	(W,H)=Dim
	mid=(W/2,H/2)
	im=Image.new("RGBA",(W,H),(0,0,0,0))
	dr=ImageDraw.Draw(im)
	lp=len(Particals)
	if Type=="Line":
		out=[[] for i in range(lp)]
	for frame in range(frames):
		if Type=="Step":
			im=Image.new("RGBA",(W,H),(0,0,0,0))
			dr=ImageDraw.Draw(im)
		for j in range(lp):
			i=Particals[j]
			Particals[j].gravity(Particals,time)
			col=(255/lp*j,255,255-(255/lp*j),200)
			if Type=="Trace" or Type=="TraceStep" or Type=="Step":
				dr.ellipse((i.pos[0]-i.radius+mid[0],i.pos[1]-i.radius+mid[1],i.pos[0]+i.radius+mid[0],i.pos[1]+i.radius+mid[1]),fill=col)
			if Type=="Line":
				out[j].append((i.pos[0]+mid[0],i.pos[1]+mid[1]))
		if Type=="TraceStep" or Type=="Step":
			im.save("Solanimation/"+(lambda a:"0"*(8-len(a))+a+".png" )(str(frame)))
	if Type=="Line":
		for j in range(len(Particals)):
			for i in range(frames-1):
				col=(255/lp*j,255,255-(255/lp*j),200)
				dr.line((out[j][i][0],out[j][i][1],out[j][(i+1)][0],out[j][(i+1)][1]),fill=(col),width=Particals[j].radius)
	del dr
	return im
	
def OrbitTrace(Particals,Dim,frames=100):
	return Orbit(Particals,Dim,"Trace",frames)

def OrbitTraceStep(Particals,Dim,frames=100):
	return Orbit(Particals,Dim,"TraceStep",frames)
	

def OrbitStep(Particals,Dim,frames=100):
	return Orbit(Particals,Dim,"Step",frames)

def OrbitSingle(Particals,Dim,frames=1000):
	return Orbit(Particals,Dim,"Single",frames)
	
def OrbitLines(Particals,Dim,frames=1000):
	return Orbit(Particals,Dim,"Line",frames)

def SolarOrbit(PlanetCount,Binary=False):
	Star=Partical((0,0,0),700,100,(0,0,0))
	Planets=[]
	for i in range(PlanetCount):
		distance=600+random()*860
		angle=random()*pi*2
		Planets.append(Partical((cos(angle)*distance,sin(angle)*distance,0),100+random()*60,10+random()*8,(cos(angle+pi/2)*50,sin(angle+pi/2)*50,0)))
	return [Star]+Planets

def Balanced(ParticalCount,distance=None,mass=None,force=None,launchangle=None):
	Star=Partical((70,0,0),200,14,(0,0,0))
	if distance==None:
		distance=100+random()*150
	if mass==None:
		mass=30+random()*20
	if force==None:
		force=30+random()*20
	if launchangle==None:
		launchangle=random()*pi*2
	Particals=[Star]
	for i in range(ParticalCount):
		angle=(i/ParticalCount)*pi*2
		Particals.append(Partical((cos(angle)*distance,sin(angle)*distance,0),mass,6,(cos(angle+launchangle)*force,sin(angle+launchangle)*force,0)))
	return Particals
	
def test(angles):
	az=angles[0]
	incl=angles[1]
	print az
	print incl
	r=10
	val=(cos(az)*sin(incl)*r,sin(az)*sin(incl)*r,cos(incl)*r)
	return toazimuthinclination((0,0,0),val)	
for i in range(10):
	print i
	print test((1,pi/5*i+0.0001))
#def Chaos:	

W=640
H=480
count=0
for frame in range(1000):
	Im=OrbitTraceStep(Balanced(2),(W,H),1000)

