# -*- coding: utf-8 -*-
from re import I
from django.http import HttpResponse
from django.shortcuts import render

<<<<<<< HEAD
"""

=======
import anomaPro.fileManager as FM
>>>>>>> a27aea8c6d62dc236e8e33b3416cef21026154e1

import pandas
import csv
import numpy
# df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="unicode_escape")
df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8-sig") # gestion caractères spéciaux

# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
    'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)

# transformer noms de col en minuscules :
df2.columns = df2.columns.str.lower()

# remplacer espaces par _ dans les noms de colonnes :
df2.columns = df2.columns.str.replace(" ","_")
#############################################################################"

#reset index
df2 = df2.reset_index()

#rename column
df2= df2.rename(columns={"index":"New_ID"})

df2['New_ID'] = df2.index 
df3 = df2.iloc[:, 0:3:2]
trans = df3.T
dicos = trans.to_dict()
""" 
dicos = [{'New_ID': 0, 'arrondissement': 18},
{'New_ID': 1, 'arrondissement': 19},
{'New_ID': 2, 'arrondissement': 20}]





<<<<<<< HEAD

def home(request):

  context = {"dicos" : dicos}
  return render(request, 'home.html', context )
=======
# all the data
a = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()

# all type of anomalies
data2 = df2['type_declaration'].unique()

from django.http import HttpResponse
from django.shortcuts import render

def home(request):

  context = {"dico" : dico}
  # print("context : ", context)

  return render(request,'home.html',context)
>>>>>>> a27aea8c6d62dc236e8e33b3416cef21026154e1

def main(request):
  context = {"dicos" : dicos}
  return render(request, 'main.html', context )

def question(request, pk):
  
  
  dico = None
  for i in dicos:
    if i['New_ID'] == int(pk):
      dico = i
<<<<<<< HEAD
  
  #context = {"dico" : dico}
  return render(request, 'question.html', context)


=======
  context = {"dico" : dico}
  """
  a = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
  
  return render(request, 'main.html')
>>>>>>> a27aea8c6d62dc236e8e33b3416cef21026154e1

def oneParis(request):
  return render(request, 'oneParis.html')

def anomalie(request):
  return render(request, 'anomali.html')