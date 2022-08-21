import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError


streamlit.title('My parents new Healthy diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 and Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach and rocket smoothie')
streamlit.text('🐔Hard_Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 make your own fruit smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Vamos a poner una lista para que puedan elegir la fruta que desean.

fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Banana', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show) 


#Creamos una función:

def get_fruityvice_data(this_fruit_choise):
  fruityvice_response=requests.get("https://www.fruityvice.com/api/fruit/" + this_fruit_choise)
  fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


  
#Nueva sección para desplegar la respuesta de la api.
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information")
 else:
  back_from_function= get_fruityvice_data(fruit_choice)
  streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
    

streamlit.write('The user entered ', fruit_choice)

#NO ejecutaremos nada pasado aquí mientras haya problemas.
#streamlit.stop()


streamlit.header("The fruit load list contains:")
#Funciones de snowflake
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()
  
#Añadir un botón para guardar la fruta
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)






#Terminamos la lista añadiendo una fruta a la lista.

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from_streamlit')")
    return 'Thanks for adding ' + new_fruit
    

add_my_fuit= streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function= insert_row_snowflake(add_my_fuit)
  streamlit.text(back_from_function)
  









