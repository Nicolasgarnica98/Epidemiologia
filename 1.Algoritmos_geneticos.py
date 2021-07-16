#Algoritmos geneticos
#SECUENCIAS BINARIAS
#las secuencias con mayor adaptabilidad tienen el chance mas alto de reproducirce
#Paralelo con secuncias binarias
#Las secuencias hijas pueden tener mutaciones simples
#la reproduccion de las secuencias puede ser sexual o asexual
# Sexual:
# 0011101
#    +      ------->  0011111 puede mutar ---> 0010110
# 0011011
#
# Asexual:
# 0011101 hijos ---> 0011101 y podria mutar

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

# #Prueba
# p = np.binary_repr(45,10)
# print(p)
# print(scipy.stats.norm(0, 1).pdf(0))

def binaryToDecimal(binary):
    binary=int(binary)
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal


#PSEUDOCODIGO
#1 - Declarar la funcion
#2 - Definir los rangos
#3 - Definir la poblacion inicial (n)
#4 - Evaluar fitness f(x), fi = Fitness del individuo i
#5 - Normalizar los fitness Fi = fi/sum(f)
#6 - Pasar a binario
#6 - Rproducir asexualmente
#7 - Generar mutaciones aleatorias dependiendo de una probabilidad
#8 - Pasar a decimal los hijos mutados
#9 - volver a empezar desde el paso 4 con los nuevo numeros

#Definiciino de la función
def f(x):    
    return 5*np.tan(4*(x**2)) + 40

rango_x = np.linspace(0,100,10000, dtype=np.int) #Rango de la función

n = 75 #Poblacion inicial

#Definiendo rango
pob = np.random.randint(0,100,n)
# pob = np.linspace(0,n,n,dtype=np.int)

#Vectores de probabilidad
vect_prob = [0.2,0.15,0.2,0.3,0.15,0.25,0.17]

#Evaluando en f(x) = fi
conv = False
counter = 0
while conv == False:
    plt.plot(rango_x,f(rango_x))
    counter = counter +1
    fitness = []
    fitness_norm = []

    for i in pob:
        fitness.append(f(i))
        fitness_norm.append(0)
    sum_fi = np.sum(fitness)
    
    #Calculo del fitness
    Fi = []
    for i in range(0,len(fitness_norm)):
        fitness_norm[i] = int(n*(fitness[i]/sum_fi))
        Fi.append(fitness_norm[i])
    
    #Binarización de int y factor de generacion de hijos
    bin_pob = []
    reprod = []
    for i in range(0,len(pob)):
        if Fi[i] != 0:
            bin_pob.append(list(np.binary_repr(pob[i],7)))
            reprod.append(Fi[i])

    m_bin = []
    for i in range(0,len(bin_pob)):
        for j in range(0,reprod[i]):
            m_bin.append(bin_pob[i])

    #Plot points
    for i in range(0,len(fitness)):
        plt.plot(pob[i],fitness[i], marker='o')
        
    plt.show()
    m_bin = np.array(m_bin)
    m_bin = np.reshape(m_bin,(len(m_bin),len(m_bin[0])))
    prob = 0

    #Generacion de mutaciones
    #Matriz de distribucion estandar de probabilidad
    m_norm = np.random.standard_normal((m_bin.shape[0],m_bin.shape[1]))
    m_prob = np.zeros((m_bin.shape[0],m_bin.shape[1]))
    for i in range(0,m_bin.shape[0]):
        for j in range(0,m_bin.shape[1]):
            m_prob[i][j] = scipy.stats.norm(0, 1).pdf(m_norm[i][j])  

    #Mutacion de acuerdo a la probabilidad
    for i in range(0,7):
        for j in range(0,19):
            if m_prob[j][i] < vect_prob[i]:
                if str(m_bin[j][i]) == '0':
                    m_bin[j][i] = '1'
                if str(m_bin[j][i]) == '1':
                    m_bin[j][i] = '0'
    
    #Conversion de binario a int
    new_bin = []
    for i in range(0,m_bin.shape[0]):
        str_actual = ''
        str_actual = str_actual.join(m_bin[i,:])
        new_bin.append(str_actual)

    new_pob = []
    for i in range(0,len(new_bin)):
        new_pob.append(binaryToDecimal(new_bin[i]))
    
    #Nueva generacion
    pob = new_pob
    
    #Criterio de convergencia
    if counter == 24:
        conv = True
