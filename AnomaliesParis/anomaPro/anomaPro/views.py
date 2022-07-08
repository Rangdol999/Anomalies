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
df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8") # gestion caractères spéciaux


# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
  'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
# transformer noms de col en minuscules :
df2.columns = df2.columns.str.lower()
# remplacer espaces par _ :
df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _


#Retourne en string le fichier
list_anomalie= ['Objets abandonnés', 'Graffitis, tags, affiches et autocollants',
       'Autos, motos, vélos...', 'Mobiliers urbains', 'Propreté',
       'Éclairage / Électricité', 'Voirie et espace public',
       'Activités commerciales et professionnelles', 'Eau',
       'Arbres, végétaux et animaux']

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

<<<<<<< HEAD
  df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
  json_records = df3.reset_index().to_json(orient ='records')
  # print("df3", df3)
=======
  df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count().reset_index(name="count")
  json_records = df3.to_json(orient ='records')
  print("df3", df3)
>>>>>>> d95e3c007e36431f73b0a58ee0234dce76e7e299
  data = []
  data = json.loads(json_records)
  # print("js", json_records)
  context = {'img': [path_bar2, path_circ2], 'data': data} 

  return render(request, 'question1.html', context)

def question2(request):

   ##func question1 permet d'afficher la vue global des data pour la 2e question :
    #Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées,par type d’anomalie ?
  return render(request, 'question2.html')

def question3(request):
  ###func question1 permet d'afficher la vue global des data pour la 3e question :
  
  return render(request, 'question3.html')

def Q1_ParArrondissement(request, pk):

  request_get = request.GET

  if request_get:
    print("request ok", request_get)
    op = request_get["anomalie"].encode('utf8')
    print("op", op)
    print("decode", str(op.decode()))
    df4 = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==op.decode(),:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")
  
<<<<<<< HEAD
  df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)

  plt.legend(bbox_to_anchor =(-0.2, 1))    
  path_Q1_ParArrondissement = './static/img/Q1_Arr{}_Hist.png'.format(pk)
  path_Q1_ParArrondissement2 ='/static/img/Q1_Arr{}_Hist.png'.format(pk)
  plt.savefig(str(path_Q1_ParArrondissement))
  
=======
    print("df4", df4)
    json_records2 = df4.to_json(orient = 'records')
    print("js in try", json_records2)
    data_type = []
    data_type = json.loads(json_records2)
    print("data in try", data_type)
    context = {'data_type': data_type , 'id':0} 
>>>>>>> d95e3c007e36431f73b0a58ee0234dce76e7e299

  else:

<<<<<<< HEAD
  #commande pour générer la tableau de données (global par arrondissement) 
  
  
  # <!-- annee de declaration =  au nombre d'anomalies-->
  #<!-- index = annee de declaration // 0 = 2021 et 1 = 2022 --> 
  df3 = df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'], as_index=False)['annee_declaration'].count()
  print("df3 : ", df3)
  json_records = df3.reset_index().to_json(orient ='records')
  # print("js", json_records)
  data = []
  data = json.loads(json_records)
=======
    df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)
    plt.legend(bbox_to_anchor =(-0.2, 1))    
    path_Q1_ParArrondissement = './static/img/Q1_Arr{}_Hist.png'.format(pk)
    path_Q1_ParArrondissement2 ='/static/img/Q1_Arr{}_Hist.png'.format(pk)
    plt.savefig(str(path_Q1_ParArrondissement))
    
>>>>>>> d95e3c007e36431f73b0a58ee0234dce76e7e299

    #commande pour générer le camembert de données / arr 
    path_Q1_Pie = "./static/img/anomalies_par_arr{}_pie.png".format(pk)
    path_Q1_Pie2 = "/static/img/anomalies_par_arr{}_pie.png".format(pk)
    df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['annee_declaration'].value_counts().plot.pie()
    plt.savefig(str(path_Q1_Pie))

    #commande pour générer le tableau de données (global par arrondissement) 
    
    
    # <!-- annee de declaration =  au nombre d'anomalies-->
    #<!-- index = annee de declaration // 0 = 2021 et 1 = 2022 --> 
    df3 = df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")
    print("df3:", df3)
    json_records = df3.reset_index().to_json(orient ='records')
    print("js", json_records)
    data = []
    data = json.loads(json_records)
    print("print test", data)

    context = {'img' : [path_Q1_ParArrondissement2, path_Q1_Pie2], 'data': data, 'id': 1} 
 
  return render(request, 'Q1_ParArrondissement.html', {'context' : context, 'list_anomalie' : list_anomalie})





def Q1_ParType(request, type, pk):
  #commande pour générer le tableau de données (par type d'anomalie selon l'arrondissement choisi en amont) 
  df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']=='',:].groupby(['annee_declaration'])['type_declaration'].value_counts()
  print("request", request.GET)
  return render(request, 'Q1_ParType.html')



def anomalie(request, type_anomalie):
  return render(request, 'anomalie.html', {'type_anomali': type_anomalie})