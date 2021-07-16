import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

#Punto 1
n_random = np.random.rand(10000)
n_random = np.sort(n_random)

distancias = []
for i in range(0,len(n_random)-1):
    dist = np.abs(n_random[i]-n_random[i+1])
    distancias.append(dist)


plt.hist(distancias,100)
plt.show()

Average_dist = np.mean(distancias)
print('Distancia promedio = ',Average_dist)
lamb = 10000/1
lamb_inv =  1/lamb
print('Lambda inverso = ',lamb_inv)


#Punto 2
w = 0.01
interval_arr = []
for i in range(0,1000):
    interval_arr.append(w)
    w = w + 0.01

cant_int = []
for i in tqdm(range(0,1000)):
    n_inicial = np.random.rand()
    count = sum(map(lambda x : x > n_inicial and x <= n_inicial + w, n_random))
    cant_int.append(count/1000)

print(cant_int)

plt.hist(cant_int,100)
plt.show()