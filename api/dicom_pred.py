import numpy as np
import cv2
import pickle
import matplotlib.pyplot as plt
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.models import Model
from sksurv.ensemble import RandomSurvivalForest
import tensorflow as tf



class Dicom_pred:
    def __init__(self, dicom_file):
        arr =dicom_file.pixel_array/255
        self.dst = cv2.resize(arr, (224, 224))
        with open('api/rsf_images_model.pkl', 'rb') as model_file_75:
            self.model = pickle.load(model_file_75)
        #with open('api/dense_model.h5', 'rb') as pretraineddense:
        self.dense_model = tf.keras.models.load_model('api/dense_model.h5')

    @staticmethod
    def make_rgb(img):
        if len(img.shape) == 3:
            return img
        img3 = np.empty(img.shape + (3,))
        img3[:, :, :] = img[:, :, np.newaxis]
        return img3    
       
    def preprocess(self):
        dst = self.dst
        print(dst.shape)
        if dst.shape == (224, 224):
            img = self.make_rgb(dst)
            print(img.shape)
            okmessage = "Good_Image"
            densemodel = self.dense_model
            image_array = np.array(img)
            image_array_with_batch = np.expand_dims(image_array, axis=0)
            test_predictions = densemodel.predict(image_array_with_batch)
            rfr = self.model
            Xsurvarray = rfr.predict_survival_function(test_predictions, return_array=True)
            return (Xsurvarray)
        else:
            okmessage = "bad_Image"
