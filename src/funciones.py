
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