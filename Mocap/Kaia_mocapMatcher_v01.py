import maya.cmds as cmds

#------------------------------------1.UI---------------------------------------------

class mocapMatcher():
    def __init__(self):
        self.winTitle = 'Kaia\'s Mocap Matcher'
        self.winName = 'kaiaMocapMatcher'
        
        #ADV means advancedskeleton controllers, HIK means humanIK joints
        self.matchNames = [
        {'name':'Hip', 'ADV':'RootX_M', 'HIK':'Hips'}, 
        {'name':'Chest', 'ADV':'IKSpine3_M', 'HIK':'Spine2'},
        {'name':'Elbow_r', 'ADV':'PoleArm_R', 'HIK':'RightForeArm'},
        {'name':'Elbow_l', 'ADV':'PoleArm_L', 'HIK':'LeftForeArm'},
        {'name':'Hand_r', 'ADV':'IKArm_R', 'HIK':'RightHand'},
        {'name':'Hand_l', 'ADV':'IKArm_L', 'HIK':'LeftHand'},
        {'name':'Knee_r', 'ADV':'PoleLeg_R', 'HIK':'RightUpLeg'},
        {'name':'Knee_l', 'ADV':'PoleLeg_L', 'HIK':'LeftUpLeg'},
        {'name':'Foot_r', 'ADV':'IKLeg_R', 'HIK':'RightFoot'},
        {'name':'Foot_l', 'ADV':'IKLeg_L', 'HIK':'LeftFoot'}
        ]
        
        self.textFieldList = []
        
        self.createWindow()

    def createWindow(self):
        #test to see if the window exists
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName) #we don't want to create extra windows

        cmds.window(self.winName, title=self.winTitle) #create a new window
        cmds.scrollLayout( 'scorllLayout' ) #makes your entire layout scrollable #first - main layout
        cmds.columnLayout( adjustableColumn=True ) #second layout - attaches to the main layout
        
        cmds.frameLayout( label='Templates', collapsable=True, collapse=False )
        cmds.columnLayout( rowSpacing = 10 ) #fourth alyout - frame layout

        cmds.text(label='Automatically fill out the text fields for you')
        cmds.button(label='Human IK to Advanced Skeleton', command=self.loadTemplate )

        cmds.setParent( '..' ) #this make the framelayout attach to the column layout #move hirearchilly up # '..' : previous

        cmds.frameLayout( label='Namespace', collapsable=True, collapse=False )
        
        cmds.text(label=
        cmds.frameLayout( label='Joints', collapsable=True, collapse=False )

        cmds.gridLayout(numberOfColumns=2, cellWidthHeight=(120, 20) ) #fourth alyout - frame layout

        cmds.text(label='AdvancedSkeleton')
        cmds.text(label='Other')

        self.createTextFields() #this is an iterator for creating text fields
        
        cmds.setParent( '..' )
        cmds.frameLayout( label='FK IK', collapsable=True, collapse=False)
        cmds.columnLayout()
        
        cmds.checkBox( label = 'Arm FK', value=True)
        cmds.checkBox( label = 'Leg FK', value=False)
        cmds.checkBox( label = 'Arm IK', value=True)
        cmds.checkBox( label = 'Leg IK', value=False)
        
        cmds.setParent( '..' )
        cmds.frameLayout( label='Functions', collapsable=True, collapse=False)
        cmds.columnLayout(rowSpacing = 10)
        
        cmds.text('Transfer MoCap data using parent constraints')
        cmds.button( label='1: Create Locators', width=170)
        cmds.button( label='2: Attach Locs to MoCap Joints', width=170)
        cmds.button( label='3: Attach ADV Ctrls to Locs', width=170)
        cmds.button( label='4: Bake', width=170)
        
        cmds.showWindow()
        

        
    def createTextFields(self):
        for i in self.matchNames:
            advField = cmds.textField(tx=i['ADV'])
            otherField = cmds.textField(tx=i['HIK'])
        
    def loadTemplate(self,args):
        print('this is wip function')
        


#-----------------------------------------------------3.execute-------------------------------------------------------------------
run = mocapMatcher()

