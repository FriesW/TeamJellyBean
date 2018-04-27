#!/bin/bash

IMAGE=$1

python label_image.py --labels=retrained_labels.txt --graph=retrained_graph.pb --image=${IMAGE};
