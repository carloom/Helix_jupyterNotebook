#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from __future__ import print_function
from PlotWiget import umbrellaSamplingPlot
from ipywidgets import Layout, Button, Box
import ipywidgets as widgets

files = ["image_1.png" , "image_2.png", "image_3.png" , "image_4.png",
         "image_5.png" , "image_6.png", "image_7.png" , "image_8.png",
         "image_9.png" , "image_10.png","image_11.png" ,"image_12.png",
         "image_13.png" ,"image_14.png","image_15.png" ,"image_16.png",
         "image_17.png" ,"image_18.png",]

mainBox  = widgets.VBox()
checkBox = widgets.HBox()
imageBox = widgets.HBox()

mainBox.children = [checkBox,imageBox]

display(mainBox)

firstPlot = umbrellaSamplingPlot('no tension','no_Tension' , imageBox , checkBox)
firstPlot.AddDropDownOption(files , 'density','den_images')
firstPlot.AddDropDownOption(files , 'carbon' ,'images')

secondPlot = umbrellaSamplingPlot( 'tension' ,'Tension' , imageBox , checkBox)
secondPlot.AddDropDownOption(files, 'density','den_images')
secondPlot.AddDropDownOption(files, 'carbon' ,'images')


# In[ ]:




