import sys
import glob
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QCheckBox, QFileDialog, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('LabelAug')
        layout= QVBoxLayout()
        
#label open button with 
        labelOpen=QPushButton("Label Open Directory", clicked=self.openDirectory)
# All augment checkboxs (add more augmentations)       
        self.rotate=QCheckBox(text='rotate')
        self.flip=QCheckBox(text='flip')
# Two variables to save the directories
        self.openDir=None
        self.saveDir=None
# All textfiles locations
        self.textfiles=None

# labelbox to show the open directory path and file info
        self.openDir=QLabel()
        self.openDirInfo=QLabel()
# Label save directory button
        labelSave=QPushButton("Label Save Directory", clicked=self.saveDirectory)
# Textbox to show the save directory path
        self.saveDir=QLabel()
        self.saveDirInfo=QLabel()
# Execute button to augment labels for checked items
        goButton=QPushButton("Go!", clicked=self.goFunctions)

        
        layout.addWidget(labelOpen)
        layout.addWidget(self.openDir)
        layout.addWidget(self.openDirInfo)
        layout.addWidget(self.rotate),layout.addWidget(self.flip)
        
        layout.addWidget(labelSave)
        layout.addWidget(self.saveDir)
        layout.addWidget(self.saveDirInfo)
        layout.addWidget(goButton)

        self.setLayout(layout)
        self.setFixedSize(QSize(400, 300))
        




    def openDirectory(self):
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self,'Select a Folder')
        self.openDir.setText(foo_dir)
        self.openDir=foo_dir
        self.textfiles=glob.glob(self.openDir+'/*.txt')
        if((len(self.textfiles))>0):
            #  .txt files exist in the directory
            self.openDirInfo.setText(str(len(self.textfiles))+' .txt files found in the directory')
        else:
            self.openDirInfo.setText('No .txt files found in the directory!')
        return
    def saveDirectory(self):
        dialog = QFileDialog()
        foo_dir = dialog.getExistingDirectory(self,'Select a Folder')
        self.saveDir.setText(foo_dir)
        self.saveDir=foo_dir
        return
    def goFunctions(self):

        if self.rotate.isChecked():
            print('rotate is on')
        if self.flip.isChecked():
            print('flip is on')
    




        

        


app= QApplication(sys.argv)

window= MyApp()
window.show()

app.exec()