#%%
import pandas as pd
import webbrowser
path = 'archivo.pkl'
df = pd.read_pickle(path).reset_index()
#%%
df['num_speakers'].astype('float')
completar = df[df['num_speakers'].isna()]
yo = completar.loc[1253::] #el indice de ustedes
idiomas = yo.ISO.to_list()
df.set_index('ISO',inplace=True)
#%%
i = 0
for iso in idiomas:
    try:
        url = f'https://www.ethnologue.com/language/{iso}'
        webbrowser.open_new_tab(url)
        valor = input('Total de hablantes:')
        df.loc[iso,'num_speakers'] = float(valor)
        print(df.loc[iso,'num_speakers'])
        i += 1 
        if i%20 == 0:
            df.to_pickle('df_num_speakers_test_4.pkl')
    except KeyboardInterrupt:
        df.to_pickle('df_num_speakers_test_4.pkl')
        break

#%%
df.to_csv('aver.csv')
df.to_pickle('aver.pkl')
feo = 123456789