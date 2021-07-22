  
import streamlit as st
from PIL import Image
from src.my_functions import *
import plotly.express as px
import pandas as pd
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
import base64
import json



#CONFIGUARIÓN HTML
st.set_page_config(page_title= 'Restaurantes Spain', page_icon = 'fries', layout='wide', initial_sidebar_state='collapsed' )

hide_streamlit_style = '''
<style> 
#MainMenu {visibility: hidden;}
footer  {visibility: hidden;}
</style>
'''
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
  '''<style>
  .reportview-container .main .block-container {padding-top: 0px; padding-bottom: 0px;}
  </style>
  ''', unsafe_allow_html=True,
)



#HEADER  TITULOOOO
header = st.beta_columns((1,6,1))

with header[1]:
  st.write("""
  # TURISMO GASTRONÓMICO EN ESPAÑA 💃
  """)

  imagen = Image.open('./img/restaurante.JPG')
  st.image(imagen)
  # st.image('carpeta/nombreimage.jpg', caption='mensaje que queramos poner a la foto')


  title = '''
  <h1 style='text-align: center> Restaurantes de España </h1>
  '''
  st.markdown(title, unsafe_allow_html=True)






#DF - DAAATTAAAA
df = df_tripad()
df_international_food = df_international_food()
df_types_of_food = df_types_of_food()
geo_json = df_geojson()







#BODY - CITIESSS
body = st.beta_columns((3,4))
with body[0]:
  st.header('Comunidad Autónoma')
  lista_region = lista_region()
  region_name = st.selectbox('(1º FILTRO)', lista_region)
  #selector_kw = st.selectbox('tipo de comida', lista_kw)


  st.header('Provincia')
  get_province = df[(df.region_.str.contains(region_name))]
  get_list = get_province.province_.unique()
  province_names = st.selectbox('(2º FILTRO)', get_list) 
  #get_province = df[(df.region_.isin(region_name))]   PARA MULTISELECT - .isin RECIBE SOLO LISTAS


  st.header('Ciudad/Pueblo')
  get_city = df[(df.region_.str.contains(province_names))]
  get_list_city = get_province.city_village.unique()
  province_names = st.selectbox('(3º filtro a preferencia) - Puedes filtrar por  (city)', get_list_city) 




with body[1]:   # MAPA
  st.write('### Distribución Total de los Restaurantes en España')
  df_map = df[['latitude', 'longitude']].copy()
  st.map(df_map, zoom=4) 







st.info('''Pedimos disculpas anticipadas por la demora en la carga 
  de la aplicación. Estamos trabajando en Ello 🤓''')









# BODYYY  KEYWORDS
keyword_food_body1 = st.beta_columns((1,3,1,3,1,3))
with keyword_food_body1[0]:    #FOOD RAMDOM
  imagen_food = Image.open('./img/fast-food.png')
  st.image(imagen_food)
  food =  ['soups', 'seafood', 'steakhouse', 'sushi', 'grill', 'pizza']
  random_food = st.radio('', food)

  df_pizza = keep_palabra_clave('pizza')
  df_seafood = keep_palabra_clave('seafood')
  df_steakhouse = keep_palabra_clave('steakhouse')
  df_sushi = keep_palabra_clave('sushi')
  df_grill = keep_palabra_clave('grill')
  df_soups = keep_palabra_clave('soups')

with keyword_food_body1[1]: 
  df_wine_bar = keep_palabra_clave('wine_bar')

  archivo = codecs.open('mapa_soups.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)








with keyword_food_body1[2]:  #BEER  &  WINE
  imagen_food = Image.open('./img/drinks.png')
  st.image(imagen_food)
  beer_wine =  ['wine_bar', 'bar', 'pub', 'brew pub', 'gastropub',  'beer_restaurants']
  lover_beer_wine = st.radio('', beer_wine)

with keyword_food_body1[3]: 

  archivo = codecs.open('mapa_wine_bar.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)

  df_brew_pub = keep_palabra_clave('brew pub')
  df_bar = keep_palabra_clave('bar')
  df_pub = keep_palabra_clave('pub')
  df_gastro_pub = keep_palabra_clave('gastropub')
  df_beer_restaurants = keep_palabra_clave('beer_restaurants')







with keyword_food_body1[4]:  # HEALTHY FOOD
  imagen_food = Image.open('./img/diet.png')
  st.image(imagen_food)
  salud_food = ['vegetarian', 'vegan', 'gluten']
  healthy_food =  st.radio('', salud_food)

  df_vegetarian = keep_palabra_clave('vegetarian_friendly')
  df_vegan = keep_palabra_clave('vegan_options')
  df_gluten_free = keep_palabra_clave('gluten_free_options')

with keyword_food_body1[5]: 

  archivo = codecs.open('mapa_vegetarian.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)








keyword_food_body2 = st.beta_columns((1,3,1,3,1,3))
with keyword_food_body2[0]:   #  SPANISH FOOD
  imagen_food = Image.open('./img/paella.png')
  st.image(imagen_food) 
  spain_food = [ 'mediterranean', 'spanish']
  spanish_food = st.radio('', spain_food)

  df_spanish_food = keep_palabra_clave('spanish')
  df_mediterranean = keep_palabra_clave('mediterranean')

with keyword_food_body2[1]: 
  
  archivo = codecs.open('mapa_spanish.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)







with keyword_food_body2[2]:   #   FLASHH FASTTT FOODDD
  imagen_food = Image.open('./img/sandwich.png')
  st.image(imagen_food)
  street_food = [ 'street_food', 'quick_bites' ]
  fast_flash_food = st.radio('', street_food)

  df_quick_bites = keep_palabra_clave('quick_bites')
  df_street_food = keep_palabra_clave('street_food')

with keyword_food_body2[3]: 
  
  archivo = codecs.open('mapa_street_food.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)





  
  




with keyword_food_body2[4]:  # COFFEE TIME
  imagen_food = Image.open('./img/coffee-cup.png')
  st.image(imagen_food)
  amantes_del_dulce = ['dessert','cafe']
  coffee_time =  st.radio('', amantes_del_dulce)

  df_coffee = keep_palabra_clave('cafe')
  df_dessert = keep_palabra_clave('dessert')

with keyword_food_body2[5]: 
  df_wine_bar = keep_palabra_clave('wine_bar')
  archivo = codecs.open('mapa_coffee.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)







keyword_food_body3 = st.beta_columns((3,2,))
with keyword_food_body3[0]:   #ECONOMIC FOOD
  imagen_food = Image.open('./img/wallet.png')
  st.image(imagen_food)
  money_food = ['cheap_eats (comida bajo)', 'mid_range (precio medio)']
  my_economic_food =  st.radio('', money_food)

  df_cheaps_eats = keep_palabra_clave('cheap_eats')
  df_mid_range = keep_palabra_clave('mid_range')

with keyword_food_body2[1]: 
  archivo = codecs.open('mapa_money.html', 'r')
  mapa = archivo.read()
  components.html(mapa, width=270,height=270)








#  FOLIUMMMM



 # food =  ['pizza', 'seafood (mariscos)', 'steakhouse (asador)', 'sushi', 'grill (a la parrilla)', 'soups (sopas)']
  #random_food = st.radio('', food)
  #if lover_beer_wine == 'beer_restaurants':
   # mapa = mapa_kw(df_beer_restaurants, lover_beer_wine)
    #folium_static(mapa)
  #else:
   # pass









#st.balloons()
#st.info('This is a purely informational message')
#st.success('This is a success message!')


