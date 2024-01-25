import sys
import glob
import os
import numpy as np
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import  QApplication, QWidget, QPushButton, QVBoxLayout, QCheckBox, QFileDialog, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LabelAug')
        layout= QVBoxLayout()
        
#label open button with 
        labelOpen=QPushButton("Label Open Directory", clicked=self.openDirectory)
# All augment checkboxs (add more augmentations)       
        self.rotateC90=QCheckBox(text='rotateC90')
        self.rotateC180=QCheckBox(text='rotateC180')
        self.rotateC270=QCheckBox(text='rotateC270')
        self.flipOnY=QCheckBox(text='flipOnY')
# Two variables to save the directories
        self.openDir=None
        self.saveDir=None
# List of all augmentation
        self.listAug=['rotateC90','rotateC180','rotateC270','flipOnY']
# List of to do augmentation
        self.toDoAugList=[]
# All textfiles locations
        self.textfiles=None

# labelbox to show the open directory path and file info
        self.openDirLabel=QLabel()
        self.openDirInfo=QLabel()
# Label save directory button
        labelSave=QPushButton("Label Save Directory", clicked=self.saveDirectory)
# Textbox to show the save directory path
        self.saveDirLabel=QLabel()
        self.saveDirInfo=QLabel()
# Execute button to augment labels for checked items
        goButton=QPushButton("Go!", clicked=self.goFunctions)

        
        layout.addWidget(labelOpen)
        layout.addWidget(self.openDirLabel)
        layout.addWidget(self.openDirInfo)
        layout.addWidget(self.rotateC90)
        layout.addWidget(self.rotateC180)
        layout.addWidget(self.rotateC270)
        layout.addWidget(self.flipOnY)
        
        layout.addWidget(labelSave)
        layout.addWidget(self.saveDirLabel)
        layout.addWidget(self.saveDirInfo)
        layout.addWidget(goButton)

        self.setLayout(layout)
        self.setFixedSize(QSize(400, 300))
        
# Open directory button action

    def openDirectory(self):
        self.saveDirInfo.setText('')
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self,'Select a Folder')
        self.openDirLabel.setText(foo_dir)
        self.openDir=foo_dir
        self.textfiles=glob.glob(self.openDir+'/*.txt')
        if((len(self.textfiles))>0):
            #  .txt files exist in the directory
            self.openDirInfo.setText(str(len(self.textfiles))+' .txt files found in the directory')
        else:
            self.openDirInfo.setText('No .txt files found in the directory!')
        return
    

# Save directory button action
    def saveDirectory(self):
        self.saveDirInfo.setText('')
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self,'Select a Folder')
        self.saveDirLabel.setText(foo_dir)
        self.saveDir=foo_dir
        return
    

# Go button action
    def goFunctions(self):
    #Check if labeldir is valid or contains .txt files
    #Check if augmentation is selected or not
    #Check if savedir is valid
        self.checkBoxStatus()
        self.saveDirInfo.setText('')
        if self.goCheck():
            print('ready !')
# Add functions to execute the augmentations '''''''''''ToDO'''''''''''
            
            for augment in self.toDoAugList:
                # For each augment checklist make directories in the save directory
                augmentDir=self.makeSaveDirectory(augment)
                print(augmentDir)
                #For each augment pass all the files in the augment function
                for file in self.textfiles:
                    self.allAugmentFactory(file,augmentDir,augment)
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
        if self.openDir==None:
            self.saveDirInfo.setText('No label directory is selected!')
            return False
        if (len(self.textfiles)==0):
            self.saveDirInfo.setText('No .txt file in the directory to augment!')
            return False
        if (len(self.toDoAugList)==0):
            self.saveDirInfo.setText('No Augment to be done! Select augment from the checklist!')
            return False
        if self.saveDir==None:
            self.saveDirInfo.setText('No save directory is selected!')
            return False
        return True
    

# Make directories in the save directory for different augmentation
    def makeSaveDirectory(self,aug):
        augPath=self.saveDir+'/'+aug+'/'

        if not os.path.isdir(augPath):
            os.makedirs(augPath)
        return augPath
    
# Augment each text file according to the augmentation method
    def allAugmentFactory(self,labelPath,savePath,aug):
        with open(labelPath, 'rt') as fd:

            text_content=[]

            for line in fd.readlines():
        # Check each line in the .txt files for valid YOLO format ---------TO DO--------------------
                row = []
                splited = line.strip().split(' ')
        #Splitted float numbers of each YOLO line 
                x_center = float(splited[1])
                y_center = float(splited[2])
                box_width = float(splited[3])
                box_height = float(splited[4])

                if (aug==self.listAug[0]): #rotateC90
                    new_xcenter= float(1-y_center)
                    new_ycenter= float(x_center)
                    new_width= box_height
                    new_height= box_width

                elif (aug==self.listAug[1]):#rotateC180
                    new_xcenter= float(1-x_center)
                    new_ycenter= float(1-y_center)
                    new_width= box_width
                    new_height= box_height
            
                elif (aug==self.listAug[2]):#rotateC270
                    new_xcenter= float(y_center)
                    new_ycenter= float(1-x_center)
                    new_width= box_height
                    new_height= box_width

                elif (aug==self.listAug[3]):#flipOnY
                    new_xcenter= float(1-x_center)
                    new_ycenter= float(y_center)
                    new_width= box_width
                    new_height= box_height

                else:
                    print("Not valid augmentation parameter! Try with 'C90', 'C180', 'C270' or 'FlipY' ")
                    return


                row.append(int(splited[0]))
                row.append(new_xcenter)
                row.append(new_ycenter)
                row.append(new_width)
                row.append(new_height)

                text_content.append(row)

            np.savetxt(savePath+os.path.basename(labelPath)[:-4]+'_'+aug+'.txt',text_content,delimiter=' ',fmt='%d %f %f %f %f')

#       -------------------------TO DO---------------
            #Validate Yolo format
            #Execution Message show
            #Error Message dialog box
        


app= QApplication(sys.argv)

window= MyApp()
window.show()

app.exec()