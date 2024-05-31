# -*- coding: utf-8 -*-
"""
Created on Fri May 31 11:21:25 2024

@author: jperezr
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import numpy as np

def main():
    st.title("Mapa con marcadores, color (rojo para los puntos del modelo de Huff y color azul para los puntos de las AFORE). Las lineas rectas indican la ruta de inicio y fin del modelo de Huff")

    # Datos de ejemplo (latitud, longitud y datos adicionales)
    data1 = {
        'Ciudad': ['LAS VEGAS-NEVADA', 'Tasquillo-Hidalgo','Panotla-Tlaxcala','San Pedro Muñoztla-Tlaxcala','Santa María Ixtulco-Tlaxcala', 'Calle Cedros 727M-Ocotlán-Tlaxcala', 'Av. Río Zahuapan 11b. Magisterial Vista Hermosa-Ocotlán-Tlaxcala'],
        'Latitud': [36.17866749, 20.52818507, 19.41292288, 19.29159211, 19.32766793, 19.32176177, 19.32032898],
        'Longitud': [-115.1647118, -99.39527522, -98.28111232, -98.17585557, -98.21091921, -98.21898739, -98.21990222],
        'Iteracion': ['punto inicial', 'iteración 1', 'iteración 2', 'iteración 3', 'iteración 4', 'iteración 5', 'iteración 6'],
        #'Poblacion': [1000000, 1500000, 800000],
        #'Area (km^2)': [500, 700, 400]
    }
    
    
    data2 = {
        'Ciudad': ['INBURSA', 'PROFUTURO', 'INVERCAP','COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'COPPEL', 'CITIBANAMEX', 'XXI-BANORTE', 'XXI-BANORTE', 'AZTECA', 'PENSIONISSSTE'],
        'Latitud': [19.3239078, 19.3203195, 19.4147072, 19.3131517, 19.3209611, 19.3108404, 19.3180202, 19.3129672, 19.4146574, 19.2159175, 19.3126161, 19.5897488, 19.3321904, 19.3170278, 19.3252766, 19.3185363, 19.3162847, 19.3246045],
        'Longitud': [-98.2318888, -98.2077986, -98.1372056, -98.1956906, -98.2361297, -97.9251893, -98.2212896, -98.1943367, -98.1404313, -98.2417004, -97.9222558, -98.5771895, -98.1953276, -98.2186318, -98.2285625, -98.2363375, -98.2468713, -98.2339656],
        'Comentario': ['punto dado', 'punto dado',  'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado', 'punto dado'],
}

    # Combinar ambos conjuntos de datos en uno solo
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df = pd.concat([df1, df2], ignore_index=True)

    # Mostrar los datos en una tabla
    st.subheader("Datos:")
    st.write(df)

    # Crear el mapa con Folium
    map_center = [df['Latitud'].mean(), df['Longitud'].mean()]
    my_map = folium.Map(location=map_center, zoom_start=4)
    
    
    # Añadir marcadores al mapa para el primer conjunto de datos
    for i, row in df1.iterrows():
        popup_html = f"""
        <b>{row['Ciudad']}</b><br>
        Iteracion: {row['Iteracion']}<br>
        """
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Ciudad'],
            icon=folium.Icon(color='red')  # Cambiar el color del marcador aquí
        ).add_to(my_map)

    # Añadir marcadores al mapa para el segundo conjunto de datos
    for i, row in df2.iterrows():
        popup_html = f"""
        <b>{row['Ciudad']}</b><br>
        Comentario: {row['Comentario']}<br>
        """
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['Ciudad'],
            icon=folium.Icon(color='blue')  # Cambiar el color del marcador aquí
        ).add_to(my_map)
    
    
# Cambiar el color del tercer marcador del primer conjunto de datos a verde
    df1_index = 6  # Índice del marcador dentro del primer conjunto de datos
    folium.Marker(
        location=[df1.iloc[df1_index]['Latitud'], df1.iloc[df1_index]['Longitud']],
        popup=folium.Popup(f"<b>{df1.iloc[df1_index]['Ciudad']}</b><br>Iteracion: {df1.iloc[df1_index]['Iteracion']}<br>", max_width=300),
        tooltip=df1.iloc[df1_index]['Ciudad'],
        icon=folium.Icon(color='black')  # Cambiar el color del marcador aquí
    ).add_to(my_map)
   


# Cambiar el color del tercer marcador del segundo conjunto de datos a verde
    df2_index = 17  # Índice del marcador dentro del segundo conjunto de datos
    folium.Marker(
        location=[df2.iloc[df2_index]['Latitud'], df2.iloc[df2_index]['Longitud']],
        popup=folium.Popup(f"<b>{df2.iloc[df2_index]['Ciudad']}</b><br>Comentario: {df2.iloc[df2_index]['Comentario']}<br>", max_width=300),
        tooltip=df2.iloc[df2_index]['Ciudad'],
        icon=folium.Icon(color='green')  # Cambiar el color del marcador aquí
    ).add_to(my_map)
   
    
    
    
 
# Trazar líneas rectas que unen las ciudades
    colors = ['black', 'black', 'black', 'black', 'black', 'black', '']
    for i, row in df1.iterrows():
        folium.PolyLine(
            locations=[[df1.iloc[i]['Latitud'], df1.iloc[i]['Longitud']], 
                       [df1.iloc[(i+1)%len(df1)]['Latitud'], df1.iloc[(i+1)%len(df1)]['Longitud']]],
            color=colors[i],
            weight=2,
            tooltip=f"Línea de {row['Ciudad']} a {df.iloc[(i+1)%len(df)]['Ciudad']}"
        ).add_to(my_map)

    # Renderizar el mapa usando Streamlit y centrarlo
    folium_static(my_map, width=1800, height=1200)

    # Centrar el mapa utilizando estilos CSS
    st.markdown(
        """
        <style>
        .css-10jc7uw {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )    
    
    
    


if __name__ == "__main__":
    main()