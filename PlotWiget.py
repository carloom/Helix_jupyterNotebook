from   ipywidgets import Layout, Button, Box
import ipywidgets as widgets
import os
import fnmatch
import re

def listToString(s):  
    str1 = " "   
    return (str1.join(s)) 

class componentData:
    def __init__(self, objType, childrenData):
        self.objType      = objType  
        self.childrenData = childrenData

class basicComponent:
    def __init__(self, parent, childrenData):
  
        self.parent          =   parent
        self.children        =   []
        self.parentDirectory =   parent.directory   
        self.directory       =   parent.directory
        
        self.container = Box(layout = Layout(display    ='flex',
                                             flex_flow  ='column',
                                             align_items='stretch',
                                             border     ='solid',
                                             flex       ='1 1 auto') )
        
        parent.container.children = parent.container.children + (self.container,) 
        self.Generate(parent, childrenData)
    
        for childData in childrenData:
            self.children.append( childData.objType( self , childData.childrenData ) )
        
    def AddWidget(self, wid):
        self.container.children = self.container.children + (wid,)
        
class AddWindow(basicComponent):
    def __init__(self, childrenData , directory):
        self.children   = []
        self.childDat   = childrenData
        self.plusButton = widgets.Button(icon="plus")
        self.directory  = directory
        
        self.mainContainer = Box(layout = Layout(display    ='flex',
                                                 flex_flow  ='column',
                                                 align_items='stretch',
                                                 border     ='solid',
                                                 flex       ='1 1 auto'))
        
        self.container = Box(layout = Layout(display    ='flex',
                                             align_items='stretch',
                                             border     ='solid',
                                             flex       ='1 1 auto'))
        
        self.mainContainer.children = [self.plusButton , self.container]
        self.plusButton.on_click( lambda change : self.OnPress(change) )
        
    def OnPress(self, change):
        self.children.append( self.childDat.objType( self , self.childDat.childrenData ) )
        
    def remove(self , child):
        
        newList = []
        for elem in self.container.children:
            if( elem != child.container ):
                newList.append(elem)
        
        self.container.children = newList
        self.children.remove(child)
        
        

class SliderImage(basicComponent):
    def Generate(self, parent, childrenData):
        self.imageList  = []
        self.imageIndex = 0 
                             
        self.imageWidget  = widgets.Image(format='png', layout = Layout(width ='auto'))
        self.sliderWidget = widgets.IntSlider(min=1   , layout = Layout(width ='auto'))
               
        self.sliderWidget.observe( lambda change: self.OnSliderMove(change) , names='value')
        self.AddWidget(self.imageWidget)
        self.AddWidget(self.sliderWidget)
        
        self.UpdateDirectoty()
        self.UpdateImage()
        
    def UpdateDirectoty(self):
        regex = re.compile(r'\d+')
        self.imageList = []
        for file_name in os.listdir( self.directory ):
            if fnmatch.fnmatch(file_name, 'image_*.png'):
                self.imageList.append((file_name , int(listToString(regex.findall(file_name))) ))
                
        self.sliderWidget.max = len(self.imageList)
        self.imageIndex       = min(self.imageIndex , len(self.imageList) )
        self.imageList.sort(key= lambda elem : elem[1] ) 
            
    def UpdateImage(self):
        file = open( self.directory + '/' + self.imageList[self.imageIndex][0], "rb")
        self.imageWidget.value = file.read()
        file.close()
        
    def OnSliderMove(self, change):
        self.imageIndex = change['new'] - 1
        self.UpdateImage()
        
    def OnParentChange(self, parent):
        self.directory = parent.directory
        self.UpdateDirectoty()
        self.UpdateImage()
    
        
class dropDownMenu(basicComponent):
    def Generate(self, parent, childrenData):
        self.directoryList   = []
        self.parentDirectory = parent.directory 
        self.currentOption   = 0
        
        self.selection = widgets.Dropdown() 
        self.selection.observe( lambda change: self.OnChangeOption(change) , names='value')
        
        self.AddWidget(self.selection)
        
        self.UpdateDirectory()
        self.UpdateState()
        
    def UpdateDirectory(self):
        i = 0
        newDir = []
        for file_name in os.listdir( self.parentDirectory ):
            if os.path.isdir(self.parentDirectory + '/' + file_name):
                newDir.append( (file_name , ++i) )  
                i = i + 1
                
        self.directoryList= newDir        
        self.selection.options = self.directoryList 
                
    def UpdateState(self): 
        self.directory = self.parentDirectory + '/' + self.directoryList[self.currentOption][0]
        
        for child in self.children:
            child.OnParentChange(self)
    
    def OnParentChange(self, parent):
        self.parentDirectory = parent.directory
        self.UpdateDirectory()
        self.UpdateState()
        
    def OnChangeOption(self, change):
        self.currentOption = change['new']
        self.UpdateState()
        

class removableContainer(basicComponent):
    def Generate(self, parent, childrenData):
        self.deleteButton = widgets.Button(value=False, layout = Layout(icon ='minus' , button_style='danger'))
        self.deleteButton.on_click(lambda change : self.OnPress(change) )  
        
        self.AddWidget(self.deleteButton)
       
    def OnPress(self,change):
            self.parent.remove(self)
      
        
