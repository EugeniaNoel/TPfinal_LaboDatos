#CARGO LOS DATASETS

import pandas as pd

path = 'C:\\Users\\eugen\\Documents\\materias\\labodatos\\TP_final_extinct_languages'

#Este es el dataset principal, la idea es utilizar todos sus registros 
#Solo incluye lenguas vulnerables a extinguirse (2722)
filename_ppal = '\\dataset_ppal.csv'
df_ppal = pd.read_csv(path+filename_ppal)

#El dataset complementario a tiene muchos Nan asi que no nos sirve

#Este dataset es complementario. Tiene información similar
#al dataset ppal,pero no necesariamente son lenguas vulnerables.
#Son (25900) registros
filename_compl_b = '\\dataset_complementario_b.csv'
df_compl_b = pd.read_csv(path+filename_compl_b)

#%% EXPLORO LOS DATASETS

print(df_ppal.columns)
print(df_compl_b.columns)


#Tanto el dataset principal como el complementario tienen varias
#columnas que en principio no aportar, asi que las desechamos.
#Tenemos en cuenta dejar la columna del codigo ISO639P3 porque
#quizas nos ayude a matchear lenguajes entre los datasets

df_ppal_1 = df_ppal[['Name in English', 'Countries', 'ISO639-3 codes',
         'Degree of endangerment', 'Number of speakers', 
         'Latitude', 'Longitude', 'Description of the location']].copy()
df_compl_b_1 = df_compl_b[['Name', 'Macroarea', 'Latitude','Longitude',
                    'ISO639P3code', 'Countries', 'Family_ID']].copy()

                    
#Voy a renombrar algunas etiquetas para que sean comunes a ambos datasets

df_ppal_1 = df_ppal_1.rename(columns={'Name in English':'Name','ISO639-3 codes':'ISO'})
df_compl_b_1= df_compl_b_1.rename(columns={'ISO639P3code':'ISO'})

print(df_ppal_1.columns)
print(df_compl_b_1.columns)


#Cambio el indice de mis dataframes y los junto a parir del mismo

df_ppal_1 = df_ppal_1.set_index('ISO')
df_compl_b_1 = df_compl_b_1.set_index('ISO')

df_all = pd.merge(df_ppal_1 ,df_compl_b_1, how="inner", on='Name')
#print(df_all)

#%%

for i in range(len(df_compl_b['Name'])):
    if df_compl_b['Name'][i] == 'Spanish':
        print(i)


print(df_compl_b.iloc[16452]['Countries'])




