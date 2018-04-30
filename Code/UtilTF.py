import numpy as np
import tensorflow as tf
import cv2

class Classifier:
    def __init__(self):
        self.__graph = self.__load_graph('../trained_model/retrained_graph.pb')
        self.__labels = self.__load_labels('../trained_model/retrained_labels.txt')
        #with tf.gfile.FastGFile('../trained_model/retrained_graph.pb') as f:
        #    graph_def = tf.GraphDef()
        #    graph_def.ParseFromString(f.read())
        #    _ = tf.import_graph_def(graph_def, name='')

    def __load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()
        
        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)
        
        return graph
    
    def __load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label
            
    def classify(self, np_img):
        o = 'unknown'
        
        #https://stackoverflow.com/questions/40273109/convert-python-opencv-mat-image-to-tensorflow-image-data
        img = cv2.resize(np_img, dsize=(299,299), interpolation = cv2.INTER_CUBIC)
        img = np.asarray(img)
        img_res = np.expand_dims(img, axis=0)
        
        input_operation = self.__graph.get_operation_by_name('import/Mul')
        output_operation = self.__graph.get_operation_by_name('import/final_result')
        
        with tf.Session(graph = self.__graph) as sess:
            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: img_res
            })
            
            results = np.squeeze(results)

            top_k = results.argsort()[-5:][::-1]
            print("Considering:")
            for i in top_k:
                print(self.__labels[i], results[i])
            
            i = top_k[0]
            o = self.__labels[i] + '(' + str(int(results[i]*100)) + '%)'
        
        return o
           
                #print('%s (score = %.5f' % (readable, score))