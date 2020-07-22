
#controlShapeNode change
#Select newShapeCtrl and then select oldShapeCtrl and run
ctrl = cmds.ls(sl=1)
curShape = cmds.listRelatives(ctrl[0], c=1)
cmds.select(cl=1)
cmds.select(curShape)
cmds.select(ctrl[1],add=1)
cmds.parent(r=1, s=1)
cmds.delete(ctrl[1]+"Shape")
cmds.rename(curShape, ctrl[1]+"Shape")

#Dynamics Scale fix
#headSquash scaleFix 
#Connect Master_Ctrl.globalScale to squashIKCurveInfoMainScale.input2X
#connectAttr -f Master_Ctrl.GlobalScale squashIKCurveInfoMainScale.input2X;
mdn = cmds.ls("*_ScaleFix_Mdn")
cmds.select(mdn)
for each in mdn:
    cmds.connectAttr("Master_Ctrl.scaleX", each+".input2X")

#hideMotionGrpJoints
import maya.cmds as cmds
jnt = cmds.listRelatives('MotionSystem', ad = 1, typ = 'joint')
for x in jnt:
    cmds.setAttr(x + '.drawStyle', 2)    

#Adding sets to orig_set     
cmds.sets("Sets", add="orig_set")

#Adding ctrls to controls_set
ctrl = cmds.ls(sl=1)
cmds.sets(ctrl, add="controls_set")


#Removing rotation values on FKXRoot_M_Jnt and reparent with HipSwingReverseRoot
cmds.delete("FKXRoot_M_parentConstraint1")
cmds.setAttr("FKXRoot_M_Jnt.rotateX", 0)
cmds.setAttr("FKXRoot_M_Jnt.rotateY", 0)
cmds.setAttr("FKXRoot_M_Jnt.rotateZ", 0)
cmds.parenConstraint("HipSwingReverseRoot", "FKXRoot_M_Jnt", mo=1)


#Fixing IKToes_L_Ctrl Placement
#To fix this, unparent IKToesHandle_L, IKOffsetToes_L orientation should match to FKOffsetToes_L then reparent 
for side in ["L", "R"]:
	cmds.parent("IKToesHandle_"+side, w=True)
	cmds.parent("IKOffsetToes_"+side, w=True)
	cmds.delete(cmds.parentConstraint("FKOffsetToes_"+side, "IKOffsetToes_"+side, mo=0))
	cmds.parent("IKToesHandle_"+side, "IKToes_"+side+"_Ctrl")
	cmds.parent("IKOffsetToes_"+side, "IKLegLiftToe_"+side)


# Fingers_L_Ctrl - spread should work properly, check Alexander 
# (change input 2x of Pinky_01_Spread_N_Bend_L_Mdn, Index_01_Spread_N_Bend_L_Mdn and 
# Middle_01_Spread_N_Bend_L_Mdn)IKToesHandle_L)
cmds.setAttr("Middle_01_Spread_N_Bend_L_Mdn.input2X", -0.2);
cmds.setAttr("Middle_01_Spread_N_Bend_R_Mdn.input2X", -0.2);


#child AimEye_M to UpperJaw_M_Jnt
cmds.parentConstraint("UpperJaw_M_Jnt", "AimEyeFollow_M")
cmds.connectAttr("eyeAimFollowSetRange.outValueX",  "AimEyeFollow_M_parentConstraint1.UpperJaw_M_JntW2")
cmds.disconnectAttr("eyeAimFollowSetRange.outValueX", "AimEyeFollow_M_parentConstraint1.Head_MW0")
cmds.setAttr("AimEyeFollow_M_parentConstraint1.Head_MW0", 0)
cmds.setAttr("AimEyeFollow_M_parentConstraint1.w0", lock=True)

#tweakOne
cmds.parent("upperTeethOffset_M", "upperFace_M")
cmds.parentConstraint("UpperJaw_M_Jnt", "upperFaceOffset_M", mo=1)

#tweakTwo
cmds.parent("FKOffsetUpperJaw_M", "Facial_Controls_Gp")
cmds.parentConstraint("FKXHead_M_Jnt", "FKOffsetUpperJaw_M", mo=1)
cmds.scaleConstraint("FKXHead_M_Jnt", "FKOffsetUpperJaw_M", mo=1)

#tweakThree
cmds.setAttr("EyeBrowInner_L_Ctrl.EyeBrowMid1Joint", 0.8)
cmds.setAttr("EyeBrowOuter_L_Ctrl.EyeBrowMid2Joint", 0.7)
cmds.setAttr("EyeBrowInner_R_Ctrl.EyeBrowMid1Joint", 0.8)
cmds.setAttr("EyeBrowOuter_R_Ctrl.EyeBrowMid2Joint", 0.7)


#copySkinCluster
import maya.cmds as cmds
import maya.mel as mel
sel = cmds.ls(sl=True)
item= sel[0]
skcName = mel.eval('findRelatedSkinCluster '+item)
jnts = cmds.skinCluster(skcName, q=1, inf=1)
newSkc = cmds.skinCluster(jnts, sel[1], tsb=True)
cmds.copySkinWeights(ss=skcName, ds=newSkc[0], nm=True, surfaceAssociation="closestPoint")


#RenameCtrlShapeNode
sel= cmds.ls(sl=1)
for each in sel:
    cmds.select(each)
    oldName = cmds.pickWalk(d="down")
    cmds.rename(oldName, each+"Shape")


    











