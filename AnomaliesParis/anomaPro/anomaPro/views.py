# -*- coding: utf-8 -*-
from django.shortcuts import render

import anomaPro.fileManager as FM

import pandas
import csv
import numpy
import json


import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy

import matplotlib
matplotlib.use('Agg')

import matplotlib
import matplotlib.pyplot as plt


import os

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

  
  return render(request, 'home.html' )

def main(request):
  
  return render(request, 'main.html')

def question(request, pk):
    
  # df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="unicode_escape")
  df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8-sig") # gestion caractères spéciaux


  # on retire les colonnes inutiles :
  df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
      'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
  # transformer noms de col en minuscules :
  df2.columns = df2.columns.str.lower()
  # remplacer espaces par _ :
  df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _


  df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
  json_records = df3.reset_index().to_json(orient ='records')



  print(df3)

  data = []
  data = json.loads(json_records)
  context = {'d': data}
  print(context)

  return render(request, 'question.html', context)



def oneParis(request):
  df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8-sig") # gestion caractères spéciaux


  # on retire les colonnes inutiles :
  df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
      'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
  # transformer noms de col en minuscules :
  df2.columns = df2.columns.str.lower()
  # remplacer espaces par _ :
  df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _

  fig, ax = plt.subplots()
  ax.pie(df2.loc[df2['arrondissement']==1,:].loc[df2['type_declaration']=='Voirie et espace public',:].groupby(['annee_declaration'])['type_declaration'].value_counts())
  
  e = './static/img/fourth.png'
  e2 ='/static/img/fourth.png'
  # fig = plt.figure()
  # plt.plot(df3)

  plt.title("second")
  plt.savefig(str(e))
  # plt.clf
  context = {'img': [e2]} #'graph'

  return render(request, 'oneParis.html', context)

def anomalie(request):
  return render(request, 'anomalie.html')