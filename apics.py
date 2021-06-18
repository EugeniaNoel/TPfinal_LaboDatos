#%%
import pandas as pd
import numpy as np

#cargo los archivos de APICS y el dataset ya armado de WALS
codes = pd.read_csv('cldf/codes.csv')
values = pd.read_csv('cldf/values.csv')
languages = pd.read_csv('cldf/languages.csv')
gloss = pd.read_csv('cldf/glossabbreviations.csv')
parameters = pd.read_csv('cldf/parameters.csv')

wals = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/WALS_completo.csv').rename(columns={'Unnamed: 0':'ID'})
#%%
languages.head()
values.head()
parameters.head()
print('Los parametros que dicen WALS ID es porque tambien estan en wals, pero con otro nombre')
#%%
#me quede solo con las columnas que me sirven
languages_df = languages[['ID','Name','Macroarea','Latitude','Longitude','ISO639P3code','Ethnologue_Name','Region','Lexifier']]
parameters.set_index('ID',inplace=True)
languages_df.set_index('ID',inplace=True)

#codigos de las features que me interesan
speakers = 313
abandono = 312
print('Me fijé en la página de APICS que codigos tenian la cantidad de hablantes y el abandono')

#con pivot paso values a un formato que me sirve
valores = values.copy()
valores_2 = valores.pivot_table('Value','Language_ID','Parameter_ID')
#%%
#Me quiero quedar solo con las features que tambien estan en wals
print('Busco que features comparte con WALS y me quedo solo con esas (y las de abandono y hablantes)')

wals_id_nans = parameters['WALS_ID'].isna() #indice de features que no estan en WALS
con_wals_id = parameters[~wals_id_nans] #features SI en wals

index_keep = list(con_wals_id.index.values) + [speakers,abandono]
valores_con_wals = valores_2[index_keep] #nuevo values pero solo con las cosas que me sirven
valores_con_wals.head()
#%%
print('Lo armo como hice con WALS, haciendo un merge sobre el ID del lenguaje')
apics = languages_df.merge(valores_con_wals, how='inner',left_index=True,right_index=True)

#para que las features tengan el mismo nombre que en wals
mapeo = con_wals_id['WALS_ID'].to_dict()
apics = apics.rename(columns=mapeo)
apics.drop(columns='Macroarea',inplace=True)
apics.rename(columns={'Region':'Macroarea'},inplace=True) #region de APICS es lo mismo que macroarea de WALS

#agrego una columna pidgin/creole asi los identifico despues
#0 = no es p/c, 1= es p/c
apics['Pidgin/Creole'] = 1
#%%
#miro los nans por idioma y por feature
nans_columnas = {}
for column in apics.columns:
    nans_columnas[column] = apics[column].isna().sum()

nans_filas = {}
for fila in apics.index:
    nans_filas[fila] = apics.loc[[fila]].isna().sum().sum()

#idiomas ordenados por orden de nans
idiomas_nans = sorted(nans_filas, key=nans_filas.get)
print(f'El idioma con más nans es: {idiomas_nans[-1]} y con menos: {idiomas_nans[0]}')
#%%
#Lo agrego a wals con un append porque quiero que agregue las columnas nuevas
unidos = wals.append(apics)
unidos.drop(columns=['Ethnologue_Name','Genus','GenusIcon'], inplace=True)
unidos['Pidgin/Creole'].fillna(0,inplace=True)
unidos.rename(columns = {313:'Num_Speakers',312:'Abandono'},inplace=True)
#%%
#para ver que significan los valores de las nuevas features
codes.set_index('Parameter_ID',inplace=True)
valores_speakers = codes.loc[313]
valores_abandono = codes.loc[312]
valores_speakers
#%%
#Busco si hay idiomas duplicados
duplicados = unidos[unidos.duplicated(subset='Name')]
unidos.drop_duplicates(subset='Name',inplace=True)

#no hay mas duplicados
unidos.duplicated(subset='Name').value_counts()


unidos.to_csv('wals_apics.csv',index=False)
# %%
