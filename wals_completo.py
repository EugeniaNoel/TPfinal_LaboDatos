#%%
import pandas as pd

#Cargamos los archivos
codes = pd.read_csv('/cldf-datasets-wals-bc8a5f9/cldf/codes.csv')
languages = pd.read_csv('/cldf-datasets-wals-bc8a5f9/cldf/languages.csv')
parameters = pd.read_csv('/cldf-datasets-wals-bc8a5f9/cldf/parameters.csv')
values = pd.read_csv('/cldf-datasets-wals-bc8a5f9/cldf/values.csv')
countries = pd.read_csv('/cldf-datasets-wals-bc8a5f9/cldf/countries.csv')
#%%
#Sacamos columnas que no nos iban a servir
languages.drop(columns=['Glottocode','Samples_100','Samples_200','Source'], inplace=True)

#Miramos los lenguajes que no tienen ISO
sin_isos =  languages[languages['ISO_codes'].isna() & languages['ISO639P3code'].isna()] #no tienen ninguno de los dos ISOs
sin_iso_639 =  languages['ISO639P3code'].isna().sum() #no tienen ISO639
sin_iso = languages['ISO_codes'].isna().sum() #no tienen ISO comun

#lista de lenguajes sin ISO
lang_sin_iso = languages['ID'][languages['ISO_codes'].isna()].tolist()
#%%
#Agregamos los features al DF de Languages
valores = values.copy() #para no tocar el csv original

#Pasamos los parametros a columnas y ponemos el valor que corresponde en cada entrada
valores_2 = valores.pivot_table('Value','Language_ID','Parameter_ID')

#Unimos los dos DF por el indice (que es el ID del idioma)
languages.set_index('ID',inplace=True)
unidos = languages.merge(valores_2,how='inner',left_index=True,right_index=True)
print('Unidos es el dataset completo, no sacamos nada todavía')
print('Para ver qué sacamos vamos a fijarnos que idioma o feature tiene muchos NaNs')
unidos
#%%
#Para ver cuantos nan hay por columna (osea por feature)
#Dict con keys=feature, values=#Nans
nans_columnas = {}
for column in unidos.columns:
    nans_columnas[column] = unidos[column].isna().sum()
print(f'Ej. la feature 91A tiene {nans_columnas["91A"]} Nans')

#Para ver cuantos nan hay por fila (osea por idioma)
#Dict con keys=idioma, values=#Nans
nans_filas = {}
for fila in unidos.index:
    nans_filas[fila] = unidos.loc[[fila]].isna().sum().sum()

#idiomas ordenados por orden de nans
idiomas_nans = sorted(nans_filas, key=nans_filas.get)

print(f'Ej. el idioma fre (frances) tiene {nans_filas["fre"]} Nans')
print(f'El idioma con más nans es: {idiomas_nans[-1]} y con menos: {idiomas_nans[0]} ')
# %%
