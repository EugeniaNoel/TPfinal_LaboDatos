#%%
from geopandas.array import points_from_xy
import pandas as pd
import numpy as np
import shapely as shp
import geopandas as gpd
import matplotlib.pylab as plt
from matplotlib import cm
from shapely.geometry import Point

# Hay que normalizar num de habitantes para el gradiente de color, no lo hice aun
from sklearn import preprocessing


def topoint(x):
    """para cargar los points como objetos de shapely"""
    if isinstance(x, list):
        return [shp.wkt.loads(point) for point in x]
    else:
        return shp.wkt.loads(x)


#%%
# region armar geodfs
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

# con geopd genero una coordenada desde las dos columnas de lat/long
df["point_lang"] = gpd.points_from_xy(df["Longitude_lang"], df["Latitude_lang"])
df["num_speakers"] = df["num_speakers"].astype(int)


# para graficar puntos necesito un df a la vez, armo uno para native:
geodf_native = gpd.GeoDataFrame(df, geometry="point_lang").drop(
    columns=["Latitude_lang", "Longitude_lang"]
)

# el de externos necesito modificarlo, para tener un punto por pais:
# tengo que explotar el df para tener una coordenada por cada pais donde se habla el idioma

# query de la coord de cada pais por ISO
query = pd.read_csv(
    "/home/ingrid/Documents/labodatos/TP_final/df_principal/geoloc/query_coord.csv"
).drop(columns=["countryLabel", "country"])

# para mapear la coordenada al pais
mapita = query.set_index("countryISO").to_dict()["point_cn"]

df2 = df.explode("countryISO").drop(columns="point_lang")

# un dato que cambie a mano porque me rompia todo
df2.loc[[2294, 2295, 2296], "countryISO"] = "MEX"
df2.loc[[2294, 2295, 2296], "point_cn"] = "Point(-102.0 23.0)"


df2["point_cn"] = df2["countryISO"].replace(mapita)
df2["point_cn"] = df2["point_cn"].apply(topoint)

geodf_ext = gpd.GeoDataFrame(df2, geometry="point_cn")

# %%
# region MAPA LATINOAMERICA SOLO NATIVOS

# los contornos de los paises los cargo de un df que viene con gpd
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# para ver solo sudamerica
ax = world[world.continent == "South America"].plot(
    edgecolor="black", figsize=(10, 10), column="name", cmap="Greens"
)

# We can now plot our ``GeoDataFrame``.
area_select = geodf_native[geodf_native.Macroarea == "South America"]

area_select.plot(
    ax=ax, marker="o", markersize=15, alpha=0.5, column="num_speakers", legend=True
)

plt.show()
# endregion
#%%
# region MUNDIAL MARCANDO DE DONDE ES C.IDIOMA (no funca porque se solapan los puntos)
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

# We restrict to South America.
ax = world.plot(edgecolor="black", figsize=(10, 10), column="continent")

# We can now plot our ``GeoDataFrame``.
geodf_ext.plot(ax=ax, column="Native_country", marker="o", markersize=15, alpha=0.5)

plt.show()
# endregion
#%%
# region MAPA NORTEAMERICA NAVITOS + EXT

# We restrict to South America.
ax = world[world.continent == "North America"].plot(
    edgecolor="black", figsize=(8, 8), color="white"
)

# We can now plot our ``GeoDataFrame``.
area_select = geodf_native[geodf_native.Macroarea == "North America"]

area_select.plot(
    ax=ax,
    marker="o",
    markersize=30,
    alpha=0.5,
    column="num_speakers",
    cmap="plasma_r",
    legend=True,
    legend_kwds={"shrink": 0.3},
)

externos = geodf_ext[geodf_ext.Macroarea == "North America"]
externos.plot(ax=ax, marker="o", color="red")

plt.show()
# endregion
# %%
ax = world[world.continent == "Africa"].plot(
    edgecolor="black", figsize=(8, 8), color="white"
)


area_select = geodf_native[geodf_native.Macroarea == "Africa"].sort_values(
    "num_speakers"
)

area_select.plot(
    ax=ax,
    marker="o",
    markersize=30,
    alpha=0.3,
    column="num_speakers",
    cmap="plasma_r",
    legend=True,
)

# externos = geodf2[geodf2.Macroarea == "Europe"]
# externos.plot(ax=bordes, marker='o',color='black')

plt.show()
# %%
