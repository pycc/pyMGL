
'''
20101031 EC
pyMGL node
'''

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
from maya.OpenMaya import MVector
from maya.OpenMaya import MPoint
import pyMGL
# import random
# import math

nodeTypeName = "mglNode"
nodeTypeId = OpenMaya.MTypeId(0x87091)
 
glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT = glRenderer.glFunctionTable()


class myType(OpenMayaMPx.MPxLocatorNode):

	global glFT

	######################
	#to incur updates
	sentinelAttr = OpenMaya.MObject()
	dSent = 0
	dList = 0
	######################
	
	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
 
	def compute(self, plug, dataBlock):
		if ( plug == myType.sentinelAttr):
			#Update?
			outSent = dataBlock.outputValue(myType.sentinelAttr)
			outSent.setInt(1)
			#outSent.setInt(self.dSent +1 % 10)
			
			outSent = dataBlock.outputValue(myType.sentinelAttr)
			
			#DRAW
			dataBlock.setClean(plug)

			
		return OpenMaya.kUnknownParameter
 
	def draw(self, view, path, style, status):

		updateDList= self.GetPlugData()
	
		thisNode = self.thisMObject()
		glPlug = OpenMaya.MPlug( thisNode, self.glList )
		glList = glPlug.asInt()

		updatePlug = OpenMaya.MPlug( thisNode, self.update )
		constantUpdate = updatePlug.asInt()
		
		textPlug = OpenMaya.MPlug( thisNode, self.text )
		textUpdate = textPlug.asInt()
		
		depthPlug = OpenMaya.MPlug( thisNode, self.depth )
		depthMaskBln = depthPlug.asInt()


		
		
		try:
			if updateDList or constantUpdate:
				#Get plug
				view.beginGL()
				
				#glFT.glPushAttrib(OpenMayaRender.MGL_ENABLE_BIT)
				glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT)
				glFT.glPushAttrib(OpenMayaRender.MGL_POINT_BIT)
				glFT.glPushAttrib(OpenMayaRender.MGL_LINE_BIT)
				glFT.glPushAttrib(OpenMayaRender.MGL_POLYGON_BIT)
				
				glFT.glEnable (OpenMayaRender.MGL_BLEND)
				
				glFT.glClearDepth(1.0)
				glFT.glEnable(OpenMayaRender.MGL_DEPTH_TEST)
				glFT.glDepthMask(OpenMayaRender.MGL_TRUE )
				
				
				if depthMaskBln:
					#glFT.glClear (OpenMayaRender.MGL_COLOR_BUFFER_BIT | OpenMayaRender.MGL_DEPTH_BUFFER_BIT);
					glFT.glDepthFunc(OpenMayaRender.MGL_LEQUAL)
				else:
					glFT.glDepthFunc(OpenMayaRender.MGL_ALWAYS)
				#print "fdddddsdf"
				
				glFT.glBlendFunc (OpenMayaRender.MGL_SRC_ALPHA, OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
				#glFT.glHint(OpenMayaRender.MGL_LINE_SMOOTH_HINT, OpenMayaRender.MGL_FASTEST);
				glFT.glEnable(OpenMayaRender.MGL_LINE_SMOOTH);


				
				try:
					if glFT.glIsList(glList):
						#print "is List"
						try:
							glFT.glCallList(glList)
						except:
							print "no list"
					else:
						print "glList not exist"
				except:
					pass

					
				#glFT.glCallList(self.dList)
				#glFT.glDisable(OpenMayaRender.MGL_DEPTH_TEST)
				glFT.glDisable(OpenMayaRender.MGL_BLEND)
				glFT.glDisable(OpenMayaRender.MGL_LINE_SMOOTH);
				
				glFT.glPopAttrib()	
				glFT.glPopAttrib()	
				glFT.glPopAttrib()	
				glFT.glPopAttrib()	
				
				view.endGL()
				
				# pyMGL.showText()
				
		except:
			pass
		
		try:
			if constantUpdate and textUpdate:
				# view.drawText( "testing", MPoint(0,0,0), OpenMayaUI.M3dView.kCenter )
				try:
					glFT.glPushAttrib(OpenMayaRender.MGL_CURRENT_BIT|OpenMayaRender.MGL_POINT_BIT) 
					for inID,hash in pyMGL.storeByID.iteritems():
						if inID in pyMGL.visibleID:
						
							# for eachType,drawList in hash.iteritems():
							textList = hash.get("text",[])
							if len(textList):
								for eachTextInfo in textList:
									point = eachTextInfo.get("point","")
									inString = eachTextInfo.get("string","")
									color = eachTextInfo.get("color",(0,0,0,1))
									glFT.glColor4f(color[0],color[1],color[2],color[3])
									view.drawText(inString, MPoint(point[0],point[1],point[2]), OpenMayaUI.M3dView.kLeft ) #######
					glFT.glPopAttrib()
				except:
					print "error drawing text"
				
		except:
			pass
		
			
	def isTransparent(self):
		return True
	
	def drawLast(self):
		return True
	
	def GetPlugData(self):
		thisNode = self.thisMObject()
		plug = OpenMaya.MPlug( thisNode, self.sentinelAttr )
		
		sent = 0
		
		#get sentinel plug, causes update
		self.dSent = plug.asInt()

		if sent != self.dSent:
			self.dSent = plug.setInt(0)
			return True
		else:
			return False
	
	#data parsing
	#######################


def nodeCreator():
	return OpenMayaMPx.asMPxPtr(myType())
 
def nodeInitializer():

	
	nAttr = OpenMaya.MFnNumericAttribute()
	myType.sentinelAttr = nAttr.create( "sentinel", "sent", OpenMaya.MFnNumericData.kInt, 0 )
	nAttr.setWritable(True)
	#nAttr.setHidden(True)
	
	#add control attr
	nAttr = OpenMaya.MFnNumericAttribute()
	myType.update = nAttr.create( "update", "u", OpenMaya.MFnNumericData.kFloat, 1.0 )
	nAttr.setKeyable(True)

	nAttr = OpenMaya.MFnNumericAttribute()
	myType.depth = nAttr.create( "depthMask", "dm", OpenMaya.MFnNumericData.kInt, 1 )
	nAttr.setKeyable(True)
	
	nAttr = OpenMaya.MFnNumericAttribute()
	myType.text = nAttr.create( "text", "tx", OpenMaya.MFnNumericData.kInt, 1 )
	nAttr.setKeyable(True)
	
	nAttr = OpenMaya.MFnNumericAttribute()
	myType.glList = nAttr.create( "glList", "gl", OpenMaya.MFnNumericData.kInt, 100 )
	nAttr.setKeyable(True)
	
	try:
		#addAttribute
		myType.addAttribute(myType.sentinelAttr)
		myType.addAttribute( myType.update )
		myType.addAttribute( myType.depth )
		myType.addAttribute( myType.glList )
		myType.addAttribute( myType.text )
	except:
		print ( "Failed to create attributes of %s node\n", nodeTypeName )
	
	try:
		myType.attributeAffects( myType.update, myType.sentinelAttr )
		myType.attributeAffects( myType.depth, myType.sentinelAttr )
		myType.attributeAffects( myType.glList, myType.sentinelAttr )
		myType.attributeAffects( myType.text, myType.sentinelAttr )
	except:
		print "error in attributeAffects"
	
	
	return OpenMaya.MStatus.kSuccess
 
def initializePlugin(obj):
	plugin = OpenMayaMPx.MFnPlugin(obj)
	try:
		plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode)
	except:
		sys.stderr.write( "Failed to register node: %s" % nodeTypeName)
 
def uninitializePlugin(obj):
	plugin = OpenMayaMPx.MFnPlugin(obj)
	try:
		plugin.deregisterNode(nodeTypeId)
	except:
		sys.stderr.write( "Failed to deregister node: %s" % nodeTypeName)