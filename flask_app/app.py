import csv
import codecs 
import algoritmo

from io import StringIO
# also importing the request module
from flask import Flask, render_template, request, jsonify, flash
from tupla import Tupla
from nodo import Nodo

headers = ['Solucion','Inicio','Fin','Archivo Entrada', 'Criterio Finalización','Criterio Padres','Generaciones',]

app = Flask(__name__)
app.debug = True

mejor_solucion = Nodo()
modelo_generado = False
# # home route
@app.route("/", methods=['GET', 'POST'])

# serving form web page
@app.route("/practica1", methods = ['GET', 'POST'])
def form():
    global mejor_solucion
    if request.method == 'GET':
           return render_template('index.html', headers=headers)
       
    if request.method == 'POST':
        if request.form['submit_button'] == "Generar modelo":
            archivo = request.files['loadFile']
            criterioFin = int(request.form.get('criterioFin'))
            criterioPadres = int(request.form.get('criterioPadres'))
            gen = request.form.get('gen')
            pob = request.form.get('pob')
            if not gen:
                error = 'Ingrese el máximo de generaciones'
                return render_template('index.html', errorG = error)
            if not pob:
                error = 'Ingrese la cantidad'
                return render_template('index.html', errorG = error)
            if not archivo or archivo.filename == '':
                error = 'Ingrese el archivo de entrada CSV'
                return render_template('index.html', errorG = error)
            if criterioFin == 0:
                error = 'Debe seleccionar un criterio de finalización'
                return render_template('index.html', errorG = error)
            if criterioPadres == 0:
                error = 'Debe seleccionar un criterio selección de padres'
                return render_template('index.html', errorG = error)
            
            fstring = StringIO(archivo.read().decode())    
            archivoEntrada = csv.DictReader(fstring, delimiter=',')
            # Numero de filas                
            datoscsv = []
            for linea in archivoEntrada:
                nuevaTupla = Tupla(int(linea['PROYECTO 1']),int(linea['PROYECTO 2']),int(linea['PROYECTO 3']),int(linea['PROYECTO 4']), float(linea['NOTA FINAL']))
                datoscsv.append(nuevaTupla)

            mejor_solucion = algoritmo.ejecutar(criterioFin,criterioPadres,datoscsv,archivo.filename, int(gen), int(pob))
            modelo_generado = True
            return render_template('index.html', solucion = mejor_solucion, headers = headers, objects = algoritmo.bitacora)
        elif request.form['submit_button'] == "Calcular Nota":
            
            p1 = request.form['proyecto1']
            p2 = request.form['proyecto2']
            p3 = request.form['proyecto3']
            p4 = request.form['proyecto4']
            
            if mejor_solucion.fitness == 0:
                error ='Debe generar un modelo'
                return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora)                
            if not p1:
                error = 'El valor del parcial 1 es requerido'                
                if modelo_generado:
                    return render_template('index.html', error = error, solucion = mejor_solucion, headers = headers, objects = algoritmo.bitacora)
                else: 
                    return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora)
            if not p2:
                error = 'El valor del parcial 2 es requerido'
                if modelo_generado:
                    return render_template('index.html', error = error, solucion = mejor_solucion, headers = headers, objects = algoritmo.bitacora)
                else: 
                    return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora)
            if not p3:
                error = 'El valor del parcial 3 es requerido'
                if modelo_generado:
                    return render_template('index.html', error = error, solucion = mejor_solucion, headers = headers, objects = algoritmo.bitacora)
                else: 
                    return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora)
            if not p4:
                error = 'El valor del parcial 4 es requerido'
                if modelo_generado:
                    return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora, solucion = mejor_solucion)
                else: 
                    return render_template('index.html', error = error, headers = headers, objects = algoritmo.bitacora)        
                    
            nc = (mejor_solucion.solucion[0]*int(p1)) + (mejor_solucion.solucion[1]*int(p2)) + (mejor_solucion.solucion[2]*int(p3)) + (mejor_solucion.solucion[3]*int(p4))
            return render_template('index.html', nc = nc, solucion = mejor_solucion, headers = headers, objects = algoritmo.bitacora)                