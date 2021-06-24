import pandas as pd
import webbrowser
path = 'C:\\Users\\eugen\\Documents\\GitHub\\TPfinal_LaboDatos'
df = pd.read_excel(path+'\\merged1.xlsx')
#%%
completar = df[df['num_speakers'].isna()]
yo = completar.loc[715:1253] #aca va los elementos que te corresponden
idiomas = yo.ISO.to_list()
indice = yo.index

#%%
i = 0
for j in range(len(idiomas)):
    iso = idiomas[j]
    numero = indice[j]
    try:
        url = f'https://www.ethnologue.com/language/{iso}'
        webbrowser.open_new_tab(url)
        valor = input('Total de hablantes:')
        df.loc[numero,'num_speakers'] = valor
        print(df.loc[numero,'ISO'])
        i += 1 
        if i%10 == 0:
            print('guardando...')
            df.to_csv('df_num_speakers_euge.csv')
#	     df.to_excel('df_num_speakers_euge.xlsx')
    except KeyboardInterrupt:
        print('guardando...')
        df.to_csv('df_num_speakers_euge.csv')
#	 df.to_excel('df_num_speakers_euge.xlsx')
        break

#OBS:GUARDAR TAMBIEN AL TERMINAR EL FOR

#%% Arreglar resultados

#df_completo_euge = pd.read_excel(path+'\\df_num_speakers_euge_terminado.xlsx')
#df_completo_euge_nuevo = df_completo_euge.copy()

columna = df_completo_euge['num_speakers'] 

for i in range(len(columna)):
    elemento = columna[i]
    if type(elemento) == str:
        if elemento[0] == '[':
            pass
        else:
            elemento_nuevo = elemento.replace(',', '') 
            df_completo_euge_nuevo['num_speakers'][i] = int(elemento_nuevo)
    else:
        pass
    
df_completo_euge_nuevo.to_excel('df_num_speakers_euge_arreglado.xlsx')    
        
    