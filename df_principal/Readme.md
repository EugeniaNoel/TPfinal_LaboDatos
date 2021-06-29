## DF principal

Acá están todos los archivos y pasos necesarios para armar el DF desde el primer merge hasta lo último que tenemos. La idea es que todas usemos el mismo (df_principal) y elijamos las columnas que queremos para cada cosa.

## merge_to_final.py:
Tiene todos los pasos desde el primer merge que hice con los datos de wals, las modificaciones que hicieron después, feature de euge, status binario, etc.
Pero junte todo, lo fui corriendo desde el primer merge y limpiandolo. Había muchos puntos donde empezabamos a usar DF distintos, ahí cuando lo juntabamos se rompía todo.
El DF tiene muchas columnas, no quise sacar nada por las dudas.

También me fuí bastante atrás para recuperar esas columnas desde cero, en vez de agregarlas después y mezclar índices.

El problema del merge fue que en una de las versiones no habíamos sacado idiomas de señas, entonces tenía mas filas que la otra. Además, en una versión
sacamos las columnas del nombre, ID, etc que servían para identificarlo.
Entonces al mergearlo, los índices numéricos no servían pero el ISO tampoco... porque no son valores únicos los ISO.
Ahí se mezcló todo. Ahora lo arreglé y por lo que pude ver eso funciona bien.

En num speakers quedaron 90 nans que no estaban en ninguno de los que completamos. Si completan eso pasenmelo que lo actualizo acá.

Si ven algo raro, traten de modificar el código del .py asi corriendo eso todas tenemos el mismo DF.
