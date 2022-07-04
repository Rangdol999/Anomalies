# -*- coding: utf-8 -*-
import pandas
import csv
import numpy
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



# %matplotlib inline

# print(pandas.__version__)

# df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="unicode_escape")
df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8-sig") # gestion caractères spéciaux


# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
    'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)

# transformer noms de col en minuscules : 
df2.columns = df2.columns.str.lower()

# remplacer espaces par _ dans les noms de colonnes :
df2.columns = df2.columns.str.replace(" ","_") 


data = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()

# print(df2.head())
# print(df2.shape)
# print(df2.columns.values)

