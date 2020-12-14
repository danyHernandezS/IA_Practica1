#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import random
import numpy as np
import csv
from nodo import Nodo
from tupla import Tupla
from datetime import datetime

#CONSTANTES DEL ALGORITMO
maximo_generaciones = 4000  #Número máximo de generaciones que va a tener el algoritmo
ultimo_fitness_mas_frecuente = 0
porcentaje_ultimo_fitness = 0
porcentaje_aceptacion = 60
valor_fitness_promedio = 1
datos = []
bitacora = []
"""
*   Función que crea la población
"""
def inicializarPoblacion():
    poblacion = []

    #La población inicial ya la definió el ingeniero en la tabla    
    #individuo = Nodo([0.45, 0.2, 0.34, 0.15],evaluarFitness([0.45, 0.2, 0.34, 0.15]))
    i = 1
    while i <= 240:
        w1 = random.uniform(-1,1)
        w2 = random.uniform(-1,1)
        w3 = random.uniform(-1,1)
        w4 = random.uniform(-1,1)
        individuo = Nodo([w1,w2,w3,w4],evaluarFitness([w1,w2,w3,w4]))
        poblacion.append(individuo)       
        i += 1

    #GENERAR LA POBLACION ESTO CON UN LOOP QUE CREE CADA NODO CON VALORES ALEATORIOS DE -2 A 2
    return poblacion #Retorno la población ya creada

"""
*   Función que verifica si el algoritmo ya llegó a su fin
"""
#HAY QUE AGREGAR QUE TIPO DE CRITERIO SE VA A UTILIZAR
#HACER UN IF O UN CASE PARA VER QUE CRITERIO SE USA
def verificarCriterio(poblacion, generacion, tipoCriterio):
    global ultimo_fitness_mas_frecuente
    global porcentaje_ultimo_fitness
    #1. Maximo numero de generaciones
    if tipoCriterio == 1:
        if generacion >= maximo_generaciones:            
            return True
    #2. Por mayor porcentaje de población con fitness igual
    elif tipoCriterio == 2:    
        frecuentes = obtenerMasFrecuentes(poblacion)
        #obtengo el mas frecuente y el numero de repicencias
        maxRepitencias = frecuentes[0][1]
        ultimo_fitness_mas_frecuente = frecuentes[0][0]
        porcentaje = (maxRepitencias/len(poblacion))*100
        porcentaje_ultimo_fitness = porcentaje
        #verifico si el porcentaje de frecuencias es mayor igual al un porcentaje o se alcanzaron el número máximo de generaciones
        if (porcentaje >= porcentaje_aceptacion and ultimo_fitness_mas_frecuente < 10) or generacion >= maximo_generaciones :
            return True
    #3. Por valor de fitness promedio
    elif tipoCriterio == 3:
        suma = 0
        for individuo in poblacion:
            suma += individuo.fitness
        if ((suma/len(poblacion))<= valor_fitness_promedio) or generacion >= maximo_generaciones:
            return True
    
    return False

def obtenerMasFrecuentes(poblacion):
    frecuencia = {}
    for individuo in poblacion:
        if individuo.fitness in frecuencia:
            frecuencia[individuo.fitness] += 1            
        else:
            frecuencia[individuo.fitness] = 1
    return sorted(frecuencia.items(), key= operator.itemgetter(1), reverse=True)


"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
*   @solucion = el número viene en un arreglo como este [0, 1, 1, 1, 0]
"""
def evaluarFitness(solucion):
    
    """ datos = []
    nuevaTupla = Tupla(75,50,90,65,71.75)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(80,95,88,80,84.65)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(20,55,60,58,52.45)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(60,28,69,50,53.9)
    datos.append(nuevaTupla) """

    suma = 0
    for dato in datos:
        nc = (solucion[0]*dato.p1) + (solucion[1]*dato.p2) + (solucion[2]*dato.p3) + (solucion[3]*dato.p4)
        dato.nc = nc
        #print('p1:',dato.p1,'|p2:',dato.p2,'|p3:',dato.p3,'|p4:',dato.p4,'|nr:',dato.nr,'|nc',dato.nc)
        suma += ((dato.nr - dato.nc)**2)    
       
    return suma/ len(datos)

"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""
#AGREGAR QUE TIPO DE CRITERIO SE VA A USAR PARA SELECCIONAR EL PADRE
def seleccionarPadres(poblacion,tipoSeleccion):
    
    padres = []
    #1. Los padres se seleccionan por torneo
    if tipoSeleccion == 1:
        i = 0
        while (i <len(poblacion)):
            #evaluo por pares cual es el mejor de los dos
            individuo1 = poblacion[i]
            individuo2 = poblacion[i+1]
            padres.append(individuo2 if individuo2.fitness < individuo1.fitness else individuo1)
            i += 2
    #2. Se seleccionan los mejores de la mitad de la población
    elif tipoSeleccion == 2:
        padres = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:int(len(poblacion)/2)] #Los ordena de menor a mayor y pasamos solo la mitad
    #3. Se seleccionan los padres en posiciones par
    elif tipoSeleccion == 3:
        i = 0
        while(i < len(poblacion)):
            if ((i % 2) ==0):
                padres.append(poblacion[i])
            i += 1
    #print ('CantidadPadres: ',len(padres))
    return padres

"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
"""
def cruzar(padre1, padre2):

    #Genero 4 numeros aleatorios entre 0 y 1
    v1 = random.uniform(0,1) 
    v2 = random.uniform(0,1)
    v3 = random.uniform(0,1)
    v4 = random.uniform(0,1)

    #Verifico si el valor de Vn es menor que 0.6 tomo el valo n del padre 1 
    #si no tomo el valor del padre 2
    w1 = padre1[0] if v1<= 0.6 else padre2[0]
    w2 = padre1[1] if v2<= 0.6 else padre2[1]
    w3 = padre1[2] if v3<= 0.6 else padre2[2]
    w4 = padre1[3] if v4<= 0.6 else padre2[3]
    
    hijo = [w1, w2, w3, w4]
    return hijo #Retorno al hijo ya cruzado

"""
*   Función que toma una solución y realiza la mutación
*   Se va a cambiar el bit con valor 0 más a la izquierda por 1
"""
def mutar(solucion):
    #Genero un número aleatorio entre 0 y 1
    mutarIndivudo = random.uniform(0,1)
    #Para calcular la probabilidad del 50%
    #Verifico si el número es menor a 0.5
    if mutarIndivudo <= 0.5:
        for i in range(0,len(solucion)):
            #De nuevo por cada elemento verifico la probabilidad del 50%
            mutarElemento = random.uniform(0,1)
            if mutarElemento <= 0.5:
                solucion[i] = random.uniform(-1,1) #Cambio el valor por nuevo elemento de -2 a 2
            break #Me salgo del ciclo

    return solucion #Retorno la misma solución, solo que ahora mutó


"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""
def emparejar(padres):    
    #Se van a generar 2 nuevos hijos, emparejando por pares etc..    

    #Ordeno a los padres en orden ascendente, de mayor a menor
    padres = sorted(padres, key=lambda item: item.fitness, reverse=False)[:len(padres)] #Los ordena de menor a mayor

    i = 0
    mitad = int(len(padres)/2)
    hijos = []
    while (i < mitad):
        if (i+1) < len(padres):
            hijo1 = Nodo() 
            hijo1.solucion = cruzar(padres[i].solucion, padres[i+1].solucion)
            hijo1.solucion = mutar(hijo1.solucion)
            hijo1.fitness = evaluarFitness(hijo1.solucion)

            hijo2 = Nodo
            hijo2.solucion = cruzar(padres[i+1].solucion, padres[i].solucion)
            hijo2.solucion = mutar(hijo2.solucion)
            hijo2.fitness = evaluarFitness(hijo2.solucion)
            
            hijos.append(hijo1)
            hijos.append(hijo2)
            
            i+=1
    
    #Ordeno a los hijos en orden ascendente, de mayor a menor
    hijos = sorted(hijos, key=lambda item: item.fitness, reverse=False)[:len(hijos)] #Los ordena de menor a mayor

    #La nueva población se hará de la siguiente manera:
    #Voy agregando a la nueva población el en orden ascendente de cada hijo/padre de cada iteración
    i = 0
    nuevaPoblacion = []
    while(i < len(padres)):
        nuevaPoblacion.append(padres[i])
        nuevaPoblacion.append(hijos[i])
        i += 1
    #nuevaPoblacion = [padres[0], hijos[1], padres[1], hijos[0]]

    return nuevaPoblacion
    
"""
*   Método para imprimir los datos de una población
"""
def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        print('Individuo: ', individuo.solucion, ' Fitness: ', individuo.fitness)

"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""
def ejecutar(criterioVerifica, criterioPadres, datoscsv, nombreArchivo):
    #np.seterr(over='raise')
    global datos
    global bitacora
    datos = datoscsv
    
#    print("Algoritmo corriendo")
#    print('maximo_generaciones:', maximo_generaciones)
#    print('porcentaje_aceptacion:',porcentaje_aceptacion)
#    print('valor_fitness_promedio', valor_fitness_promedio)

    ini = datetime.now()
    ini_formated =  ini.strftime("%d/%m/%Y %H:%M:%S")

    generacion = 0
    poblacion = inicializarPoblacion()
    fin = verificarCriterio(poblacion, generacion,criterioVerifica)    

    print('*************** GENERACION ', generacion, ini_formated, " ***************")    
    #imprimirPoblacion(poblacion)

    while(fin == False):
        padres = seleccionarPadres(poblacion, criterioPadres)
        poblacion = emparejar(padres)
        generacion += 1 #Lo pongo aquí porque en teoría ya se creó una nueva generación
       
        if generacion/maximo_generaciones == 0.5:
            now = datetime.now()
            dt_formated =  now.strftime("%d/%m/%Y %H:%M:%S")
            print('*************** 50% en GENERACION ', generacion, dt_formated, " Poblacion:",len(poblacion), " ***************")    
            #imprimirPoblacion(poblacion)
        if generacion/maximo_generaciones == 0.75:
            now = datetime.now()
            dt_formated =  now.strftime("%d/%m/%Y %H:%M:%S")
            print('*************** 75% en GENERACION ', generacion, dt_formated, " Poblacion:",len(poblacion), " ***************")    
            #imprimirPoblacion(poblacion)
        
        fin = verificarCriterio(poblacion, generacion,criterioVerifica)        


    #Imprimo la última población
    fin = datetime.now()
    fin_formated =  fin.strftime("%d/%m/%Y %H:%M:%S")
    print('*************** ULTIMA GENERACION ', generacion, fin_formated, " Poblacion:",len(poblacion), " ***************")    
    if criterioVerifica == 1 or criterioVerifica == 3:
        arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:1] #Los ordena de menor a mayor
        mejorIndividuo = arregloMejorIndividuo[0]        
        print('\n\n*************** MEJOR INDIVIDUO***************')
        print('Individuo: ', mejorIndividuo.solucion, ' Fitness: ', mejorIndividuo.fitness) 
        strSolucion = str(mejorIndividuo.solucion[0]) + "," + str(mejorIndividuo.solucion[1]) + "," + str(mejorIndividuo.solucion[2]) + "," + str(mejorIndividuo.solucion[3])        
        bitacora.append(dict(s=strSolucion, ini=ini_formated, fin=fin_formated, arch=nombreArchivo, c1=criterioVerifica, c2= criterioPadres,g=generacion))
        return mejorIndividuo
    elif criterioVerifica == 2:
        for individuo in poblacion:
            if individuo.fitness == ultimo_fitness_mas_frecuente:
                mejorIndividuo = individuo
                print('\n\n*************** MEJOR INDIVIDUO***************')
                print('Individuo: ', mejorIndividuo.solucion, ' Fitness: ', mejorIndividuo.fitness) 
                strSolucion = str(mejorIndividuo.solucion[0]) + "," + str(mejorIndividuo.solucion[1]) + "," + str(mejorIndividuo.solucion[2]) + "," + str(mejorIndividuo.solucion[3])
                bitacora.append(dict(s=strSolucion, ini=ini_formated, fin=fin_formated, arch=nombreArchivo, c1=criterioVerifica, c2= criterioPadres,g=generacion))                            
                return mejorIndividuo
    


#Corro el algoritmo
""" archivoEntrada = csv.DictReader(open("Practica1_Entrada.csv"), delimiter=',')
datoscsv = []
for linea in archivoEntrada:
    #file_up += ', '.join(row)
    nuevaTupla = Tupla(int(linea['PROYECTO 1']),int(linea['PROYECTO 2']),int(linea['PROYECTO 3']),int(linea['PROYECTO 4']), float(linea['NOTA FINAL']))
    datoscsv.append(nuevaTupla)
ejecutar(1,1,datoscsv) """