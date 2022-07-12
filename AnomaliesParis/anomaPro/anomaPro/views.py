# -*- coding: utf-8 -*-
from django.shortcuts import render
import anomaPro.fileManager as FM
import pandas
import csv
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy
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


# df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="unicode_escape")
df = pandas.read_csv(r"static/dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8") # gestion caractères spéciaux

# df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
#   'CONSEIL DE QUARTIER','DATE DECLARATION', 'MOIS DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)

# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
  'CONSEIL DE QUARTIER','DATE DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
# transformer noms de col en minuscules :
df2.columns = df2.columns.str.lower()
# remplacer espaces par _ :
df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _


#Liste des Types d'Anomalies pour crée les menu déroulants
list_anomalie= ['Objets abandonnés', 'Graffitis, tags, affiches et autocollants',
       'Autos, motos, vélos...', 'Mobiliers urbains', 'Propreté',
       'Éclairage / Électricité', 'Voirie et espace public',
       'Activités commerciales et professionnelles', 'Eau',
       'Arbres, végétaux et animaux']

list_months = {'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet','Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'}

        

def home(request):
  #Première page vue par le client
  #il a 3 choix : accéder à l'interface des Question 1 , 2 et 3
  return render(request, 'home.html' )

#Func question1 permet d'afficher une vue global des data et des graphs pour la 1ere question :
def question1(request):
  
  # Question 1 : Quelles sont les année pour lesquelles il y a + ou - d'anom par arrondissement

  ########################################################################
  #PIE GRAPH - commande pour crée le diag circulaire par année et par arr
  Q1_Niv0_Pie = "./static/img/Q1_Niv0_Pie.png"
  Q1_Niv0_Pie2 = "/static/img/Q1_Niv0_Pie.png"
  
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
  plt.savefig(Q1_Niv0_Pie)
  plt.close()

  ########################################################################
  #BAR GRAPH - commande pour crée l'histogramme par arr et type anomalies
  pandas.crosstab(df2['arrondissement'],df2['annee_declaration']).plot.bar()
  Q1_Niv0_Bar = './static/img/Q1_Niv0_Bar.png'
  Q1_Niv0_Bar2 ='/static/img/Q1_Niv0_Bar.png'
  plt.savefig(str(Q1_Niv0_Bar))
  plt.close()

  ########################################################################
  #DATA - commande pour générer la tableau de données (global)
  df3 = pandas.crosstab(df2['arrondissement'],df2['annee_declaration'])
  json_records = df3.to_json(orient ='index')
  #print("json record q1", json_records)
  #print("df3", df3)
  data = []
  data = json.loads(json_records)
  #print("data q1", data)
  context = {'img': [Q1_Niv0_Bar2, Q1_Niv0_Pie2], 'data': data} 

  return render(request, 'question1.html', context)


#Func question2 permet d'afficher une vue global des data et des graphs pour la 2e question :
def question2(request):

  #Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées,par type d’anomalie ?
  
  ########################################################################
  ##PIE GRAPH - Nombre d'anomalies par mois et par années
  Q2_Niv0_Pie = "./static/img/Q2_Niv0_Pie.png"
  Q2_Niv0_Pie2 = "/static/img/Q2_Niv0_Pie.png"
  fig, ax = plt.subplots()

  ax.pie(df2.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
        labels=df2['annee_declaration'].unique(),
        radius=1, wedgeprops=dict(width=1, edgecolor='w'),
        # colors = outer_colors,
        labeldistance = 0.5)
          # , explode=[0.3,0])
          # , autopct='%1.1f%%'

  ax.pie(df2.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].value_counts(),
        labels=df2.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].unique(),
        radius=1.5, wedgeprops=dict(width=0.5, edgecolor='w'),
        # colors = inner_colors,
        labeldistance = 0.9)
          # , autopct='%1.1f%%'

  ax.set(aspect="equal")
  plt.savefig(Q2_Niv0_Pie)
  plt.close()

  ########################################################################
  #BAR GRAPH - Nombre d'anomalies par mois et par années
  Q2_Niv0_Bar = "./static/img/Q2_Niv0_Bar.png"
  Q2_Niv0_Bar2 = "/static/img/Q2_Niv0_Bar.png"
  pandas.crosstab(df2['mois_declaration'],df2['annee_declaration']).plot.bar()
  plt.savefig(Q2_Niv0_Bar)
  plt.close()

  ########################################################################
  #DATA - Nombre d'anomalies par mois et par années
  df3 = pandas.crosstab(df2['mois_declaration'],df2['annee_declaration'])
  json_records = df3.to_json(orient ='index')
  data = []
  data = json.loads(json_records)
  context = {'img': [Q2_Niv0_Pie2, Q2_Niv0_Bar2], 'data': data}
  print("context in question 2 ", context)

  return render(request, 'question2.html', context)

def question3(request):
  ###Quel(s) arrondissement(s) comportent le plus / le moins d’anomalies signalées, par type d’anomalies ?
  
  ########################################################################
  ##PIE GRAPH - Nombre d'anomalies par arr et par type
 
 
  ####################################################################################
  #BAR GRAPH - Nombre d'anomalies par arr et par type
  Q3_Niv0_Bar = "./static/img/Q3_Niv0_Bar.png"
  Q3_Niv0_Bar2 = "/static/img/Q3_Niv0_Bar.png"
  pandas.crosstab(df2['arrondissement'],df2['annee_declaration']).plot.bar()
  plt.savefig(Q3_Niv0_Bar)
  plt.close()


  ####################################################################################
  #DATA - Nombre d'anomalies par arrondissement et par type d'anomalies
  df3 = pandas.crosstab(df2['arrondissement'],df2['type_declaration'])
  json_records = df3.to_json(orient ='index')
  print("df3", df3)
  data = []
  data = json.loads(json_records)
  print("js", json_records)
  context = {'img' : [Q3_Niv0_Bar2], 'data': data}

  return render(request, 'question3.html', context)

def Q1_ParAnnée(request, pk):

  #Get le type d'anomalie choisi afin d'afficher correctement le nveau de détail
  request_get = request.GET

  #Niveau 2 de détails pour la question 1
  #Affiche le nombre d'anomalie et les graphs par le type d'anomalie sélectionné dans le menu déroulant
  
  #Si le client selectionne un type dans le menu déroulant :
  if request_get:

    #on sélectionne dans le QueryDict 'Objets abandonnés'
    #<QueryDict: {'anomalie': ['Objets abandonnés']}>
    op = request_get["anomalie"].encode('utf8')

    #print de contrôle
    print("request ok", request_get)
    print("op", op)
    print("decode", str(op.decode()))

    ####################################################################################
    #PIE GRAPH - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].value_counts().plot.pie()
    Q1_Niv1_Pie = './static/img/Q1_Niv1{}_{}_Pie.png'.format(str(op.decode()),pk)
    Q1_Niv1_Pie2 ='/static/img/Q1_Niv1{}_{}_Pie.png'.format(str(op.decode()),pk)
    plt.savefig(str(Q1_Niv1_Pie))
    plt.close()

    ####################################################################################    
    #BAR GRAPH - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].value_counts().plot.bar()
    Q1_Niv1_Bar = './static/img/Q1_Niv1{}_{}_Bar.png'.format(str(op.decode()),pk)
    Q1_Niv1_Bar2 ='/static/img/Q1_Niv1{}_{}_Bar.png'.format(str(op.decode()),pk)
    plt.savefig(str(Q1_Niv1_Bar))
    plt.close()

    ####################################################################################
    #DATAFRAME - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df4 = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")
  
    print("df4", df4)
    json_records2 = df4.to_json(orient = 'records')
    print("js in try", json_records2)
    data_type = []
    data_type = json.loads(json_records2)
    print("data in try", data_type)
  
    #Dict à retourner si le client à selectionné le détails de niveau 2
    context = {'img_type' : [Q1_Niv1_Bar2, Q1_Niv1_Pie2], 'data_type': data_type , 'pk':pk, 'id':0} 


    #Niveau 1 de détails pour la question 1
    #Affiche le nombre d'anomalie par arr et par type d'ano sélectionné dans le menu déroulant
  else:

    def absolute_value(val):
      a  = numpy.round(val/100.*df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['annee_declaration'].count().sum(), 0)
      return a

    ####################################################################################
    #PIE CHART - Nb d'Anomalies par type dans l'arrondissement selectionné par le client  
    Q1_Niv2_Pie = "./static/img/Q1_Niv2{}_Pie.png".format(pk)
    Q1_Niv2_Pie2 = "/static/img/Q1_Niv2{}_Pie.png".format(pk)
    df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['annee_declaration'].count().plot.pie(autopct=absolute_value)
    plt.savefig(str(Q1_Niv2_Pie))
    plt.close()


    ####################################################################################
    #BAR CHART -  Nb d'Anomalies par type dans l'arrondissement selectionné par le client
    df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)
    #plt.legend(bbox_to_anchor =(-0.2, 1))    
    Q1_Niv2_Bar = './static/img/Q1_Niv2{}_Bar.png'.format(pk)
    Q1_Niv2_Bar2 ='/static/img/Q1_Niv2{}_Bar.png'.format(pk)
    plt.savefig(str(Q1_Niv2_Bar))
    plt.close()
    
    ####################################################################################
    ##DATAFRAME - Nb d'Anomalies par type dans l'arrondissement selectionné par le client  
    df3 = df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")
    print("df3:", df3)
    json_records = df3.reset_index().to_json(orient ='records')
    print("js", json_records)
    data = []
    data = json.loads(json_records)
    print("print test", data)

    #Dict à renvoyer 
    context = {'img' : [Q1_Niv2_Bar2, Q1_Niv2_Pie2], 'data': data,'pk':pk, 'id': 1} 
 
  
  print(context)
  return render(request, 'Q1_ParAnnée.html', {'context' : context, 'list_anomalie' : list_anomalie})


def Q2_ParMois(request, pk):

  #Get le type d'anomalie choisi afin d'afficher correctement le nveau de détail
  request_get = request.GET

  #Niveau 2 de détails pour la question 2
  #Affiche le nombre d'anomalie et les graphs par le type d'anomalie sélectionné dans le menu déroulant
  
  #Si le client selectionne un type dans le menu déroulant :
  if request_get:

    #on sélectionne dans le QueryDict 'Objets abandonnés'
    #<QueryDict: {'anomalie': ['Objets abandonnés']}>
    op = request_get["anomalie"].encode('utf8')

    #print de contrôle
    print("request ok", request_get)
    print("op", op)
    print("decode", str(op.decode()))

    #Définition de l'arrondissement et quelle type d'anomalie recherché 
    df3 = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode())]
    

    #PIE - 
    fig, ax = plt.subplots()

    ax.pie(df3.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
        labels=df2['annee_declaration'].unique(),
        radius=1, wedgeprops=dict(width=1, edgecolor='w'),
        # colors = outer_colors,
        labeldistance = 0.5)
        # , explode=[0.3,0])
        # , autopct='%1.1f%%'

    ax.pie(df3.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].value_counts(),
        labels=df2.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].unique(),
        radius=1.5, wedgeprops=dict(width=0.5, edgecolor='w'),
        # colors = inner_colors,
        labeldistance = 0.9)
        # , autopct='%1.1f%%'

    Q2_Niv2_Pie = './static/img/Q2_Niv2_{}_{}_Pie.png'.format(str(op.decode()), pk)
    Q2_Niv2_Pie2 = '/static/img/Q2_Niv2_{}_{}_Pie.png'.format(str(op.decode()), pk)
    plt.savefig(str(Q2_Niv2_Pie))
    plt.close()


    #HIST
    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration']).plot.bar()
    Q2_Niv2_Bar = './static/img/Q2_Niv2_{}_{}_Bar.png'.format(str(op.decode()),pk)
    Q2_Niv2_Bar2 ='/static/img/Q2_Niv2_{}_{}_Bar.png'.format(str(op.decode()), pk)
    plt.savefig(str(Q2_Niv2_Bar))
    plt.close()


    # data : 
    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration'])
    
    print("df4 type Q2", df4)
    json_records2 = df4.to_json(orient = 'index')
    print("json type q2 ", json_records2)
    data_type = []
    data_type = json.loads(json_records2)
    print("data in q2 try", data_type)

    context = {'img' : [Q2_Niv2_Bar2, Q2_Niv2_Pie2], 'data_type' : data_type, 'id' : 0, 'list_anomalie' : list_anomalie}

  else :

    #DATA
    df3 = df2.loc[df2['arrondissement']==pk,:]
    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration'])
    json_records = df4.reset_index().to_json(orient ='records')
    print("js", json_records)
    data = []
    data = json.loads(json_records)
    print("print test", data)

    # hist chart :
    pandas.crosstab(df3['mois_declaration'],df3['annee_declaration']).plot.bar()
    Q2_Niv1_Bar = './static/img/Q2_Niv1{}_Hist.png'.format(pk)
    Q2_Niv1_Bar2 ='/static/img/Q2_Niv1{}_Hist.png'.format(pk)
    plt.savefig(str(Q2_Niv1_Bar))
    plt.close()

    # pie chart :
    fig, ax = plt.subplots()

    ax.pie(df3.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
          labels=df2['annee_declaration'].unique(),
          radius=1, wedgeprops=dict(width=1, edgecolor='w'),
          # colors = outer_colors,
          labeldistance = 0.5)
            # , explode=[0.3,0])
            # , autopct='%1.1f%%'

    ax.pie(df3.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].value_counts(),
          labels=df2.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].unique(),
          radius=1.5, wedgeprops=dict(width=0.5, edgecolor='w'),
          # colors = inner_colors,
          labeldistance = 0.9)
            # , autopct='%1.1f%%'
      
    ax.set(aspect="equal", title='Anomalies par année et par mois')
    Q2_Niv1_Pie = './static/img/Q2_Niv1{}_Pie.png'.format(pk)
    Q2_Niv1_Pie2 ='/static/img/Q2_Niv1{}_Pie.png'.format(pk)
    plt.savefig(str(Q2_Niv1_Pie))
    plt.close()



    context = {'img' : [Q2_Niv1_Bar2, Q2_Niv1_Pie2], 'data' : data, 'id' : 1, 'list_anomalie' : list_anomalie}
  
  print("q2", context)
  return render(request, 'Q2_ParMois.html', context) 

def Q3_ParArr(request, arr):
  return render(request, 'Q3_ParArr.html')