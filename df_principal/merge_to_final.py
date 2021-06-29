#%%
# CARGO LOS DATASETS
import pandas as pd
import numpy as np
from shapely.geometry import Point
import shapely as shp 
import geopandas as gpd
from geopandas.array import points_from_xy

path = "merged1_listas.pkl"
df_merge1 = pd.read_pickle(path)

df_merge1.reset_index(inplace=True)
#%%
#region PART 1: DESDE EL PRIMER MERGE HASTA COMPLETAR SPEAKERS

#Pasamos todas las string-lista a listas de verdad por si quedó alguna
def sep(x):
    """para pasar posibles string-listas a listas-listas"""
    if (isinstance(x, str)) and ("[" in x): 
        return x.replace("'", "").strip("][").split(", ")
    else:
        return x

def sep_float(x):
    """para pasar posibles string-listas-float a listas-float"""
    if (isinstance(x, str)) and ("[" in x): 
        lista = x.replace("'", "").strip("][").split(", ")
        return [float(x_n) for x_n in lista]
    elif isinstance(x,list):
        return [float(x_n) for x_n in x]
    else:
        print(x)
        return float(x)

#para cargar los points en geopandas como coordenadas
def topoint(x):
    if isinstance(x, list):
        return [shp.wkt.loads(point) for point in x]
    else:
        return shp.wkt.loads(x)

#%%
df1 = df_merge1.applymap(sep)

print('Ahora las columnas problematicas solo tienen listas-listas \n\n#Listas por columna:')
print(df1.applymap(lambda x: isinstance(x,list)).sum())

print('\nY las que tienen valores numéricos no tienen ningún string \n\n#Strings por columna:')
print(df1.applymap(lambda x: isinstance(x,str)).sum())
#%%
# MACROAREA: llenamos a mano los 14 NaN que encontramos

macronan = df1[df1["Macroarea"].isnull()]

# Agregamos macroareas  en una copia del dataframe original
df2 = df1.copy()

macroareas_faltantes = [
    "Papunesia",
    "South America",
    "Africa",
    "Eurasia",
    "Eurasia",
    "Eurasia",
    "Australia",
    "Australia",
    "North America",
    "North America",
    "Australia",
    "Eurasia",
    "Africa",
    "Australia",
]

df2.loc[macronan.index, "Macroarea"] = macroareas_faltantes
#%% 
# LENGUAJE DE SEÑAS: Quitamos las filas correspondientes

# cambio el nombre de la columna porque se confunde con los espacios y la ñ
df3 = df2.rename(columns={"Lenguaje de Señas": "senas"})

indexNames = df3[df3["senas"] == 1].index
df3.drop(indexNames, inplace=True)
df3 = df3.reset_index(drop=True)

#%%
# NUM_SPEAKER: Despues de haber chequado algunos datos en Ethnologe
# concluimos que le valor mas grande que aparece en la lista es el
# nro de hablantes total. Nos quedamos solo con este elemento
# de cada lista

# entradas que son listas
list_bool = df3["num_speakers"].apply(
    lambda x: isinstance(x, list)
)  

# lista de las listas
num_speaker_lists = df3["num_speakers"][list_bool]  

# con la función lambda tomo el máximo, reemplazo esos valores en el df
df3.loc[num_speaker_lists.index, "num_speakers"] = num_speaker_lists.apply(
    lambda x: max(x)
)
#%% COMENZAMOS CON EL ARMADO DE FEAUTURES

# Nueva feauture con la cantidad de paises

# Cantidad de elementos de la lista o no lista
def num_countries(x):
    if isinstance(x,list):
        return len(x)
    else:
        return 1

df3['cant_paises']  = df3['countryISO'].apply(lambda x: num_countries(x))

#%%
# Armo una nueva feauture hable de la cercania entre lenguajes
# La feauture sera cuantos lenguajes tiene a menos de cierta medida
# de distancia

#transformo los string-point a un objeto de la clase Point de shapely
df4 = df3.copy()
df4['Country_coord'] = df4['Country_coord'].apply(topoint)

col_latitude = []
col_longitude = []

for i, item in df4['Country_coord'].items():
    if isinstance(item,Point):
        col_latitude.append(item.x)
        col_longitude.append(item.y)
    
    elif isinstance(item,list):
        sublist_lat = [subitem.x for subitem in item]
        sublist_long = [subitem.y for subitem in item]

        col_latitude.append(sublist_lat)
        col_longitude.append(sublist_long)

df4['Country_lat'] = col_latitude
df4['Country_long'] = col_longitude
#%%
#esta parte la comento porque tarda en correr, por las dudas

# largo = len(df4)
# col_nearest = np.zeros(largo)

# print('Corremos el loop de euge para armar la feature nearest languages')
# for i in range(largo):
#     print(i)
#     if df4["cant_paises"][i] == 1:
#         lat = df4["Latitude"][i]
#         long = df4["Longitude"][i]
#         cercanos = 0
#         for j in range(largo):
#             if j != i:
#                 if df4["cant_paises"][j] == 1:
#                     lat1 = df4["Latitude"][j]
#                     long1 = df4["Longitude"][j]
#                     dif_lat = lat1 - lat
#                     dif_long = long1 - long
#                     if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
#                         cercanos = cercanos + 1
#                 else:
#                     for k in range(df4["cant_paises"][j]):
#                         lat1 = df4["Country_lat"][j][k]
#                         long1 = df4["Country_long"][j][k]
#                         dif_lat = lat1 - lat
#                         dif_long1 = long1 - long
#                         if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
#                             cercanos = cercanos + 1
#     else:
#         cercanos = 0
#         for m in range(df4["cant_paises"][i]):
#             lat = df4["Country_lat"][i][m]
#             long = df4["Country_long"][i][m]
#             for j in range(largo):
#                 if j != i:
#                     if df4["cant_paises"][j] == 1:
#                         lat1 = df4["Latitude"][j]
#                         long1 = df4["Longitude"][j]
#                         dif_lat = lat1 - lat
#                         dif_long = long1 - long
#                         if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
#                             cercanos = cercanos + 1
#                     else:
#                         for k in range(df4["cant_paises"][j]):
#                             lat1 = df4["Country_lat"][j][k]
#                             long1 = df4["Country_long"][j][k]
#                             dif_lat = lat1 - lat
#                             dif_long1 = long1 - long
#                             if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
#                                 cercanos = cercanos + 1
#     col_nearest[i] = cercanos

#endregion
#%%
# df4.to_pickle('paso1.pkl')
# df4.to_csv('paso1.csv')
#%%
#region PART 2: AGREGAR SPEAKERS DE CADA UNA AL DF PRINCIPAL
#df4 = pd.read_pickle('paso1.pkl')
#df_principal = df4.copy()
ingrid = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/df_principal/completados_INGRID.csv')
euge = pd.read_excel('/home/ingrid/Documents/labodatos/TP_final/df_principal/df_num_speakers_euge_arreglado_v2.xlsx')
mai = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/df_principal/completados_MAIA.csv')
romi = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/df_principal/romi_completos.csv')
#%%
#Los df merge1 no habian pasado por todos los pasos anteriores
#En uno de esos quitabamos varias filas, eso hizo lio con los indexados
#Con esto se acomodó:
df_principal = pd.read_pickle('paso1.pkl')

def senas(df):
    df2 = df.rename(columns={"Lenguaje de Señas": "senas"})
    indexNames = df2[df2["senas"] == 1].index
    df2.drop(indexNames, inplace=True)
    df2 = df2.drop(columns='senas').reset_index(drop=True)
    return df2

euge = senas(euge)
romi = senas(romi)
df_principal = senas(df_principal)

#%%
#Ahora los 4 DF tienen el mismo indice, se puede probar para cada par con:
(romi['num_speakers'] == ingrid['num_speakers']).value_counts()


#El rango que reemplazo cada una
index_mai=range(661)
index_euge=range(662,1253)
index_ingrid=range(1253,1800)
index_romi=range(1800,2524)


ingrid = ingrid.loc[index_ingrid,['ISO','num_speakers']]
euge = euge.loc[index_euge,['ISO','num_speakers']]
mai = mai.loc[index_mai,['ISO','num_speakers']]
romi = romi.loc[index_romi,['ISO','num_speakers']]

numspeakers_full = pd.concat([mai,euge,ingrid,romi])

print('Ahora spa esta bien :)')
print(numspeakers_full.set_index('ISO').loc['spa'])

print(f'Quedaron 90 nans')
numspeakers_full[numspeakers_full['num_speakers'].isna()]

#agregandolo al df principal
df_principal['num_speakers'] = numspeakers_full['num_speakers']
#%%

#Al mergearlo de nuevo, volvieron algunos valores de un DF viejo que estaban en string
#lo volvemos a limpiar

df_principal['num_speakers'] = df_principal['num_speakers'].apply(sep_float)

list_bool = df_principal["num_speakers"].apply(
    lambda x: isinstance(x, list)
)  

# lista de las listas
num_speaker_lists = df_principal["num_speakers"][list_bool]  

# con la función lambda tomo el máximo, reemplazo esos valores en el df
df_principal.loc[num_speaker_lists.index, "num_speakers"] = num_speaker_lists.apply(
    lambda x: max(x)
)
#endregion
#%%
#df_principal.to_pickle('paso2.pkl')
#df_principal.to_csv('paso2.csv')
#%%
#region PART 3: STATUS BINARIO Y PAIS OFICIAL
#df5 = pd.read_pickle("paso2.pkl")
df5 = df_principal.copy()
#%%
#Armo la variable binaria:

#cosas que que vi mal y cambie a mano:
df5.loc[2050,'Status'] = '6b Threatened'
df5.loc[2376,'countryISO'] = 'WLF'

status_dict = {'6b Threatened':0, '4 Educational':1, '5 Developing':1,
       '3 Wider Communication':1,'2 Provincial':1, '8b Nearly Extinct':0,
       '6a Vigorous':1, '7 Shifting':0, '8a Moribund':0, '1 National':1,
       '10 Extinct':0, '9 Dormant':0, '9 Reawakening':0,
       '9 Second language only':0, '0 International':1}

df5['Status_binario'] = df5['Status'].replace(status_dict)

#%%
#Para agregar idioma oficial
query = (
    pd.read_csv("/home/ingrid/Documents/labodatos/TP_final/df_final/query_final.csv")
    .rename(
        columns={
            "countryISO": "official_in",
        }
    )
    .drop(columns=["language","country"])
)
lang_imploded = query.groupby(query["ISO"]).official_in.agg(list)

df6 = df5.merge(lang_imploded, on="ISO", how="left")
#endregion
#%%
#Le cambio acá los nombres para que no confunda
df6 = df6.drop(columns='Status_X_L').rename(columns={'Country_ID':
'Native_country', 'Latitude':'Latitude_lang','Longitude':'Longitude_lang',
'wiki_country':'Country_name'})
#%%
df6.to_pickle('df_principal.pkl')
df6.to_csv('df_principal.csv')


