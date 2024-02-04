import sys
sys.dont_write_bytecode=True
import glob
import os
import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import  QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox, QFileDialog, QLabel, QMessageBox, QHBoxLayout
import cv2

from libs.validateYolo import yoloCheck
from libs.lineParser import lineParse

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LabelAug')
        parentLayout= QVBoxLayout()

        horizontal1Layout=QHBoxLayout()
        horizontalDirInfoLayout=QHBoxLayout()
        ver1CheckboxLayout=QHBoxLayout()


        
#label open button with 
        labelOpen=QPushButton("Label Open Directory", clicked=self.openLabelDirectory)

# Image open button 
        imgOpen=QPushButton("Image Open Directory",clicked=self.openImageDirectory)
# All augment checkboxs (add more augmentations)
        checkLabel=QLabel('Augmentation')       
        self.rotateC90=QCheckBox(text='rotateC90')
        self.rotateC180=QCheckBox(text='rotateC180')
        self.rotateC270=QCheckBox(text='rotateC270')
        self.flipOnY=QCheckBox(text='flipOnY')
# Two variables to save the directories
        self.openLabDir=None
        self.openImgDir=None
        self.saveDir=None
# List of all augmentation
        self.listAug=['rotateC90','rotateC180','rotateC270','flipOnY']
# List of to do augmentation
        self.toDoAugList=[]
# All textfiles locations
        self.textFiles=None
# All imgfiles locations
        self.imgFiles=None

# labelbox to show the open directory path and save dir path
        self.openLabelPath=QLabel()
        self.openImagePath=QLabel()
        self.savePath=QLabel()
# Label save directory button
        labelSave=QPushButton("Label Save Directory", clicked=self.saveDirectory)
# Textbox to show the image and label info
        self.imgInfo=QLabel()
        self.labelInfo=QLabel()
# Execute button to augment labels for checked items
        goButton=QPushButton("Go!", clicked=self.goFunctions)

        

        
        horizontal1Layout.addWidget(labelOpen)
        horizontal1Layout.addWidget(imgOpen)
        horizontal1Layout.addWidget(labelSave)
        horizontalDirInfoLayout.addWidget(self.openLabelPath)
        horizontalDirInfoLayout.addWidget(self.openImagePath)
        horizontalDirInfoLayout.addWidget(self.savePath)
        
        ver1CheckboxLayout.addWidget(self.rotateC90)
        ver1CheckboxLayout.addWidget(self.rotateC180)
        ver1CheckboxLayout.addWidget(self.rotateC270)
        ver1CheckboxLayout.addWidget(self.flipOnY)
        
        
        parentLayout.addLayout(horizontal1Layout)
        parentLayout.addLayout(horizontalDirInfoLayout)

        parentLayout.addWidget(self.labelInfo)
        parentLayout.addWidget(self.imgInfo)

        parentLayout.addWidget(checkLabel)
        parentLayout.addLayout(ver1CheckboxLayout)
        
        parentLayout.addWidget(goButton)

        self.setLayout(parentLayout)
        self.setMinimumSize(QSize(400, 300))
  

# Open directory button action

    def openLabelDirectory(self):
   
        self.directoryOpen('label')
        if((len(self.textFiles))>0):
            #  .txt files exist in the directory
            self.labelInfo.setText(str(len(self.textFiles))+' .txt files found in the directory')
        else:
            self.labelInfo.setText('No .txt files found in the directory!')
        return


# Open image directory button action
    def openImageDirectory(self):
        
        self.directoryOpen('image')
        if((len(self.imgFiles))>0):
            #  .jpg files exist in the directory
            self.imgInfo.setText(str(len(self.imgFiles))+' image files found in the directory')
        else:
            self.imgInfo.setText('No .jpg files found in the directory!')
        
    

# Save directory button action
    def saveDirectory(self):
        #self.saveDirInfo.setText('')
        self.directoryOpen('save')


# Directory open function
    def directoryOpen(self,info):
        # (info='image' image open directory, 'label' label open directory 'save' save directory)
        dialog=QFileDialog()
        foo_dir=dialog.getExistingDirectory(self,'Select a Folder')
        if info=='image':
            self.openImgDir=foo_dir
            self.imgFiles=glob.glob(self.openImgDir+'/*.jp*g')
            self.openImagePath.setText('Image Dir: '+foo_dir)
        elif info=='label':
            self.openLabDir=foo_dir
            self.textFiles=glob.glob(self.openLabDir+'/*.txt')
            self.openLabelPath.setText('Label Dir: '+foo_dir)

        else:
            self.saveDir=foo_dir
            self.savePath.setText('Save Directory: '+ foo_dir)
        return

        
# Go button action
    def goFunctions(self):
    #Check if labeldir is valid or contains .txt files
    #Check if augmentation is selected or not
    #Check if savedir is valid
        self.checkBoxStatus()
        
        if self.goCheck():
# Satiesfies all prerequisites for starting the augmentation process          
            for augment in self.toDoAugList:
                # For each augment checklist make directories in the save directory
                augmentDir=self.makeSaveDirectory(augment)
                #For each augment pass all the files in the augment function
                for file in self.textFiles:
                    self.allLabelAugmentFactory(file,augmentDir,augment)
                # For each augment pass all the img files in the img aug factory
                for file in self.imgFiles:
                    self.allImageAugmentFactory(file,augmentDir,augment)
            # Change it to information message '''''''''''''ToDO''''''''''''''
            self.warningMessage('Augmentation Completed!')
        else:
            print('Not ready')


    def checkBoxStatus(self):
        self.toDoAugList=[]
        if self.rotateC90.isChecked():
            self.toDoAugList.append('rotateC90')
        if self.rotateC180.isChecked():
            self.toDoAugList.append('rotateC180')
        if self.rotateC270.isChecked():
            self.toDoAugList.append('rotateC270')
        if self.flipOnY.isChecked():
            self.toDoAugList.append('flipOnY')

# Check if open, save , augment conditions for satisfy before go   
    def goCheck(self):
        if self.openLabDir==None:
            self.warningMessage('Select a directory which contains the label .txt files!')
            return False
        if (len(self.textFiles)==0):
            self.warningMessage('No .txt file in the directory to augment!')
            return False
        if self.openImgDir==None:
            self.warningMessage('Select a directory which contains the image files!')
            return False
        if(len(self.imgFiles)==0):
            self.warningMessage('No image file in the directory to augment!')
            return False
        if (len(self.toDoAugList)==0):
            self.warningMessage('No Augment to be done! Select an augment from the checklist!')
            return False
        if self.saveDir==None:
            self.warningMessage('Select a directory to save the augmented files!')
            return False
        return True
    

# Make directories in the save directory for different augmentation
    def makeSaveDirectory(self,aug):
        augPath=self.saveDir+'/'+aug+'/'

        if not os.path.isdir(augPath):
            os.makedirs(augPath)
        return augPath
    
# Augment each text file according to the augmentation method
    def allLabelAugmentFactory(self,labelPath,savePath,aug):
        with open(labelPath, 'rt') as fd:

            text_content=[]

            for line in fd.readlines():
                row = []
                splited = line.strip().split(' ')
                flag=True
            # YOLO format validation
                flag= yoloCheck(splited)
                if flag==False:
                    continue
            #Splitted float numbers of each YOLO line 
                cla,new_xcenter,new_ycenter,new_width,new_height=lineParse(splited,aug)

                row.append(cla)
                row.append(new_xcenter)
                row.append(new_ycenter)
                row.append(new_width)
                row.append(new_height)

                text_content.append(row)
            if text_content!=[]:
                
                np.savetxt(savePath+os.path.basename(labelPath)[:-4]+'_'+aug+'.txt',text_content,delimiter=' ',fmt='%d %f %f %f %f')
            else:
                # YOLO format error message
                print(labelPath+ ' does not contain valid YOLO format!')
    
    # All image augment function
    def allImageAugmentFactory(self,imagePath,savePath, aug):
        img=cv2.imread(imagePath)

        if (aug==self.listAug[0]): #rotateC90
            newImg=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
        elif (aug==self.listAug[1]):#rotateC180
            newImg=cv2.rotate(img,cv2.ROTATE_180)
        elif (aug==self.listAug[2]):#rotateC270
            newImg=cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif (aug==self.listAug[3]):#flipOnY
            newImg=cv2.flip(img, 1)
        else:
            print('No valid augmentation')
        if (os.path.basename(imagePath)[-2:]=='eg'):
            cv2.imwrite(savePath+os.path.basename(imagePath)[:-5]+'_'+aug+'.jpeg',newImg)
        else:
            cv2.imwrite(savePath+os.path.basename(imagePath)[:-4]+'_'+aug+'.jpg',newImg)

    
    def warningMessage(self,message):
        button = QMessageBox.warning(self,'Warning',message)
        if button==QMessageBox.StandardButton.Ok:
            pass



app= QApplication(sys.argv)

window= MyApp()
window.show()

app.exec()