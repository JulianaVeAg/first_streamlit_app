import streamlit
import pandas

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

#Nueva sección para desplegar la respuesta de la api.
streamlit.header("Fruityvice Fruit Advice!")
import requests

fruityvice_respnse=requests.get("https://www.fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_respnse.json())

#Cogemos la versión json de la respuesa y la normalizamos.
fruityvice_normalized=pandas.json_normalized(fruityvice_respnse.json())






