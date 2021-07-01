#%%
#region LIBRERIAS
import pandas as pd
import numpy as np

from geopandas.array import points_from_xy
from geopandas.geodataframe import GeoDataFrame
import pyproj #para calcular distancias

import shapely as shp
from shapely.geometry import Point
import geopandas as gpd

import matplotlib.pyplot as plt
from matplotlib import cm

import folium
from folium import Marker, GeoJson, CircleMarker
from folium import plugins
from folium.plugins import HeatMap
from folium.map import *

import plotly.graph_objects as go


from tqdm import tqdm

def topoint(x):
    """para cargar los points como objetos de shapely"""
    if isinstance(x, list):
        return [shp.wkt.loads(point) for point in x] #si son listas
    else:
        return shp.wkt.loads(x)

#DF de geopandas con los contornos del mapa
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
sistema = world.crs
print(f'Estamos usando el sistema {sistema}')
#endregion
#%%
# region armo GeoDF
df = pd.read_pickle(
    "/home/ingrid/Documents/labodatos/TP_final/df_principal/df_principal.pkl"
).drop(
    columns=[
        "Africa",
        "Australia",
        "Eurasia",
        "North America",
        "South America",
        "Country_coord",
        "Country_lat",
        "Country_long",
        "Papunesia",
        "Country_name",
    ]
)

#quedaron de señas :()
boolean = df['Genus'].str.contains('Sign').fillna(False)
df = df.drop(df[boolean].index)

#Genero una columna Status numérico
stat_dict = {'6b Threatened':6.5, '4 Educational':4, '5 Developing':5,
       '3 Wider Communication':3, '10 Extinct':10, '2 Provincial':2,
       '8b Nearly Extinct':8.5, '6a Vigorous':6, '7 Shifting':7, '8a Moribund':8,
       '1 National':1, '9 Dormant':9.5, '9 Reawakening':9,
       '9 Second language only':9, '0 International':0}


df['num_status'] = df['Status'].replace(stat_dict)

#completo unos valores a mano
df.loc[[2294, 2295, 2296], "countryISO"] = "MEX"
df.loc[[2294, 2295, 2296], "point_cn"] = "Point(-102.0 23.0)"

# con geopd genero una coordenada/Point desde las dos columnas de lat/long
df["point_lang"] = gpd.points_from_xy(df["Longitude_lang"], df["Latitude_lang"], crs='epsg:4326')
df["num_speakers"] = df["num_speakers"].astype(int)


# y creo el geoDF
geodf = gpd.GeoDataFrame(df, geometry="point_lang")

#endregion
# %%
# region EJ: SUDAMERICA PLT

#genero el colormap discreto
cmap = cm.get_cmap('plasma_r', 11)

# para ver solo sudamerica
ax = world[world.continent == "South America"].plot(
    edgecolor="black", figsize=(10, 10),color='white'
)

#me quedo solo con la macroarea
area_select = geodf[geodf.Macroarea == "South America"]

#para plotear por tamaño
pointsize = geodf['num_speakers'].tolist()
pointsize = np.log(pointsize)*10

#ahora si ploteo
area_select.plot(
    ax=ax, marker="o", markersize=pointsize, alpha=0.5, column="num_status", legend=True,
    cmap=cmap
)

plt.show()
#endregion

#%%
#region NEAREST LANG

geod = pyproj.Geod(ellps = 'WGS84')

def lang_dist(lang1, lang2, geod = geod):
    lat_inicial = lang1.y # El eje y es la latitud
    long_inicial = lang1.x # El eje x es la longitud

    lat_final = lang2.y
    long_final = lang2.x

    un_angulo, otro_angulo, distancia =  geod.inv(lat_inicial,
                                                  long_inicial,
                                                  lat_final,
                                                  long_final)
    return distancia
#%%
#(aparte porque tarda mil años en correr)
lang = geodf['WALS_ID'].tolist()
dots = geodf['point_lang'].tolist()
nearest = []

n = 0
for i, dot1 in tqdm(enumerate(dots)):
    near = 0
    radius = 100_000 #en metros
    for j, dot2 in enumerate(dots):
        if i!=j:
            dist = lang_dist(dot1,dot2)
            if dist < radius:
                near +=1
    n +=1
    print(lang[i], near)
    nearest.append(near)
#endregion

#%%
#region FOLIUM MAP 2
cdanger = [6.5,7,8,8.5,9,9.5]
cext = 10
gdanger = geodf[df['num_status'].apply(lambda x: x in cdanger)]
gext = geodf[geodf.num_status == 10]
gsafe = geodf[geodf.Status_binario == 1]

m = folium.Map([-15.783333, -47.866667],
                  zoom_start=4,
                  tiles='cartodbpositron')

heatmap_layer = FeatureGroup(name='Heatmap')

HeatMap(data=gdanger[['Latitude_lang', 'Longitude_lang']], radius=15, min_opacity=0.4,
 blur = 10).add_to(heatmap_layer.add_to(m))


for idx, row in gdanger.iterrows():
    dot = CircleMarker([row['Latitude_lang'], row['Longitude_lang']], radius=3,
    tooltip = f"{gdanger.loc[idx,'Name']}, {gdanger.loc[idx,'Status']}",
    color='black')
    dot.add_to(m)

feature_group_safe = FeatureGroup(name='No amenazados', show=False)

for idx, row in gsafe.iterrows():
    dot = CircleMarker([row['Latitude_lang'], row['Longitude_lang']], radius=3,
    tooltip = f"{gsafe.loc[idx,'Name']}, {gsafe.loc[idx,'Status']}",
    color='black',
    alpha=0.5)
    feature_group_safe.add_child(dot)


feature_group_ext = FeatureGroup(name='Extintos')

for idx, row in gext.iterrows():
    dot = CircleMarker([row['Latitude_lang'], row['Longitude_lang']], radius=3,
    tooltip = f"{gext.loc[idx,'Name']}, {gext.loc[idx,'Status']}",
    color='black',
    alpha=0.5)
    feature_group_ext.add_child(dot)


m.add_child(feature_group_ext)
m.add_child(feature_group_safe)
m.add_child(folium.map.LayerControl())
#endregion
#%%
#region PLOTLY
#pointsize = geodf['num_speakers']
pointsize = np.log(geodf['num_speakers']+1)
geodf['numlog'] = pointsize

import plotly.express as px
fig = px.scatter_mapbox(geodf,
                        lat=geodf.geometry.y,
                        lon=geodf.geometry.x,
                        color="num_status", 
                        size="numlog",
                        color_continuous_scale=px.colors.cyclical.IceFire, 
                        size_max=15, 
                        hover_name='Name',
                        text=geodf['num_speakers'],
                        zoom=1)


fig.update_traces(hovertemplate=None)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

#fig.update_traces(hovertemplate=f'Número de hablantes: %{size}')

fig.show()


#fig.write_html("/home/ingrid/Documents/labodatos/TP_final/df_principal/geoloc/speakers_riesgo.html")
#%%
#region cosas
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
query_official = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/df_principal/query_final.csv')
df_test = world.copy()

mapita1 = query_official.set_index("countryISO").to_dict()["ISO"]
mapita1['USA'] = 'eng'
mapita1['MEX'] = 'spa'
df["official_lang_iso"] = df["Native_country_ISO"].replace(mapita1)


#%%
#cat = ['6b Threatened', '4 Educational', '5 Developing','6a Vigorous', '7 Shifting']
#df_cat = df[df['Status'].apply(lambda x: x in cat)]

idiso = pd.read_csv('/home/ingrid/Documents/labodatos/TP_final/df_principal/iso_to_id.csv')

mapid = idiso.set_index('countryID').to_dict()['countryISO']
mappbi = world.set_index("iso_a3").to_dict()["gdp_md_est"]

df['Native_country_ISO'] = df['Native_country'].replace(mapid).apply(lambda x: x.upper())

df['PBI_native'] = df['Native_country_ISO'].replace(mappbi)
# %%
mandar = df[['ISO','WALS_ID','Native_country','Native_country_ISO','PBI_native','official_lang_iso']]
mandar.to_csv('pbi_oficial_lang.csv')