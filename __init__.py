import maya.cmds as cmds
import json
#------------------------------------1.UI---------------------------------------------
usd = cmds.internalVar(usd=True) #result: C:/Users/user/Documents/maya/2022/scripts/
mayascripts = '%s/%s' % (usd.rsplit('/', 3)[0], 'scripts') #result: C:/Users/user/Documents/maya/scripts

class mocapMatcher():
    def __init__(self):
        self.winTitle = 'Kaia\'s Mocap Matcher'
        self.winName = 'kaiaMocapMatcher'

        self.nameSpace1 = None
        self.nameSpace2 = None
        
        
        basePath = mayascripts+'/Kaia_MocapMatcher/'
        advCtrlPath = basePath + 'ADV_ctrl_names.json'
        hikJntPath = basePath + 'HIK_jnt_names.json'
        advJntPath = basePath + 'ADV_jnt_names.json'

        with open(advCtrlPath, 'r') as read_file:
            advData = json.load(read_file)
            self.nameList = advData['nameList']
            self.ADVhandleList = advData['ADVhandleList']

        with open(hikJntPath, 'r') as read_file:
            self.hikJntByName = {i['name']: i['jnt'] for i in json.load(read_file)['nameList']}

        with open(advJntPath, 'r') as read_file:
            self.advJntByName = {i['name']: i['jnt'] for i in json.load(read_file)['nameList']}

        ###
        self.bakeList = []
        
        self.advCtrlList = []

        self.createWindow()

    def createWindow(self):

        #test to see if the window exists
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName) #we don't want to create extra windows


        cmds.window(self.winName, title=self.winTitle, width=355, height=530, s=False) #create a new window
        cmds.scrollLayout( 'scorllLayout') #makes your entire layout scrollable #first - main layout
        cmds.columnLayout( adjustableColumn=True ) #second layout - attaches to the main layout

        cmds.frameLayout( label='Templates', collapsable=True, collapse=False )
        cmds.columnLayout( rowSpacing = 10, cat=('left',10), h=90 ) #fourth alyout - frame layout

        cmds.text(label='Automatically fill out the text fields for you')
        cmds.button(label='Human IK to Advanced Skeleton', c=self.loadTemplate )
        cmds.button(label='ADV to ADV', c=self.loadTemplateADV )

        cmds.setParent( '..' ) #this make the framelayout attach to the column layout #move hirearchilly up # '..' : previous
        cmds.setParent( '..' )

        cmds.frameLayout( label='NameSpace', collapsable=True, collapse=False )
        cmds.columnLayout( h=55 )
        
        self.nameSpace1 = cmds.textFieldButtonGrp( l='Mo Cap', bl='detect from selected', bc=self.detectNameSpace1, cal=(10,'left'), cw3=(100,120,100))
        self.nameSpace2 = cmds.textFieldButtonGrp( l='Advanced Skeleton', bl='detect from selected', bc=self.detectNameSpace2, cal=(10,'left'), cw3=(100,120,100))


        cmds.setParent('..')
        cmds.setParent('..')
        
        cmds.frameLayout( label='Prefix', collapsable=True, collapse=True )
        cmds.columnLayout( h=30 )

        self.HikPrefix = cmds.textFieldButtonGrp( l='Human IK', bl='detect from selected', bc=self.detectHikPrefix, cal=(10,'left'), cw3=(100,120,100))

        cmds.setParent('..')
        cmds.setParent('..')


        cmds.frameLayout( label='Joints / Controllers', collapsable=True, collapse=True )

        cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(120, 20) ) #fourth alyout - frame layout

        cmds.text(label=' ')
        cmds.text(label='Mo Cap')
        cmds.text(label='AdvancedSkeleton')

        self.createTextFields() #this is an iterator for creating text fields

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout( label='Functions', collapsable=True, collapse=False)
        cmds.columnLayout(rowSpacing = 10, cat=('left',10))

        cmds.text(l='Transfer MoCap data using parent constraints')
        cmds.button( label='1: Create Locators', width=170, c=self.createLocators )
        cmds.button( label='2: Attach Locs to MoCap Joints', width=170, c=self.attachLocsToMoCapJoints )
        cmds.button( label='3: Attach ADV Ctrls to Locs', width=170, c=self.attachAdvCtrlsToLocs )
        cmds.button( label='4: Bake', width=170, c=self.bakeMoCapSimulation )
        
        cmds.button( label='Helper: Select ADV Ctrls', c=lambda x: cmds.select(self.advCtrlList))

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

        if ':' in sel:
            ns = ns.split(':')[1]
            
        cmds.textFieldButtonGrp(self.HikPrefix, e=True, tx=ns)
    
    def queryText(self,x):
        y = cmds.textField( x, q=True, tx=True)
        return y
        
    def queryTextButGrp(self,x):
        y = cmds.textFieldButtonGrp(x, q=True, tx=True)
        return y

    def loadTemplate(self,_):
        for i in self.nameList:
            cmds.textField(i['field1'], e=True, tx=self.hikJntByName.get(i['name'], '') )
            cmds.textField(i['field2'], e=True, tx=i['ctrl'] )

    def loadTemplateADV(self,_):
        for i in self.nameList:
            cmds.textField(i['field1'], e=True, tx=self.advJntByName.get(i['name'], '') )
            cmds.textField(i['field2'], e=True, tx=i['ctrl'] )
        cmds.textFieldButtonGrp(self.HikPrefix, e=True, tx='')
    
    def createLocators(self,_):
        MatchGrp = cmds.group(empty=True, name = 'mocapMatch_grp')#create a group to put in the locators
        for i in self.nameList:
            loc = cmds.spaceLocator(name=i['name']+'_loc')#create locators
            offsetGrp = cmds.group(loc, name=i['name']+'_loc_offset')#create offset group
            nulGrp = cmds.group(offsetGrp, name=i['name']+'_loc_nul')#create nul group
            cmds.parent(nulGrp,MatchGrp)#parent locators to mocapMatch_grp

    def attachLocsToMoCapJoints(self,_):
        self.cRoot = 'Group'
        for i in self.nameList:
            moCapJnt = self.queryTextButGrp(self.nameSpace1) + self.queryTextButGrp(self.HikPrefix) + self.queryText(i['field1'])#name space + joints
            nulGrp = i['name']+'_loc_nul'
            #attach nul group instead of actual locators, allowing offset offsets
            const1 = cmds.parentConstraint( moCapJnt, self.queryTextButGrp(self.nameSpace2)+self.cRoot, nulGrp, maintainOffset=False )[0]
            cmds.setAttr(const1+'.'+self.cRoot+'W1', 0)

    def attachAdvCtrlsToLocs(self, _):
        self.bakeList = []
        self.advCtrlList = []
        
        cmds.currentTime(0)
        for i in self.nameList:
            moCapJnt = self.queryTextButGrp(self.nameSpace1) + self.queryTextButGrp(self.HikPrefix) + self.queryText(i['field1'])
            cmds.rotate(0, 0, 0, moCapJnt)
            cmds.setKeyframe(moCapJnt, at=['rx','ry','rz'], t=0)

        for i in self.nameList:
            loc = i['name']+'_loc'
            offsetGrp = i['name']+'_loc_offset'
            moCapJnt = self.queryTextButGrp(self.nameSpace1) + self.queryTextButGrp(self.HikPrefix) + self.queryText(i['field1'])#name space + joints
            advCtrl = self.queryTextButGrp(self.nameSpace2)+ self.queryText(i['field2'])#name space + controllers
            
            self.advCtrlList.append(advCtrl)
            
            if i['part']=='arm':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='IK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='pole':
                    cmds.setAttr(advCtrl+'.followMain',10) #pole follow off, it might create weird double transform when it's on
                    cmds.setAttr(advCtrl+'.followRoot',0) #pole follow off, it might create weird double transform when it's on
                    cmds.setAttr(advCtrl+'.followChest',0) #pole follow off, it might create weird double transform when it's on
                    cmds.setAttr(advCtrl+'.followArm',0) #pole follow off, it might create weird double transform when it's on
                    self.offsetPole(offsetGrp, moCapJnt,(0,0,0))
                    self.constTR(loc, advCtrl)

            if i['part']=='leg':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='IK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='pole':
                    cmds.setAttr(advCtrl+'.followMain',10) #pole follow off
                    cmds.setAttr(advCtrl+'.followRoot',0) #pole follow off
                    cmds.setAttr(advCtrl+'.followLeg',0) #pole follow off
                    if '_l' in i['name']:
                        self.offsetPole(offsetGrp, moCapJnt,(0,0,0)) #0, -30, 0
                    elif '_r' in i['name']:
                        self.offsetPole(offsetGrp, moCapJnt,(0,0,0)) #0, 30, 0
                    self.constTR(loc, advCtrl)

            if i['part']=='spine':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='IK':
                    self.constTR(loc, advCtrl)
                elif i['type']=='pole':
                    self.offsetPole(offsetGrp, moCapJnt)
                    self.constTR(loc, advCtrl)

            if i['part']=='shoulder':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)

            if i['part']=='finger':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)
            
            if i['part']!='arm' and i['part']!='leg' and i['part']!='spine' and i['part']!='finger':
                if i['type']=='FK':
                    self.constTR(loc, advCtrl)
                if i['type']=='IK':
                    self.constTR(loc, advCtrl)

    def offsetPole(self, grp, jnt,pos):
        cmds.move(pos[0],pos[1],pos[2], grp, relative=True, objectSpace=True)

    def constTR(self, loc, ctrl): #constraint translation and rotation
        try:
            cmds.pointConstraint( loc, ctrl, maintainOffset=False )
        except Exception as e:
            print(e)

        
        try:
            cmds.orientConstraint( loc, ctrl, maintainOffset=True )
        except Exception as e:
            print(e)
        self.bakeList.append(ctrl)

    def bakeMoCapSimulation(self, _):
        minTime = cmds.playbackOptions(q=True, minTime=True)
        maxTime = cmds.playbackOptions(q=True, maxTime=True)
        cmds.bakeResults( self.bakeList, simulation=True, t=(minTime,maxTime) )



#-----------------------------------------------------3.execute-------------------------------------------------------------------


