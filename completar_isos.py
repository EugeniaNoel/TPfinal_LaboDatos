#%%
import pandas as pd
import numpy as np
#%%
wals = pd.read_csv('WALS_completo.csv').rename(columns={'Unnamed: 0':'WALS_ID'})
wals_apics = pd.read_csv('wals_apics.csv')
langindex = pd.read_csv('LanguageIndex.tab', sep='\t')
langcode = pd.read_csv('LanguageCodes.tab',sep='\t').set_index('LangID')
country = pd.read_csv('CountryCodes.tab',sep='\t')
#%%
#Armo df con solo los idiomas y sus codigos

lang_wals = wals[['WALS_ID','Name','ISO_codes','ISO639P3code','Country_ID','Family','Subfamily']].rename(
            columns={'Name':'WALS_name',
             'ISO_codes':'ISO','ISO639P3code':'ISO639P3', 'Country_ID':'CountryID'})

lang_iso = langindex.rename(columns={'LangID':'ISO','Name':'Eth_name'}).set_index('ISO')
sin_isos = lang_wals[lang_wals['ISO'].isna()].set_index('WALS_ID')
lang_wals.set_index('WALS_ID',inplace=True)
wals.set_index('WALS_ID',inplace=True)
#%%
#Para buscar entradas que contengan el string del nombre del idioma
def namesearch(wals_name):
    return lang_iso[lang_iso['Eth_name'].str.contains(wals_name)]
#%%
#lenguajes de señas
sgs = lang_wals[lang_wals['WALS_name'].str.contains('Sign')]
sgs_index = sgs.index.values

sgn = {lang:1 for lang in sgs_index}
# %%
"""Separe los nombres con espacio y busque en el DF de isos entradas que coincidan
Guarde todo lo que coincidia en un diccionario con clave para cada codigo"""

lista = sin_isos['WALS_name'].str.split(' ').to_list()
ids = sin_isos.index.to_list()
isos = {}
nombre = {}
for idx,idioma in enumerate(lista):
    isos[ids[idx]] = namesearch(idioma[0])
    nombre[ids[idx]] = lang_wals.loc[ids[idx]]

#%%
#aca voy a ir poniendo los id a iso para despues cambiarlos en el DF
id_to_iso = {}

#los que tengan un valor univoco los reemplazo de una, sino lo miro a mano en revisar
revisar = [] 
nf = []
for k,v in isos.items():
    if v.shape[0] == 1:
        id_to_iso[k] = v.index.item()
    elif v.shape[0]> 1:
        revisar.append(k)
    elif v.shape[0] == 0:
        nf.append(k)
#%%
#aca estoy mirando a mano todos los que no tenian un valor unico .-.
#region #A OJO
id_to_iso['aab'] = 'aah'
id_to_iso['cco'] = 'coq'
id_to_iso['cuc'] = 'NF'
id_to_iso['kdg'] = 'kuq'
id_to_iso['hok'] = 'zgm'
id_to_iso['kdg'] = 'knt'
namesearch('Uma’ Lung')
id_to_iso['keu'] = 'ulu'
id_to_iso['kfc'] = 'rop'
id_to_iso['lul'] = 'ule'
namesearch('Khamnigan')
id_to_iso['mkh'] = 'evn'
id_to_iso['mkw'] = 'xak'
namesearch('Pochutla')
id_to_iso['nhp'] = 'ztp'
namesearch('Huauchinango')
id_to_iso['nhu'] = 'tqt'
id_to_iso['rse'] = 'rmn'
id_to_iso['smp'] = 'sii'
id_to_iso['tms'] = 'dto'
id_to_iso['wdo'] = 'ntj'
id_to_iso['yyg'] = 'xya'
id_to_iso['ksn'] = 'syo'
id_to_iso['mcc'] = 'omc'
id_to_iso['mbb'] = 'vmb'
id_to_iso['bfg'] = 'grr'
id_to_iso['nhp'] = 'nhn'
id_to_iso['nmp'] = 'nhn'
id_to_iso['mdm'] = 'dmd'

ext = {'yrm': 'X',
 'alc': 'X',
 'ayo': 'X',
 'bti': 'X',
 'clc': 'X',
 'esm': 'X',
 'mcc': 'X',
 'mpr': 'X',
 'rcp': 'X',
 'toy': 'X',
 'tsm': 'X',
 'tup':'X',
 'mdm':'X',
 'abi':'X'}

sgn['lgh'] = 1 
sgn['isl'] = 1
sgn['hsl'] = 1
#endregion
# %%
wals['Status'] = np.nan
wals['Lenguaje de Señas'] = 0

for id, iso in id_to_iso.items():
    wals.loc[id,'ISO_codes'] = iso

for id, sg in sgn.items():
    wals.loc[id,'Lenguaje de Señas'] = sg
#%%
for id in wals.index.values:
    try:
        iso = wals.loc[id,'ISO_codes']
        wals.loc[id,'Status'] = langcode.loc[iso,'LangStatus']
    except:
        continue

for id, extn in ext.items():
    wals.loc[id,'Status'] = extn

# %%
wals_con_isos = wals[['ISO_codes','Name','Macroarea','Country_ID','Latitude','Longitude',
                    'Family','Genus','Lenguaje de Señas','Status']].rename(columns={'ISO_codes':'ISO'}).reset_index()
# %%
wals_con_isos.to_csv('ISO_completos.csv',index=False)
# %%
wals_guardar = wals.drop(columns=['GenusIcon','ISO639P3code']).rename(columns={'ISO_codes':'ISO'}).reset_index()
wals_guardar.to_csv('ISO_completos_features.csv',index=False)