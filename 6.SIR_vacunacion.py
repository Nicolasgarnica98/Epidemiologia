import numpy as np
import matplotlib.pyplot as plt

def SIR_func(N, Lambda, Mu, K, VE):
    # N = Tamaño de la población
    # Lambda = tasa de contagios (no. contagios / dia)
    # Mu = Tasa de recuperación. (1/Mu) = Tiempo promedio que requiere una persona para recuperarse.
    t = 0  # Tiempo incial
    I = 1  # Infectados
    S = N - I  # Suceptibles
    R = 0  # Recuperados
    S_array = []
    t_array = []
    I_array = []
    R_array = []
    start_vac = 10
    past_day = 0
    down = 0

    while I > 0:
        current_day = int(t)
        if current_day == past_day + 1:
            past_day = current_day
            if current_day > start_vac:
                q = S / (S + I)
                r = np.round(K * q * VE)
                S = S - np.minimum(r, S)
                R = R + np.minimum(r, S)
        # if I+R > np.round(0.1*N) and down == 0:
        #     Lambda = Lambda/2
        #     down = 1
        # Decidir el evento
        inf_rate = Lambda * I * (S / N)  # Infection rate S->I
        rem_rate = Mu * I  # Removal rate S->I
        to_rate = inf_rate + rem_rate
        p_inf = inf_rate / to_rate
        if np.random.uniform(0.000001, 1) < p_inf:  # Alguien se infecta
            I += 1
            S = S - 1
        else:  # Alguien se recupera
            I = I - 1
            R += 1

        # Decidir el siguiente evento
        tnext = (-1 * np.log(np.random.uniform(0.000001, 1))) / to_rate

        # Efecto de vacunación

        t = t + tnext

        t_array.append(t)
        S_array.append(S)
        R_array.append(R)
        I_array.append(I)

    plt.plot(t_array, S_array, color='blue', label='Suceptibles')
    plt.plot(t_array, R_array, color='green', label='Recuperados')
    plt.plot(t_array, I_array, color='red', label='Infectados')
    plt.legend()
    plt.title('Modelo SIR')
    plt.xlabel('Tiempo (Dias)')
    plt.ylabel('No. Personas')
    plt.show()


N = int(input('Insertar tamaño de la población: '))
Lmda = float(input('Insertar Lambda: '))
Mu = float(input('Insertar tasa de recuperación: '))
k = int(input('Insertar vacunados po día: '))
VE = float(input('Insertar fraccion de vacnados VE: '))

SIR_func(N, Lmda, Mu, k, VE)
