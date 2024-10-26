
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline
import seaborn as sns

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


def datos_grafico_comparacion_max_min(ejex,ejey,hue,data,pallete,categoria_producto,distancia_datalabel):  
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20, 5), sharex=True, sharey=True)
    sns.boxplot(x= ejex, y= ejey, hue= hue, data=data, palette= pallete, ax = axes[0], capprops={'color':'purple'}) # para cambiar el color de los bigotes
    axes[0].set_title(f"Distribución del precio de la {categoria_producto} en distintos supermercados hoy")
    axes[0].set_xlabel("Supermercados")
    axes[0].set_ylabel("Precio")

    sns.barplot(x= ejex, y= ejey, hue= hue, data=data, palette= pallete, ax = axes[1])
    axes[1].set_title(f"Precio Medio de la {categoria_producto} por supermercado hoy")
    axes[1].set_xlabel("Supermercados")
    axes[1].set_ylabel("Precio Medio")
    for container in axes[1].containers:
        axes[1].bar_label(container, fmt="%.2f",  padding=distancia_datalabel) 



def datos_grafico_comparacion_max_minhist(ejex,ejey,hue,data,pallete,categoria_producto,distancia_datalabel):  
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20, 5), sharex=True, sharey=True)
    sns.boxplot(x= ejex, y= ejey, hue= hue, data=data, palette= pallete, ax = axes[0], capprops={'color':'purple'}) # para cambiar el color de los bigotes
    axes[0].set_title(f"Distribución del precio de la {categoria_producto} en distintos supermercados historico")
    axes[0].set_xlabel("Supermercados")
    axes[0].set_ylabel("Precio")

    sns.barplot(x= ejex, y= ejey, hue= hue, data=data, palette= pallete, ax = axes[1])
    axes[1].set_title(f"Precio Medio de la {categoria_producto} por supermercado historico")
    axes[1].set_xlabel("Supermercados")
    axes[1].set_ylabel("Precio Medio")
    for container in axes[1].containers:
        axes[1].bar_label(container, fmt="%.2f",  padding=distancia_datalabel) 




def grafico_evolucion_variacion_acumulada(ejex,ejey,hue,data,categoria_producto):
    plt.figure(figsize=(20,10))
    sns.lineplot(x= ejex, y= ejey, hue= hue, data=data, marker="x", linewidth = 1,palette="bright", style_order=data[1])
    plt.title(f"Evolución de la Variación acumulada del precio de la {categoria_producto} por supermercado")
    plt.xlabel("Tiempo")
    plt.ylabel(f"Variación del precio de la {categoria_producto}")        