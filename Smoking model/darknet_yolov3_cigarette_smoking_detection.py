# -*- coding: utf-8 -*-
"""Darknet_YOLOv3_Cigarette_Smoking_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/hardik0/Deep-Learning-with-GoogleColab/blob/master/Darknet_YOLOv3_Cigarette_Smoking_Detection.ipynb

Cigarette Smoking detection using YOLOv3 darknet
--
"""

!apt update
!apt upgrade -y
!uname -m && cat /etc/*release
!gcc --version
!uname -r

ls

"""To access Google Drive Folder and Files"""

# Load the Drive helper and mount to 
from google.colab import drive

# This will prompt for authorization.
drive.mount('/content/drive')

# After executing the cell above, Drive
# files will be present in "/content/drive/My Drive".
!ls -a "/content/drive/My Drive/GColab/"

"""**Original Version of Darknet**"""

# Commented out IPython magic to ensure Python compatibility.
# %rm -r darknet
!git clone https://github.com/pjreddie/darknet
# %cd darknet/

"""**Modify Version of Darknet**"""

# Commented out IPython magic to ensure Python compatibility.
#%rm -r darknet
!git clone https://github.com/AlexeyAB/darknet/
# %cd darknet/

!apt install libopencv-dev python-opencv ffmpeg

"""Changing the variables to include OpenCV and GPU in the Makefile"""

# Commented out IPython magic to ensure Python compatibility.
!sed -i 's/OPENCV=0/OPENCV=1/g' Makefile
!sed -i 's/GPU=0/GPU=1/g' Makefile
#!sed -i 's/CUDNN=0/CUDNN=1/g' Makefile
# %pycat Makefile

!make

"""**How to train (to detect your custom objects):**
---

**Training Yolo v3:**

1.Create file yolo-obj.cfg with the same content as in yolov3.cfg (or copy yolov3.cfg to yolo-obj.cfg) and:

* change line batch to batch=64
* change line subdivisions to subdivisions=8
* change line classes=80 to your number of objects in each of 3 [yolo]-layers:
  * yolov3.cfg#L610
  * yolov3.cfg#L696
  * yolov3.cfg#L783
* change [filters=255] to filters=(classes + 5)x3 in the 3 [convolutional] before each [yolo] layer
  * yolov3.cfg#L603
  * yolov3.cfg#L689
  * yolov3.cfg#L776
  
So if classes=1 then should be filters=18. If classes=2 then write filters=21.
"""

# Commented out IPython magic to ensure Python compatibility.
# %cp cfg/yolov3.cfg cfg/yolo-obj.cfg
!sed -i 's/batch=1/batch=64/g' cfg/yolo-obj.cfg
!sed -i 's/subdivisions=1/subdivisions=32/g' cfg/yolo-obj.cfg
!sed -i 's/classes=80/classes=1/g' cfg/yolo-obj.cfg
!sed -i 's/filters=255/filters=18/g' cfg/yolo-obj.cfg
!sed -i 's/width=416/width=608/g' cfg/yolo-obj.cfg
!sed -i 's/height=416/height=608/g' cfg/yolo-obj.cfg

# Commented out IPython magic to ensure Python compatibility.
# %pycat cfg/yolo-obj.cfg

"""2.Create file obj.names in the directory `build\darknet\x64\data\` with objects names - each in new line


"""

# Commented out IPython magic to ensure Python compatibility.
all_classes = """Smoking
"""

file = """text_file = open("build/darknet/x64/data/obj.names", "w");text_file.write(all_classes);text_file.close()""" 

exec(file)
# %pycat build/darknet/x64/data/obj.names

"""3.Create file obj.data in the directory `build\darknet\x64\data\` containing (where classes = number of objects):"""

# Commented out IPython magic to ensure Python compatibility.
obj_data = """classes= 1
train  = build/darknet/x64/data/train.txt
valid  = build/darknet/x64/data/valid.txt
names = build/darknet/x64/data/obj.names
backup = build/darknet/x64/backup/
"""

file = """text_file = open("build/darknet/x64/data/obj.data", "w");text_file.write(obj_data);text_file.close()""" 

exec(file)
# %pycat build/darknet/x64/data/obj.data

"""4.Put image-files (.jpg) of your objects in the directory build/darknet/x64/data/obj/

"""

# Commented out IPython magic to ensure Python compatibility.
#%mkdir build/darknet/x64/data/obj
# %cp -r "/content/drive/My Drive/GColab/Smoking/." build/darknet/x64/data/obj/

# Commented out IPython magic to ensure Python compatibility.
# %ls -1 build/darknet/x64/data/obj/*.jpg | wc -l
# %ls -1 build/darknet/x64/data/obj/*.txt | wc -l

"""5.You should label each object on images from your dataset. Use this visual GUI-software for marking bounded boxes of objects and generating annotation files for Yolo v2 & v3: 

---
**LabelImg**
  
LabelImg is a graphical image annotation tool.: 
https://github.com/tzutalin/labelImg


---

**Yolo_mark**

Windows & Linux GUI for marking bounded boxes of objects in images for training Yolo v3 and v2

https://github.com/AlexeyAB/Yolo_mark

It will create `.txt`-file for each `.jpg`-image-file - in the same directory and with the same name, but with `.txt`-extension, and put to file: object number and object coordinates on this image, for each object in new line: `<object-class> <x> <y> <width> <height>`

Where:


*   `<object-class>` - integer object number from 0 to (classes-1)
*   `<x_center> <y_center> <width> <height>` - float values relative to width and height of image, it can be equal from (0.0 to 1.0]
*   for example: `<x> = <absolute_x> / <image_width>` or `<height> = <absolute_height> / <image_height>`
*   atention: `<x_center> <y_center>` - are center of rectangle (are not top-left corner)


For example for img1.jpg you will be created img1.txt containing:


```
1 0.716797 0.395833 0.216406 0.147222
0 0.687109 0.379167 0.255469 0.158333
1 0.420312 0.395833 0.140625 0.166667
```

6.Create file train.txt and valid.txt in directory `build\darknet\x64\data\` with filenames of your images, each filename in new line, with path relative to darknet, for example containing:
"""

import os, fnmatch
import numpy as np

train_file = open("build/darknet/x64/data/train.txt", "w")
valid_file = open("build/darknet/x64/data/valid.txt", "w")
listOfFiles = os.listdir('build/darknet/x64/data/obj/')  
pattern = "*.jpg"  
for f_name in listOfFiles:  
  if fnmatch.fnmatch(f_name, pattern):
    if np.random.rand(1) < 0.8:
      train_file.write("build/darknet/x64/data/obj/"+f_name+"\n")
      #print ("data/obj/"+f_name)
    else:
      valid_file.write("build/darknet/x64/data/obj/"+f_name+"\n")  
      
train_file.close()
valid_file.close()

#Count number of files 
!wc -l build/darknet/x64/data/train.txt
!wc -l build/darknet/x64/data/valid.txt

# Commented out IPython magic to ensure Python compatibility.
# %pycat build/darknet/x64/data/valid.txt

"""7.Download pre-trained weights for the convolutional layers (154 MB): https://pjreddie.com/media/files/darknet53.conv.74 and put to the directory `build\darknet\x64`"""

!wget -P build/darknet/x64/ https://pjreddie.com/media/files/darknet53.conv.74
#%ls build/darknet/x64/

"""8.training by using the command line:


```
./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/darknet53.conv.74 -dont_show
```

8.1. For training with mAP (mean average precisions) calculation for each 4 Epochs (set valid=valid.txt or train.txt in obj.data file) and run: 



```
./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/darknet53.conv.74 -dont_show -map
```


"""

!./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/darknet53.conv.74 -dont_show

"""9.After training is complete - get result yolo-obj_final.weights from path `build\darknet\x64\backup\`


*   After each 100 iterations you can stop and later start training from this point. For example, after 2000 iterations you can stop training, and later just copy yolo-obj_2000.weights from `build\darknet\x64\backup\` to` build\darknet\x64\ `and start training using: 


```
./darknet detector train data/obj.data yolo-obj.cfg yolo-obj_2000.weights
```




"""

!./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/yolo-obj_1000.weights -dont_show

"""Custom object detection:
---
Example of Cigarette Smoking detection:

**Image : **

```
./darknet detector test build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/smoking_1000it.weights -thresh 0.20 data/cigarette.jpg
```


**Video : **

```
./darknet detector demo build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/smoking_1000it.weights -thresh 0.20 -dont_show Smoking.mp4 -out_filename Smoking_output.mp4
```


"""

!./darknet detector demo build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/smoking_800it_1avgLoss.weights -thresh 0.20 -dont_show Smoking.mp4 -out_filename Smoking_20%.mp4

ls -lh *.mp4

"""**Playing videos on google colab**"""

import io
import base64
from IPython.display import HTML
video = io.open('Smoking_20%.mp4', 'r+b').read()
encoded = base64.b64encode(video)
HTML(data='''<video alt="test" controls><source src="data:video/mp4;base64,{0}" type="video/mp4" /></video>'''.format(encoded.decode('ascii')))

"""Extra Tutorial
---

Copying data from google colab to google drive
"""

# Commented out IPython magic to ensure Python compatibility.
# %cp -r build/darknet/x64/yolo-obj_1500up_05avgLoss.weights "/content/drive/My Drive/GColab/"
# %cp -r Smoking_20%.mp4 "/content/drive/My Drive/GColab/"

"""Downloading the data from the colab"""

from google.colab import files
files.download('build/darknet/x64/yolo-obj_1500up_05avgLoss.weights')

"""Copying data from google drive to google colab"""

# Commented out IPython magic to ensure Python compatibility.
# %cp -r "/content/drive/My Drive/GColab/yolo-obj_1500up_05avgLoss.weights" build/darknet/x64/
# %cp -r "/content/drive/My Drive/GColab/SmokingDEMO.mp4" .

"""Youtube Link: 
---
https://youtu.be/vEnQIptZzyI
"""
