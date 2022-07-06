# -*- coding: utf-8 -*-
from django.shortcuts import render

import anomaPro.fileManager as FM

import pandas
import csv
import numpy as np
import json


import matplotlib.pyplot as plt
import numpy

import matplotlib
matplotlib.use('Agg')


import os
# df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="unicode_escape")
df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8-sig") # gestion caractères spéciaux


# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
  'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
# transformer noms de col en minuscules :
df2.columns = df2.columns.str.lower()
# remplacer espaces par _ :
df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _


#Retourne en string le fichier
class FilePath():
    def __init__(self, fichier):
        self.fichier = str(fichier)
    #
    def __str__(self):  
        absPath = os.path.abspath(__file__)
        pthDir1 = os.path.dirname(absPath)
        pthDir2 = os.path.dirname(pthDir1)
        fchPath = os.path.join(pthDir2,self.fichier)
        return(fchPath)
        

def home(request):
  #first page where client can choose which question he wants
  #he has 3 choices, each choice redirect him to question1, 2 or 3 respectively
  return render(request, 'home.html' )

def question1(request):
  
  #func question1 permet d'afficher la vue global des data pour la 1er question :
  # Quelles sont les année pour lesquelles il y a + ou - d'anom par arrondissement
  return render(request, 'main.html')

def question2(request):

   ##func question1 permet d'afficher la vue global des data pour la 2e question :
    #Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées,par type d’anomalie ?
  return render(request, 'main2.html')

def question3(request):
  ###func question1 permet d'afficher la vue global des data pour la 3e question :
  
  return render(request, 'main3.html')

def question(request, pk):
    
  df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
  json_records = df3.reset_index().to_json(orient ='records')



  print(df3)

  data = []
  data = json.loads(json_records)
  context = {'d': data}
  print(context)

  return render(request, 'question.html', context)



def oneParis(request):
  

  # commande pour crée l'histogramme par arr et type anomalies
  df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)
  path_bar = './static/img/anomalies_par_annee_et_arr.png'
  path_bar2 ='/static/img/anomalies_par_annee_et_arr.png'
  plt.savefig(str(path_bar))

  # commande pour crée le diag circulaire
  path_circ = "./static/img/anomalies_par_annee_et_arr_circ.png"
  path_circ2 = "/static/img/anomalies_par_annee_et_arr_circ.png"
  
  fig, ax = plt.subplots()
  cmap = plt.get_cmap("tab20c")
  outer_colors = cmap(np.arange(2)*4)
  inner_colors = plt.get_cmap('Greys')(np.array([i*3 for i in range(10,30)]))
  # inner_colors = cmap(np.array([i for i in range(1,21)]))

  ax.pie(df2.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
        labels=df2['annee_declaration'].unique(),
        radius=1, wedgeprops=dict(width=1, edgecolor='w'),
        colors = outer_colors,
        labeldistance = 0.5)
          # , explode=[0.3,0])
          # , autopct='%1.1f%%'

  ax.pie(df2.groupby(['annee_declaration','arrondissement'])['arrondissement'].value_counts(),
        labels=df2.groupby(['annee_declaration','arrondissement'])['arrondissement'].unique(),
        radius=1.5, wedgeprops=dict(width=0.5, edgecolor='w'),
        colors = inner_colors,
        labeldistance = 0.9)
          # , autopct='%1.1f%%'

  print("nombre d'anomalies par annee et par arrondissement")
  ax.set(aspect="equal")
  plt.savefig(path_circ)

  #commande pour générer la tableau de données (global)

  df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
  json_records = df3.reset_index().to_json(orient ='records')

  data = []
  data = json.loads(json_records)
  
  context = {'img': [path_bar2, path_circ2], 'data': data} 

  return render(request, 'oneParis.html', context)




def anomalie(request):
  return render(request, 'anomalie.html')