#%%
#CARGO LOS DATASETS
import pandas as pd

path = '/home/ingrid/Documents/labodatos/TP_final/merges/merged1.pkl'

df_merge1 = pd.read_pickle(path)

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
df1.loc[indexnan,'Macroarea'] = macroareas_faltantes

#Quitamos lenguage de señas    
df = df1.copy()
df.rename(columns = {'Lenguaje de Señas':'senas'}, inplace = True)

indexNames = df[ df['senas'] == 1 ].index
df.drop(indexNames , inplace=True)
df = df.reset_index(drop=True)

df.loc[df.Status_X_L =='L','Status_X_L']= 0
df.loc[df.Status_X_L =='X','Status_X_L']= 1
#%%
#Ponemos el mayor nro de hablantes

list_bool = df['num_speakers'].apply(lambda x: isinstance(x,list)) #entradas que son listas

num_speaker_lists = df['num_speakers'][list_bool] #para corroborar que sean esas

#con la función lambda tomo el máximo, reemplazo esos valores en el df
df.loc[num_speaker_lists.index,'num_speakers'] = num_speaker_lists.apply(lambda x: max(x))
    
#%% Nos quedamos con lo que nos importa por ahora
df = df[['ISO', 'Macroarea', 'Latitude',
       'Longitude', 'Status_X_L',
       'countryISO', 'num_speakers',
       'country_population', 'Country_coord']]

#%%
#Nueva feauture con la cantidad de paises

df = df.assign(cant_paises = '')
df['cant_paises'] = 1 #primero asigno 1 a toda la columna

list_bool = df['countryISO'].apply(lambda x: isinstance(x,list)) #las entradas que son listas

#para corroborar que sean esas
countries_lists = df['countryISO'][list_bool]

#con la función lambda tomo el largo de la lista, reemplazo esos valores en el df
df.loc[countries_lists.index,'cant_paises'] = countries_lists.apply(lambda x: len(x))
#%%
#chequeando que no haya quedado alguna lista adentro de strings
strings_bool = df['countryISO'].apply(lambda x: isinstance(x,str))
countries_strings = df['countryISO'][strings_bool]

#que no tengan ni comas ni espacios
countries_strings[countries_strings.str.contains(',')]
countries_strings[countries_strings.str.contains(' ')]
# %%
df.to_pickle('arreglar_df_v2.pkl')