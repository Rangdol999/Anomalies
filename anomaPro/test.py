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
#df2['New_ID'] = df2.index
df3 = df2.iloc[:, 2:3]
newdf2 = df3.to_dict(orient = 'index')
print(newdf2)
"""
df3 = df2.iloc[:, 0:3:2]
trans = df3.T
"""

"""
print(newdf2)
print(df3)
print(dicos)

dicos = df3.to_dict(orient = "dict")
{'New_ID': {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7

dicos = df2.to_dict(orient = "index")
 258: {'New_ID': 258, 'type_declaration': 'Objets abandonnés', 'arrondissement': 4, 'annee_declaration': 2021, 'geo_point_2d': '48.8597339971246,2.351992595510865'}, 259: {'New_ID': 259, 'type_declaration': 'Objets abandonnés', 'arrondissement': 12, 'annee_declaration': 2021, 'geo_point_2d': '48.84457000057794,2.412084303035094'}}


df3 = df2.iloc[:, 0:3:2]
trans = df3.T


df3 = df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].count()
dicos = df3.to_dict()
#{(1, 2021): 1440, (1, 2022): 256, (2, 2021): 2180, (2, 2022): 389, (3, 2021): 2275, (3, 2022): 444,


df3 = df2.iloc[:, 1:2]
#951846 : {'arrondissement': 19}, 951847: {'arrondissement': 5}
newdf = df3.T
print(newdf)
newdf2 = newdf.to_dict()
print(newdf2)
#951846 : {'arrondissement': 19}, 951847: {'arrondissement': 5}

"""

