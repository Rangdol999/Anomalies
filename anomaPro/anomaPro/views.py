# -*- coding: utf-8 -*-
from re import I
from django.http import HttpResponse
from django.shortcuts import render


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
dico = trans.to_dict()

from django.http import HttpResponse
from django.shortcuts import render

def home(request):

  context = {"dico" : dico}
  return render(request,
      'home.html', context)

def main(request, pk):

  """
  for i in dico:
    if i['New_ID'] == int(pk):
      dico = i
  context = {"dico" : dico}
  """

  return render(request, 'main.html')

