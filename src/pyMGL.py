


'''
20101225 EC@PYCHEUNG pyMGL V2
maya-python-sketch revised

changelog:
20100903 python OPENGL toolset
20101029 update
20101225 v2 - module
20110427 - update drawing primitves +plane + polygon

'''
def splash():
	#pyMGL V2 BUILD20101225
	return """
pyMGL V2.1 BUILD20110216
2010-2011 E.PYC 
required pyMGLnode.py
more info at http://eric.pycheung.com
	"""
print splash()

def about():
	cmds.confirmDialog( title='About', message=splash(), button='ok')
	

import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import math
import random
from maya.OpenMaya import MVector
from maya.OpenMaya import MPoint
from maya.OpenMaya import MImage
from maya.OpenMaya import MColor
import maya.cmds as cmds
import maya.mel as mel
import os
import time

#pyMGL specification documentation

timedebug = 0
HUD = 0
'''
use:
this script initiate the python MGL drawing overlay in the current viewport
read and draws the global variables stored as list/hash as points, line, rect, circle

#import pyMGL
'''



############ DATA METHODS
'''
append(type,data)

clear(type)
'''

############ DATA STUCTURE
'''
list =
{
color:(),
fill:(),
weight:(),
size:5,
normal:() *
}
'''

'''
TYPES:
pointList = []
vectorList = []
lineList = []
voxelList = []
quadList = []
circleList = []
'''

#Init data list
pointList = []
vectorList = []
lineList = []
voxelList = []
rectList = []
rect2List = []
circleList = []
ellipseList = []

textList = []

drawTypes = ["point","vector","line","polyline","voxel","rect","rect2","circle","ellipse","plane","polygon"]

storeByID = {0:{"point":[],"vector":[],"line":[],"polyline":[],"voxel":[],"rect":[],"rect2":[],"circle":[],"ellipse":[],"text":[]}}

visibleID = set([0])


def getList(type,inID=0):
	# if type == "point":
		# return pointList
	# elif type == "vector":
		# return vectorList
	# elif type == "line":
		# return lineList
	# elif type == "voxel":
		# return voxelList
	# elif type == "rect":
		# return rectList
	# elif type == "rect2":
		# return rect2List
	# elif type == "circle":
		# return circleList
	# elif type == "ellipse":
		# return ellipseList
	# elif type == "text":
		# return textList
	# else:
		# print "error getType: check type name"
		# return []
	if inID in storeByID:
		return storeByID.get(inID).get(type,[])
	else:
		return []
	
def add(type,inData,inID=0):
	global storeByID,visibleID
	# print inID
	try:
		if inData.get("point"):
			# print inData
			tempList = getList(type,inID)
			tempList.append(inData)
			# print tempList
			if inID in storeByID:
				storeByID.get(inID).update({type:tempList})
			else:
				# print "add"
				storeByID.update({inID:{type:tempList}})
				visibleID.add(inID)
			# print storeByID.get(inID,0)
		else:
			print "invalid data" + str(type) + " " + str(inData)
			
	except:
		print "invalid data"

def showAll():	
	global visibleID
	visibleID = set(storeByID.keys())
	
def showID(inID=0):
	global visibleID
	visibleID.add(inID)
	
def hideID(inID=0):
	global visibleID
	visibleID.discard(inID)

#drawID as text
def debugID():
	global storeByID,visibleID
	clearID("debug")
	pointIDpair = []
	for inID,hash in storeByID.iteritems():
		if inID in visibleID and inID != "debug":
			# print inID
			for eachType,drawList in hash.iteritems():
				if eachType != "text":
					for eachHash in drawList:
						point = eachHash.get("point",0)
						point = MPoint(point[0],point[1]+1,point[2])
						pointIDpair.append([point,inID])
						# print eachHash
					
	if len(pointIDpair):
		for each in pointIDpair:
			id("debug")
			text(each[0],"ID "+str(each[1]))
	
	reset()
	
def clear(type):
	global storeByID
	try:

		for inID,hash in storeByID.iteritems():
			hash.update({type:[]})
		# del getList(type,inID)[:]
	except:
		pass
		
def clear2(type,inID=0):
	global storeByID
	try:
		if inID in storeByID:
			storeByID.get(inID).update({type:[]})
		# del getList(type,inID)[:]
	except:
		pass
		
def clearID(inID=0):
	global storeByID
	try:
		if inID in storeByID:
			del storeByID[inID]
		# del getList(type,inID)[:]
	except:
		pass
	
def clearall():
	# if fadeBln:
		# fadeall()
	# else:
	for eachType in drawTypes:
		clear(eachType)
		
	clear("text")
		
		
############################### SLOW
#Fade data list
pointFade = []
vectorFade = []
lineFade = []
voxelFade = []
rectFade = []
rect2Fade = []
circleFade = []
ellipseFade = []
textFade = []

def getFadeList(type):
	if type == "point":
		return pointFade
	elif type == "vector":
		return vectorFade
	elif type == "line":
		return lineFade
	elif type == "voxel":
		return voxelFade
	elif type == "rect":
		return rectFade
	elif type == "rect2":
		return rect2Fade
	elif type == "circle":
		return circleFade
	elif type == "ellipse":
		return ellipseFade
	elif type == "text":
		return textFade
	else:
		print "error getType: check type name"
		return []

def writeFadeList(type,list):
	global pointFade, vectorFade, lineFade, voxelFade, rectFade,rect2Fade, circleFade, textFade,ellipseFade

	if type == "point":
		pointFade = list
	elif type == "vector":
		vectorFade = list
	elif type == "line":
		lineFade = list
	elif type == "voxel":
		voxelFade = list
	elif type == "rect":
		rectFade = list
	elif type == "rect2":
		rect2Fade = list
	elif type == "circle":
		circleFade = list
	elif type == "ellipse":
		ellipseFade = list
	elif type == "text":
		textFade = list
	else:
		print "error getType: check type name"
		
def fade(type,inID=1):
	#store current list in temp & clear current
	# getFadeList(type).extend(getList(type,inID))
	# clear(type)
	# writeFade(type)
	print "fade disabled"
	
def fadeall():
	for type in drawTypes:
		fade(type)
	fade("text")


def writeFade(type):
	#read stored data adjust color alpha value
	# if alpha value < 0.2 discard
	fadeList = getFadeList(type)
	#del getFadeList(type)[:]
	tempList = []
	
	for eachHash in fadeList:
	
		addThis = False
		fadeColor = eachHash.get("color")
		fadeFill = eachHash.get("fill",0)
		alpha = fadeColor[3]
		
		if fadeBln > 1:
			modFactor = 1
		else:
			modFactor = fadeBln
			
		newAlpha = alpha*modFactor
		if newAlpha > 0.1 and newAlpha < 1:
			eachHash.update({"color":(fadeColor[0],fadeColor[1],fadeColor[2],newAlpha)})
			addThis = True
		
		if fill:
			try:
				if newAlpha > 0.1 and newAlpha < 1:
					eachHash.update({"fill":(fadeFill[0],fadeFill[1],fadeFill[2],newAlpha)})
					addThis = True
			except:
				pass
		
		if addThis:
			tempList.append(eachHash)
		
		
	writeFadeList(type,tempList)
	
	#print getFadeList(type)
	
def purgeFade():
	try:
		for eachType in drawTypes:
			del getFadeList(eachType)[:]
			
		del getFadeList("text")[:]
	except:
		pass
	
def setFade(num):
	global fadeBln
	fadeBln = num
	#print fadeBln
	
fadeBln = 0.0
'''



pyMGL.fade("point")
pyMGL.writeFade("point")
timeWrapper()


'''


############################### SLOW
	
	
#default value
defaultValue = {
"color":(0,0,0,0),
"vector":(0,0,0),
"fill":(0,0,0,0),
"weight":5,
"size":5,
"normal":(0,1,0)
}


	
'''
def buildList(type):
	for eachHash in getList(type):
		testDraw(type,eachHash)
'''

		
		

	

def buildGL():

	def createDrawing(type,inHash):
		point = inHash.get("point",0)
		if point:
			color = inHash.get("color",defaultValue["color"])
			if len(color) == 3:
				color = (color[0],color[1],color[2],1)
						
			fill = inHash.get("fill",defaultValue["fill"])
			weight = inHash.get("weight",defaultValue["weight"])
			id = inHash.get("id",0)
			glow = inHash.get("glow",0)
			
			if type == "point":
				
				if glow:
					glowcolor = inHash.get("glowcolor",color)
					if not glowcolor:
						glowcolor = color
					
					glowrange = glow*0.4
					glowstep = glow/float(glowrange)
					for i in range(1,glow-3):
						adjustweight = (weight+glow-(glowstep*i))
						if adjustweight < weight:
							break
						# print adjustweight,i/float(glow
						newAlpha = i/float(glow)
						# print newAlpha,color[3]
						if newAlpha >= color[3]:
							break
						color2 = (glowcolor[0],glowcolor[1],glowcolor[2],newAlpha)
						drawPoint(point,color2,adjustweight)
						
				drawPoint(point,color,weight) #######
				
			elif type == "vector":
				vector = inHash.get("vector",defaultValue["vector"])
				size = inHash.get("size",0.05)
				unit = inHash.get("unit",0)
				drawVector(point,vector,color,weight,size,unit) #######
			elif type == "line":
				point2 = inHash.get("point2",point)
				drawLine(point,point2,color,weight) #######
				
			elif type == "polyline":
				ptlist = inHash.get("list")
				close = inHash.get("close")
				if len(ptlist):
					zippedPair = zip(ptlist[0::1], ptlist[1::1])
					if close:
						zippedPair.append((ptlist[len(ptlist)-1],ptlist[0]))
					for eachPair in zippedPair:
						drawLine(eachPair[0],eachPair[1],color,weight)
						# print "draw pair"
						
			elif type == "polygon":
				ptlist = inHash.get("list")
				# close = inHash.get("close")
				if len(ptlist):
					# ptlist.append(ptlist[0])
					drawPolygon(ptlist,color,weight,fill)
						# print "draw pair"
				
			elif type == "voxel":
				size = inHash.get("size",defaultValue["size"])
				drawVoxel(point,color,weight,size) #######
				
			elif type == "rect":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				fill = inHash.get("fill",0)
				drawRect(point,color,weight,size,normal,fill) #######
				
			elif type == "rect2":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",(0,0,0))
				plane = inHash.get("plane",(0,0,0))
				upVec = inHash.get("up",(0,0,0))
				fill = inHash.get("fill",0)
				drawRect2(point,color,weight,size,(0,0,0),normal,upVec,fill) #######
				
			elif type == "plane":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",(0,1,0))
				fill = inHash.get("fill",0)
				drawPlane(point,color,weight,size,normal,fill) #######
				
			elif type == "circle":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				fill = inHash.get("fill",0)
				drawCircle(point,color,weight,size,normal,fill) #######
				
			elif type == "ellipse":
				x = inHash.get("x",defaultValue["size"])
				y = inHash.get("y",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				angle = inHash.get("angle",0)
				fill = inHash.get("fill",0)
				drawEllipse(point,color,weight,x,y,normal,fill,angle) #######
			
			# elif type == "text":
				# inString = inHash.get("string","")
				# drawText(point,inString) #######
			elif type == "text":
				pass
				
			else:
				print "type error: check type name"

				

	def drawPoint(point,color,weight):
		#print point,color,weight
		#glFT.glPointSize(size)
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT|OpenMayaRender.MGL_LINE_BIT)
		#,OpenMayaRender.MGL_POINT_BIT
		glFT.glPointSize(weight)
		glFT.glEnable ( OpenMayaRender.MGL_POINT_SMOOTH )
		glFT.glBegin(OpenMayaRender.MGL_POINTS)
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(point[0],point[1],point[2])
		#glFT.glPointSize(1)
		glFT.glEnd()
		glFT.glPopAttrib()

	def drawVector(point,vector,color,weight,size=0.05,unit=0):
	
		#glFT.glLineWidth(1.5)
		#glFT.glPointSize(10)
		
		drawPoint(point,color,5)
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT|OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
		#glFT.glPointSize(weight)
		vec = MVector(vector[0],vector[1],vector[2])
		if unit:
			vec.normalize()
			vec *= unit
		pt2 = MVector(point[0],point[1],point[2])+vec
		
		glFT.glLineWidth(weight)
		glFT.glBegin(OpenMayaRender.MGL_LINES)
		#openGL draw
		#glFT.glColor3f(1,0,0)
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(point[0],point[1],point[2])
		glFT.glVertex3f(pt2[0],pt2[1],pt2[2])
		#openGL draw
		glFT.glEnd()
		glFT.glPopAttrib()
		#draw arrow
		
		
		xProduct = vec^MVector(0,1,0)
		ptTemp = MVector(point[0],point[1],point[2])+vec*0.85
		point = ptTemp-xProduct*size #.normal()
		pt3 = ptTemp+xProduct*size
		
		drawTriangleGL(pt2,point,pt3,color)
		glFT.glPopAttrib()
		
		
	def drawLine(point,point2,color,weight):
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
		glFT.glLineWidth(weight)
		
		glFT.glBegin(OpenMayaRender.MGL_LINES)
		#openGL draw
		#glFT.glColor3f(1,0,0)
		#glFT.glLineWidth(0.5)
		#glFT.glPointSize(0.5)
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(point[0],point[1],point[2])
		glFT.glVertex3f(point2[0],point2[1],point2[2])
		#openGL draw
		glFT.glEnd()
		glFT.glPopAttrib()
		
	def drawVoxel(pt,color,weight,size):
	
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT|OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
		glFT.glLineWidth(weight)
		
		sizedPoint = (size*0.5+pt[0], size*0.5+pt[1], size*0.5+pt[2])
		NsizedPoint = (-size*0.5+pt[0], -size*0.5+pt[1], -size*0.5+pt[2])
		
		glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
		glFT.glBegin(OpenMayaRender.MGL_QUADS)
		#openGL draw
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(NsizedPoint[0], NsizedPoint[1], NsizedPoint[2])
		glFT.glVertex3f(sizedPoint[0], NsizedPoint[1], NsizedPoint[2])
		glFT.glVertex3f(sizedPoint[0], NsizedPoint[1], sizedPoint[2])
		glFT.glVertex3f(NsizedPoint[0], NsizedPoint[1], sizedPoint[2])
		#openGL draw
		glFT.glEnd()
		
		glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
		glFT.glBegin(OpenMayaRender.MGL_QUADS)
		glFT.glVertex3f(NsizedPoint[0], sizedPoint[1], NsizedPoint[2])
		glFT.glVertex3f(sizedPoint[0], sizedPoint[1], NsizedPoint[2])
		glFT.glVertex3f(sizedPoint[0], sizedPoint[1], sizedPoint[2])
		glFT.glVertex3f(NsizedPoint[0], sizedPoint[1], sizedPoint[2])
		glFT.glEnd()
		glFT.glPopAttrib()
		
		drawLine((NsizedPoint[0], NsizedPoint[1], NsizedPoint[2]),(NsizedPoint[0], sizedPoint[1], NsizedPoint[2]),color,weight)
		drawLine((sizedPoint[0], NsizedPoint[1], NsizedPoint[2]),(sizedPoint[0], sizedPoint[1], NsizedPoint[2]),color,weight)
		drawLine((sizedPoint[0], NsizedPoint[1], sizedPoint[2]),(sizedPoint[0], sizedPoint[1], sizedPoint[2]),color,weight)
		drawLine((NsizedPoint[0], NsizedPoint[1], sizedPoint[2]),(NsizedPoint[0], sizedPoint[1], sizedPoint[2]),color,weight)
		
	def drawPolygon(ptlist,color,weight,fill):
	
		
		

		if weight:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
			glFT.glLineWidth(weight)
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)
			glFT.glColor4f(color[0],color[1],color[2],color[3])
			
			# glFT.glVertex3f(ptlist[0][0],ptlist[0][1],ptlist[0][2])
			# for i in range(1,len(ptlist)):
				# eachpt = ptlist[i]
			for eachpt in ptlist:
				glFT.glVertex3f(eachpt[0],eachpt[1],eachpt[2])
				
			glFT.glEnd()

			glFT.glPopAttrib()
			# size = 100
		
		if fill:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)
			try:
				glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			except:
				pass
				
			glFT.glVertex3f(ptlist[0][0],ptlist[0][1],ptlist[0][2])
			# for i in range(1,len(ptlist)):
				# eachpt = ptlist[i]
			for eachpt in ptlist:
				glFT.glVertex3f(eachpt[0],eachpt[1],eachpt[2])
				
			glFT.glEnd()

			glFT.glPopAttrib()
		
	
	def drawRect(pt,color,weight,size,normalTuple,fill=0):
	
		normal = MVector(normalTuple[0],normalTuple[1],normalTuple[2])
		crossX = normal^MVector(0,1,0)
		rotateAngle = math.degrees(normal.angle(MVector(0,1,0)))*-1
		rotateAxis = (crossX[0],crossX[1],crossX[2])
		
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)

		# glFT.glLineWidth(weight)
		
		glFT.glPushMatrix()
		#glFT.glScalef(scaled,1,scaled)
		glFT.glTranslatef(pt[0],pt[1],pt[2])
		glFT.glRotatef(rotateAngle,rotateAxis[0],rotateAxis[1],rotateAxis[2])
		

		glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
		glFT.glBegin(OpenMayaRender.MGL_QUADS)
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(-size*0.5, 0, -size*0.5)
		glFT.glVertex3f(size*0.5, 0, -size*0.5)
		glFT.glVertex3f(size*0.5, 0, size*0.5)
		glFT.glVertex3f(-size*0.5,  0, size*0.5)
		glFT.glEnd()
		
		# if fill:
			# glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			# glFT.glBegin(OpenMayaRender.MGL_QUADS)
			
			# if type(fill) == 'tuple':
				# glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			# elif fill == 1:
				# glFT.glColor4f(color[0],color[1],color[2],color[3])
			# centerRect()
			# glFT.glEnd()
		
		glFT.glPopMatrix()
		glFT.glPopAttrib()
		

		if fill:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
			glFT.glPushMatrix()
			glFT.glTranslatef(pt[0],pt[1],pt[2])
			glFT.glRotatef(rotateAngle,rotateAxis[0],rotateAxis[1],rotateAxis[2])
			
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			glFT.glBegin(OpenMayaRender.MGL_QUADS)
			try:
				glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			except:
				pass
			# if type(fill) == 'tuple':
				# glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			# elif fill == 1:
			glFT.glVertex3f(-size*0.5, 0, -size*0.5)
			glFT.glVertex3f(size*0.5, 0, -size*0.5)
			glFT.glVertex3f(size*0.5, 0, size*0.5)
			glFT.glVertex3f(-size*0.5,  0, size*0.5)
			glFT.glEnd()
			
			glFT.glPopMatrix()
			glFT.glPopAttrib()

		
	def drawPlane(pt,color,weight,size,normal=(0,0,0),fill=0):

		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
		

			
		pointVec = MVector(pt[0],pt[1],pt[2])
		normalVec = MVector(normal[0],normal[1],normal[2])
		normalVec.normalize()
		# vectorBetween = normalVec-pointVec
		# angle = math.degrees(vectorBetween.angle(crossVec))
		
		crossVec = MVector(0,0,1)
		angle = normalVec.angle(crossVec)
		if angle:
			Up = normalVec^crossVec
			Up.normalize()
		else:
			crossVec = MVector(0,1,0)
			angle = normalVec.angle(crossVec)
			if angle:
				Up = normalVec^crossVec
				Up.normalize()
			else:
				crossVec = MVector(1,0,0)
				# angle = normalVec.angle(crossVec)
				Up = normalVec^crossVec
				Up.normalize()

			
		#// Calculate the quad corners
		Left = normalVec^Up
		Left.normalize()
		
		# Left = Left.rotateBy(normalVec,vectorBetween.angle(crossVec))
		
		# point(pointVec,weight=20)
		# vector(pointVec,normalVec*10)
		# vector(pointVec,Left)
		
		uppercenter = (Up * size / 2) + pointVec;
		UpperLeft = uppercenter - (Left * size / 2)
		UpperRight = uppercenter + (Left * size / 2)
		LowerLeft = UpperLeft - (Up * size);
		LowerRight = UpperRight - (Up * size);
		
		if weight:
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
			glFT.glBegin(OpenMayaRender.MGL_QUADS)
			
			# global pointGL
			# pointGL.update({Left:{"color":(1,1,0,1),"weight":15}})
			glFT.glColor4f(color[0],color[1],color[2],color[3])
			glFT.glVertex3f(UpperLeft[0], UpperLeft[1], UpperLeft[2])
			glFT.glVertex3f(UpperRight[0], UpperRight[1], UpperRight[2])
			glFT.glVertex3f(LowerRight[0], LowerRight[1], LowerRight[2])
			glFT.glVertex3f(LowerLeft[0], LowerLeft[1], LowerLeft[2])
			glFT.glEnd()
		
		if fill:
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			glFT.glBegin(OpenMayaRender.MGL_QUADS)
			try:
				glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			except:
				pass
			
			glFT.glVertex3f(UpperLeft[0], UpperLeft[1], UpperLeft[2])
			glFT.glVertex3f(UpperRight[0], UpperRight[1], UpperRight[2])
			glFT.glVertex3f(LowerRight[0], LowerRight[1], LowerRight[2])
			glFT.glVertex3f(LowerLeft[0], LowerLeft[1], LowerLeft[2])
			glFT.glEnd()
			
		#openGL draw
		glFT.glEnd()
		glFT.glPopAttrib()
			
		
	def drawRect2(pt,color,weight,size,plane=(0,1,0),normal=(0,0,0),upVec=(0,0,0),fill=0):
	
	
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POLYGON_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		# glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)

		# glFT.glLineWidth(weight)
		
		glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
		if fill:
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
		
		#openGL draw
		#glFT.glColor4f(r,g,b,1.0)
		#PLAN
		# if plane == (0,1,0):
			# glFT.glVertex3f(-size*0.5+pt[0], pt[1], -size*0.5+pt[2])
			# glFT.glVertex3f(size*0.5+pt[0], pt[1], -size*0.5+pt[2])
			# glFT.glVertex3f(size*0.5+pt[0], pt[1], size*0.5+pt[2])
			# glFT.glVertex3f(-size*0.5+pt[0],  pt[1], size*0.5+pt[2])
			
		# elif plane == (0,0,1):
			# glFT.glVertex3f(-size*0.5+pt[0], -size*0.5+pt[1], pt[2])
			# glFT.glVertex3f(size*0.5+pt[0], -size*0.5+pt[1], pt[2])
			# glFT.glVertex3f(size*0.5+pt[0], size*0.5+pt[1], pt[2])
			# glFT.glVertex3f(-size*0.5+pt[0], size*0.5+pt[1], pt[2])
			
		# elif plane == (1,0,0):
			# glFT.glVertex3f(pt[0], -size*0.5+pt[1], -size*0.5+pt[2])
			# glFT.glVertex3f(pt[0], size*0.5+pt[1], -size*0.5+pt[2])
			# glFT.glVertex3f(pt[0], size*0.5+pt[1], size*0.5+pt[2])
			# glFT.glVertex3f(pt[0], -size*0.5+pt[1], size*0.5+pt[2])
			
		# else:
		
		#print "HERE"
		Up = MVector(upVec[0],upVec[1],upVec[2])
		Up.normalize()
		#print normal
		normalVec = MVector(normal[0],normal[1],normal[2])
		normalVec.normalize()
		#// Calculate the quad corners
		Left = normalVec^Up
		Left.normalize()
		uppercenter = (Up * size / 2) + MVector(pt[0],pt[1],pt[2]);
		UpperLeft = uppercenter + (Left * size / 2)
		UpperRight = uppercenter - (Left * size / 2)
		LowerLeft = UpperLeft - (Up * size);
		LowerRight = UpperRight - (Up * size);
		
		glFT.glBegin(OpenMayaRender.MGL_QUADS)
		
		# global pointGL
		# pointGL.update({Left:{"color":(1,1,0,1),"weight":15}})
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		
		try:
			glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
		except:
			pass
		glFT.glVertex3f(UpperLeft[0], UpperLeft[1], UpperLeft[2])
		glFT.glVertex3f(UpperRight[0], UpperRight[1], UpperRight[2])
		glFT.glVertex3f(LowerRight[0], LowerRight[1], LowerRight[2])
		glFT.glVertex3f(LowerLeft[0], LowerLeft[1], LowerLeft[2])

		#openGL draw
		glFT.glEnd()
		glFT.glPopAttrib()
		
	def drawRectGL(pt,color,weight,size,normal):
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
		glFT.glLineWidth(weight)
		
		glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_LINE)
		glFT.glBegin(OpenMayaRender.MGL_QUADS)
		#openGL draw
		#glFT.glColor4f(r,g,b,1.0)
		
		glFT.glVertex3f(-size*0.5+pt[0], pt[1], -size*0.5+pt[2])
		glFT.glVertex3f(size*0.5+pt[0], pt[1], -size*0.5+pt[2])
		glFT.glVertex3f(size*0.5+pt[0], pt[1], size*0.5+pt[2])
		glFT.glVertex3f(-size*0.5+pt[0],  pt[1], size*0.5+pt[2])
		#openGL draw
		glFT.glEnd()
		
		glFT.glPopAttrib()
		
		
	# def drawPolygon(pt,color,weight,size,normalTuple,fill):
		# pass

	def drawCircle(pt,color,weight,size,normalTuple,fill):
	#def drawCircleRoGL(pt,radius,stroke,rotateAngle,rotateAxis):
	
		# normal = MVector(camNorm[0],camNorm[1],camNorm[2])*-1
		# crossX = normal^MVector(0,1,0)
		# angle = math.degrees(normal.angle(MVector(0,1,0)))*-1
		# circleRoHashGL.update({contextPos:{'radius':20,'angle':angle,'axis':(crossX[0],crossX[1],crossX[2])}})
		normal = MVector(normalTuple[0],normalTuple[1],normalTuple[2])
		crossX = normal^MVector(0,1,0)
		rotateAngle = math.degrees(normal.angle(MVector(0,1,0)))*-1
		rotateAxis = (crossX[0],crossX[1],crossX[2])
		radius = size
		
		'''
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT)
		
		glFT.glPushMatrix()
		#glFT.glScalef(scaled,1,scaled)
		glFT.glTranslatef(pt[0],pt[1],pt[2])
		glFT.glRotatef(rotateAngle,rotateAxis[0],rotateAxis[1],rotateAxis[2])
		#glFT.glTranslatef(pt[0],pt[1],pt[2])
		if weight:
			#glFT.glLineWidth(0.1)
			glFT.glPointSize(0.1)
			glFT.glEnable ( OpenMayaRender.MGL_POINT_SMOOTH )
			glFT.glBegin(OpenMayaRender.MGL_POINTS) #glFT.glBegin(OpenMayaRender.MGL_LINES)
			glFT.glColor4f(color[0],color[1],color[2],color[3])
		else:
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)
			glFT.glColor4f(color[0],color[1],color[2],0.1)
			#glFT.glColor4f(0,1,0,0.5)

		#openGL draw
		#r = 10
		k = pt[0]
		h = pt[2]
		#glFT.glNewList(2,OpenMayaRender.MGL_COMPILE)
		#glFT.glColor4f(1,0,0,0.5)
		tempPts = []
		
		
		for i in range(1,50):
			x = radius * math.cos(i)-k
			y = radius * math.sin(i)+h
			#glFT.glVertex3f(x+pt[0], 0, y-pt[2])
			#tempPts.append((x+pt[0], 0, y-pt[2]))
			x = radius * math.cos(i+0.1)-k
			y = radius * math.sin(i+0.1)+h
			#glFT.glVertex3f(x+pt[0], 0, y-pt[2])
			#tempPts.append((x+pt[0], 0, y-pt[2]))
			xx = math.sin(360/i)*radius
			yy = math.cos(360/i)*radius
			glFT.glVertex3f(xx, 0, yy)
			tempPts.append((xx, 0, yy))
		
		glFT.glEnd()
		#glFT.glEndList()
		
		

		
		
		#glFT.glCallList(2)
		glFT.glPopMatrix()
		glFT.glPopAttrib()
		'''
		#draw points as lines
		# zippedPair = zip(tempPts[0::1], tempPts[1::1])
		# print zippedPair
		# for eachPair in zippedPair:
			# drawLine(eachPair[0],eachPair[1],color,weight)
			
			
		segments = 30

		tempPts = []
		num = float(360)/float(segments)
		#print num

		for i in range(0,segments+1):
		  xx = math.sin(math.radians(i*num))*radius
		  yy = math.cos(math.radians(i*num))*radius
		  tempPts.append((xx, 0, yy))

		#pyMGL.clear("line")

		zippedPair = zip(tempPts[0::1], tempPts[1::1])
		#print zippedPair
		glFT.glPushMatrix()
		#glFT.glScalef(scaled,1,scaled)
		glFT.glTranslatef(pt[0],pt[1],pt[2])
		glFT.glRotatef(rotateAngle,rotateAxis[0],rotateAxis[1],rotateAxis[2])
		
		for eachPair in zippedPair:
			# pyMGL.add("line",{"point":eachPair[0],"point2":eachPair[1],"color":(1,0,0,1),"weight":1})
			drawLine(eachPair[0],eachPair[1],color,weight)
			
		if fill:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
			glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
			glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
			glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
			
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)

			try:
				glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			except:
				pass
			# if type(fill) == 'tuple':
				# glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			# elif fill == 1:
				# glFT.glColor4f(color[0],color[1],color[2],color[3])
				
			for eachPt in tempPts:
				glFT.glVertex3f(eachPt[0], eachPt[1], eachPt[2])
				
			glFT.glEnd()
			glFT.glPopAttrib()
			
		glFT.glPopMatrix()
	
	def drawEllipse(pt,color,weight,x,y,normalTuple,fill,angle):
	
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
	
		normal = MVector(normalTuple[0],normalTuple[1],normalTuple[2])
		crossX = normal^MVector(0,1,0)
		rotateAngle = math.degrees(normal.angle(MVector(0,1,0)))*-1
		rotateAxis = (crossX[0],crossX[1],crossX[2])
		#radius = size
	
		segments = 30

		tempPts = []
		num = float(360)/float(segments)
		#print num

		for i in range(0,segments+1):
		  xx = math.sin(math.radians(i*num))*x
		  yy = math.cos(math.radians(i*num))*y
		  tempPts.append((xx, 0, yy))
		
		# print x
		# print y
		
		#pyMGL.clear("line")

		zippedPair = zip(tempPts[0::1], tempPts[1::1])
		#print zippedPair
		glFT.glPushMatrix()
		#glFT.glScalef(scaled,1,scaled)
		glFT.glTranslatef(pt[0],pt[1],pt[2])
		glFT.glRotatef(rotateAngle,rotateAxis[0],rotateAxis[1],rotateAxis[2])
		
		for eachPair in zippedPair:
			# pyMGL.add("line",{"point":eachPair[0],"point2":eachPair[1],"color":(1,0,0,1),"weight":1})
			drawLine(eachPair[0],eachPair[1],color,weight)
			
		if fill:
			glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT) 
			
			glFT.glPolygonMode(OpenMayaRender.MGL_FRONT_AND_BACK, OpenMayaRender.MGL_FILL)
			glFT.glBegin(OpenMayaRender.MGL_POLYGON)

			try:
				glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			except:
				pass
			# if type(fill) == 'tuple':
				# glFT.glColor4f(fill[0],fill[1],fill[2],fill[3])
			# elif fill == 1:
				# glFT.glColor4f(color[0],color[1],color[2],color[3])
				
			for eachPt in tempPts:
				glFT.glVertex3f(eachPt[0], eachPt[1], eachPt[2])
				
			glFT.glEnd()
			glFT.glPopAttrib()
			
		glFT.glPopMatrix()
		glFT.glPopAttrib()
		
	
	#SS update pending
	def drawTriangleGL(pt1,pt2,pt3,color):
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
		glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
		
		glFT.glBegin(OpenMayaRender.MGL_TRIANGLES)
		#glFT.glColor4f(1,1,0,1)
		glFT.glColor4f(color[0],color[1],color[2],color[3])
		glFT.glVertex3f(pt1[0],pt1[1],pt1[2])
		glFT.glVertex3f(pt2[0],pt2[1],pt2[2])
		glFT.glVertex3f(pt3[0],pt3[1],pt3[2])
		glFT.glEnd()
		glFT.glPopAttrib()

	# PENDING
	#draw text
	
		
		
	################################################## REQUIRED TO CHEAT 3D SPACE WHEN OVERLAYING GL
	def drawHUD(string):
		#glFT.glColor3f(0,1,0)
		activeView.drawText( string, textPositionNearPlane, OpenMayaUI.M3dView.kLeft )

	################################################## HEADER INIT GL FUNCTIONS
	global dList 
	
	glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
	glFT = glRenderer.glFunctionTable()
	 
	 
	''''''
	maya3DViewHandle = OpenMayaUI.M3dView()
	activeView = maya3DViewHandle.active3dView()	


	''''''
	####################

	#drawHUD("") # required to cheat 3d space without using node

	glFT.glPushAttrib(OpenMayaRender.MGL_ENABLE_BIT)
	glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
	#glFT.glPushAttrib(OpenMayaRender.MGL_ALL_ATTRIB_BITS)
	
	glFT.glEnable (OpenMayaRender.MGL_BLEND);
	glFT.glEnable(OpenMayaRender.MGL_DEPTH_TEST)
	# glFT.glDepthFunc(OpenMayaRender.MGL_LEQUAL)
	# glFT.glDepthMask( OpenMayaRender.MGL_FALSE )
	
	
	glFT.glBlendFunc (OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA);
	# glFT.glHint(OpenMayaRender.MGL_LINE_SMOOTH_HINT, OpenMayaRender.MGL_FASTEST);
	glFT.glEnable(OpenMayaRender.MGL_LINE_SMOOTH);
	####################
	
	try:
		if dList:
			pass
	except:
		dList = glFT.glGenLists(1)
		
	'''
	try:
		if eList:
			pass
	except:
		eList = glFT.glGenLists(2)
		
	glFT.glNewList(eList,OpenMayaRender.MGL_COMPILE)
	try:
		glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT) 
		glFT.glColor4f(0,0,0,0.5)
		glFT.glCallList(dList)
		glFT.glPopAttrib()
	except:
		print "no list"
	glFT.glEndList()
	'''
	
	glFT.glNewList(dList,OpenMayaRender.MGL_COMPILE) #_AND_EXECUTE
	
	############################################################## CURRENT VISUAL BLOCK
	if timedebug:
		start_time = time.time()
		
	global storeByID,visibleID
	for inID,hash in storeByID.iteritems():
		if inID in visibleID:
		
			for eachType,drawList in hash.iteritems():
			# for eachType in drawTypes:
				# drawList = getList(eachType,0)
				

				for eachHash in drawList:
					try:
						createDrawing(eachType,eachHash)
					except:
						print "problem drawing geometry" + str(eachType)
						print eachHash

						#pass
				else:
					#print eachType+" is empty"
					pass
					
				if fadeBln:
					fadeList2 = getFadeList(eachType)
					if len(fadeList2):
						for eachHash2 in fadeList2:
							try:
								createDrawing(eachType,eachHash2)
							except:
								#print "problem drawing geometry"
								pass
	if timedebug:					
		print "Time elapsed: ", time.time() - start_time, "s"
	
	glFT.glEndList()
		
	############################################################## CURRENT VISUAL BLOCK END
	
	if HUD:
		textPositionNearPlane = MPoint()
		textPositionFarPlane = MPoint()
		activeView.viewToWorld(10, 10, textPositionNearPlane, textPositionFarPlane )

		activeView.beginGL()
		activeView.beginOverlayDrawing()
		drawHUD("v2 beta")
		activeView.endOverlayDrawing()
		activeView.endGL()
	# 
	
	# activeView.beginGL()
	# activeView.drawText( "test", MPoint(0,0,0), OpenMayaUI.M3dView.kCenter )
	# activeView.endGL()

	glFT.glEndList() #
	
	glFT.glDisable(OpenMayaRender.MGL_BLEND);
	glFT.glDisable(OpenMayaRender.MGL_DEPTH_TEST)
	glFT.glDisable(OpenMayaRender.MGL_LINE_SMOOTH);
	
	glFT.glPopAttrib()
	
	
	#buildGL ends
	updateIDList()

	
## Pending drawText function
def showText():

	glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
	glFT = glRenderer.glFunctionTable()
	
	glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT) 
	
	#glFT.glColor4f(0,1,0,1)
	
	maya3DViewHandle = OpenMayaUI.M3dView()
	activeView = maya3DViewHandle.active3dView()
	textPositionNearPlane = MPoint()
	textPositionFarPlane = MPoint()
	activeView.viewToWorld(10, 10, textPositionNearPlane, textPositionFarPlane )
	
	#maya3DViewHandle.setDrawColor(MColor(0.0,0.0,0.0,1.0))
	
	activeView.beginGL()
	activeView.beginOverlayDrawing()
	#activeView.drawText( "testing", MPoint(0,200,0), OpenMayaUI.M3dView.kCenter )
	try:
		global storeByID,visibleID
		for inID,hash in storeByID.iteritems():
			if inID in visibleID:
			
				# for eachType,drawList in hash.iteritems():
				textList = hash.get("text",[])
				if len(textList):
					for eachTextInfo in textList:
						point = eachTextInfo.get("point","")
						inString = eachTextInfo.get("string","")
						color = eachTextInfo.get("color",(0,0,0,1))
						glFT.glColor4f(color[0],color[1],color[2],color[3])
						activeView.drawText(inString, MPoint(point[0],point[1],point[2]), OpenMayaUI.M3dView.kLeft ) #######

	except:
		print "error drawing text"
				
	activeView.endOverlayDrawing()
	
	glFT.glPopAttrib()
	
	
############ openGL drawing procedures
'''
.point()
point:(0,0,0)
color:(r,g,b,a)
weight:1

.vector()
point:(0,0,0)
vector:(0,0,0)
color:(r,g,b,a)
weight:1

.line()
point01:(0,0,0)
point02:(0,0,0)
color:(r,g,b,a)
weight:1

.voxel()
color:(r,g,b,a)
weight:1
size:1

.quad()
color:(r,g,b,a)
weight:1
size:1
normal:(0,0,0)

.circle()
color:(r,g,b,a)
weight:1
size:1
normal:(0,0,0)
'''

############ Functions

######################## refreshText on camera change


def createIdleSJ():
	jobNum3 = cmds.scriptJob( runOnce=True, e= ["idle",showText], protected=True)
	#print "setJob"

def refreshGLd():
	cmds.evalDeferred("pyMGL.showText()")

#LOAD or RELOADDRAW on UPDATE
def keepText(kill=0,camera='persp'):
	
	try:
		global refrshGLJob1
		global refrshGLJob2
	except:
		pass
		
	try:
		cmds.scriptJob( kill=refrshGLJob1, force=True)
	except:
		pass

	try:
		cmds.scriptJob( kill=refrshGLJob2, force=True)
	except:
		pass
		
	#createIdleSJ()
	if not kill:
		refrshGLJob1 = cmds.scriptJob( attributeChange=[camera+".translateX",refreshGLd], protected=True)
		refrshGLJob2 = cmds.scriptJob( e=["timeChanged",refreshGLd], protected=True)


######################## buildGL()

######################## initNode()
myNode = ""
path = r'S:\mayaModules'

def initNode(debug=0):
	global myNode,path
	#Load/Reinit plugin
	try:
		if debug:
			cmds.delete("transform*")
			cmds.delete("mglNode*") # del all nodes for debug
		else:
			cmds.delete(myNode)
	except:
		pass
		
	if debug:
		try:
			cmds.flushUndo()
			cmds.unloadPlugin(scriptName)
		except:
			pass

	#path = r'S:\Maya (Python)\pyGL'
	
	
	#path = r'C:\Scripts\Maya (Python)\pyGL'
	scriptName = "pyMGLnode"

	#normpath(path)
	scriptPath = os.path.abspath(path)
	
	cmds.loadPlugin(scriptPath+"\\"+scriptName+'.py')
	
	nodeName = "mglNode"
	myNode = cmds.createNode(nodeName)
	try:
		cmds.setAttr(myNode+'.glList',dList)
	except:
		pass
		
# initNode()

######################## updateNode() [SS: updateGLnode()]
def updateNode():
	global dList
	global myNode
	cmds.setAttr(myNode+'.glList',dList)
	
def redrawBln():
	try:
		if cmds.getAttr(myNode+'.update'):
			cmds.setAttr(myNode+'.update',0)
			print "pyMGL | current redraw status: 0"
		else:
			cmds.setAttr(myNode+'.update',1)
			print "pyMGL | current redraw status: 1"			
	except:
		pass
######################## ui()

######################## saveScreen()
def saveScreen2(frame=0,type="jpg"):
	######## TEST GROUND
	maya3DViewHandle = OpenMayaUI.M3dView()
	activeView = maya3DViewHandle.active3dView()	
	
	testImg = MImage()
	activeView.pushViewport(0,100,1000,1000)
	#activeView.refresh(0,1,1)
	activeView.readColorBuffer(testImg,1)
	#testImg.getSize(widthPtr,heightPtr)

	#testImg.convertPixelFormat(OpenMaya.MImage.kFloat,5.0,0.0)
	#testImg.convertPixelFormat(OpenMaya.MImage.kByte,1.0,0.0)
	#testImg.writeToFile( "C:\\testMImage.tif","tif")
	#testImg.writeToFile( "C:\\testMImage.iff","iff")
	testImg.writeToFile( "C:\\playblast\\screenshot"+str(frame)+"."+type,type)
	#testImg.writeToFile( "C:\\playblast\\screenshot"+str(frame)+".tif","tif")

	#activeView.popViewport()
	
def saveScreen(frame=0,type="jpg"):
	######## TEST GROUND
	maya3DViewHandle = OpenMayaUI.M3dView()
	activeView = maya3DViewHandle.active3dView()	
	
	testImg = MImage()

	activeView.readColorBuffer(testImg,1)
	#testImg.getSize(widthPtr,heightPtr)

	#testImg.convertPixelFormat(OpenMaya.MImage.kFloat,5.0,0.0)
	#testImg.convertPixelFormat(OpenMaya.MImage.kByte,1.0,0.0)
	#testImg.writeToFile( "C:\\testMImage.tif","tif")
	#testImg.writeToFile( "C:\\testMImage.iff","iff")
	testImg.writeToFile( "C:\\playblast\\screenshot"+str(frame)+"."+type,type)
	#testImg.writeToFile( "C:\\playblast\\screenshot"+str(frame)+".tif","tif")
	
################################## test script in maya
'''

sys.path.append("s:\mayaModules") 

import pyMGL

reload(pyMGL)

pyMGL.defaultValue

print pyMGL.createUID()



print pyMGL.getList("point")
pyMGL.clear("point")


pyMGL.add("point","fdsdfdfs")

pyMGL.buildList("point")

pyMGL.buildGL()

if pyMGL.dList

pyMGL.initNode()
pyMGL.updateNode()


#one point test
pyMGL.add("point",{"point":(0,0,0),"color":(1,0,0,1)})
pyMGL.buildGL()


################################################
################################################ EXAMPLE/TESTS




sys.path.append("s:\mayaModules") 

import pyMGL
reload(pyMGL)
pyMGL.initNode(debug=1)


def ranNum(offset=0):
	return random.randrange(0+offset,1000+offset)
def rP(offset=0):
	return (ranNum(offset),ranNum(0),ranNum(0))

	
# test points
for i in range (0,20):
	pyMGL.add("point",{"point":rP(0),"color":(random.random(),0,0,1),"weight":10})
	
# test vector
for i in range (0,20):
	pyMGL.add("vector",{"point":rP(1500),"vector":rP(0),"color":(random.random(),0,0,1),"weight":10,"size":0.1})
	
tempptlist = []
for i in range (0,20):
    tempptlist.append(rP(3000))
for each in tempptlist:
    pyMGL.add("line",{"point":each,"point2":rP(3000),"color":(random.random(),0,0,1),"weight":1})

#test voxel
for i in range (0,20):
	pyMGL.add("voxel",{"point":rP(4500),"color":(random.random(),0,0,1),"weight":random.randrange(1,5),"size":100})


	
tempVectors = []
for i in range (0,20):
	tempVectors.append((rP(6000),rP(0)))

	
for each in tempVectors:
	pyMGL.add("vector",{"point":each[0],"vector":each[1],"color":(random.random(),0,0,1),"weight":5,"unit":500})
	
#test circle
for each in tempVectors:
	pyMGL.add("circle",{"point":each[0],"color":(random.random(),0,0,1),"weight":random.randrange(1,2),"size":random.randrange(100,200),"normal":each[1],"fill":random.randrange(0,2)})
	
#test rect
for each in tempVectors:
	pyMGL.add("rect",{"point":each[0],"color":(random.random(),0,0,1),"weight":random.randrange(1,2),"size":100,"normal":each[1]})
	
#test text
for each in tempVectors:
	pyMGL.add("text",{"point":each[0],"string":str(each[0]),"color":(0,0,0,1)})

	
pyMGL.HUD = 1
pyMGL.buildGL()
pyMGL.updateNode()

#draw text init by function call
cmds.refresh()
pyMGL.showText()

pyMGL.keepText(kill=0,camera='persp')
#pyMGL.saveScreen(2000,"jpg")





################################################
################################################

'''
def getplane(normalVec,**kwargs):

	defaultArg = {"type":0}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
			
	crossVec = MVector(0,0,1)
	angle = normalVec.angle(crossVec)
	if angle:
		localX = normalVec^crossVec
		localX.normalize()
	else:
		crossVec = MVector(0,1,0)
		angle = normalVec.angle(crossVec)
		if angle:
			localX = normalVec^crossVec
			localX.normalize()
		else:
			crossVec = MVector(1,0,0)
			angle = normalVec.angle(crossVec)
			localX = normalVec^crossVec
			localX.normalize()
			
	
	angleD = math.degrees(angle)

	getType = defaultArg.get("type",0)
	# print getType
	if getType == "euler":
		return (localX[0]*angleD,localX[1]*angleD,localX[2]*angleD) 
	elif getType == "plane":
		
		return (localX[0],localX[1],localX[2],angleD)
	elif getType == "localZ":
		localZ = localX^normalVec
		localZ.normalize()
		# print "norm"
		return localZ
	elif getType == "info":
		localZ = localX^normalVec
		localZ.normalize()
		return {"localX":localX,"plane":(localX[0],localX[1],localX[2],angleD),"euler":(localX[0]*angleD,localX[1]*angleD,localX[2]*angleD),"localZ":localZ}
	else:
		return localX

################ processing-like syntax wrapper


PValue = {
			"Pcolor":(0,0,0,1),
			"Pstrokeweight":1,
			"Pfill":0,
			"Pnormalize":0,
			"Psize":0.1,
			"Pnormal":(0,1,0),
			"Pup":(0,0,0),
			"PID":0
			}

			
def resetAttr():
	global Pcolor
	Pcolor = PValue.get("Pcolor")
	global Pstrokeweight
	Pstrokeweight = PValue.get("Pstrokeweight")
	global Pfill
	Pfill = PValue.get("Pfill")
	global Pnormalize
	Pnormalize = PValue.get("Pnormalize")
	global Psize
	Psize = PValue.get("Psize")
	global Pnormal
	Pnormal = PValue.get("Pnormal")
	global Pup
	Pup = PValue.get("Pup")
	global Vsize
	Vsize = 0.1
	global PID
	PID = 0

def reset():
	resetAttr()
	
resetAttr()

def color(color):
	global Pcolor
	Pcolor = color
def strokeweight(num):
	global Pstrokeweight
	Pstrokeweight = num
def weight(num):
	global Pstrokeweight
	Pstrokeweight = num
def fill(numColor):
	global Pfill
	Pfill = numColor
def normalize(num):
	global Pnormalize
	Pnormalize = num
def size(num):
	global Psize
	Psize = num
def vectorsize(num):
	global Vsize
	Vsize = num
def normal(vec):
	global Pnormal
	Pnormal = (vec[0],vec[1],vec[2])
def up(vec):
	global Pup
	Pup = (vec[0],vec[1],vec[2])
def id(num):
	global PID
	PID = num
	
	
#### append to data store
def point(pt,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":5,"glow":0,"glowcolor":0,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("point",defaultArg,defaultArg.get("id",0))
	
def points(pt,**kwargs):
	defaultArg = {"color":Pcolor,"weight":5,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
			
	for item in pt:
		point(item,**defaultArg)
		# print item
	
def line(pt1,pt2,**kwargs):
	defaultArg = {"point":pt1,"point2":pt2,"color":Pcolor,"weight":Pstrokeweight,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("line",defaultArg,defaultArg.get("id",0))
	
def polyline(ptlist,close,**kwargs):
	# if len(ptlist):
		# zippedPair = zip(ptlist[0::1], ptlist[1::1])
		# if close:
			# zippedPair.append((ptlist[len(ptlist)-1],ptlist[0]))
		# for eachPair in zippedPair:
			# line(eachPair[0],eachPair[1])
	defaultArg = {"list":ptlist,"close":close,"point":(0,0,0),"color":Pcolor,"weight":Pstrokeweight,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("polyline",defaultArg,defaultArg.get("id",0))
	
def polygon(ptlist,**kwargs):
	defaultArg = {"list":ptlist,"point":(0,0,0),"color":Pcolor,"fill":Pfill,"weight":Pstrokeweight,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("polygon",defaultArg,defaultArg.get("id",0))

	
def vector(pt,vec,**kwargs):
	defaultArg = {"point":pt,"vector":vec,"color":Pcolor,"weight":Pstrokeweight,"size":Vsize,"unit":Pnormalize,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("vector",defaultArg,defaultArg.get("id",0))

def voxel(pt,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"size":Psize,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("voxel",defaultArg,defaultArg.get("id",0))

def circle(pt,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"size":Psize,"normal":Pnormal,"fill":Pfill,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("circle",defaultArg,defaultArg.get("id",0))
	
def ellipse(pt,x=10,y=10,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"x":x,"y":y,"normal":Pnormal,"fill":Pfill,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("ellipse",defaultArg,defaultArg.get("id",0))
	
def rect(pt,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"size":Psize,"normal":Pnormal,"fill":Pfill,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("rect",defaultArg,defaultArg.get("id",0))
	
def rect2(pt,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"size":Psize,"normal":Pnormal,"up":Pup,"fill":Pfill,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("rect2",defaultArg,defaultArg.get("id",0))
	
def plane(pt,normal,**kwargs):
	defaultArg = {"point":pt,"color":Pcolor,"weight":Pstrokeweight,"size":Psize,"normal":normal,"fill":Pfill,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("plane",defaultArg,defaultArg.get("id",0))
	
def vectorplane(point,normalVec,**kwargs):

	defaultArg = {"color":(0,0,0),"weight":1,"size":10,"fill":0,"id":"plane"}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
			
	info = getplane(normalVec,type="info")
	# print info
	localX = info.get("localX")
	localZ = info.get("localZ")
	getSize = defaultArg.get("size")
	vector(point,normalVec.normal()*getSize*0.2,id=defaultArg.get("id"),color=(0.5,1,0.5))
	vector(point,localX*getSize*0.2,id=defaultArg.get("id"),color=(1,0.5,0.5))
	vector(point,localZ*getSize*0.2,id=defaultArg.get("id"),color=(0.5,0.5,1))
	# pyMGL.plane(point,normalVec,id="plane")
	plane(point,normalVec,size=getSize,fill=defaultArg.get("fill"),id=defaultArg.get("id"))
	
def text(pt,string,**kwargs):
	defaultArg = {"point":pt,"string":str(string),"color":Pcolor,"id":PID}
	for key,val in kwargs.iteritems():
		if key in defaultArg:
			defaultArg.update({key:val})
	add("text",defaultArg,defaultArg.get("id",0))
	
	
################################################ BAKE geom in current list

def bakePL(inID=0):
	drawList = getList("polyline",inID)
	for inHash in drawList:
		getlist = inHash.get("list",[])
		posList = []
		for each in getlist:
			pos = (each[0],each[1],each[2])
			posList.append(pos)
		
		cmds.curve(d=1,p=posList)
	
	
def bake(type):

	drawList = getList(type)
	for inHash in drawList:
		point = inHash.get("point",0)
		if point:
			pt01 = (point[0],point[1],point[2])
			if type == "point":
				cmds.spaceLocator(p=pt01) #######
				cmds.rename("MGLpoint")
			elif type == "vector":
				vector = inHash.get("vector",defaultValue["vector"])
				size = inHash.get("size",0.05)
				unit = inHash.get("unit",0)
				# drawVector(point,vector,color,weight,size,unit) #######
				
				vec01 = MVector(point[0],point[1],point[2])
				vec02 = MVector(vector[0],vector[1],vector[2])
				vec03 = vec01+vec02
				pt02 = (vec03[0],vec03[1],vec03[2])
				
				cmds.curve(p=[pt01,pt02],d=1)
				cmds.rename("MGLvector")

			elif type == "line":
				point2 = inHash.get("point2",point)
				cmds.curve(p=[pt01,(point2[0],point2[1],point2[2])],d=1)
				cmds.rename("MGLline")
				# drawLine(point,point2,color,weight) #######
				
			elif type == "voxel":
				size = inHash.get("size",defaultValue["size"])
				# drawVoxel(point,color,weight,size) #######
			elif type == "rect":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				fill = inHash.get("fill",0)
				# drawRect(point,color,weight,size,normal,fill) #######
				
			elif type == "rect2":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",(0,0,0))
				plane = inHash.get("plane",(0,0,0))
				upVec = inHash.get("up",(0,0,0))
				fill = inHash.get("fill",0)
				# drawRect2(point,color,weight,size,(0,0,0),normal,upVec,fill) #######
				
			elif type == "circle":
				size = inHash.get("size",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				fill = inHash.get("fill",0)
				# drawCircle(point,color,weight,size,normal,fill) #######
				
			elif type == "ellipse":
				x = inHash.get("x",defaultValue["size"])
				y = inHash.get("y",defaultValue["size"])
				normal = inHash.get("normal",defaultValue["normal"])
				angle = inHash.get("angle",0)
				fill = inHash.get("fill",0)
				# drawEllipse(point,color,weight,x,y,normal,fill,angle) #######
			
			elif type == "text":
				inString = inHash.get("string","")
				# drawText(point,inString) #######
				
			else:
				print "type error: check type name"
		
	
################################################
'''

# test example with processing-like syntax

sys.path.append("s:\mayaModules") 

import pyMGL
reload(pyMGL)
pyMGL.initNode(debug=1)


def ranNum(offset=0):
	return random.randrange(0+offset,1000+offset)
def rP(offset=0):
	return (ranNum(offset),ranNum(0),ranNum(0))

### INSERT CODE HERE

pyMGL.color((0,0,0,1))

pyMGL.strokeweight(10)
# POINT
pyMGL.point((0,0,0))
pyMGL.text((0,0,0),"Point:(0,0,0)")


pyMGL.strokeweight(2)
# LINE
pyMGL.line((20,0,0),(20,0,20))
pyMGL.text((20,0,0),"Point1:(20,0,0)")
pyMGL.text((20,0,20),"Point2:(20,0,20)")


pyMGL.strokeweight(1)
# VECTOR
pyMGL.vector((40,0,0),(0,0,20))
pyMGL.text((40,0,0),"Point:(40,0,0)")
pyMGL.text((40,0,20),"Vector:(0,0,20)")

pyMGL.resetAttr()

pyMGL.fill((1,0,0,0.5))

# RECTANGLE
pyMGL.size(20)
pyMGL.rect((70,0,0))
pyMGL.text((70,0,0),"Rectangle center:(70,0,0)")

# CIRCLE
pyMGL.size(10)
pyMGL.circle((110,0,0))
pyMGL.text((110,0,0),"Circle center:(110,0,0)")

# ELLIPSE
pyMGL.ellipse(pt=(110,0,30),x=20,y=10)
pyMGL.text((110,0,30),"Ellipse center:(110,0,30)")

# VOXEL
pyMGL.size(20)
pyMGL.voxel((150,0,0))
pyMGL.text((150,0,0),"Voxel center: (150,0,0)")


### INSERT CODE HERE END
	
pyMGL.HUD = 1
pyMGL.buildGL()
pyMGL.updateNode()

#draw text init by function call
cmds.refresh()
pyMGL.showText()

pyMGL.keepText(kill=0,camera='persp')
#pyMGL.saveScreen(2000,"jpg")


pyMGL.ui()

'''
runCount = 0

########### UI
def getTextValue(fieldName):
	#print cmds.textField(fieldName, q=1,tx=1 )
	return cmds.textField(fieldName, q=1,tx=1 )
	
def setExpression(function):
	#evalDeferred `python("timeWrapper()")`; 

	expression = cmds.expression(s="evalDeferred `python( \""+function+"()\" )`;")
	#expression = cmds.expression(s="python( \""+function+"\" );")
	
def runCommand(function,times, ss):
	# evalDeferred `python("timeWrapper()")`; 
	try:
		#print ss
		for i in range(0, int(times)):
			
			if int(ss) != 0:
				exec(function+"()")
				saveScreen(i)
				# cmds.evalDeferred(function+"()")
				# cmds.refresh()
				# playBlast(i)
			else:
				cmds.evalDeferred(function+"()")
	except:
		print "not run: check function/times"
	#expression = cmds.expression(s="python( \""+function+"\" );")

cmds.setAttr("defaultRenderGlobals.imageFormat",8) #JPG
#cmds.playblast(cf="c:\\playblast\\screenshot.jpg",fmt="image",viewer=0,orn=0,p=100,wh=[4000,3000],) #fr=1
def playBlast(frame):
	#cmds.setAttr("defaultRenderGlobals.imageFormat",8) #JPG
	#cmds.playblast(cf="c:\\playblast\\screenshot"+str(frame)+".jpg",fmt="image",viewer=0,orn=0,p=100,wh=[4000,3000],fr=frame) #fr=1
	cmds.playblast(cf="c:\\playblast\\screenshot"+str(frame)+".jpg",fmt="image",viewer=0,orn=0,p=100,fr=frame) #fr=1
	print "saved"
  
  
def exe(function):
	#print function
	#exec(function)
	#exec("timeWrapper()")
	mel.eval("python("+str(function)+");")
	
########################################################################
	
class textScrollList(object):
	global scope
	# def __init__(self,givenname):
		# self.name = givenname
	
	def create(self,name,height=200,ams=1,dcc="()"):
		nameAsString = '\"'+name+'\"'
	
		cmds.textScrollList(name, h=height,allowMultiSelection=ams, dkc=scope+'newScrollList.pop('+nameAsString+')', doubleClickCommand=dcc) #dkc
		# cmds.button( label='add', command=( scope+'newScrollList.add('+nameAsString+',["test"])') )
		# cmds.button( label='add selected', command=( scope+'newScrollList.add('+nameAsString+',cmds.ls(sl=1))') )
		# cmds.button( label='list selected', command=('print '+scope+'newScrollList.ls('+nameAsString+')') )
		# cmds.button( label='list all', command=('print '+scope+'newScrollList.all('+nameAsString+')') )
		# cmds.button( label='remove selected', command=(scope+'newScrollList.pop('+nameAsString+')') )
	
	def add(self,name,list):
		newSet = set()
		allItem = cmds.textScrollList(name, q=1,ai=1)
		try:
			newSet = set(allItem)
		except:
			pass
			
		if len(list):
			for eachItem in list:
				if eachItem not in newSet:
					cmds.textScrollList(name, e=1,append=eachItem)

	def ls(self,name):
		try:
			cmds.select(cmds.textScrollList(name, q=1,selectItem=1),r=1)
		except:
			pass
		return cmds.textScrollList(name, q=1,selectItem=1)
		
	def all(self,name):
		# try:
			# cmds.select(cmds.textScrollList(name, q=1,allItems=1),r=1)
		# except:
			# pass
		return cmds.textScrollList(name, q=1,allItems=1)
		
	def pop(self,name):
		delList = cmds.textScrollList(name, q=1,selectIndexedItem=1)
		selItem = cmds.textScrollList(name, q=1,selectItem=1)
		# print selItem
		for eachID in selItem:
			# print eachID
			try:
				if eachID.isdigit():
					cmds.evalDeferred("pyMGL.clearID("+eachID+")")
				else:
					cmds.evalDeferred("pyMGL.clearID(\""+eachID+"\")")
				cmds.evalDeferred("pyMGL.buildGL()")
				cmds.evalDeferred("pyMGL.updateNode()")
			except:
				pass
		try:
			delList.sort()
			delList.reverse()
			# print delList
			cmds.textScrollList(name, e=1,rii=delList)
		except:
			pass
	def clear(self,name):
		cmds.textScrollList(name, e=1,removeAll=1)
		
	
newScrollList = textScrollList()
scope = "pyMGL"+"."

def updateIDList():
	#if cmds.window("pymglUI",exists=1):
	try:
		newScrollList.clear("pyMGL_idList")
		hiddenList = []
		for eachID in storeByID.iterkeys():
			if eachID in visibleID:
				newScrollList.add("pyMGL_idList",[eachID])
			else:
				hiddenList.append(eachID)
		# if len(hiddenList):		
		newScrollList.clear("pyMGL_hideidList")
		newScrollList.add("pyMGL_hideidList",hiddenList)
	except:
		pass
		
def toggleVisSel(toggle):
	if toggle:
		selList = newScrollList.ls("pyMGL_hideidList")
	else:
		selList = newScrollList.ls("pyMGL_idList")
		
	if selList:
		function = "hideID"
		if toggle:
			function = "showID"
			
		for eachID in selList:
	
			if eachID.isdigit():
				cmds.evalDeferred("pyMGL."+function+"("+eachID+")")
			else:
				cmds.evalDeferred("pyMGL."+function+"(\""+eachID+"\")")

		cmds.evalDeferred("pyMGL.buildGL()")
		cmds.evalDeferred("pyMGL.updateNode()")
		cmds.evalDeferred("pyMGL.updateIDList()")
		
def clearByType():
	getType = newScrollList.ls("pyMGL_type")
	if getType:
		useType = getType[0]
		cmds.evalDeferred("pyMGL.clear(\""+useType+"\")")
		cmds.evalDeferred("pyMGL.buildGL()")
		cmds.evalDeferred("pyMGL.updateNode()")
		print "pyMGL PROMPT: clear " +str(useType)
	else:
		print "pyMGL ERROR: select a primitive type"
		
def clearByTypeID():
	getType = newScrollList.ls("pyMGL_type")
	getID = newScrollList.ls("pyMGL_idList")
	if getType:
		useType = getType[0]
		# print useType
		if getID:
			if len(getID) == 1:
				useID = getID[0]
				if useID.isdigit():
					cmds.evalDeferred("pyMGL.clear2(\""+useType+"\","+useID+")")
				else:
					cmds.evalDeferred("pyMGL.clear2(\""+useType+"\",\""+useID+"\")")
				cmds.evalDeferred("pyMGL.buildGL()")
				cmds.evalDeferred("pyMGL.updateNode()")
				print "pyMGL PROMPT: clear " +str(useType) +" in "+ str(useID)
			else:
				print "pyMGL ERROR: select one id only"
		else:
			print "pyMGL ERROR: select a id from visible id list"
	else:
		print "pyMGL ERROR: select a primitive type"
		
def ui2():
	
	if cmds.dockControl("pyMGLdock",exists=1):
		cmds.deleteUI("pyMGLdock")
	if cmds.window("pymglUI",exists=1):
		cmds.deleteUI("pymglUI")
	mglwindow = cmds.window("pymglUI", title="pyMGL.ui() v2", iconName='pyMGL', widthHeight=(300, 600) )
	
	cmds.columnLayout( adjustableColumn=True )
	
	allowedAreas = ['right', 'left']
	cmds.dockControl("pyMGLdock",l="pyMGL", w=300, area='right', content=mglwindow, allowedArea=allowedAreas )

	cmds.frameLayout( label='pyMGL', borderStyle='in' ,cll=1)
	cmds.rowColumnLayout( numberOfColumns=1)
	cmds.button( label='initNode(1)', command=('pyMGL.initNode(1)') )
	cmds.button( label='redrawBln()', command=('pyMGL.redrawBln()') )
	cmds.button( label='buildGL()', command=('pyMGL.buildGL()') )
	cmds.button( label='updateNode()', command=('pyMGL.updateNode()') )
	cmds.setParent( '..' )
	cmds.setParent( '..' )

	cmds.frameLayout( label='DISPLAY ID', borderStyle='in' ,cll=1)
	cmds.rowColumnLayout( numberOfColumns=1)
	# cmds.text( label='DISPLAY ID', align='left')
	
	cmds.button( label='debugID()', command=('pyMGL.debugID();pyMGL.buildGL();pyMGL.updateNode()') )
	cmds.button( label='updateIDList()', command=('pyMGL.updateIDList()') )
	cmds.setParent( '..' )
	
	cmds.rowColumnLayout( numberOfColumns=2)
	cmds.text( label='VISIBLE ID', align='left')
	cmds.text( label='HIDDEN ID', align='left')
	newScrollList.create("pyMGL_idList",height=200,ams=1,dcc="(pyMGL.toggleVisSel(0))")
	newScrollList.create("pyMGL_hideidList",height=200,ams=1,dcc="(pyMGL.toggleVisSel(1))")
	cmds.button( label='HIDE >>', command=('pyMGL.toggleVisSel(0)') )
	cmds.button( label='<< SHOW', command=('pyMGL.toggleVisSel(1)') )
	cmds.setParent( '..' )
	
	cmds.setParent( '..' )
	
	cmds.frameLayout( label='PRIMITIVE TYPE', borderStyle='in' ,cll=1)
	cmds.rowColumnLayout( numberOfColumns=1)
	cmds.text( label='PRIMITIVE TYPE', align='left')
	newScrollList.create("pyMGL_type",height=100,ams=0)
	newScrollList.add("pyMGL_type",["point","vector","line","voxel","rect","rect2","circle","ellipse","text"])
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	
	cmds.frameLayout( label='CLEAR', borderStyle='in' ,cll=1)
	cmds.rowColumnLayout( numberOfColumns=1)
	# cmds.button( label='pyMGL.clear(type)', command=('pyMGL.clear(type) ') )
	# cmds.button( label='pyMGL.clear2(type,inID=0) ', command=('pyMGL.clear2(type,inID=0)') )
	cmds.button( label='clear2(TYPE,ID) ', command=('pyMGL.clearByTypeID()') )
	cmds.button( label='clear(TYPE)', command=('pyMGL.clearByType() ') )
	cmds.button( label='clearall()', command=('pyMGL.clearall()') )
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	#cmds.button( label='pyMGL.showAll()', command=('pyMGL.showAll()') )

	
	cmds.frameLayout( label='INFO', borderStyle='in' ,cll=1, cl=1)
	cmds.rowColumnLayout( numberOfColumns=1)
	cmds.button( label='about()', command=('pyMGL.about()') )
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	
	
	cmds.setParent( '..' )
	# cmds.showWindow( mglwindow )
	
	#import pyMGL to root
	mel.eval("python(\"import pyMGL\")")
	
ui2()

def ui():

	if cmds.window("pymglUI",exists=1):
		cmds.deleteUI("pymglUI")

	window = cmds.window("pymglUI", title="pyMGL.ui() v2", iconName='TT', widthHeight=(300, 500) )

	#cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 130),(2, 50), (3, 120)] )
	cmds.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, 200),(1, 100)] )


	# TITLE
	cmds.separator( style='none' )
	cmds.text( label='FUNCTION', align='left')
	#
	cmds.checkBox( label='debug')
	cmds.button( label='pyMGL.initNode(debug)', command=('pyMGL.initNode(debug=1)') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.buildGL()', command=('pyMGL.buildGL();pyMGL.updateNode()') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.updateNode()', command=('pyMGL.updateNode()') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.redrawBln()', command=('pyMGL.redrawBln()') )
	
	#
	cmds.separator( style='none' )
	cmds.text( label='TEXT FUNCTION', align='left')
	
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.keepText(kill0,camera)', command=('pyMGL.keepText(kill=0,camera="persp")') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.keepText(kill1,camera)', command=('pyMGL.keepText(kill=1,camera="persp")') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.showText()', command=('pyMGL.showText()') )
	#

	#
	cmds.separator( style='none' )
	cmds.text( label='DECAY FUNCTION', align='left')
	#
	cmds.textField( "fadeVar", tx='0.35')
	cmds.button( label='pyMGL.setFade(0)', command=('pyMGL.fadeBln=float(pyMGL.getTextValue("fadeVar"))') )
	#
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.purgeFade()', command=('pyMGL.purgeFade()') )
	#
	

	# CLEARING
	cmds.separator( style='none' )
	cmds.text( label='CLEAR FUNCTION', align='left')
	#
	cmds.textField( "clearType", tx='point')
	cmds.button( label='pyMGL.clear(type)', command=('pyMGL.clear(pyMGL.getTextValue("clearType"))') )
	#
	cmds.separator( style='none' )
	cmds.button( label='pyMGL.clearAll()', command=('pyMGL.clearall()') )
	#
	
	# OUTPUT
	cmds.separator( style='none' )
	cmds.text( label='OUTPUT FUNCTION', align='left')
	
	cmds.textField( "myFloat2txt", tx='0')
	cmds.button( label='pyMGL.saveScreen(1,"jpg")', command=('pyMGL.saveScreen(pyMGL.getTextValue("myFloat2txt"),"jpg")') )
	#
	
	
	cmds.separator( style='none' )
	cmds.text( label='EXPRESSION', align='left')

	cmds.textField( "myFloat1txt", tx='timeWrapper')
	cmds.button( label='attach', command=('pyMGL.setExpression(pyMGL.getTextValue("myFloat1txt"))') )

	cmds.separator( style='none' )
	cmds.button( label='runOnce', command=('pyMGL.runCommand(pyMGL.getTextValue("myFloat1txt"),1,0)') )

	# cmds.textField( "myFloatSStxt", tx='0')
	# cmds.text( label='saveScreen', align='left')
	
	cmds.textField( "myFloatTimetxt", tx='20')
	cmds.button( label='runXtimes', command=('pyMGL.runCommand(pyMGL.getTextValue("myFloat1txt"),pyMGL.getTextValue("myFloatTimetxt"),0)') )

	# cmds.separator( style='none' )
	# cmds.button( label='runExec', command=('pyMGL.exe(pyMGL.getTextValue("myFloat1txt"))') )
	


	#cmds.button( label='attach', command=('print "python("+getTextValue("myFloat1txt")+")"') )

	#expression = cmds.expression(s="python( \""+getTextValue("myFloat1txt")+"\" );")
	#test = "timeWrapper()"
	#expression = cmds.expression(s="python( \""+test+"\" );")



	cmds.setParent( '..' )
	cmds.showWindow( window )