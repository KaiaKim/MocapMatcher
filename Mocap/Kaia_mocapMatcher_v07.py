import maya.cmds as cmds
import json
#------------------------------------1.UI---------------------------------------------

class mocapMatcher():
    def __init__(self):
        self.winTitle = 'Kaia\'s Mocap Matcher'
        self.winName = 'kaiaMocapMatcher'

        self.nameSpace1 = None
        self.nameSpace2 = None
        
        jsonPath = r"D:\Thesis\Assets\Scripts\Mocap\matchNames.json"
        
        #get json data
        with open(jsonPath,"r") as read_file:
            self.nameList = json.load(read_file)['nameList']
            
        with open(jsonPath,"r") as read_file:
            self.ADVhandleList = json.load(read_file)['ADVhandleList']

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

        cmds.window(self.winName, title=self.winTitle, width=355, height=530, s=False) #create a new window
        cmds.scrollLayout( 'scorllLayout') #makes your entire layout scrollable #first - main layout
        cmds.columnLayout( adjustableColumn=True ) #second layout - attaches to the main layout

        cmds.frameLayout( label='Templates', collapsable=True, collapse=False )
        cmds.columnLayout( rowSpacing = 10, cat=('left',10), h=55 ) #fourth alyout - frame layout

        cmds.text(label='Automatically fill out the text fields for you')
        cmds.button(label='Human IK to Advanced Skeleton', c=self.loadTemplate )

        cmds.setParent( '..' ) #this make the framelayout attach to the column layout #move hirearchilly up # '..' : previous
        cmds.setParent( '..' )

        cmds.frameLayout( label='NameSpace', collapsable=True, collapse=False )
        cmds.columnLayout( h=55 )
        
        self.nameSpace1 = cmds.textFieldButtonGrp( l='Mo Cap', bl='detect from selected', bc=self.detectNameSpace1, cal=(10,'left'), cw3=(100,120,100))
        self.nameSpace2 = cmds.textFieldButtonGrp( l='Advanced Skeleton', bl='detect from selected', bc=self.detectNameSpace2, cal=(10,'left'), cw3=(100,120,100))


        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.frameLayout( label='Prefix', collapsable=True, collapse=False )
        cmds.columnLayout( h=30 )

        self.HikPrefix = cmds.textFieldButtonGrp( l='Human IK', bl='detect from selected', bc=self.detectHikPrefix, cal=(10,'left'), cw3=(100,120,100))

        cmds.setParent('..')
        cmds.setParent('..')


        cmds.frameLayout( label='Joints / Controllers', collapsable=True, collapse=True )

        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 20) ) #fourth alyout - frame layout

        cmds.text(label=' ')
        cmds.text(label='Mo Cap')
        cmds.text(label='AdvancedSkeleton')

        self.createTextFields() #this is an iterator for creating text fields

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='FK IK', collapsable=True, collapse=False)
        cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(170,80) )
        
        cmds.gridLayout( numberOfColumns=2, cellWidthHeight=(80,20) )

        self.armFkChecker = cmds.checkBox( label = 'Arm FK', value=True)
        self.armIkChecker = cmds.checkBox( label = 'Arm IK', value=False)
        self.legFkChecker = cmds.checkBox( label = 'Leg FK', value=False)
        self.legIkChecker = cmds.checkBox( label = 'Leg IK', value=True)
        self.spineFkChecker = cmds.checkBox( label = 'Spine FK', value=False)
        self.spineIkChecker = cmds.checkBox( label = 'Spine IK', value=True)
        
        cmds.setParent('..')
        cmds.columnLayout(rowSpacing = 7)
        
        cmds.text( label='Advanced Skeleton only')
        cmds.button( label='Set Handles', c=self.setHandlesADV)
        
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='Functions', collapsable=True, collapse=False)
        cmds.columnLayout(rowSpacing = 10, cat=('left',10))

        cmds.text(l='Transfer MoCap data using parent constraints')
        cmds.button( label='1: Create Locators', width=170, c=self.createLocators )
        cmds.button( label='2: Attach Locs to MoCap Joints', width=170, c=self.attachLocsToMoCapJoints )
        cmds.button( label='3: Attach ADV Ctrls to Locs', width=170, c=self.attachAdvCtrlsToLocs )
        cmds.button( label='4: Bake', width=170, c=self.bakeMoCapSimulation )

        cmds.showWindow()

    def createTextFields(self):
        for i in self.nameList:
            if '_r' in i['name']:
                simpleName = i['name'].strip('_r') #right side
            elif '_l' in i['name']:
                simpleName = ' ' #left side
            else:
                simpleName = i['name'] #middle
            cmds.text(label=simpleName)

            i['field1'] = cmds.textField() #store text field for query & edit
            i['field2'] = cmds.textField()
            

    def detectNameSpace1(self):
        sel=cmds.ls(sl=True)[0] #get selection. use first when multiple selected
        if ':' in sel:
            ns = sel.split(':')[0] + ':'
        else:
            ns = ''
        
        cmds.textFieldButtonGrp(self.nameSpace1, e=True, tx=ns)
        
    def detectNameSpace2(self):
        sel=cmds.ls(sl=True)[0] #get selection. use first when multiple selected
        if ':' in sel:
            ns = sel.split(':')[0] + ':'
        else:
            ns = ''
        
        cmds.textFieldButtonGrp(self.nameSpace2, e=True, tx=ns)
            
    def detectHikPrefix(self):
        sel=cmds.ls(sl=True)[0] #get selection. use first when multiple selected
        if 'Ctrl_' in sel:
            ns = sel.split('Ctrl_')[0] + 'Ctrl_'
        else:
            ns = ''
        
        cmds.textFieldButtonGrp(self.HikPrefix, e=True, tx=ns)
    
    def queryText(self,x):
        y = cmds.textField( x, q=True, tx=True)
        return y
        
    def queryTextButGrp(self,x):
        y = cmds.textFieldButtonGrp(x, q=True, tx=True)
        return y

    def queryCheckBox(self, x):
        y = cmds.checkBox( x, q=True, v=True)
        return y

    def loadTemplate(self,_):
        for i in self.nameList:
            cmds.textField(i['field1'], e=True, tx=i['HIK'] )
            cmds.textField(i['field2'], e=True, tx=i['ADV'] )
            

    def setHandlesADV(self,_):
        for i in self.ADVhandleList:
            hdl = self.queryTextButGrp(self.nameSpace2)+i['handle']
            
            if i['type']=='arm':
                if self.queryCheckBox(self.armIkChecker)==True:
                    attr=10
                elif self.queryCheckBox(self.armFkChecker)==True:
                    attr=0
                
            if i['type']=='leg':
                if self.queryCheckBox(self.legIkChecker)==True:
                    attr=10
                elif self.queryCheckBox(self.legFkChecker)==True:
                    attr=0
                    
            if i['type']=='spine':
                if self.queryCheckBox(self.spineIkChecker)==True:
                    attr=10
                elif self.queryCheckBox(self.spineFkChecker)==True:
                    attr=0
            
            cmds.setAttr(hdl+'.FKIKBlend', attr)
            
    
    def createLocators(self,_):
        MatchGrp = cmds.group(empty=True, name = 'mocapMatch_grp')#create a group to put in the locators
        for i in self.nameList:
            loc = cmds.spaceLocator(name=i['name']+'_loc')#create locators
            offsetGrp = cmds.group(loc, name=i['name']+'_loc_offset')#create offset group
            nulGrp = cmds.group(offsetGrp, name=i['name']+'_loc_nul')#create nul group
            cmds.parent(nulGrp,MatchGrp)#parent locators to mocapMatch_grp

    def attachLocsToMoCapJoints(self,_):
        for i in self.nameList:
            moCapJnt = self.queryTextButGrp(self.nameSpace1) + self.queryTextButGrp(self.HikPrefix) + self.queryText(i['field1'])#name space + joints
            nulGrp = i['name']+'_loc_nul'
            #attach nul group instead of actual locators, allowing offset offsets
            cmds.parentConstraint( moCapJnt, nulGrp, maintainOffset=False )

    def attachAdvCtrlsToLocs(self, _):
        for i in self.nameList:
            loc = i['name']+'_loc'
            offsetGrp = i['name']+'_loc_offset'
            moCapJnt = self.queryTextButGrp(self.nameSpace1) + self.queryTextButGrp(self.HikPrefix) + self.queryText(i['field1'])#name space + joints
            advCtrl = self.queryTextButGrp(self.nameSpace2)+ self.queryText(i['field2'])#name space + controllers

            if i['part']=='arm':
                if self.queryCheckBox(self.armFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.armIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            cmds.setAttr(advCtrl+'.follow',0) #pole follow off, it might create weird double transform when it's on
                            self.offsetPole(offsetGrp, moCapJnt,(0,0,-10))
                            self.constT(loc, advCtrl)

            if i['part']=='leg':
                if self.queryCheckBox(self.legFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.legIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            cmds.setAttr(advCtrl+'.follow',0) #pole follow off
                            self.offsetPole(offsetGrp, moCapJnt,(0,0,10))
                            self.constT(loc, advCtrl)

            if i['part']=='spine':
                if self.queryCheckBox(self.spineFkChecker)==True:
                    if i['type']=='FK':
                        self.constR(loc, advCtrl, moCapJnt)
                if self.queryCheckBox(self.spineIkChecker)==True:
                        if i['type']=='IK':
                            self.constTR(loc, advCtrl)
                        elif i['type']=='pole':
                            self.offsetPole(offsetGrp, moCapJnt)
                            self.constT(loc, advCtrl)

            if i['part']=='shoulder':
                if i['type']=='FK':
                    self.constR(loc,advCtrl,moCapJnt)
            
            if i['part']!='arm' and i['part']!='leg' and i['part']!='spine':
                if i['type']=='FK':
                    self.constR(loc, advCtrl, moCapJnt)
                if i['type']=='IK':
                    self.constTR(loc, advCtrl)

    def offsetPole(self, grp, jnt,pos):
        cmds.move(pos[0],pos[1],pos[2], grp, relative=True, objectSpace=True)

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

    def bakeMoCapSimulation(self, _):
        minTime = cmds.playbackOptions(q=True, minTime=True)
        maxTime = cmds.playbackOptions(q=True, maxTime=True)
        cmds.bakeResults( self.bakeList, simulation=True, t=(minTime,maxTime) )



#-----------------------------------------------------3.execute-------------------------------------------------------------------
run = mocapMatcher()
