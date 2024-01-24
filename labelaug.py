import sys
import glob
from PyQt6.QtCore import QSize, Qt
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
    def saveDirectory(self):
        self.saveDirInfo.setText('')
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self,'Select a Folder')
        self.saveDirLabel.setText(foo_dir)
        self.saveDir=foo_dir
        return
    def goFunctions(self):
#Check if labeldir is valid or contains .txt files
#Check if augmentation is selected or not
#Check if savedir is valid
        self.checkBoxStatus()
        self.saveDirInfo.setText('')
        if self.goCheck():
            print('ready !')
# Add functions to execute the augmentations '''''''''''ToDO'''''''''''
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
            
            
         


    




        

        


app= QApplication(sys.argv)

window= MyApp()
window.show()

app.exec()