# pyMGL
Enabler for drawing computer geometry directly into Maya viewport when coding in python

![alt text](https://www.pycheung.com/weblog/wp-content/uploads/zrtn_002p277bc43e_tn.jpg)

This script enables drawing geometry directly from python code into the Maya openGL viewport.  It has been developed around 2010-2011 for an older version of Maya. I am posting my source code for reference for those who might want to work with the Maya viewport.

The problem of injecting opengl code into the Maya viewport is that it does not presist once it is drawn once. One known way to counter that is to draw using a custom locator node (as demonstrated in [https://www.fevrierdorian.com/blog/post/2010/02/12/Creating-custom-locator-with-Maya-s-Python-API](https://www.fevrierdorian.com/blog/post/2010/02/12/Creating-custom-locator-with-Maya-s-Python-API)). Another problem is to make the opengl context more accessible in the Maya python editor for geometry. The way this is done here is to store geometry with an ID which gets turned into raw GL code stored in a display list in openGL. In the custom locator node, the display list is used for constant redraw to maintain the drawing in the viewport. 

## Use
First set the path in pyMGL.py pointing to where pyMGLnode.py is located

```python
line 1363: path = r'S:\mayaModules'
```
```python
import pyMGL
reload(pyMGL)
pyMGL.initNode(debug=1) #or load pyMGLnode using Maya plugin dialog
pyMGL.ui()
```

```python

### primitives
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



### build and refresh pyMGL
pyMGL.HUD = 1
pyMGL.buildGL()
pyMGL.updateNode()

#draw text init by function call
cmds.refresh()
pyMGL.showText()
```

see demo here https://www.pycheung.com/weblog/post/449

## Limitations

![alt text](https://www.pycheung.com/weblog/wp-content/uploads/zrtn_002p50800343_tn.jpg)

This has been initially developed before Maya viewport 2.0 

While I had modified it to work with an earlier version of viewport 2.0 (by switching MHardwareRenderer to MRenderer in the node) it appears that the api has now been updated so it may no longer work for later version of viewport 2.0. (see https://www.pycheung.com/weblog/post/700)

For those who are interested, the code example https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__py_ref_scripted_2py_foot_print_node_8py_example_html may provide some insights into updating the code to match the later version of the maya API.