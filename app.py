
from flask import Flask, render_template, request, url_for, redirect, flash
import pyodbc
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Configuración de la conexión a SQL Server
server = 'LAPTOP-PP6N1N88\SQLEXPRESS'
database = 'cereales'
username = 'sa'
password = 'artesanos10'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)


# Setting
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cursor = cnxn.cursor()
    cursor.execute('SELECT cereal, noOpiniones FROM opiniones')
    rows = cursor.fetchall()
    # Grafica de barras
    crear_grafica_barras = graficaBarras(rows)
    # Grafica de barras horizontal
    crear_grafica_barras_h = graficaBarrasHorizontal(rows)

    return render_template('index.html', datos = rows, chart_image=crear_grafica_barras, charth_image=crear_grafica_barras_h)


# Grafica de barras
def graficaBarras(rows):
    lista_x = []
    lista_y = []

    for row in rows:
        lista_x.append(row[0])
        lista_y.append(row[1])

        # Colores de las barras
    colores = ['#FB7506', '#E3CF0B', '#0B56E3']

        # Crear la gráfica de barras	
    plt.bar(lista_x, lista_y, color=colores)
    plt.xlabel('Cerelaes Preferidos')
    plt.ylabel('Número de votos por persona')
    plt.title('Cereales preferidos')
    plt.xticks(rotation=45)
    plt.tight_layout()

        # Guardar la gráfica en un archivo temporal
    image_path = 'static/bar_chart.png'
    plt.savefig(image_path)
    plt.close()

    return image_path

# Grafica de barras horizontal

def graficaBarrasHorizontal(rows):

    lista_x = []
    lista_y = []

    for row in rows:
        lista_x.append(row[0])
        lista_y.append(row[1])


    # Colores de la grafica
    colores = ['#FB7506', '#E3CF0B', '#0B56E3']

    plt.figure(figsize=(5, 2.5))  # Ancho x Alto en pulgadas

    plt.barh(lista_x, lista_y, color = colores)

        # Etiquetas y título
    plt.xlabel('Nuemero de Votos')
    plt.ylabel('Cereales')
    plt.title('Cereales preferidos')
    plt.tight_layout()



        # Guardar la gráfica en un archivo temporal
    image_path = 'static/bar_charth.png'
    plt.savefig(image_path)
    plt.close()

    return image_path


if __name__ == '__main__':
    app.run(port = 3000, debug = True)

