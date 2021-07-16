import numpy as np
import matplotlib.pyplot as plt

def SIR_func(N,Lambda,Mu):
    #N = Tamaño de la población
    #Lambda = tasa de contagios (no. contagios / dia)
    #Mu = Tasa de recuperación. (1/Mu) = Tiempo promedio que requiere una persona para recuperarse.
    t = 0 #Tiempo incial
    I = 1 #Infectados
    S = N - I #Suceptibles
    R = 0 #Recuperados
    S_array = []
    t_array = []
    I_array = []
    R_array = []
    down = 0
    down1 = 0
    down2 = 0
    while I>0:
        # if I+R > np.round(0.1*N) and down == 0:
        #     Lambda = Lambda/2
        #     down = 1
        #Decidir el evento
        inf_rate = Lambda*I*(S/N) #Infection rate S->I
        rem_rate = Mu*I #Removal rate S->I
        to_rate = inf_rate + rem_rate
        p_inf = inf_rate/to_rate

        ##Miedo
        if (I+R) > int(0.15*N) and down == 0: #Debido a que las infecciones son mayores al 15% la gente decide quedarse en casa y el lambda de la enfermedad disminuye.
            Lambda = Lambda/2
            down = 1

        if t>=4 and down1 == 0: #Tras pasar más de t = 4 días la gente sale nuevamente a trabajar y el lambda aumenta.
            Lambda = Lambda*2

            down1 = 1;

        if t>=7 and down2 == 0: #Al pasar 7 días un vuelo que venía de ASIA trae 25 nuevas personas infectadas.
            I = I + 25
            down2 = 1


        if np.random.uniform(0.000001,1) < p_inf: #Alguien se infecta
            I += 1
            S = S - 1
        else: #Alguien se recupera
            I = I-1
            R += 1
        
        #Decidir el siguiente evento
        tnex = (-1*np.log(np.random.uniform(0.000001,1)))/to_rate
        t = t+tnex

        

        t_array.append(t)
        S_array.append(S)
        R_array.append(R)
        I_array.append(I)

    plt.plot(t_array,S_array,color='blue',label='Suceptibles')
    plt.plot(t_array,R_array,color='green',label='Recuperados')
    plt.plot(t_array,I_array,color='red',label='Infectados')
    plt.legend()
    plt.title('Modelo SIR')
    plt.xlabel('Tiempo (Dias)')
    plt.ylabel('No. Personas')
    plt.show()

N = int(input('Insertar tamaño de la población: '))
Lmda = float(input('Insertar Lambda: '))
Mu = float(input('Insertar tasa de recuperación: '))
   
SIR_func(N,Lmda,Mu)