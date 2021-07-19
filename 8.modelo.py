import numpy as np
import matplotlib.pyplot as plt

#Tasas promedio de salida son 1/promedio
#Cada infectado infecta a una tasa Lambda*I
#De la caja S a I0 e I1. Si las tasas de 
#infeccion de I0 e I1 son diferentes: Lambda1*I1*S/N + Lambda0*I0*S/N
#Si son iguales, la tasa es: Lambda*(I0 + I1)S/N
#Agregar proporiones: de S a I1 ---> p y de S a I0 ---> 1-p
#P es giaul a 0.0098
#Tasa de salida r de recuperación de I0 a R = 1/11 (Le toma 11 dias en recuperarse)
#Tasa de I0 a R = r*I0
#Tasa de salida de I1 a H = r1*I1 donde r1 es igual a 1/t1 donde t1 es el
#tiempo de t1 ---> encontrado en la base de dtos.
#Tasa de salida de H a D = alpha*H*w1 Donde alphaes el tiempo promedio de estadia en H Y W1
#la proporcion de H que muere en D.
#Tasa de salida de H a R = alpha*H*w2 donde w2 es la prporcion de H que se recupera al salir del hospital
#Tasa de salida de H a ICU = alpha*H*W3 donde w3 es la tasa de H que debe ir a una UCI.
#Tasa de salida de ICU a D = miu*ICU*theta donde theta es la tasa de ICU que muere y miu el timepo
#promedio de estadia en una UCI.
#Tasa de salida de ICU a R = miu*ICU*(1-theta)
#Los tiempos se obtienen de la base de datos.

w1 = 0.412
w2 = 0.00322
w3 = 0.577
theta = 0.0833
N = int(input('Insertar tamaño de la poblacion N: '))
Ro = float(input('Insertar R0: ')) #Se puede encontrar en bibliografia para cualquier epidemia.
Lambda = Ro*11
r0 = 1/11
r1 = 1/3.541
alpha = 1/11.8
miu = 1/11.29
p = 0.0098

def model(N,Ro):
    S = N   #Suceptibles
    i0 = 1  #Infectados sin sintomas ----> No detectados
    i1 = 0  #Infectados de la BD ----> Detectados
    R = 0   #Recuperados
    D = 0   #Muertos
    H = 0   #Hospitalizados
    ICU = 0 #UCI
    t = 0

    if np.random.uniform(0.000001,1) < p:
        i1 += 1
        S = S - 1

    else:
        i0 += 1
        S = S - 1

    while len(i0)+len(i1) != 0:                       #[S,I0,I1,H,R,ICU,D]
        t_s_i1 = ((Lambda*(i1+i0)*S)/N)*p              #[-1,0,1,0,0,0,0]
        t_s_io = ((Lambda*(i1+i0)*S)/N)*(1-p)          #[-1,1,0,0,0,0,0]
        t_io_R = r0*i0                                 #[0,-1,0,0,1,0,0]
        t_i1_H = r1*i1                                 #[0,0,-1,1,0,0,0]
        t_H_R = alpha*H*w3                             #[0,0,0,-1,1,0,0]
        t_H_D = alpha*H*w1                             #[0,0,0,-1,0,1,0]
        t_H_ICU = alpha*H*w2                           #[0,0,0,-1,0,0,1]
        t_ICU_D = miu*ICU*theta                        #[0,0,0,0,0,-1,1]
        t_ICU_R = miu*ICU*(1-theta)                    #[0,0,0,0,-1,1,0]

        mT = [[-1,0,1,0,0,0,0]
              [-1,1,0,0,0,0,0]
              [0,-1,0,0,1,0,0]
              [0,0,-1,1,0,0,0]
              [0,0,0,-1,1,0,0]
              [0,0,0,-1,0,1,0]
              [0,0,0,-1,0,0,1]
              [0,0,0,0,0,-1,1]
              [0,0,0,0,-1,1,0]]

        rates = [t_s_i1,t_s_io,t_io_R,t_i1_H,t_H_R,t_H_ICU,t_H_D,t_ICU_D,t_ICU_R]
        totrates = np.sum(rates)
        prob_array = rates/totrates
        
        #Next event
        tnex = (-1*np.log(np.random.uniform(0.000001,1)))/totrates
        
        

        print(prob_array)


model(N,Ro)

