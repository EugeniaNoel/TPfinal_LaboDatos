#CARGO LOS DATASETS

import pandas as pd

path = 'C:\\Users\\eugen\\Documents\\materias\\labodatos\\TP_final_extinct_languages'

filename_merge1 = '\\merged1.csv'
df_merge1 = pd.read_csv(path+filename_merge1)

columnas = df_merge1.columns

#Inspecciono el dataset
for i in range(len(columnas)):
    print(str(i) + ' : ' + str(columnas[i]))

#%% Vamos mirando columna por columna cuales son necesarías y
#que modificaciones hay que hacerles

# MACROAREA: llenamos a mano los 14 NaN que encontramos
    
macronan = df_merge1[df_merge1['Macroarea'].isnull()]
indexnan = macronan.index

#Agregamos macroareas  en una copia del dataframe original
df1 = df_merge1.copy()
macroareas_faltantes = ['Papunesia','South America','Africa','Eurasia','Eurasia','Eurasia','Australia','Australia','North America','North America','Australia','Eurasia','Africa', 'Australia']
for i in range(len(indexnan)):
    j = indexnan[i]
    print(j)
    df1['Macroarea'][j] = macroareas_faltantes[i]

# LENGUAJE DE SEÑAS: Quitamos las filas correspondientes
#a lenguages de señas en una copia del dataframe anterior 

df = df1.copy()
#cambio el nombre de la columna porque se confunde con los espacios
#y la ñ
df.rename(columns = {'Lenguaje de Señas':'senas'}, inplace = True)

indexNames = df[ df['senas'] == 1 ].index
df.drop(indexNames , inplace=True)
df = df.reset_index(drop=True)

# STATUS_X_L: cambiamos L por 0 y X por 1

df.loc[df.Status_X_L =='L','Status_X_L']= 0
df.loc[df.Status_X_L =='X','Status_X_L']= 1

#%%
# NUM_SPEAKER: Despues de haber chequado algunos datos en Ethnologe
#concluimos que le valor mas grande que aparece en la lista es el
#nro de hablantes total. Nos quedamos solo con este elemento
#de cada lista

#Poner el mayor nro de hablantes
for i in range(len(df['num_speakers'])):    
    linea = str(df['num_speakers'][i])
    linea = linea.strip('][').split(',')
    new_list = []
    for m in linea:
        new_list.append(float(m))
    df['num_speakers'][i] = max(new_list) 

#%% Nos quedamos solo con algunas columnas

#Nos quedamos solo con ISO porque WALS_ID, countryISO, Name 
#y ISO  representan lo mismo

#Nos deshicimos de Family y Genus porque tiene 75 NaN.
#si fueran necesarios los buscamos llenar a mano

#En una primera aproximacion, nos quedamos con Status_X_L
#y nos deshacemos de Status

#Nos deshacemos de HDI por el momento, aunque la pensamos incluir
#luego

#Nos quedamos con country_population para poder armar alguna feauture
#que tenga que ver con la proporcion de hablantes 

#Nos quedamos con Country_coord porque en Latitude y Longitude
#solo tenemos un valor por lenguage, aunque se hable en varios paises

df = df[['ISO', 'Macroarea', 'Latitude',
       'Longitude', 'Status_X_L',
       'countryISO', 'num_speakers',
       'country_population', 'Country_coord']]

#%% COMENZAMOS CON EL ARMADO DE FEAUTURES

#Nueva feauture con la cantidad de paises

df = df.assign(cant_paises = '')

for i in range(len(df['countryISO'])):    
    linea = str(df['countryISO'][i])
    linea = linea.strip('][').split(',')
    num = len(linea)
    df['cant_paises'][i] = num

#%%




#%%
