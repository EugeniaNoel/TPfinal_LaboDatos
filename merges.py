#%%
import numpy as np
import pandas as pd
from orderedset import OrderedSet as oset
#%%
wals = pd.read_csv('ISO_completos.csv').rename(columns={'Status':'Status_X_L'})
wals_2 = pd.read_csv('ISO_completos_features.csv').rename(columns={'Status':'Status_X_L'})
wiki_merged = pd.read_csv('Wikidata_Wals_IDWALS.csv')
wiki = pd.read_csv('wikidata_v3.csv')
#%%
#region IMPLODE
#los agrupo por ISO y le pido que ponga todos lso valores en una lista
country_imploded = wiki.groupby(wiki['ISO']).countryLabel.agg(list)
#%%
#defini una función porque voy a hacer esto muchas veces
def implode(df,index_column,data_column):
    """ index_column = valor en común para agrupar (en este caso es el ISO), string 
        data_column = datos que queremos agrupar en una sola columna, string """
    return df.groupby(df[index_column])[data_column].agg(list)
#%%
#lo hice para todas las columnas y lo guarde en una lista
agrupadas = []
for column in wiki.columns.values:
    if column != 'ISO':
        agrupadas.append(implode(wiki,'ISO',column))
#%%
#ahora armo un df con las series que ya estan agrupadas
df_imploded = pd.concat(agrupadas, axis=1).rename(
                columns={'languageLabel':'wiki_name',
                'countryLabel':'wiki_country',
                'country_ISO':'wiki_countryISO',
                'Ethnologe_stastusLabel':'wiki_Status',
                'number_of_speaker':'num_speakers',
                'coordinates':'wiki_lang_coord',
                'population':'country_population'})

#endregion
#%%
#region COLLAPSE
#Voy a pasar cada lista del DF a un set, para quedarme con los valores únicos
#Luego reemplazo esa entrada por el set, además si el valor es uno solo lo agrego como string
#y no como lista

df_test = df_imploded.copy()
column = df_test['wiki_name']
new_column = []

for index, item in column.items():
    values = list(oset(item))
    if len(values) == 1:
        new_column.append(values[0])
    else:
        new_column.append(values)
#%%
def notna(list):
    return [x for x in list if str(x) != 'nan']

#defino una función para hacer esto muchas veces
def group_idem_oset(df,column_name):
    """Para sacar valores unicos dentro de las listas que quedaron """
    new_column = []
    for index, item in df[column_name].items():
        values = notna(list(oset(item))) #hace un set de todos los valores de la fila
        if len(values) == 1: 
            new_column.append(values[0]) #si hay un unico valor lo reemplaza directamente
        elif not values: 
            new_column.append(np.nan) #si es una lista vacía pone un 0
        else:
            new_column.append(values) #si hay varios valores distintos los conservamos
    return new_column
#%%
#y lo hago para todas las columnas del df nuevo
collapsed = []
for column_name in df_test.columns.values:
    new_column = pd.Series(group_idem_oset(df_test,column_name),name=column_name, index=df_test.index)
    collapsed.append(new_column)

df_collapsed = pd.concat(collapsed, axis=1)
#endregion
#%%
#para ver entradas donde todavía hay listas de valores, por columna
list_index = df_collapsed['wiki_name'].apply(lambda x: isinstance(x,list))
#%%
#intento de merge con wals
merged = wals.merge(df_collapsed, left_on='ISO',right_index=True,how='inner').rename(
        columns={'Ethnologe_statusLabel':'Status',
                'country_coordinates':'Country_coord'}
).drop(columns=['wiki_lang_coord','wiki_name']).set_index('ISO')

merged.to_csv('merged1.csv')
#%%
merged2 = wals_2.merge(df_collapsed, left_on='ISO',right_index=True,how='inner').rename(
        columns={'Ethnologe_statusLabel':'Status',
                'country_coordinates':'Country_coord'}
).drop(columns=['wiki_lang_coord','wiki_name']).set_index('ISO')

merged2.to_csv('merged2.csv')
# %%
#para ver las listas que quedaron:
merged[merged['Status'].apply(lambda x: isinstance(x,list))]