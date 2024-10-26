
import pandas as pd

def sacar_tabla(tabla_indiv, mercado, producto, variante):
    tr_tabla=tabla_indiv.findAll("tr")
    th_tabla = tabla_indiv.findAll("th")
    td_tabla=tabla_indiv.findAll("td")
    df_cuerpo=pd.DataFrame([r.findAll('td') for r in tr_tabla][1:]).map(lambda x: x.text)
    dicc_encabezado=dict(enumerate(pd.DataFrame(th_tabla).T.values[0]))  #enumerate porque coincide el 0,1 y 2 con los titulos de las columnas
    df_tabla= df_cuerpo.rename(dicc_encabezado, axis=1)
    df_tabla["supermercado"]= mercado
    df_tabla["producto"]= producto
    df_tabla["variante"]= variante
    return df_tabla


def crear_df_id (df, col):
    df_nuevo= pd.DataFrame(df[col])
    df_nuevo[f"id_{col}"]= pd.RangeIndex(start=1,stop = len(df_nuevo)+1,step=1)
    return df_nuevo



def añadir_id_mapeado(Df_diccionario, Columnadicc_nombre, Columnadicc_id, Columna_a_mapear, Nombre_nueva_col_id, Df_donde_mapear):
    diccionario_prod= {}
    datos = Df_diccionario.groupby(Columnadicc_nombre)[Columnadicc_id].first()
    datos_prod = list(datos.index)
    lista_prod = list(datos.values)
    for i in range(0, len(datos_prod)):
        diccionario_prod[datos_prod[i]] = lista_prod[i]

    Df_donde_mapear[Nombre_nueva_col_id] = Df_donde_mapear[Columna_a_mapear].map(diccionario_prod)

    Df_donde_mapear.drop(columns=Columna_a_mapear, inplace=True)
    return Df_donde_mapear