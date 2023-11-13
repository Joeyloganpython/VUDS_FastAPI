from lib2to3.pgen2.pgen import DFAState
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pickle
from sksurv.ensemble import RandomSurvivalForest


class NN_by_pressure:
    def __init__(self, arr, ebc):
        #txtfile2 = txtfile.open("r")
        self.arr = arr
        self.ebc = ebc

        with open('api/rsf_model_25.pkl', 'rb') as model_file25:
            self.twentyfive_model = pickle.load(model_file25)
        with open('api/rsf_model_50.pkl', 'rb') as model_file_50:
            self.fifty_model = pickle.load(model_file_50)
        with open('api/rsf_model_75.pkl', 'rb') as model_file_75:
            self.model = pickle.load(model_file_75)

            

        self.feventtimes =np.array([  24.33333333,   35.33333333,   64.66666667,   77.33333333,
        86.        ,   93.66666667,  120.33333333,  138.33333333,
        150.66666667,  186.33333333,  208.66666667,  265.66666667,
        311.33333333,  317.        ,  341.        ,  346.        ,
        376.66666667,  474.33333333,  502.33333333,  557.        ,
        581.33333333,  677.33333333,  772.        ,  803.33333333,
        837.66666667,  905.33333333,  938.66666667,  968.        ,
        1007.33333333, 1044.66666667, 1115.33333333, 1165.66666667,
        1361.33333333, 1510.        , 1526.66666667, 1825.66666667])

    @staticmethod
    def _reshape_to_tensor(df1, mymodel):
        Xsurvarray = mymodel.predict_survival_function(df1, return_array=True)
        return Xsurvarray


    def make_predictions(self):
        df = self.arr
        df["percent"] = df["VH2O"] / self.ebc
        df["percent"] = df["percent"].round(2)
        df = df.loc[df["percent"] >= 0.01]  ### Normalizing
        df = df.loc[df["percent"] <= 1.0]
        df = df[["Pdet", "percent"]]


        df = df.groupby(["percent"])["Pdet"].mean().reset_index()
        del df["percent"]
        df1 = df.transpose().reset_index()  ## create array
        del df1["index"]
        dflen = df1.to_numpy()

        if dflen.shape[1] >= 73:
            df1 = df1.iloc[:, :73]
            pred = self._reshape_to_tensor(df1, self.model)

        elif dflen.shape[1] >= 48:
            df1 = df1.iloc[:, :48]
            pred = self._reshape_to_tensor(df1, self.fifty_model)

        elif dflen.shape[1] >= 23:
            df1 = df1.iloc[:, :23]
            pred = self._reshape_to_tensor(df1, self.twentyfive_model)

        else:  ### Error with file or less than 25% filled
            pred = "error"


        return (pred)