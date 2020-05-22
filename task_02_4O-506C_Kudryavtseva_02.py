import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mt
import re
import requests as rqst

import scipy.special as sc

#Вычисление коэффициента а:
def a(n, x):
    return sc.spherical_jn(n, x) / h(n, x)

#Вычисление коэффициента b:
def b(n, x):
    return ((x * sc.spherical_jn(n - 1, x) - n * sc.spherical_jn(n, x))
            / (x * h(n - 1, x) - n * h(n, x)))

#Вычисление сферической функции Бесселя третьего рода:
def h(n, x):
    return sc.spherical_jn(n, x) + 1j * sc.spherical_yn(n, x)

#Вычисление ЭПР идеально проводящей сферы:
def RCS(D, fmin, fmax):
    c = 3e8
    r = D/2
    f = np.arange(fmin, fmax+1e8, 1e8)
    sigma = []
    for i in f:
        lambda_ = c / i
        k = 2 * np.pi / lambda_
        summa = []
        for n in range(1,100):
            summa.append((-1) ** n * (n + 0.5) * (b(n, k * r) - a(n, k * r)))
        sigma.append((lambda_ ** 2 / np.pi) * abs(sum(summa)) ** 2)
    with open('results/task_02_4O-506C_Kudryavtseva_02.txt', 'w') as ouf:
        ouf.write('f, [ГГц]\tsigma, [м^2]\n')
        for i in range(len(f)):
            ouf.write(str('{0:.2f}\t\t{1}\n'.format(f[i] * 1e-9, sigma[i])))
    plt.plot(f, sigma)
    plt.grid()
    plt.ylabel(r'$\sigma$, [$м^2$]', fontsize = 8)
    plt.xlabel('$f$, [ГГц]')
    plt.show()
    
#Извлечение данных из файла:
if not os.path.exists('results'):
    os.mkdir('results')
r = rqst.get('https://jenyay.net/uploads/Student/Modelling/task_02.txt')
z = re.search(r'^2\..+', r.text, flags=re.M)
z1 = (z.group().split(';'))
D = float(z1[0].split('=')[1])
fmin = float(z1[1].split('=')[1])
fmax = float(z1[2].split('=')[1])
RCS(D, fmin, fmax)
