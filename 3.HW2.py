import numpy as np

theta = float(input('Insertar theta: '))
Min_sup = int(input('Insertar el umbral de generacion de supervivencia mínimo: '))
N = 1
vive = 0
muere = 0
gen = 0

for i in range(0,1000):
    N = 1
    gen = 0
    while gen <= 20:
        N = int(np.random.poisson(N*theta))
        gen += 1
        if N>Min_sup:
            vive += 1
        else:
            muere += 1
            break

p_vive = vive/(vive+muere)*100
p_muere = muere/(vive+muere)*100


print('Prob. vive = ',np.round(p_vive,2),'%')
print('Prob. Extincion = ',np.round(p_muere,2),'%')
