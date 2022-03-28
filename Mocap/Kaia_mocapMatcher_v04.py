import maya.cmds as cmds
import maya.OpenMaya as om
import json
#------------------------------------1.UI---------------------------------------------

class mocapMatcher():
    def __init__(self):
        self.winTitle = 'Kaia\'s Mocap Matcher'
        self.winName = 'kaiaMocapMatcher'

        self.MoCapNameSpaceField = None
        self.advNameSpaceField = None

        #get json data
        with open("D:\Thesis\Assets\Scripts\Mocap\matchNames.json","r") as read_file:
            self.matchNames = json.load(read_file)['nameList']

        self.bakeList = []

        self.armFkChecker = None
        self.armIkChecker = None
        self.legFkChecker = None
        self.legIkChecker = None
        self.spineFkChecker = None
        self.spineIkChecker = None

        self.createWindow()

    def createWindow(self):
        #test to see if the window exists
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName) #we don't want to create extra windows

        cmds.window(self.winName, title=self.winTitle) #create a new window
        cmds.scrollLayout( 'scorllLayout', width=320) #makes your entire layout scrollable #first - main layout
        cmds.columnLayout( adjustableColumn=True ) #second layout - attaches to the main layout

        cmds.frameLayout( label='Templates', collapsable=True, collapse=False )
        cmds.columnLayout( rowSpacing = 10 ) #fourth alyout - frame layout

        cmds.text(label='Automatically fill out the text fields for you')
        cmds.button(label='Human IK to Advanced Skeleton', command=self.loadTemplate )

        cmds.setParent( '..' ) #this make the framelayout attach to the column layout #move hirearchilly up # '..' : previous
        cmds.setParent( '..' )

        cmds.frameLayout( label='NameSpace', collapsable=True, collapse=False )
        cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(150,20) )

        cmds.text(label='Mo Cap')
        cmds.text(label='Advanced Skeleton')
        self.moCapNameSpaceField = cmds.textField() #text fields for name space or prefix
        self.advNameSpaceField = cmds.textField()

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='Joints / Controllers', collapsable=True, collapse=False )

        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 20) ) #fourth alyout - frame layout

        cmds.text(label=' ')
        cmds.text(label='Mo Cap')
        cmds.text(label='AdvancedSkeleton')

        self.createTextFields() #this is an iterator for creating text fields

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='FK IK', collapsable=True, collapse=False)
        cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(80,20) )

        self.armFkChecker = cmds.checkBox( label = 'Arm FK', value=True)
        self.armIkChecker = cmds.checkBox( label = 'Arm IK', value=False)
        self.legFkChecker = cmds.checkBox( label = 'Leg FK', value=False)
        self.legIkChecker = cmds.checkBox( label = 'Leg IK', value=True)
        self.spineFkChecker = cmds.checkBox( label = 'Spine FK', value=True)
        self.spineIkChecker = cmds.checkBox( label = 'Spine IK', value=False)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='Functions', collapsable=True, collapse=False)
        cmds.columnLayout(rowSpacing = 10)

        cmds.text('Transfer MoCap data using parent constraints')
        cmds.button( label='1: Create Locators', width=170, command=self.createLocators )
        cmds.button( label='2: Attach Locs to MoCap Joints', width=170, command=self.attachLocsToMoCapJoints )
        cmds.button( label='3: Attach ADV Ctrls to Locs', width=170, command=self.attachAdvCtrlsToLocs )
        cmds.button( label='4: Bake', width=170, command=self.bakeMoCapSimulation )

        cmds.showWindow()

    def createTextFields(self):
        for i in self.matchNames:
            if '_r' in i['name']:
                simpleName = i['name'].strip('_r') #right side
            elif '_l' in i['name']:
                simpleName = ' ' #left side
            else:
                simpleName = i['name'] #middle
            cmds.text(label=simpleName)

            i['field1'] = cmds.textField() #store text field for query & edit
            i['field2'] = cmds.textField()

    def queryText(self,x):
        y = cmds.textField( x, q=True, tx=True)
        return y

    def queryCheckBox(self, x):
        y = cmds.checkBox( x, q=True, v=True)
        return y

    def loadTemplate(self,args):
        cmds.textField(self.moCapNameSpaceField, e=True, tx='Daisy_HIK_v02_Ctrl_') #tempary code for fast testing. Users would have to write it manually
        cmds.textField(self.advNameSpaceField, e=True, tx='Daisy_rig_v019_ADV:') #tempary code
        for i in self.matchNames:
            cmds.textField(i['field1'], e=True, tx=i['HIK'] )
            cmds.textField(i['field2'], e=True, tx=i['ADV'] )


    def createLocators(self, args):
        MatchGrp = cmds.group(empty=True, name = 'mocapMatch_grp')#create a group to put in the locators
        for i in self.matchNames:
            loc = cmds.spaceLocator(name=i['name']+'_loc')#create locators
            offsetGrp = cmds.group(loc, name=i['name']+'_loc_offset')#create offset group
            nulGrp = cmds.group(offsetGrp, name=i['name']+'_loc_nul')#create nul group
            cmds.parent(nulGrp,MatchGrp)#parent locators to mocapMatch_grp

    def attachLocsToMoCapJoints(self, args):
        for i in self.matchNames:
            moCapJnt = self.queryText(self.moCapNameSpaceField) + self.queryText(i['field1'])#name space + joints
            nulGrp = i['name']+'_loc_nul'
            #attach nul group instead of actual locators, allowing offset offsets
            cmds.parentConstraint( moCapJnt, nulGrp, maintainOffset=False )

    def attachAdvCtrlsToLocs(self, args):
        for i in self.matchNames:
            loc = i['name']+'_loc'
            offsetGrp = i['name']+'_loc_offset'
            moCapJnt = self.queryText(self.moCapNameSpaceField) + self.queryText(i['field1'])#name space + joints
            advCtrl = self.queryText(self.advNameSpaceField)+ self.queryText(i['field2'])#name space + controllers

            if i['part']=='arm':
                if self.queryCheckBox(self.armFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.armIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)
                            self.constT(loc, advCtrl)

            if i['part']=='leg':
                if self.queryCheckBox(self.legFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.legIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)

            if i['part']=='spine':
                if self.queryCheckBox(self.spineFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.spineIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)

            if i['part']!='arm' and i['part']!='leg':
                if i['type']=='IK':
                    self.constTR(loc, advCtrl)
                if i['type']=='FK':
                    self.constR(loc, advCtrl, moCapJnt)

    def offsetPole(self, grp, jnt):
        #calculate the pole vector using vector math
        #apply offset translation
        #reference: https://youtu.be/bB_HL1tBVHY
        nameSpace = self.queryText(self.moCapNameSpaceField)
        
        Hip_r = nameSpace + self.queryText( self.matchNames[21]['field1'] )
        Knee_r = nameSpace + self.queryText( self.matchNames[23]['field1'] )
        Foot_r = nameSpace + self.queryText( self.matchNames[25]['field1'] )
        
        pole_r = self.calculatePoleVector(Hip_r, Knee_r, Foot_r)
        print(pole_r.x, pole_r.y, pole_r.z)
        
        cmds.move(0, 0, 10, grp, relative=True) #WIP

    def calculatePoleVector(self, root, mid, end):
        root_pos = cmds.xform(root, q=True, ws=True, t=True)
        mid_pos = cmds.xform(mid, q=True, ws=True, t=True)
        end_pos = cmds.xform(end, q=True, ws=True, t=True)
        
        root_vec = om.MVector(root_pos[0], root_pos[1], root_pos[2])
        mid_vec = om.MVector(mid_pos[0], mid_pos[1], mid_pos[2])
        end_vec = om.MVector(end_pos[0], end_pos[1], end_pos[2])
        
        line = (end_vec - root_vec)
        point = (mid_vec - root_vec)
        
        scale_val = (line*point) / (line*line)
        proj_vec = line * scale_val + root_vec
        
        root_to_mid_len = (mid_vec - root_vec).length()
        mid_to_end_len = (end_vec - mid_vec).length()
        total_len = root_to_mid_len + mid_to_end_len
        
        pole_vec = (mid_vec - proj_vec).normal() * total_len
        return pole_vec

    def constT(self, loc, ctrl): #constraint translation
        cmds.parentConstraint( loc, ctrl, skipRotate=['x','y','z'], maintainOffset=False )
        self.bakeList.append(ctrl)

    def constR(self, loc, ctrl, jnt): #constraint rotation
        cmds.autoKeyframe(state=False)
        cmds.rotate(0,0,0,jnt) ###set HIK joint roatation to 0, but no key
        cmds.parentConstraint( loc, ctrl, skipTranslate=['x','y','z'], maintainOffset=True )
        self.bakeList.append(ctrl)

    def constTR(self, loc, ctrl): #constraint translation and rotation
        cmds.parentConstraint( loc, ctrl, maintainOffset=False )
        self.bakeList.append(ctrl)

    def bakeMoCapSimulation(self, args):
        minTime = cmds.playbackOptions(q=True, minTime=True)
        maxTime = cmds.playbackOptions(q=True, maxTime=True)
        cmds.bakeResults( self.bakeList, simulation=True, t=(minTime,maxTime) )



#-----------------------------------------------------3.execute-------------------------------------------------------------------
run = mocapMatcher()

#cmds.move(-17.19942224639838, -5.954297307988585, 72.88195937844529, 'Daisy_rig_v019_ADV:PoleLeg_R', absolute=True)