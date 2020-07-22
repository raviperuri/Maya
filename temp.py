for each in cmds.ls(sl=1):
    cmds.setAttr(each+".visibility", 0)
    cmds.setAttr(each+".visibility", lock=True) 


for jnt in cmds.ls(sl=1):
    cmds.setAttr(jnt + '.drawStyle', 2)  


#Normal- 0, template- 1, Reference- 2
cmds.setAttr("R_Leg_Base_geo.overrideDisplayType", 2)   
cmds.setAttr("L_Leg_Base_geo.overrideDisplayType", 2)



#Correction for Adelaid
#Fist - thumb should not penetrate.
#Dynamic On/Off not connected.

#Selecting influenceJoints of an SkinnedObject
sel = cmds.ls(sl=1)
jnts = cmds.skinCluster(sel, q=1, inf=1)


#want name of skin cluster on  selection
import maya.cmds as cmds
import maya.mel as mel
selection = cmds.ls(sl=True)
item= selection[0]
print mel.eval('findRelatedSkinCluster '+item)


#copySkinCluster
import maya.cmds as cmds
import maya.mel as mel
sel = cmds.ls(sl=True)
item= sel[0]
skcName = mel.eval('findRelatedSkinCluster '+item)
jnts = cmds.skinCluster(skcName, q=1, inf=1)
newSkc = cmds.skinCluster(jnts, sel[1], tsb=True)
cmds.copySkinWeights(ss=skcName, ds=newSkc[0], nm=True, surfaceAssociation="closestPoint")


#copy BS from old mesh to new mesh(create individual BS mesh)
#wont work if old bsNode doesn't have targets
#just select old mesh which contain bsNode and run the script
history = cmds.listHistory(cmds.ls(sl=1))
blendshapes = cmds.ls(history, type = 'blendShape')
bsNames = cmds.listAttr( blendshapes[0] + '.w' , m=True )
for each in bsNames:
    if each == "SquintLayer":
        continue
    if each == "zipperLips_RLayer":
        continue
    if each == "zipperLips_LLayer":
        continue
    if each == "UpMidLoLayer":
        continue
    if each == "faceLipsLayer_geo":
        continue
    if each == "Mrph_face_geo":
        continue
    print each    
    cmds.select(each+"_geo", add=1)                             
    name = cmds.ls(each+"_geo")
    oldName = cmds.rename(name[0], "old_"+name[0])    
    cmds.duplicate('face_geo', n= name[0])
    #copySkinning
    item= oldName
    skcName = mel.eval('findRelatedSkinCluster '+item)
    jnts = cmds.skinCluster(skcName, q=1, inf=1)
    newSkc = cmds.skinCluster(jnts, name, tsb=True)
    cmds.copySkinWeights(ss=skcName, ds=newSkc[0], nm=True, surfaceAssociation="closestPoint")


#snap the object to selected object
cmds.delete(cmds.parentConstraint(mo=0))


