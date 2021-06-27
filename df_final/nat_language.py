#%%
import pandas as pd
import numpy as np

#%%
df = pd.read_pickle("df_compĺeto.pkl")
#%%
query = (
    pd.read_csv("query_final.csv")
    .rename(
        columns={
            "countryISO": "official_in",
        }
    )
    .drop(columns=["language","country"])
)
lang_imploded = query.groupby(query["ISO"]).official_in.agg(list)
#%%
df2 = df.merge(lang_imploded, on="ISO", how="left")
df2.to_pickle('df_completo_2.pkl')
df2.to_csv('df_completo2.csv')