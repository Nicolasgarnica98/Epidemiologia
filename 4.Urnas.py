import numpy as np
from tqdm import tqdm

sim = 1000
x = np.zeros(sim)
for i in tqdm(range(0,sim)):
    R0 = 1.5
    N=1000
    I = np.unique(np.random.uniform(N,1,1))
    R = []
    while len(I)>0:
        ocupados = np.union1d(I,R)
        theta = R0*len(R)
        totballs = np.random.poisson(theta)
        places = np.unique(np.random.uniform(N,totballs,1))
        new = np.setdiff1d(places,ocupados)
        I = new
        R = ocupados
        print(R)

    x[i] = len(R)
    

print(np.mean(x))

