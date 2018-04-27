#!/bin/bash

#Call the program like `./label.sh <PATH_TO_IMAGE>

#Overall on a random sample 83% correct rate.

IMAGE=$1
python label_image.py --labels=retrained_labels.txt --graph=retrained_graph.pb --image=${IMAGE};
