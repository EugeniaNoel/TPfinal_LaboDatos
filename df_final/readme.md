# DF versión final
Los que dicen *parcial* tienen solo las features que habíamos dejado hasta esta semana

Los que dicen *completo* tienen status de ethnologue, país de origen, todas las coord. y otras features que por ahora no usamos pero para no perder la info.
Además tienen la feature que armó Euge.

Le cambié un poco los nombres porque me pareció que sino confundía que era cada cosa. Tipo countryID y countryISO, uno era el nativo y otro las listas. Así que le puse native country a countryID. 

Está el pkl para poder usar las listas y sino el csv.

Cuando haga la parte geográfica lo voy a hacer en otra carpeta, asi no mezclamos todo y aca queda solo el DF.

## Oficial_en:
Tiene el o los paises donde el idioma es un idioma oficial. Si no es en ninguno tiene un NaN, si es más de uno es una lista.
Los países figuran con su código ISO de 3 letras

## Native_country:
El país de origen del idioma (según WALS)

## Family/Genus:
Para agrupar idiomas según características comunes. Es lo de la foto del grupo de whatsapp.

## Nearest_languages:
La feature que armó Euge de cuantos idiomas tiene cerca
