import pandas as pd
import numpy as np

#carga del archivo de excel ---> Cargar la hoja BD
df = pd.read_excel('BD_covid19.xlsx',['BD'])['BD']
df_m = df[df.EDAD_ANO.isin(['50'])]
print(df_m)

#Tarea: contruit tabla de comorbilidades (estan en excel) vs no comorbilidades, como muestra el excel
# de BloqueNeon. Para hombres y mujeres mayores de 50 años.

