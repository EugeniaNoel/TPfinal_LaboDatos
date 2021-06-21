#CARGO LOS DATASETS

import pandas as pd

path = 'C:\\Users\\eugen\\Documents\\materias\\labodatos\\TP_final_extinct_languages'

filename_merge1 = '\\merged1.csv'
df_merge1 = pd.read_csv(path+filename_merge1)

columnas = df_merge1.columns

for i in range(len(columnas)):
    print(i)
    print(columnas[i])

#%%
macronan = df_merge1[df_merge1['Macroarea'].isnull()]

indexnan = macronan.index

#Agregamos macroareas faltantes
df1 = df_merge1.copy()

macroareas_faltantes = ['Papunesia','South America','Africa','Eurasia','Eurasia','Eurasia','Australia','Australia','North America','North America','Australia','Eurasia','Africa', 'Australia']

for i in range(len(indexnan)):
    j = indexnan[i]
    print(j)
    df1['Macroarea'][j] = macroareas_faltantes[i]

#Quitamos lenguage de señas    
df = df1.copy()
df.rename(columns = {'Lenguaje de Señas':'senas'}, inplace = True)

indexNames = df[ df['senas'] == 1 ].index
df.drop(indexNames , inplace=True)
df = df.reset_index(drop=True)

df.loc[df.Status_X_L =='L','Status_X_L']= 0
df.loc[df.Status_X_L =='X','Status_X_L']= 1

#%%
#Poner el mayor nro de hablantes
for i in range(len(df['num_speakers'])):    
    linea = str(df['num_speakers'][i])
    linea = linea.strip('][').split(',')
    new_list = []
    for m in linea:
        new_list.append(float(m))
    df['num_speakers'][i] = max(new_list) 

#%% Nos quedamos con lo que nos importa por ahora
df = df[['ISO', 'Macroarea', 'Latitude',
       'Longitude', 'Status_X_L',
       'countryISO', 'num_speakers',
       'country_population', 'Country_coord']]

#%%
#Nueva feauture con la cantidad de paises

df = df.assign(cant_paises = '')

for i in range(len(df['countryISO'])):    
    linea = str(df['countryISO'][i])
    linea = linea.strip('][').split(',')
    num = len(linea)
    df['cant_paises'][i] = num

#%%



#%%
