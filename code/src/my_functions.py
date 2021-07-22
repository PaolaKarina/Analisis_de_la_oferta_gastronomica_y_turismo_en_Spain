import pandas as pd 
import re
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import plotly.express as px 
import json 

from streamlit_folium import folium_static
from branca.element import Figure

from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

import folium
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster



import codecs
import streamlit.components.v1 as components




#LIMPIEZA DATA TRIPADVISOR 

def porcentageROW(dataframe):
    return dataframe.isnull().sum(axis=1).apply(lambda x: x/dataframe.shape[1]).sort_values(ascending=False)

def porcentageCOL(dataframe):
    return dataframe.isnull().sum().apply(lambda x: x/dataframe.shape[0]).sort_values(ascending=False)

def dropping_col(dataframe):
    delete = ['working_shifts_per_week','open_hours_per_week', 'terrible', 'excellent', 'very_good', 
    'average', 'poor', 'keywords', 'awards', 'open_days_per_week', 'atmosphere', 'original_location']
    return dataframe.drop( axis=1, columns= delete, inplace=True)





def kw_column(dataframe,columns):
    """
    Creamos una lista única de las Keywords, de la columna que contenga strings, o una lista de strings
    y podamos categorizar esas keywords en 10.
    """
    d=list(dataframe[str(columns)].unique())
    de = [e for e in d if type(e) == str]
    dee = []
    for e in de:
        b = e.split(',')
        dee.append(b)
    lista = []
    for e in dee:
        for x in e:
            lista.append(x.strip())
    lista_unica_kw = set(lista)
    return lista_unica_kw



def contador_kw(dataframe,lista_kws, column):
    """
    Función para que me cuente cuantas veces aparece una Keyword (palabra clave) en cada fila, es decir,
    que me vaya sumando las filas cada vez que se encuentre con esa palabra clave y nos devuelva un diccionario. Así poder saber cuáles son las palabras(keywords) que más aparecen, quedarnos con las 9 más repetidas y 
    agrupar el resto de keywords en una sola.
    """
    lis= {}
    for kw in lista_kws:  #lista de keywords únicas 
        lis[kw]= 0
        for index, fila in dataframe.iterrows():  #dataframe (en este caso df2, que es el dataset limpio)
            if kw in str(fila[str(column)]): #al iterar nos aseguramos de que además de la fila sea la columna ('top_tags')
                lis[kw] += 1
            else:
                lis[kw] += 0
    return lis




def kw_sorted(dict_kw):
    """
    Devuelve el diccionario de las keywords ordenada por los valores de forma descendente
    """
    kw_count = dict(sorted(dict_kw.items(), key=lambda item: item[1], reverse=True))
    return kw_count 






#TABLAS TOTALES  SUMA TOTALES  DASHBOARDS

def dosistotal_Spain_Farma(df1):
    Moderna = df1.dosisEntregadasModerna.sum()
    Janssen = df1.dosisEntregadasJanssen.sum()
    Astrazeneca = df1.dosisEntregadasAstrazeneca.sum()
    Pfizer = df1.dosisEntregadasPfizer.sum()

    dic_farma = [ ('Dosis etregadas Moderna', Moderna), ('Dosis etregadas Janssen', Janssen), 
           ('Dosis etregadas Astrazeneca', Astrazeneca),('Dosis etregadas Pfizer', Pfizer)]

    dosis_Spain_Farma = pd.DataFrame(dic_farma)
    return dosis_Spain_Farma


def dosistotal_unadosis_dosiscompleta(df1):
    unadosis = df1.dosisPrimeraDosis.sum()
    pautacompleta = df1.dosisPautaCompletada.sum()

    list_dosis = [ ('Una dosis', unadosis), ('Dosis Completa', pautacompleta)]
    dosis_Spain_total = pd.DataFrame(list_dosis)
    return dosis_Spain_total















# GRÁFICAS  DOSIS x CCAA


def grafica_pfizer_moderna(df1):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1 = sns.barplot(y =df1.ccaa, x=df1.dosisEntregadasPfizer, ax= ax1, palette='dark:salmon_r')
    ax1.set_title('Dosis Entregadas PFISER - MILLONES', fontsize=14)
    ax1.set_ylabel('CCAA', fontsize=12)
    #ax1.set_xlabel(xmin=df1.dosisEntregadasPfizer[0], xmax=df1.dosisEntregadasPfizer[-1])

    ax2= sns.barplot(y =df1.ccaa, x=df1.dosisEntregadasModerna, ax= ax2, palette='mako')
    ax2.set_title('Dosis Entregadas MODERNA - MILES(vacunas)', fontsize=14)
    ax2.set_ylabel(' ')


    fig.suptitle('DOSIS ENTREGADAS DISTRIBUIDAS', fontsize=18)
    plt.show()


def grafica_aztrazeneca_janssen(df1):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1 = sns.barplot(y =df1.ccaa, x=df1.dosisEntregadasAstrazeneca, ax= ax1, palette='dark:salmon_r')
    ax1.set_title('Dosis Entregadas AZTRAZENECA - MILLONES', fontsize=14)
    ax1.set_ylabel('CCAA', fontsize=12)
    #ax1.set_xlabel(xmin=df1.dosisEntregadasPfizer[0], xmax=df1.dosisEntregadasPfizer[-1])

    ax2= sns.barplot(y =df1.ccaa, x=df1.dosisEntregadasJanssen, ax= ax2, palette='mako')
    ax2.set_title('Dosis Entregadas JANSSEN - MILES', fontsize=14)
    ax2.set_ylabel(' ')


    fig.suptitle('DOSIS ENTREGADAS DISTRIBUIDAS', fontsize=18)
    plt.show()   


def grafica_unadosis_dosiscompleta(df1):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 13))

    ax1 = sns.barplot(x =df1.ccaa, y=df1.dosisPrimeraDosis, ax= ax1, palette='Spectral')
    ax1.set_title('Spain - CCAA', fontsize=14)
    ax1.set_ylabel('PRIMERA DOSIS - MILLONES', fontsize=12)

    ax2= sns.barplot(x =df1.ccaa, y=df1.dosisPautaCompletada, ax= ax2, palette='coolwarm')
    ax2.set_title('Spain - CCAA', fontsize=14)
    ax2.set_ylabel('DOSIS COMPLETA - MILLONES', fontsize=12)

    fig.suptitle('DOSIS ADMINISTRADAS', fontsize=18)
    plt.show()

    




#GRAFICA DE TRIPADVISOR
def grafica_ccaa_total_tripAD(df):
    fig, ax = plt.subplots(1, 1, figsize=(27, 8))

    ax = sns.countplot(x=df.region, palette='viridis', )
    ax.set_title('CCAA', fontsize=14)
    fig.suptitle('NUMÉRO DE RESTAURANTES POR CCAA QUE APARECE EN TRIPADVISOR', fontsize=18)
    plt.show()



def grafica_comparativa_CCAA_tripYvacu(df_tablatotal_region_tripAd, df_tablatotal_region_vacunas):
    gridsize = (1, 2)
    fig = plt.figure(figsize=(20, 7))

    ax1 = plt.subplot2grid(gridsize, (0, 0))
    ax2 = plt.subplot2grid(gridsize, (0, 1))

    ax1= sns.barplot(y=('region'), x=('total restaurantes'), data=df_tablatotal_region_tripAd, ax= ax1)
    ax1.set_title('TOTAL RESTAURANTES')

    ax2 = sns.barplot(y=('ccaa'), x=('dosisAdministradas'), data=df_tablatotal_region_vacunas, ax= ax2)
    ax2.set_title('DOSIS ADMINISTRADAS (MILL)', fontsize=14)
    ax2.set_ylabel('CCAA', fontsize=12 )


    fig.suptitle('CCAA - COMPARATIVA TOTAL RESTAURANTES y TOTAL VACUNADOS', fontsize=18)
    plt.show()






def graficas_ratings(df):
    gridsize = (2,1 )
    fig = plt.figure(figsize=(20, 30))

    ax1 = plt.subplot2grid(gridsize, (0, 0))
    ax2 = plt.subplot2grid(gridsize, (1, 0))

    ax1= sns.countplot(y=df.region, hue=df.avg_rating, palette='Set1' ,ax= ax1)
    ax1.set_title('AVG RATING RESTAURANTS')
    ax1.legend(loc= 'center right', fontsize= 'xx-large')

    ax2 = sns.countplot(y=df.region, hue=df.food, palette='Set3' ,ax= ax2)
    ax2.set_title('FOOD SPAIN', fontsize=14)
    ax2.legend(loc= 'center right',fontsize= 'xx-large' )  #bbox_to_anchor=(0.5, 0.5), se queda en medio del todo

    plt.show()





#CARGA DATA


def data1():
    df1 = pd.read_csv('./DATA/data.CSV/df_tablatotal_region_restaurant.csv')
    return df1
def data2():
    df2 = pd.read_csv('df2_dosisEntregadas.csv')
    return df2
def data3():
    df3 = pd.read_csv('df3_unadosis.csv')
    return df3
def data4():
    df4 = pd.read_csv('df4_dosiscompleta.csv')
    return df4
def data5():
    df5 = pd.read_csv('df5_edades_unadosis.csv')
    return df5
def data6():
    df6 = pd.read_csv('df6_edades_unadosis.csv')
    return df6
def data():
    df = pd.read_csv('df_tripAd_Spain_Restaurants.csv') 
    return df
def table_trip():
    df_tablatotal_ccaa_tripAd = pd.read_csv('df_tablatotal_region_restaurant.csv')
    return df_tablatotal_ccaa_tripAd
def table_trip():
    df_tablatotal_ccaa_vacunas = pd.read_csv('df_tablatotal_region_vacunas.csv.csv')
    return df_tablatotal_ccaa_vacunas






# STREAMLIT



#  DATAFRAMES 
def df_tripad():
    data = pd.read_csv('df_tripAD_Spain.csv')
    return data

def df_international_food():
    df_international_food = pd.read_csv('df_international_food.csv')
    return df_international_food

def df_types_of_food():
    df_types_of_food = pd.read_csv('df_types_of_food.csv')
    return df_types_of_food

def df_geojson():
    df_geo = json.load(open('./DATA/spain-communities.geojson'))
    return df_geo













def lista_region():    
    data = df_tripad()  #data
    return data.region_.unique()

def lista_province(region):    
    data = df_tripad()  #data
    get_list_province = data[(data.region_ == region)]
    return list(get_list_province.province_.unique())










def kw_food():
    deli_food =  ['pizza', 'seafood', 'steakhouse', 'sushi', 'grill', 'soups']
    return deli_food

def kw_spanish_food():
    spanish_food = ['spanish', 'mediterranean']
    return spanish_food

def kw_street_food():
    street_food = [ 'quick_bites', 'street_food']
    return street_food

def kw_beer_wine():
    beer_wine =  ['brew pub', 'bar', 'pub', 'wine_bar', 'gastropub', ' dining_bars', 
    'beer_restaurants']
    return beer_wine

#healthy_food = ['vegetarian_friendly', 'healthy', 'vegan_options', 'vegetarian_friendly', 'gluten_free_options']

def kw_cafe_dessert():
    amantes_del_dulce = ['cafe', 'dessert', 'bakeries']

def kw_my_economic_food():
    cost_food = ['cheap_eats', 'mid_range']
    return cost_food








def keep_palabra_clave(palabra_clave):
    df_types_of_food = pd.read_csv('df_types_of_food.csv')
    df_bar = df_types_of_food[(df_types_of_food[f'{palabra_clave}'] == 1)].copy()
    return df_bar 


def mapa_kw(df_kw, col_kw):
    mapa = folium.Map(location= [40.463667,-3.74922], zoom_start = 5.5)
    folium_static(mapa)

    '''
    Conseguido el datframe del KW aplicar ese dataframe específico para que te 
    pinte en el mapa 
    '''

    
    for i,row in df_kw.iterrows():
        restaurants = {'location': 
                    [row['latitude'], row['longitude']],
                   'tooltip': row['restaurant_name']}

        if row[f'{col_kw}'] == 1:
            icono = Icon (color = "green",
                         prefix = "fa",
                         icon = "glass",
                         icon_color = "red")
        else: 
            pass

        marker = Marker(**restaurants, icon = icono)
        marker.add_to (mapa)

    return mapa