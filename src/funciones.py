
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline
import seaborn as sns

def sacar_tabla(tabla_indiv, mercado, producto, variante):
    """
    Extrae datos tabulares de un elemento HTML de tabla y los organiza en un DataFrame con columnas adicionales.

    La función toma un elemento HTML que representa una tabla, extrae sus filas y encabezados, 
    y crea un DataFrame con la información tabular. Agrega columnas para identificar el supermercado,
    producto y variante correspondiente a los datos.

    Args:
        tabla_indiv (bs4.element.Tag): Un elemento BeautifulSoup que representa la tabla HTML a extraer.
        mercado (str): El nombre del supermercado al que pertenece la tabla.
        producto (str): El nombre del producto al que pertenece la tabla.
        variante (str): La variante del producto en la tabla.

    Returns:
        pd.DataFrame: Un DataFrame con los datos de la tabla HTML, incluyendo columnas adicionales:
            - 'supermercado': Nombre del supermercado.
            - 'producto': Nombre del producto.
            - 'variante': Variante del producto.
    """
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
    """
    Crea y devuelve un DataFrame con una columna específica y un ID único para cada fila.

    La función selecciona una columna de un DataFrame dado y genera un nuevo DataFrame que incluye
    la columna seleccionada y una columna adicional de IDs secuenciales.

    Args:
        df (pd.DataFrame): El DataFrame original del que se extraerá la columna.
        col (str): El nombre de la columna que se desea extraer y añadir al nuevo DataFrame.

    Returns:
        pd.DataFrame: Un DataFrame con dos columnas:
            - La columna especificada en el argumento 'col'.
            - 'id_{col}': Una columna con IDs únicos secuenciales para cada fila, que comienza en 1.
    """    
    df_nuevo= pd.DataFrame(df[col])
    df_nuevo[f"id_{col}"]= pd.RangeIndex(start=1,stop = len(df_nuevo)+1,step=1)
    return df_nuevo



def añadir_id_mapeado(Df_diccionario, Columnadicc_nombre, Columnadicc_id, Columna_a_mapear, Nombre_nueva_col_id, Df_donde_mapear):
    """
        Añade una columna de IDs mapeados a un DataFrame basado en otra columna que se reemplaza.

        La función toma un DataFrame de diccionario de referencia y crea un diccionario de mapeo entre nombres y 
        sus correspondientes IDs. Luego, utiliza este mapeo para agregar una columna de ID en otro DataFrame,
        reemplazando la columna original con la nueva columna de IDs.

        Args:
            Df_diccionario (pd.DataFrame): DataFrame de referencia que contiene la relación entre nombres y sus IDs.
            Columnadicc_nombre (str): Nombre de la columna en `Df_diccionario` que contiene los nombres a mapear.
            Columnadicc_id (str): Nombre de la columna en `Df_diccionario` que contiene los IDs.
            Columna_a_mapear (str): Nombre de la columna en `Df_donde_mapear` que será reemplazada por la columna de IDs.
            Nombre_nueva_col_id (str): Nombre de la nueva columna de IDs que se añadirá al DataFrame de destino.
            Df_donde_mapear (pd.DataFrame): DataFrame en el que se añadirá la columna de IDs mapeados.

        Returns:
            pd.DataFrame: El DataFrame `Df_donde_mapear` con la columna de IDs mapeados añadida y la columna original reemplazada.
    """    
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
    """
    Crea gráficos de comparación para la distribución y el precio medio de un producto en distintos supermercados.

    La función genera dos gráficos en una figura con dos subgráficas: un boxplot que muestra la distribución de precios y un barplot que muestra el precio medio.
    Agrega etiquetas a cada barra en el gráfico de barras para indicar los valores medios.

    Args:
        ejex (str o int): Nombre de la columna del DataFrame que se utilizará en el eje X para ambos gráficos.
        ejey (str o int): Nombre de la columna del DataFrame que se utilizará en el eje Y para ambos gráficos.
        hue (str o int): Nombre de la columna que define el factor de color para diferenciar los datos en ambos gráficos.
        data (pd.DataFrame): DataFrame que contiene los datos a visualizar en los gráficos.
        pallete (str or list): Paleta de colores para los gráficos.
        categoria_producto (str): Categoría del producto para el título de los gráficos.
        distancia_datalabel (int): Distancia entre la etiqueta de la barra y la barra en el gráfico de barras.

    Returns:
        None: La función muestra la figura con dos subgráficas, un boxplot y un barplot, comparando la distribución de precios y los precios medios por supermercado.
    """      
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
    """
    Crea gráficos históricos de comparación para la distribución y el precio medio de un producto en distintos supermercados.

    La función genera una figura con dos subgráficas: un boxplot para visualizar la distribución de precios y un barplot para mostrar
    el precio medio en diferentes supermercados en un contexto histórico. Se añaden etiquetas de valor en el gráfico de barras.

    Args:
        ejex (str o int): Nombre de la columna que representa el eje X en ambos gráficos.
        ejey (str o int): Nombre de la columna que representa el eje Y en ambos gráficos.
        hue (str o int): Nombre de la columna que se usará para diferenciar los datos por color en ambos gráficos.
        data (pd.DataFrame): DataFrame que contiene los datos de precios a visualizar.
        pallete (str or list): Paleta de colores para los gráficos.
        categoria_producto (str): Nombre de la categoría del producto para usar en los títulos de los gráficos.
        distancia_datalabel (int): Distancia entre las etiquetas de datos y las barras en el gráfico de barras.

    Returns:
        None: La función muestra una figura con dos subgráficas (boxplot y barplot) que comparan la distribución de precios
        y el precio medio de un producto en distintos supermercados a lo largo del tiempo.
    """  
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
    """
    Crea un gráfico de líneas que muestra la evolución de la variación acumulada del precio de un producto por supermercado a lo largo del tiempo.

    La función genera un gráfico de líneas para visualizar la tendencia de precios acumulada, permitiendo observar cómo los precios varían
    en diferentes supermercados para la categoría de producto especificada.

    Args:
        ejex (str o int): Nombre de la columna que representa el eje X (generalmente la variable de tiempo).
        ejey (str o int): Nombre de la columna que representa el eje Y (variación acumulada de precios).
        hue (str o int): Nombre de la columna que se usará para diferenciar las líneas por color según cada supermercado.
        data (pd.DataFrame): DataFrame que contiene los datos de precios a visualizar en el gráfico.
        categoria_producto (str): Nombre de la categoría del producto, para su inclusión en el título y etiquetas del gráfico.

    Returns:
        None: La función muestra un gráfico de líneas que representa la evolución de la variación acumulada de precios por supermercado.
    """    
    plt.figure(figsize=(20,10))
    sns.lineplot(x= ejex, y= ejey, hue= hue, data=data, marker="x", linewidth = 1,palette="bright", style_order=data[1])
    plt.title(f"Evolución de la Variación acumulada del precio de la {categoria_producto} por supermercado")
    plt.xlabel("Tiempo")
    plt.ylabel(f"Variación del precio de la {categoria_producto}")        




def grafico_evol_precio_medio(ejex,ejey,hue,data,categoria_producto):
    """
    Crea un gráfico de líneas que muestra la evolución de los precios medios de un producto por supermercado a lo largo del tiempo.

    La función genera un gráfico de líneas para visualizar cómo varían los precios medios en distintos supermercados para la categoría
    de producto especificada, permitiendo observar tendencias de precios a lo largo del tiempo.

    Args:
        ejex (str o int): Nombre de la columna que representa el eje X (usualmente la variable de tiempo).
        ejey (str o int): Nombre de la columna que representa el eje Y (precio medio).
        hue (str o int): Nombre de la columna que se usará para diferenciar las líneas por color según cada supermercado.
        data (pd.DataFrame): DataFrame que contiene los datos de precios medios a visualizar en el gráfico.
        categoria_producto (str): Nombre de la categoría del producto, para su inclusión en el título y etiquetas del gráfico.

    Returns:
        None: La función muestra un gráfico de líneas que representa la evolución de los precios medios del producto en distintos supermercados.
    """  
    plt.figure(figsize=(20,10))
    sns.lineplot(x= ejex, y= ejey, hue= hue, data=data, marker="D", linewidth = 1,palette="bright", style_order=data[1])
    plt.title(f"Evolución de los precios medios de la {categoria_producto} por supermercado")
    plt.xlabel("Tiempo")
    plt.ylabel(f" Precio medio de la {categoria_producto}")  



def grafica_anomalias(ejex,ejey,hue,data,categoria_producto):
    """
    Genera un gráfico de líneas que muestra la evolución de las anomalías en la variación del precio de un producto en distintos supermercados.

    Esta función visualiza las anomalías en los precios, permitiendo identificar patrones inusuales de variación en el tiempo para 
    la categoría de producto especificada y en cada supermercado representado.

    Args:
        ejex (str o int): Nombre de la columna que representa el eje X (generalmente la variable de tiempo).
        ejey (str o int): Nombre de la columna que representa el eje Y (variación de precios).
        hue (str o int): Nombre de la columna que se usará para diferenciar las líneas de cada supermercado por color.
        data (pd.DataFrame): DataFrame que contiene los datos de variación de precios a visualizar en el gráfico.
        categoria_producto (str): Nombre de la categoría del producto, utilizado en el título y etiquetas del gráfico.

    Returns:
        None: La función muestra un gráfico de líneas que representa la evolución de las anomalías de precios por supermercado.
    """
    plt.figure(figsize=(20,10))
    sns.lineplot(x= ejex, y= ejey, hue= hue, data=data, marker="D", linewidth = 1,palette="bright", style_order=data[1])
    plt.title(f"Evolución de las Anomalias de la variacion del precio de {categoria_producto} por supermercado")
    plt.xlabel("Tiempo")
    plt.ylabel(f"Variación del precio de {categoria_producto}")   