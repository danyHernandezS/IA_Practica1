#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np
from nodo import Nodo
from tupla import Tupla

#CONSTANTES DEL ALGORITMO
maximo_generaciones = 100 #Número máximo de generaciones que va a tener el algoritmo
suma_anterior = 1 #Para guardar la suma de la población anterior

        

"""
*   Función que crea la población
"""
def inicializarPoblacion():
    poblacion = []

    #La población inicial ya la definió el ingeniero en la tabla
    #Individuo 1
    """ individuo = Nodo([1, 0, 1, 1, 0], evaluarFitness([1, 0, 1, 1, 0]), 22)
    poblacion.append(individuo)
    #Individuo 2
    individuo = Nodo([1, 1, 0, 0, 0], evaluarFitness([1, 1, 0, 0, 0]), 24)
    poblacion.append(individuo)
    #Individuo 3
    individuo = Nodo([0, 0, 1, 0, 0], evaluarFitness([0, 0, 1, 0, 0]), 4)
    poblacion.append(individuo)
    #Individuo 4
    individuo = Nodo([1, 1, 0, 1, 1], evaluarFitness([1, 1, 0, 1, 1]), 27)
    poblacion.append(individuo) """

    i = 1
    while i <= 10:
        w1 = random.uniform(-2,2)
        w2 = random.uniform(-2,2)
        w3 = random.uniform(-2,2)
        w4 = random.uniform(-2,2)
        individuo = Nodo([w1,w2,w3,w4],evaluarFitness([w1,w2,w3,w4]))
        poblacion.append(individuo)
        print("individuo:",individuo.solucion, "|ValorFitness", individuo.fitness)
        i += 1

    #GENERAR LA POBLACION ESTO CON UN LOOP QUE CREE CADA NODO CON VALORES ALEATORIOS DE -2 A 2
    return poblacion #Retorno la población ya creada


"""
*   Función que verifica si el algoritmo ya llegó a su fin
"""

#HAY QUE AGREGAR QUE TIPO DE CRITERIO SE VA A UTILIZAR
#HACER UN IF O UN CASE PARA VER QUE CRITERIO SE USA
def verificarCriterio(poblacion, generacion, tipoCriterio):
    
    #Maximo numero de generaciones
    if tipoCriterio == 1:
        if generacion > maximo_generaciones:
            return True
    elif tipoCriterio == 2:    
        fitnessAnterior = 0
        for individuo in poblacion:
            individuo.fitness = evaluarFitness(individuo.solucion)
            if fitnessAnterior == 0:
                fitnessAnterior = individuo.fitness
        
        #Verifico si ya se llegó a una razón mayor o igual a 85%
    #return True if razon >= 0.80 else None

"""
*   Función que convierte un número binario a decimal
*   el número viene en un arreglo como este [0, 1, 1, 1, 0]
"""    
def convertirBinario(arreglo):
    base = 2 #Base 2 porque es binario
    decimal = 0
    for valor in arreglo:
        decimal = decimal * base + valor

    return decimal

"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
*   @solucion = el número viene en un arreglo como este [0, 1, 1, 1, 0]
"""
def evaluarFitness(solucion):
    
    datos = []
    nuevaTupla = Tupla(75,50,90,65,71.75)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(80,95,88,80,84.65)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(20,55,60,58,52.45)
    datos.append(nuevaTupla)
    nuevaTupla = Tupla(60,28,69,50,53.9)
    datos.append(nuevaTupla)

    suma = 0
    for dato in datos:
        nc = solucion[0]*dato.p1 + solucion[1]*dato.p2 + solucion[2]*dato.p3 + solucion[3]*dato.p4
        dato.nc = nc
        suma += ((dato.nr - dato.nc)**2)
    
    #for dato2 in datos:
    #   suma = dato2.
    #    print('p1:',dato2.p1,'|p2:',dato2.p2,'|p3:',dato2.p3,'|p4:',dato2.p4,'|nr:',dato2.nr,'|nc',dato2.nc)
       
    return suma/ len(datos)

"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""
#AGREGAR QUE TIPO DE CRITERIO SE VA A USAR PARA SELECCIONAR EL PADRE
def seleccionarPadres(poblacion):
    #Los padres se seleccionan por torneo
    #Mejor entre individuo 1 y 2 y mejor entre individuo 3 y 4
    padres = []

    #Mejor entre individuo 1 y 2
    individuo1 = poblacion[0]
    individuo2 = poblacion[1]
    padres.append(individuo2 if individuo2.fitness < individuo1.fitness else individuo1)

    #Mejor entre individuo 3 y 4
    individuo3 = poblacion[2]
    individuo4 = poblacion[3]
    padres.append(individuo4 if individuo4.fitness < individuo3.fitness else individuo3)

    return padres


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""
def cruzar(padre1, padre2):
    #padre1 = [1, 0, 1, 1, 0]
    #padre2 = [0, 0, 1, 0, 1]
    #hijo = [1, 0, 1, 0, 0]
    hijo = [padre1[0], padre2[1], padre1[2], padre2[3], padre1[4]]
    return hijo #Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
*   Se va a cambiar el bit con valor 0 más a la izquierda por 1
"""
def mutar(solucion):
    for i in range(0,len(solucion)):
        if solucion[i] == 0:
            solucion[i] = 1 #Cambio el valor por 1
            break #Me salgo del ciclo

    return solucion #Retorno la misma solución, solo que ahora mutó


"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""
def emparejar(padres):

    #Se van a generar 2 nuevos hijos, se tienen 2 padres

    #Genero al hijo 1
    hijo1 = Nodo()
    hijo1.solucion = cruzar(padres[0].solucion, padres[1].solucion)
    hijo1.solucion = mutar(hijo1.solucion)

    #Genero al hijo 2
    hijo2 = Nodo()
    hijo2.solucion = cruzar(padres[1].solucion, padres[0].solucion)
    hijo2.solucion = mutar(hijo2.solucion)

    #Ordeno a los padres en orden ascendente, de menor a mayor
    padres = sorted(padres, key=lambda item: item.fitness, reverse=False)[:len(padres)] #Los ordena de menor a mayor

    #Creo un arreglo de hijos para luego ordenarlos
    hijos = [hijo1, hijo2]
    #Ordeno a los hijos en orden ascendente, de menor a mayor
    hijos = sorted(hijos, key=lambda item: item.fitness, reverse=False)[:len(hijos)] #Los ordena de menor a mayor

    #La nueva población se hará de la siguiente manera:
    #El mejor padre, el segundo mejor hijo, el segundo mejor padre, el mejor hijo
    nuevaPoblacion = [padres[0], hijos[1], padres[1], hijos[0]]

    return nuevaPoblacion
    










"""
*   Método para imprimir los datos de una población
"""
def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        print('Individuo: ', individuo.solucion, ' Valor de NC: ', individuo.nc, ' Fitness: ', individuo.fitness)




"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""
def ejecutar():
    #np.seterr(over='raise')
    print("Algoritmo corriendo")

    generacion = 0
    poblacion = inicializarPoblacion()
    """ fin = verificarCriterio(poblacion, generacion)

    #Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion)
        poblacion = emparejar(padres)
        generacion += 1 #Lo pongo aquí porque en teoría ya se creó una nueva generación
        fin = verificarCriterio(poblacion, generacion)
        #generacion += 1

        #Imprimo la población
        print('*************** GENERACION ', generacion, " ***************")
        imprimirPoblacion(poblacion)

    #print('Cantidad de generaciones:', generacion)
    #imprimirPoblacion(poblacion) #Población final

    #Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[:1] #Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    print('Individuo: ', mejorIndividuo.solucion, ' Valor de nc: ', mejorIndividuo.nc, ' Fitness: ', mejorIndividuo.fitness) """
    




#Corro el algoritmo
ejecutar()