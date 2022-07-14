# -*- coding: utf-8 -*-
from django.shortcuts import render
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


###################################################################################################################################################################
################################ Filtrage de la DATABASE ##########################################################################################################*

# lecture du CSV et gestion des caractères spéciaux
df = pandas.read_csv(r"dans-ma-rue.csv", sep=';',header = 0,encoding="utf-8") 
# on retire les colonnes inutiles :
df2 = df.drop(['ID DECLARATION','SOUS TYPE DECLARATION','ADRESSE','CODE POSTAL', 'VILLE',
  'CONSEIL DE QUARTIER','DATE DECLARATION','OUTIL SOURCE','INTERVENANT','ID_DMR','geo_shape'], axis=1)
# transformer noms de col en minuscules :
df2.columns = df2.columns.str.lower()
# remplacer espaces par _ :
df2.columns = df2.columns.str.replace(" ","_") # remplacer espaces dans les noms de colonnes par _
df2['type_declaration'] = df2['type_declaration'].replace(['Éclairage / Électricité'],'Éclairage, Électricité')

#Liste des Types d'Anomalies pour crée les menu déroulants
list_anomalie= ['Objets abandonnés', 'Graffitis, tags, affiches et autocollants',
       'Autos, motos, vélos...', 'Mobiliers urbains', 'Propreté',
       'Éclairage, Électricité', 'Voirie et espace public',
       'Activités commerciales et professionnelles', 'Eau',
       'Arbres, végétaux et animaux']

list_months = {'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 
        'Juillet','Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'}


def home(request):
  #Première page vue par le client
  #il a 3 choix : accéder à l'interface des Question 1 , 2 et 3
  return render(request, 'home.html' )

#Question 1 : Quelles sont les année pour lesquelles il y a + ou - d'anom par arrondissement

def question1(request):
#affichage d'une vue global des data et des graphs pour la 1ere question :
  

  ########################################################################
  #PIE GRAPH - commande pour crée le diag circulaire par année et par arr
  Q1_Niv0_Pie = "./static/img/Q1_Niv0_Pie.png"
  Q1_Niv0_Pie2 = "/static/img/Q1_Niv0_Pie.png"
  
  # croiser par arrondissement et année :
  # résultat : 1 df dont l'index correspond aux arrondissements, avec 1 colonne par année
  df_q1 = pandas.crosstab(df2['arrondissement'],df2['annee_declaration'])

  # préparer données pour graph : 
  years=[]
  years_values=[]
  arrondissements = []
  arrondissements_values = []
  arrondissements_max = [] #liste de booléen : true pour la valeur max, false pour les autres
  explode = []
  explode_factor=0.2

  for column in df_q1.columns:
      # 1. années et valeurs totales par année
      years_values.append(df_q1[column].sum())
      years.append(column)
      
      # 2. arrondissements et valeurs par arrondissement 
      
      for index, row in df_q1.iterrows():
          arrondissements.append(index)
          arrondissements_values.append(row[column])
          arrondissements_max.append(1 if (row[column] == np.max(df_q1[column])) else 0)

  # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
  explode = [explode_factor * i for i in arrondissements_max]

  # Definir les couleurs avec la map tab20 : 
  # couleur principale (indexes pairs) pour les annees
  # couleurs secondaires (indexes impairs ) pour les arrondissements correspondants.

  cmap = plt.get_cmap("tab20c")
  inner_colors = cmap(np.arange(10)*4)
  outer_colors = cmap(np.array([1 + 4 * j for j in range(0,len(years)) for i in range(0,20)]))

  fig1, ax1 = plt.subplots()
  ax1.pie(arrondissements_values
      ,colors = outer_colors
      ,explode= explode
      ,labels = arrondissements
      ,labeldistance = 0.9
      ,radius = 1.5
      ,wedgeprops=dict(width=0.8, edgecolor='w')
      )
  ax1.pie(years_values
      ,textprops={'fontsize': 14}
      ,labeldistance = 0.5
      ,colors = inner_colors
      ,labels = years
      ,radius = 1)

  ax1.axis()

  ax1.set(aspect="equal")
  plt.savefig(Q1_Niv0_Pie,bbox_inches="tight")
  plt.close()

  ########################################################################
  #BAR GRAPH - commande pour crée l'histogramme par arr et type anomalies
  pandas.crosstab(df2['arrondissement'],df2['annee_declaration']).plot.bar(title="Anomalies par arrondissement, par année.")
  Q1_Niv0_Bar = './static/img/Q1_Niv0_Bar.png'
  Q1_Niv0_Bar2 ='/static/img/Q1_Niv0_Bar.png'
  plt.savefig(str(Q1_Niv0_Bar),bbox_inches="tight")
  plt.close()

  ########################################################################
  #DATA - commande pour générer la tableau de données (global)
  df3 = pandas.crosstab(df2['arrondissement'],df2['annee_declaration'])
  print("df3", df3)
  max = df3.to_numpy().max()
  min = df3.to_numpy().min()
  json_records = df3.to_json(orient ='index')
  data = []
  data = json.loads(json_records)
  print("max et min", max, min)
  context = {'img': [Q1_Niv0_Bar2, Q1_Niv0_Pie2], 'data': data, 'max' : max, 'min' : min} 

  return render(request, 'question1.html', context)


#Quels sont les mois pour lesquels il y a le plus / le moins d’anomalie signalées,par type d’anomalie ?
def question2(request):

  #Affichage d'une vue global des data et des graphs pour la 2e question :

  
  ########################################################################
  ##PIE GRAPH - Nombre d'anomalies par mois et par années
  Q2_Niv0_Pie = "./static/img/Q2_Niv0_Pie.png"
  Q2_Niv0_Pie2 = "/static/img/Q2_Niv0_Pie.png"
  
  # croiser par arrondissement et année :
  # résultat : 1 df dont l'index correspond aux arrondissements, avec 1 colonne par année
  df_q2 = pandas.crosstab(df2['mois_declaration'],df2['annee_declaration'])

  # préparer données pour graph : 
  years=[]
  years_values=[]
  mois = []
  mois_values = []
  mois_max = [] #liste de booléen : true pour la valeur max, false pour les autres
  explode = []
  explode_factor=0.2

  for column in df_q2.columns:
      # 1. années et valeurs totales par année
      years_values.append(df_q2[column].sum())
      years.append(column)
      
      # 2. arrondissements et valeurs par arrondissement 
      
      for index, row in df_q2.iterrows():
          mois.append(index)
          mois_values.append(row[column])
          mois_max.append(1 if (row[column] == np.max(df_q2[column])) else 0)

  # replace months with 0 data with empty str "" and other months with complete months name in labels list
  mois_dict = {1:"janvier",2:"fevrier",3:"mars",4:"avril",5:"mai",6:"juin",7:"juillet",8:"août",9:"septembre",10:"octobre",11:"novembre",12:"décembre"}
  mois = [mois_dict[mois] if (mois_values[i]!=0) else "" for i,mois in enumerate(mois) ]


  # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
  explode = [explode_factor * i for i in mois_max]

  # Definir les couleurs avec la map tab20 : 
  # couleur principale (indexes pairs) pour les annees
  # couleurs secondaires (indexes impairs ) pour les arrondissements correspondants.

  cmap = plt.get_cmap("tab20c")
  inner_colors = cmap(np.arange(10)*4)
  outer_colors = cmap(np.array([1 + 4 * j for j in range(0,len(years)) for i in range(0,12)]))

  fig1, ax1 = plt.subplots()
  ax1.pie(mois_values
      ,colors = outer_colors
      ,explode= explode
      ,labels = mois
      ,rotatelabels = True
      ,labeldistance = 0.7
      ,radius = 1.5
      ,wedgeprops=dict(width=0.8, edgecolor='w')
      )
  ax1.pie(years_values
      ,textprops={'fontsize': 14}
      ,labeldistance = 0.5
      ,colors = inner_colors
      ,labels = years
      ,radius = 1)

  ax1.axis()
  ax1.set(aspect="equal")
  plt.savefig(Q2_Niv0_Pie,bbox_inches="tight")
  plt.close()

  ########################################################################
  #BAR GRAPH - Nombre d'anomalies par mois et par années
  Q2_Niv0_Bar = "./static/img/Q2_Niv0_Bar.png"
  Q2_Niv0_Bar2 = "/static/img/Q2_Niv0_Bar.png"
  pandas.crosstab(df2['mois_declaration'],df2['annee_declaration']).plot.bar()
  plt.savefig(Q2_Niv0_Bar,bbox_inches="tight")
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


###Quel(s) arrondissement(s) comportent le plus / le moins d’anomalies signalées, par type d’anomalies ?
def question3(request):

  request_get = request.GET
  if request_get:
    #Niveau 2 de détails pour la question 2
    #Affichage du nombre d'anomalie et les graphs par type d'anomalie sélectionné dans le menu déroulant

    #on sélectionne dans le QueryDict 'Objets abandonnés'
    #exemple : <QueryDict: {'anomalie': ['Objets abandonnés']}>
    op = request_get["anomalie"].encode('utf8')

    print("op", str(op.decode()))

    df3 = df2.loc[df2['type_declaration']==str(op.decode())]
    
    ########################################################################
    ## PIE - Nombre d'anomalies par type d'anomalie pour tout les arrondissement
    Q3_Niv1_Pie = "./static/img/Q3_Niv1_Pie.png"
    Q3_Niv1_Pie2 = "/static/img/Q3_Niv1_Pie.png"
  
    df_q3_1 = pandas.crosstab(df3['type_declaration'],df3['annee_declaration'])

    # manage data to plot and explode parameter :
    years = []
    years_values = []
    type_declaration = []
    type_decalaration_values = []
    type_declaration_max = []
    explode_factor=0.1

    for column in df_q3_1.columns:
        years_values.append(df_q3_1[column].sum())
        years.append(column)
        for index, row in df_q3_1.iterrows():
            type_declaration.append(index)
            type_decalaration_values.append(row[column])
            type_declaration_max.append(1 if (row[column] == np.max(df_q3_1[column])) else 0)

    # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
    explode = [explode_factor * i for i in type_declaration_max]

    # Definir les couleurs 
    # couleurs annee_declaration :
    cmap = plt.get_cmap("tab20c")
    inner_colors = cmap(np.arange(10)*4)

    # couleurs type_declaration : 
    categories = df3['type_declaration'].unique()
    n = len(categories)
    cmap = plt.get_cmap('twilight')
    # cmap = plt.get_cmap('winter')
    outer_colors = [cmap(i/n) for i in range(0,n)]

    # graph :
    fig1, ax1 = plt.subplots()
    pie  = ax1.pie(type_decalaration_values
        ,colors = outer_colors
        # raccourcir les etiquettes aux premiers caractères uniquement, afficher seulement pour les max
        ,labels = [(f"{label[:7]}..." if type_declaration_max[i] else "") for i , label in enumerate(type_declaration)]
        ,rotatelabels =True
        ,explode= explode
        ,labeldistance = 0.6
        ,radius = 1.5
        ,wedgeprops=dict(width=0.8, edgecolor='w')
        )
    ax1.pie(years_values
        ,textprops={'fontsize': 14}
        ,labeldistance = 0.5
        ,colors = inner_colors
        ,labels = years
        ,wedgeprops=dict(width=1, edgecolor='w')
        ,radius = 1)

    ax1.legend(pie[0],categories, bbox_to_anchor=(1.45,0.5), loc="center right", fontsize=10, 
              bbox_transform=plt.gcf().transFigure)
    
    # ax1.set(aspect="equal")
    plt.savefig(Q3_Niv1_Pie, bbox_inches="tight")
    plt.close()

    ########################################################################
    ## HIST - Nombre d'anomalies par type d'anomalie pour tout les arrondissement
    pandas.crosstab(df3['arrondissement'],df3['type_declaration']).plot.bar()
    Q3_Niv1_Bar = "./static/img/Q3_Niv1_Bar.png"
    Q3_Niv1_Bar2 = "/static/img/Q3_Niv1_Bar.png"
    plt.savefig(Q3_Niv1_Bar,bbox_inches="tight")
    plt.close()

    ########################################################################
    ### DATA - Nombre d'anomalies par type d'anomalie pour tout les arrondissement
    df4 = pandas.crosstab(df3['arrondissement'],df3['annee_declaration'])
    json_records = df4.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    context = {'img' : [Q3_Niv1_Bar2, Q3_Niv1_Pie2], 'data' : data, 'list_anomalie' : list_anomalie, 'id' : 0}

    return render(request, 'question3.html', context)


  ##Niveau 0 de détails pour la question 3
  else:

    ########################################################################
    ## PIE GRAPH - Nombre d'anomalies pour tout les arr et pour tout les types
    Q3_Niv0_Pie = "./static/img/Q3_Niv0_Pie.png"
    Q3_Niv0_Pie2 = "/static/img/Q3_Niv0_Pie.png"
    
    df_q3 = pandas.crosstab(df2['type_declaration'],df2['annee_declaration'])

    # manage data to plot and explode parameter :
    years = []
    years_values = []
    type_declaration = []
    type_decalaration_values = []
    type_declaration_max = []
    explode_factor=0.1

    for column in df_q3.columns:
        years_values.append(df_q3[column].sum())
        years.append(column)
        for index, row in df_q3.iterrows():
            type_declaration.append(index)
            type_decalaration_values.append(row[column])
            type_declaration_max.append(1 if (row[column] == np.max(df_q3[column])) else 0)

    # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
    explode = [explode_factor * i for i in type_declaration_max]

    # Definir les couleurs 
    # couleurs annee_declaration :
    cmap = plt.get_cmap("tab20c")
    inner_colors = cmap(np.arange(10)*4)

    # couleurs type_declaration : 
    categories = df2['type_declaration'].unique()
    n = len(categories)
    cmap = plt.get_cmap('twilight')
    # cmap = plt.get_cmap('winter')
    outer_colors = [cmap(i/n) for i in range(0,n)]

    # graph :
    fig1, ax1 = plt.subplots()
    pie  = ax1.pie(type_decalaration_values
        ,colors = outer_colors
        # raccourcir les etiquettes aux premiers caractères uniquement, afficher seulement pour les max
        ,labels = [(f"{label[:7]}..." if type_declaration_max[i] else "") for i , label in enumerate(type_declaration)]
        ,rotatelabels =True
        ,explode= explode
        ,labeldistance = 0.6
        ,radius = 1.5
        ,wedgeprops=dict(width=0.8, edgecolor='w')
        )
    ax1.pie(years_values
        ,textprops={'fontsize': 14}
        ,labeldistance = 0.5
        ,colors = inner_colors
        ,labels = years
        ,wedgeprops=dict(width=1, edgecolor='w')
        ,radius = 1)

    ax1.legend(pie[0],categories, bbox_to_anchor=(1.45,0.5), loc="center right", fontsize=10, 
              bbox_transform=plt.gcf().transFigure)

    plt.savefig(Q3_Niv0_Pie, bbox_inches="tight")
    plt.close()
  

    ####################################################################################
    #BAR GRAPH - Nombre d'anomalies pour tout les arr et pour tout les types
    Q3_Niv0_Bar = "./static/img/Q3_Niv0_Bar.png"
    Q3_Niv0_Bar2 = "/static/img/Q3_Niv0_Bar.png"
    pandas.crosstab(df2['arrondissement'],df2['annee_declaration']).plot.bar()
    plt.savefig(Q3_Niv0_Bar,bbox_inches="tight")
    plt.close()


    ####################################################################################
    #DATA - Nombre d'anomalies pour tout les arr et pour tout les types
    df3 = pandas.crosstab(df2['arrondissement'],df2['type_declaration'])
    json_records = df3.to_json(orient ='index')
    data = []
    data = json.loads(json_records)
    context = {'img' : [Q3_Niv0_Bar2, Q3_Niv0_Pie2], 'data': data, 'list_anomalie' : list_anomalie, 'id' : 1}

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


    ####################################################################################
    #PIE GRAPH - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].value_counts().plot.pie()
    Q1_Niv2_Pie = './static/img/Q1_Niv2_{}_{}_Pie.png'.format(str(op.decode()),pk)
    Q1_Niv2_Pie2 ='/static/img/Q1_Niv2_{}_{}_Pie.png'.format(str(op.decode()),pk)
    plt.savefig(str(Q1_Niv2_Pie),bbox_inches="tight")
    plt.close()

    ####################################################################################    
    #BAR GRAPH - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].value_counts().plot.bar()
    Q1_Niv2_Bar = './static/img/Q1_Niv2_{}_{}_Bar.png'.format(str(op.decode()),pk)
    Q1_Niv2_Bar2 ='/static/img/Q1_Niv2_{}_{}_Bar.png'.format(str(op.decode()),pk)
    plt.savefig(str(Q1_Niv2_Bar),bbox_inches="tight")
    plt.close()

    ####################################################################################
    #DATAFRAME - Nb d'Anomalies sur l'arrondissement et par type selectionné par le client 
    df4 = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")

    json_records2 = df4.to_json(orient = 'records')
    data_type = []
    data_type = json.loads(json_records2)
  
    ####################################################################################
    # Data for mapping
    # data_to_map = df
    data_to_map = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode()),:]['geo_point_2d']
    data_to_map = data_to_map.to_json()
    data_to_map = json.loads(data_to_map)
    #Dict à retourner si le client à selectionné le détails de niveau 2
    context = {'img_type' : [Q1_Niv2_Bar2, Q1_Niv2_Pie2], 'data_type': data_type , 'pk':pk, 'id':0, 'data_to_map':data_to_map} 


  else:

    #Niveau 1 de détails pour la question 1
    #Affiche le nombre d'anomalie par arr et par type d'ano sélectionné dans le menu déroulant

    def absolute_value(val):
      a  = numpy.round(val/100.*df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['annee_declaration'].count().sum(), 0)

    ####################################################################################
    #PIE CHART - Nb d'Anomalies par type dans l'arrondissement selectionné par le client  
    Q1_Niv1_Pie = "./static/img/Q1_Niv1_{}_Pie.png".format(pk)
    Q1_Niv1_Pie2 = "/static/img/Q1_Niv1_{}_Pie.png".format(pk)
    
    df_q1_1 = df2.loc[df2['arrondissement']==pk,:]
    df_q1_1 = pandas.crosstab(df_q1_1['type_declaration'],df_q1_1['annee_declaration'])

    # manage data to plot and explode parameter :
    years = []
    years_values = []
    type_declaration = []
    type_decalaration_values = []
    type_declaration_max = []
    explode_factor=0.1

    for column in df_q1_1.columns:
        years_values.append(df_q1_1[column].sum())
        years.append(column)
        for index, row in df_q1_1.iterrows():
            type_declaration.append(index)
            type_decalaration_values.append(row[column])
            type_declaration_max.append(1 if (row[column] == np.max(df_q1_1[column])) else 0)

    # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
    explode = [explode_factor * i for i in type_declaration_max]

    # Definir les couleurs 
    # couleurs annee_declaration :
    cmap = plt.get_cmap("tab20c")
    inner_colors = cmap(np.arange(10)*4)

    # couleurs type_declaration : 
    categories = df2['type_declaration'].unique()
    n = len(categories)
    cmap = plt.get_cmap('twilight')
    # cmap = plt.get_cmap('winter')
    outer_colors = [cmap(i/n) for i in range(0,n)]

    # graph :
    fig1, ax1 = plt.subplots()
    pie  = ax1.pie(type_decalaration_values
        ,colors = outer_colors
        # raccourcir les etiquettes aux premiers caractères uniquement, afficher seulement pour les max
        ,labels = [(f"{label[:7]}..." if type_declaration_max[i] else "") for i , label in enumerate(type_declaration)]
        ,rotatelabels =True
        ,explode= explode
        ,labeldistance = 0.6
        ,radius = 1.5
        ,wedgeprops=dict(width=0.8, edgecolor='w')
        )
    ax1.pie(years_values
        ,textprops={'fontsize': 14}
        ,labeldistance = 0.5
        ,colors = inner_colors
        ,labels = years
        ,wedgeprops=dict(width=1, edgecolor='w')
        ,radius = 1)

    ax1.legend(pie[0],categories, bbox_to_anchor=(1.45,0.5), loc="center right", fontsize=10, 
              bbox_transform=plt.gcf().transFigure)


    ax1.axis()  
    plt.savefig(str(Q1_Niv1_Pie),bbox_inches='tight')
    plt.close()


    ####################################################################################
    #BAR CHART -  Nb d'Anomalies par type dans l'arrondissement selectionné par le client
    # Definir les couleurs 
    # couleurs type_declaration : 
    categories = df2['type_declaration'].unique()
    n = len(categories)
    cmap = plt.get_cmap('twilight')
    # cmap = plt.get_cmap('winter')
    outer_colors = [cmap(i/n) for i in range(0,n)]

    ax = df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(
        stacked=True
        ,color = outer_colors)

    ax.legend(pie[0],categories, bbox_to_anchor=(1.45,0.5), loc="center right", fontsize=10, 
           bbox_transform=plt.gcf().transFigure)    

    Q1_Niv1_Bar = './static/img/Q1_Niv1_{}_Bar.png'.format(pk)
    Q1_Niv1_Bar2 ='/static/img/Q1_Niv1_{}_Bar.png'.format(pk)
    plt.savefig(str(Q1_Niv1_Bar),bbox_inches='tight')
    plt.close()
    
    ####################################################################################
    ##DATAFRAME - Nb d'Anomalies par type dans l'arrondissement selectionné par le client  
    df3 = df2.loc[df2['arrondissement']==pk,:].groupby(['annee_declaration'])['type_declaration'].count().reset_index(name="count")
    json_records = df3.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    #Dict à renvoyer 
    context = {'img' : [Q1_Niv1_Bar2, Q1_Niv1_Pie2], 'data': data,'pk':pk, 'id': 1} 
 
  
  return render(request, 'Q1_ParAnnée.html', {'context' : context, 'list_anomalie' : list_anomalie})


def Q2_ParMois(request, pk):

  #Get le type d'anomalie choisi afin d'afficher correctement le nveau de détail
  request_get = request.GET


  #Niveau 2 de détails pour la question 2
  #Affiche le nombre d'anomalie et les graphs par mois et pour le type d'anomalie sélectionné dans le menu déroulant
  
  #Définition de l'arrondissement et quelle type d'anomalie recherché 
  
  #Si le client selectionne un type dans le menu déroulant :
  if request_get:
    op = request_get["anomalie"].encode('utf8')
    df3 = df2.loc[df2['arrondissement']==pk,:].loc[df2['type_declaration']==str(op.decode())]

    #on sélectionne dans le QueryDict 'Objets abandonnés'
    #<QueryDict: {'anomalie': ['Objets abandonnés']}>
    op = request_get["anomalie"].encode('utf8')

    ########################################################################
    ## PIE - Nombre d'anoamlie pour un arrondissement et un type d'ano selectionnée
    Q2_Niv2_Pie = './static/img/Q2_Niv2_{}_{}_Pie.png'.format(str(op.decode()), pk)
    Q2_Niv2_Pie2 = '/static/img/Q2_Niv2_{}_{}_Pie.png'.format(str(op.decode()), pk)

    fig, ax = plt.subplots()

    ax.pie(df3.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
        labels=df3['annee_declaration'].unique(),
        radius=1, wedgeprops=dict(width=1, edgecolor='w'),
        # colors = outer_colors,
        labeldistance = 0.5)
        # , explode=[0.3,0])
        # , autopct='%1.1f%%'

    ax.pie(df3.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].value_counts(),
        labels=df3.groupby(['annee_declaration','mois_declaration'])['mois_declaration'].unique(),
        radius=1.5, wedgeprops=dict(width=0.5, edgecolor='w'),
        # colors = inner_colors,
        labeldistance = 0.9)
        # , autopct='%1.1f%%'


    plt.savefig(str(Q2_Niv2_Pie),bbox_inches='tight')
    plt.close()

    ########################################################################
    ## HIST - Nombre d'anoamlie pour un arrondissement et un type d'ano selectionnée
    Q2_Niv2_Bar = './static/img/Q2_Niv2_{}_{}_Bar.png'.format(str(op.decode()),pk)
    Q2_Niv2_Bar2 ='/static/img/Q2_Niv2_{}_{}_Bar.png'.format(str(op.decode()), pk)

    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration']).plot.bar()
    plt.savefig(str(Q2_Niv2_Bar),bbox_inches='tight')
    plt.close()

    ########################################################################
    ## DATA - Nombre d'anoamlie pour un arrondissement et un type d'ano selectionnée
    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration'])
    
    json_records2 = df4.to_json(orient = 'index')
    data_type = []
    data_type = json.loads(json_records2)

    context = {'img' : [Q2_Niv2_Bar2, Q2_Niv2_Pie2], 'data_type' : data_type, 'id' : 0, 'list_anomalie' : list_anomalie}

  else :

    ########################################################################
    # PIE  : Nombre total d'anomalie par mois dans un arrondissement
    Q2_Niv1_Pie = './static/img/Q2_Niv1_{}_Pie.png'.format(pk)
    Q2_Niv1_Pie2 ='/static/img/Q2_Niv1_{}_Pie.png'.format(pk)
    
    # croiser par mois et année :
    # résultat : 1 df dont l'index correspond aux arrondissements, avec 1 colonne par année
    df_q2 = df2.loc[df2['arrondissement']==pk,:]
    df_q2 = pandas.crosstab(df_q2['mois_declaration'],df_q2['annee_declaration'])

    # préparer données pour graph : 
    years=[]
    years_values=[]
    mois = []
    mois_values = []
    mois_max = [] #liste de booléen : true pour la valeur max, false pour les autres
    explode = []
    explode_factor=0.2

    for column in df_q2.columns:
        # 1. années et valeurs totales par année
        years_values.append(df_q2[column].sum())
        years.append(column)
        
        # 2. arrondissements et valeurs par arrondissement 
        
        for index, row in df_q2.iterrows():
            mois.append(index)
            mois_values.append(row[column])
            mois_max.append(1 if (row[column] == np.max(df_q2[column])) else 0)

    # replace months with 0 data with empty str "" and other months with complete months name in labels list
    mois_dict = {1:"janvier",2:"fevrier",3:"mars",4:"avril",5:"mai",6:"juin",7:"juillet",8:"août",9:"septembre",10:"octobre",11:"novembre",12:"décembre"}
    mois = [mois_dict[mois] if (mois_values[i]!=0) else "" for i,mois in enumerate(mois) ]


    # paramètre explode du graph pie pour gérer identification de l'arrondissement max:
    explode = [explode_factor * i for i in mois_max]

    # Definir les couleurs avec la map tab20 : 
    # couleur principale (indexes pairs) pour les annees
    # couleurs secondaires (indexes impairs ) pour les arrondissements correspondants.

    cmap = plt.get_cmap("tab20c")
    inner_colors = cmap(np.arange(10)*4)
    outer_colors = cmap(np.array([1 + 4 * j for j in range(0,len(years)) for i in range(0,12)]))

    fig1, ax1 = plt.subplots()
    ax1.pie(mois_values
        ,colors = outer_colors
        ,explode= explode
        ,labels = mois
        ,rotatelabels = True
        ,labeldistance = 0.7
        ,radius = 1.5
        ,wedgeprops=dict(width=0.8, edgecolor='w')
        )
    ax1.pie(years_values
        ,textprops={'fontsize': 14}
        ,labeldistance = 0.5
        ,colors = inner_colors
        ,labels = years
        ,radius = 1)

    ax1.axis()


    plt.savefig(str(Q2_Niv1_Pie),bbox_inches='tight')
    plt.close()

    ########################################################################
    # HIST : Nombre total d'anomalie par mois dans un arrondissement
    Q2_Niv1_Bar = './static/img/Q2_Niv1_{}_Hist.png'.format(pk)
    Q2_Niv1_Bar2 ='/static/img/Q2_Niv1_{}_Hist.png'.format(pk)
    
    pandas.crosstab(df2['mois_declaration'],df2['annee_declaration']).plot.bar()
    plt.savefig(str(Q2_Niv1_Bar),bbox_inches='tight')
    plt.close()


    ########################################################################
    #DATA : Nombre total d'anomalie par mois dans un arrondissement
    df3 = df2.loc[df2['arrondissement']==pk,:]
    df4 = pandas.crosstab(df3['mois_declaration'],df3['annee_declaration'])
    json_records = df4.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)

    context = {'img' : [Q2_Niv1_Bar2, Q2_Niv1_Pie2], 'data' : data, 'id' : 1, 'list_anomalie' : list_anomalie}
  
  return render(request, 'Q2_ParMois.html', context) 