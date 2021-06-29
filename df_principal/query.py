
#%%
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

endpoint_url = "https://query.wikidata.org/sparql"
user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
sparql = SPARQLWrapper(endpoint_url,agent=user_agent)
sparql.setReturnFormat(JSON)
#%%
query = """
SELECT DISTINCT ?country ?countryLabel ?language ?languageLabel ?ISO ?countryISO
WHERE
{
  ?country wdt:P37 ?language;
           wdt:P298 ?countryISO.
  ?language wdt:P220 ?ISO.
  ?country rdfs:label ?countryLabel . FILTER(lang(?countryLabel)='en')
  ?language rdfs:label ?languageLabel . FILTER(lang(?languageLabel)='en')
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
}
ORDER BY ?country
"""
#endregion
#%%
sparql.setQuery(query)
results = sparql.query().convert()
df = pd.json_normalize(results["results"]["bindings"])
df = df[[col for col in df.columns if 'value' in col]]
df = df.rename(columns = lambda col: col.replace(".value", ""))
#df.to_csv('query_final.csv')
# %%