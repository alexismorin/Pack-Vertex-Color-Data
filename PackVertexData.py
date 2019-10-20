# This one click-script packs vertex data into your meshes for further use in your shaders

import maya.cmds as cmds
import random

maxHeight = 0.0
maxAO = 0.0

sel = cmds.ls(sl=True, o=True)[0]
sel_vtx = cmds.ls('{}.vtx[:]'.format(sel), fl=True)

# Height and AO Prepass
for prepassObj in sel_vtx:
    prepassAoValue = 0.0
    prepassPos = cmds.xform( prepassObj, query=True, translation=True, worldSpace=True )
    
    if prepassPos[1] > maxHeight:
        maxHeight = prepassPos[1]
    for aoElement in sel_vtx:
        prepassAoPos = cmds.xform( aoElement, query=True, translation=True, worldSpace=True )
        prepassAoValue = prepassAoValue + abs((prepassPos[0]-prepassAoPos[0])+(prepassPos[1]-prepassAoPos[1])+(prepassPos[2]-prepassAoPos[2]))
    if prepassAoValue > maxAO:
        maxAO = prepassAoValue

for obj in sel_vtx:
    aoValue = 0.0
    vtxPos = cmds.xform( obj, query=True, translation=True, worldSpace=True )

    for ao in sel_vtx:
        aoPos = cmds.xform( ao, query=True, translation=True, worldSpace=True )
        aoValue = aoValue + abs((vtxPos[0]-aoPos[0])+(vtxPos[1]-aoPos[1])+(vtxPos[2]-aoPos[2]))
    
    cmds.select(obj)
    cmds.polyColorPerVertex( rgb=(1.0 / maxHeight * vtxPos[1] , 1.0-(1.0/maxAO*aoValue), random.random()), cla=True) 
   
cmds.select(sel)
