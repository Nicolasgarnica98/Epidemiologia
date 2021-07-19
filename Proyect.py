#Author: Nicolás Garnica
#IFR = 5
#R0 = 3.5
#Aplicación de la vacuna al comienzo de la pandemia.


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

w1 = 0.136
w2 = 0.543
w3 = 0.321
theta = 0.0833
N = 1000
Ro = 3.5 #Se puede encontrar en bibliografia para cualquier epidemia.
r0 = 1/11
r1 = 1/5.23
alpha = 1/11.8
miu = 1/11.29
beta = 0.41
IFR = 5/1000
p = IFR/beta
Lambda = Ro*r0
cH = np.round((5/1000)*N) #Beds available
VE = 0.6
K = 30

def model(N,Ro):
       
    i0 = 1  #Infectados sin sintomas ----> No detectados
    i1 = 20  #Infectados de la BD ----> Detectados
    R = 0   #Recuperados
    D = 0   #Muertos
    H = 0   #Hospitalizados
    ICU = 0 #UCI
    t = 0
    S = N -(i0+i1) #Suceptibles
    t_array = []
    t_array.append(t)
    past_day = 0
    start_vac = 10

    y = [[S, i0, i1, H, R, ICU, D]]
    temp = y[0]


    while (i0 + i1 )  > 0:
        
        #Vacunados
        current_day = int(t)
        if current_day == past_day + 1:
            past_day = current_day
            if current_day > start_vac:
                q = S / (S + i0+i1)
                r = np.round(K * q * VE)
                S = S - np.minimum(r, S)
                R = R + np.minimum(r, S)

        t_s_i1 = ((Lambda*(i1+i0)*S)/N)*p              #[-1,0,1,0,0,0,0]
        t_s_io = ((Lambda*(i1+i0)*S)/N)*(1-p)          #[-1,1,0,0,0,0,0]
        t_io_R = r0*i0                                 #[0,-1,0,0,1,0,0]
        t_i1_H = r1*i1                                 #[0,0,-1,1,0,0,0]
        t_H_R = alpha*H*w3                             #[0,0,0,-1,1,0,0]
        t_H_D = alpha*H*w1                             #[0,0,0,-1,0,1,0]
        t_H_ICU = alpha*H*w2                           #[0,0,0,-1,0,0,1]
        t_ICU_D = miu*ICU*theta                        #[0,0,0,0,0,-1,1]
        t_ICU_R = miu*ICU*(1-theta)                    #[0,0,0,0,-1,1,0]

        mT = [[-1,0,1,0,0,0,0],
              [-1,1,0,0,0,0,0],
              [0,-1,0,0,1,0,0],
              [0,0,-1,1,0,0,0],
              [0,0,0,-1,1,0,0],
              [0,0,0,-1,0,1,0],
              [0,0,0,-1,0,0,1],
              [0,0,0,0,0,-1,1],
              [0,0,0,0,-1,1,0]]

        rates = [t_s_i1,t_s_io,t_io_R,t_i1_H,t_H_R,t_H_ICU,t_H_D,t_ICU_D,t_ICU_R]
        totrates = np.sum(rates)
        prob_array = rates/totrates
        
        #Next event
        t_array.append(t)
        tnex = (-1*np.log(np.random.uniform(0.000001,1)))/totrates
        t = t+tnex

        pos = np.random.multinomial(1, prob_array)
        event = mT[np.argwhere(pos)[0][0]]
        
        #Update data
        x = np.add(temp, event)
        temp = x
        S,i0,i1,H,R,ICU,D = x[0],x[1],x[2],x[3],x[4],x[5],x[6]
        y.append(x)

        if R <0:
            break
    
    y = np.reshape(y,(len(y),len(y[0])))
    print(len(y[:,0]))
    print(len(t_array))
    plt.plot(t_array, y[:,0], color='blue', label='Suceptibles')
    plt.plot(t_array, y[:,1], color='brown', label='Asintomaticos')
    plt.plot(t_array, y[:,2], color='orange', label='Sintomaticos')
    plt.plot(t_array, y[:,3], color='pink', label='Hospitalizados')
    plt.plot(t_array, y[:,4], color='green', label='Recuperados')
    plt.plot(t_array, y[:,5], color='red', label='UCI')
    plt.plot(t_array, y[:,6], color='black', label='Muertos')
    plt.legend()
    plt.title('Modelo de la epidemia')
    plt.xlabel('Tiempo (Dias)')
    plt.ylabel('Individuos')
    plt.show()


model(N,Ro)



