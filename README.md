# Jelly Bean Identifier

The issue of determining jelly bean flavours is an age old problem. Many flavors of jelly beans look too similar to distinguish them by human vision only. As a result of this, we wanted to create a jelly bean identifier that takes in only the sight of the jelly bean under (ideal) conditions and outputs the correct flavour.

#### Collecting Jelly Bean Training Data

In order to train the neural network we first needed to get training data jelly beans and flavors. This required manual sorting of a 2 lb. bag of Jelly Belly jelly beans. Now this opens the project up for human error, as we did not want to eat all of our training data to make sure it was the flavour we thought it was. 

The setup involved placing jelly beans in the custom 3D printed tray, and taking a high-quality picture of them with adequate lighting. The camera was used essentially as a live view webcam and was used in parallel with the **collector.py** script. This will be nearly impossible to recreate unless you edit the script for your needs. 

Upon collecting the data, you must put them in folders categorized by flavour, which a main directory containing all the subdirectories, for example:

* jelly_photos directory
  * tutti_frutti directory
    * img_1.jpg
    * img_2.jpg
  * dr_pepper directory
    * img_1.jpg
    * img_n.jpg

#### Retraining the model

In order to retrain the model you must have the following prerequisites:
+ Python >= 2.7
+ TensorFlow (pip install tensorflow)
+ Moderate amount of training data (> 100 preferred)

Now, assuming you have the **retrain.py** script in a directory called `<$DIR>` (placeholder) you call

```
# python retrain.py \
  --bottleneck_dir=<$DIR>/bottlenecks \
  --how_many_training_steps=2000 \
  --model_dir=<$DIR>/models/ \
  --output_graph=<$DIR>/retrained_graph.pb \
  --output_labels=<$DIR>/retrained_labels.txt \
  --architecture="inception_v3" \
  --image_dir=<$JELLY_PHOTOS_DIR>
```
  You can change how many training steps you want, default is 4,000.
  
  This will download the inception_v3 pretrained model, and then retrain the top layer on the image_dir provided.
  
  #### Classifying Images with New Model
  
  To classify an image with the **label_image.py** script or **label.sh** bash script you can call
  
  ` python label_image.py --graph=<$PATH_TO_GRAPH.pb> --image=<$PATH_TO_IMAGE.jpg>`
  
  or with **label_image.py** and **label.sh** in same directory
  
  `./label.sh <$PATH_TO_IMAGE.jpg>`