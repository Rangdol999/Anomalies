############## GRAPH ANOMALIES

"""
Q1 - Global : Etat initiale - hist :
    df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)
plt.savefig('anomalies_par_annee_et_arr_hist.png')


Q1.1 - histogramme :

  df2.groupby(['arrondissement','annee_declaration'])['type_declaration'].value_counts().unstack().plot.bar(stacked=True)
  path_bar = './static/img/anomalies_par_annee_et_arr.png'
  path_bar2 ='/static/img/anomalies_par_annee_et_arr.png'
  plt.savefig(str(path_bar))

Q1.2 - camembert : fig, ax = plt.subplots()

cmap = plt.get_cmap("tab20c")
outer_colors = cmap(np.arange(2)*4)
inner_colors = plt.get_cmap('Greys')(np.array([i*3 for i in range(10,30)]))
# inner_colors = cmap(np.array([i for i in range(1,21)]))

ax.pie(df2.groupby(['annee_declaration'])['annee_declaration'].value_counts(),
       labels=df2['annee_declaration'].unique(),
       radius=2, wedgeprops=dict(width=2, edgecolor='w'),
       colors = outer_colors,
       labeldistance = 0.5)
        # , explode=[0.3,0])
        # , autopct='%1.1f%%'

ax.pie(df2.groupby(['annee_declaration','arrondissement'])['arrondissement'].value_counts(),
       labels=df2.groupby(['annee_declaration','arrondissement'])['arrondissement'].unique(),
       radius=2.5, wedgeprops=dict(width=0.5, edgecolor='w'),
       colors = inner_colors,
       labeldistance = 0.9)
        # , autopct='%1.1f%%'


print("nombre d'anomalies par annee et par arrondissement")
ax.set(aspect="equal", title='Anomalies par année et arrondissement')
plt.savefig('anomalies_par_annee_et_arr.png')
plt.show()

"""