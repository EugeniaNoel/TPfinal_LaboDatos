#CARGO LOS DATASETS
import pandas as pd

path = 'C:\\Users\\eugen\\Documents\\GitHub\\TPfinal_LaboDatos'
filename_merge1 = '\\merged1_listas.pkl'
df_merge1 = pd.read_pickle(path+filename_merge1)

#El pkl tiene como index el ISO, como no quiero perderlo
#lo transformo en columna
df_merge1.reset_index(inplace=True)

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

#Esto no funcionó, pero lo dejo pq ingrid lo puso
#df1.loc[indexnan,'Macroarea'] = macroareas_faltantes

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
list_bool = df['num_speakers'].apply(lambda x: isinstance(x,list)) #entradas que son listas

num_speaker_lists = df['num_speakers'][list_bool] #para corroborar que sean esas

#con la función lambda tomo el máximo, reemplazo esos valores en el df
df.loc[num_speaker_lists.index,'num_speakers'] = num_speaker_lists.apply(lambda x: max(x))
    
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

df = df[['ISO','Name', 'Macroarea', 'Latitude',
       'Longitude', 'Status_X_L',
       'countryISO', 'num_speakers',
       'country_population', 'Country_coord']]

#%% COMENZAMOS CON EL ARMADO DE FEAUTURES

#Nueva feauture con la cantidad de paises

df = df.assign(cant_paises = '')
df['cant_paises'] = 1 #primero asigno 1 a toda la columna

list_bool = df['countryISO'].apply(lambda x: isinstance(x,list)) #las entradas que son listas

#para corroborar que sean esas
countries_lists = df['countryISO'][list_bool]

#con la función lambda tomo el largo de la lista, reemplazo esos valores en el df
df.loc[countries_lists.index,'cant_paises'] = countries_lists.apply(lambda x: len(x))

#%%

#Modificamos la feauture Country_coord para que las coordenadas 
#esten escritas iguales que en Latitude y Longitude

df = df.assign(Country_lat = '')
df = df.assign(Country_long = '')

for i in range(len(df['Country_coord'])):
    linea = df['Country_coord'][i]
    list_lat = []
    list_long = []
    if type(linea) == str:
        elemento = linea.strip(')Point(').split(' ') 
        list_lat.append(float(elemento[1]))
        list_long.append(float(elemento[0]))
    else:
        for j in range(len(linea)):
            elemento = linea[j].strip(')Point(').split(',')
            elemento = elemento[0].split(' ')
            list_lat.append(float(elemento[1]))
            list_long.append(float(elemento[0]))
    df['Country_lat'][i] = list_lat
    df['Country_long'][i] = list_long

df = df.drop('Country_coord',axis=1)

#%%
#Armo una nueva feauture hable de la cercania entre lenguajes
#La feauture sera cuantos lenguajes tiene a menos de cierta medida
#de distancia

df = df.assign(Nearest_languages = '')

largo = len(df['Nearest_languages'])

for i in range(largo):   
    print(i)
    if df['cant_paises'][i] == 1:
        lat = df['Latitude'][i]
        long = df['Longitude'][i]
        cercanos = 0
        for j in range(largo):
            if j == i:
                pass
            else:
                if df['cant_paises'][j]==1:
                    lat1 = df['Latitude'][j]
                    long1 = df['Longitude'][j]
                    dif_lat = lat1-lat
                    dif_long = long1-long
                    if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
                        cercanos = cercanos+1
                    else:
                        pass
                else:
                    for k in range(df['cant_paises'][j]):
                        lat1 = df['Country_lat'][j][k]
                        long1 = df['Country_long'][j][k]
                        dif_lat = lat1-lat
                        dif_long1 = long1-long
                        if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
                            cercanos = cercanos+1
                        else:
                            pass                    
    else:
        cercanos = 0
        for m in range(df['cant_paises'][i]):
            lat = df['Country_lat'][i][m]
            long = df['Country_long'][i][m]
            for j in range(largo):
                if j == i:
                    pass
                else:
                    if df['cant_paises'][j]==1:
                        lat1 = df['Latitude'][j]
                        long1 = df['Longitude'][j]
                        dif_lat = lat1-lat
                        dif_long = long1-long
                        if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
                            cercanos = cercanos+1
                        else:
                            pass
                    else:
                        for k in range(df['cant_paises'][j]):
                            lat1 = df['Country_lat'][j][k]
                            long1 = df['Country_long'][j][k]
                            dif_lat = lat1-lat
                            dif_long1 = long1-long
                            if (abs(dif_lat) < 10) and (abs(dif_long) < 10):
                                cercanos = cercanos+1
                            else:
                                pass                                                                                
    df['Nearest_languages'][i] = cercanos
                    


#%%
#chequeando que no haya quedado alguna lista adentro de strings
#strings_bool = df['countryISO'].apply(lambda x: isinstance(x,str))
#countries_strings = df['countryISO'][strings_bool]

#que no tengan ni comas ni espacios
#countries_strings[countries_strings.str.contains(',')]
#countries_strings[countries_strings.str.contains(' ')]

#%%


# %%
#df.to_pickle('arreglar_df_v2.pkl')