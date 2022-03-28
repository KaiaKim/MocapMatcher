import maya.cmds as cmds

#------------------------------------1.UI---------------------------------------------

class mocapMatcher():
    def __init__(self):
        self.winTitle = 'Kaia\'s Mocap Matcher'
        self.winName = 'kaiaMocapMatcher'

        self.MoCapNameSpaceField = None
        self.advNameSpaceField = None


        
        self.matchNames =[
        {'name':'Hip', 'type':'IK', 'part':'hip','field1':None, 'field2':None, 'ADV':'RootX_M','HIK':'Hips'},
        {'name':'Chest_IK','type':'IK', 'part':'spine', 'field1':None, 'field2':None, 'ADV':'IKSpine3_M', 'HIK':'Spine2'},
        {'name':'Neck_FK', 'type':'FK', 'part':'head', 'field1':None, 'field2':None, 'ADV':'FKNeck_M', 'HIK':'Neck'},

        {'name':'ElbowPole_IK_r','type':'pole','part':'arm', 'field1':None, 'field2':None, 'ADV':'PoleArm_R', 'HIK':'RightForeArm'},
        {'name':'ElbowPole_IK_l','type':'pole','part':'arm', 'field1':None, 'field2':None, 'ADV':'PoleArm_L', 'HIK':'LeftForeArm'},
        {'name':'Hand_IK_r','type':'IK','part':'arm', 'field1':None, 'field2':None, 'ADV':'IKArm_R', 'HIK':'RightHand'},
        {'name':'Hand_IK_l','type':'IK','part':'arm', 'field1':None, 'field2':None, 'ADV':'IKArm_L', 'HIK':'LeftHand'},

        {'name':'Shoulder_FK_r','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKScapula_R', 'HIK':'RightShoulder'},
        {'name':'Shoulder_FK_l','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKScapula_L', 'HIK':'LeftShoulder'},
        {'name':'UpperArm_FK_r','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKShoulder_R', 'HIK':'RightArm'},
        {'name':'UpperArm_FK_l','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKShoulder_L', 'HIK':'LeftArm'},
        {'name':'LowerArm_FK_r','type':'FK','part':'arm', 'field1': None, 'field2':None, 'ADV': 'FKElbow_R', 'HIK':'RightForeArm'},
        {'name':'LowerArm_FK_l','type':'FK','part':'arm', 'field1': None, 'field2':None, 'ADV': 'FKElbow_L', 'HIK':'LeftForeArm'},
        {'name':'Hand_FK_r','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKWrist_R', 'HIK':'RightHand'},
        {'name':'Hand_FK_l','type':'FK','part':'arm', 'field1':None, 'field2':None, 'ADV':'FKWrist_L', 'HIK':'LeftHand'},

        {'name':'KneePole_IK_r','type':'pole','part':'leg', 'field1':None, 'field2':None, 'ADV':'PoleLeg_R', 'HIK':'RightUpLeg'},
        {'name':'KneePole_IK_l','type':'pole','part':'leg', 'field1':None, 'field2':None, 'ADV':'PoleLeg_L', 'HIK':'LeftUpLeg'},
        {'name':'Foot_IK_r','type':'IK','part':'leg', 'field1':None, 'field2':None, 'ADV':'IKLeg_R',  'HIK':'RightFoot'},
        {'name':'Foot_IK_l','type':'IK','part':'leg', 'field1':None, 'field2':None, 'ADV':'IKLeg_L', 'HIK':'LeftFoot'},

        {'name':'UpperLeg_FK_r','type':'FK','part':'leg', 'field1':None, 'field2':None, 'ADV':'FKHip_R', 'HIK':'RightUpLeg'},
        {'name':'UpperLeg_FK_l','type':'FK','part':'leg', 'field1':None, 'field2':None, 'ADV':'FKHip_L', 'HIK':'LeftUpLeg'}
        ]

        self.armFkChecker = None
        self.armIkChecker = None
        self.legFkChecker = None
        self.legIkChecker = None

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
        cmds.columnLayout()

        self.armFkChecker = cmds.checkBox( label = 'Arm FK', value=True)
        self.armIkChecker = cmds.checkBox( label = 'Arm IK', value=False)
        self.legFkChecker = cmds.checkBox( label = 'Leg FK', value=False)
        self.legIkChecker = cmds.checkBox( label = 'Leg IK', value=True)

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

            i['field1'] = cmds.textField() #store text field for quary & edit
            i['field2'] = cmds.textField()

    def quaryText(self,x):
        y = cmds.textField( x, q=True, tx=True)
        return y

    def quaryCheckBox(self, x):
        y = cmds.checkBox( x, q=True, v=True)
        return y

    def loadTemplate(self,args):
        cmds.textField(self.moCapNameSpaceField, e=True, tx='Daisy_HIK_v02_Ctrl_') #tempary code for fast testing. Users would have to write it manually
        cmds.textField(self.advNameSpaceField, e=True, tx='Daisy_rig_v019_ADV:') #tempary code
        for i in self.matchNames:
            cmds.textField(i['field1'], e=True, tx=i['ADV'] )
            cmds.textField(i['field2'], e=True, tx=i['HIK'] )


    def createLocators(self, args):
        MatchGrp = cmds.group(empty=True, name = 'mocapMatch_grp')#create a group to put in the locators
        for i in self.matchNames:
            loc = cmds.spaceLocator(name=i['name']+'_loc')#create locators
            offsetGrp = cmds.group(loc, name=i['name']+'_loc_offset')#create offset group
            nulGrp = cmds.group(offsetGrp, name=i['name']+'_loc_nul')#create nul group
            cmds.parent(nulGrp,MatchGrp)#parent locators to mocapMatch_grp

    def attachLocsToMoCapJoints(self, args):
        for i in self.matchNames:
            moCapJnt = self.quaryText(self.moCapNameSpaceField) + self.quaryText(i['field2'])#name space + joints
            nulGrp = i['name']+'_loc_nul'
            #attach nul group instead of actual locators, allowing offset offsets
            cmds.parentConstraint( moCapJnt, nulGrp, maintainOffset=False )

    def attachAdvCtrlsToLocs(self, args):
        for i in self.matchNames:
            loc = i['name']+'_loc'
            offsetGrp = i['name']+'_loc_offset'
            moCapJnt = self.quaryText(self.moCapNameSpaceField) + self.quaryText(i['field2'])#name space + joints
            advCtrl = self.quaryText(self.advNameSpaceField)+ self.quaryText(i['field1'])#name space + controllers

            if i['part']=='arm':
                if self.quaryCheckBox(self.armFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.quaryCheckBox(self.armIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)
                            self.constT(loc, advCtrl)

            if i['part']=='leg':
                if self.quaryCheckBox(self.legFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.quaryCheckBox(self.legIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)
                            self.constT(loc, advCtrl)

            if i['part']!='arm' and i['part']!='leg':
                if i['type']=='IK':
                    self.constTR(loc, advCtrl)
                if i['type']=='FK':
                    self.constR(loc, advCtrl, moCapJnt)

    def offsetPole(self, grp, jnt):
        #calculate the pole vector using vector math
        #apply offset translation
        #reference: https://youtu.be/bB_HL1tBVHY
        cmds.move(0, 0, 10, grp, relative=True) #WIP

    def constT(self, loc, ctrl): #constraint translation
        cmds.parentConstraint( loc, ctrl, skipRotate=['x','y','z'], maintainOffset=False )

    def constR(self, loc, ctrl, jnt): #constraint rotation
        cmds.rotate(0,0,0,jnt) ###set HIK joint roatation to 0, but no key
        cmds.parentConstraint( loc, ctrl, skipTranslate=['x','y','z'], maintainOffset=True )

    def constTR(self, loc, ctrl): #constraint translation and rotation
        cmds.parentConstraint( loc, ctrl, maintainOffset=False )

    def bakeMoCapSimulation(self, args):
        print('Bake Simulation working') #WIP



#-----------------------------------------------------3.execute-------------------------------------------------------------------
run = mocapMatcher()
