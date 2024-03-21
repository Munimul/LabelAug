# About labelaug

labelaug is a simple python GUI app that is written in python and uses QT for graphical interface. It allows user to easily augment images and their corresponding labels in YOLO format. It offers multiple basic augmentation techniques which are most commonly used for data augmentation. Users can also see the bounding boxes on their images as well as export the image as a .jpg file. It takes care of augmentation of multiple images and labels in a given directory without any sweat!

# Installation

Python 3.0 or above
Clone the repository

```bash

git clone https://github.com/Munimul/LabelAug.git

```

Change directory (cd) to the repository where it is cloned

```bash

cd LabelAug

```

Create a virtual Environment and acitvate it before installing dependencies(Optional)

Install Dependencies

```bash

pip install -r requirements.txt

```

Run the labelaug.py file

```bash

python labelaug.py

```

# Usage

Follow the steps above and run the labelaug.py file

1. Select the directory using 'Label Open Directory' button where your label or yolo.txt files are located
2. If the images are located in different folder, select that folder using 'Image Open Directory' button or select the same directory
3. Select a folder where you want to save the augmented images and labels
4. All the image can be displayed with their corresponding labels. Navigate by 'Next' and 'Previous' button
5. Current image displayed on the GUI can be saved as a .jpg file.
6. Select atleast one or multiple augmentation method
7. Push 'Go' button
8. For every augmentation, a subfolder will be created in your selected save directory. Images and label files will be located there.

# Constraints

LabelAug can only work with valid Yolo label format in the .txt file which is : class, x_center, y_center, width , height
The class should be an integer value and rest of the four in normalized(0-1) float value.

# Demo
![python_dvl2XoXF7A](https://github.com/Munimul/LabelAug/assets/77501611/e2c56382-2edb-4365-8065-31ada857a170)


### Picture sample

#### Sample user interface displaying all directory information and contained images and labels information

<img src="data/ui.jpg" width="416">

#### Separate folders for each agumentation

<img src="data/ui2.jpg" width="416">

### Output image example

#### Input image with labels

<img src="data/image1.jpg" width="416">

#### Output augmentation results.

<img src="data/image2.jpg" width="300"> <img src="data/image4.jpg" width="300">
<img src="data/image3.jpg" width="300"> <img src="data/image5.jpg" width="300">
