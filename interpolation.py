import numpy as np
from math import floor
import itertools

def find(array, value):
    L = 0
    R = len(array)
    while L < R:
        mid = floor((L + R) / 2)
        if array[mid] < value:
            L = mid + 1
        else:
            R = mid
    return L-1

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
target = (22, 0.7, 35, 0.6, 0.4)

with open('permap.txt', 'r') as f:
    features = []
    nfeatures = []
    for _ in range(5):
        s = f.readline().replace(',', '').split(' ')
        nfeatures.append(num(s[2]))
        features.append([num(v) for v in s[4:]])
    f.readline()
    locs = np.array([find(feature, value) for feature, value in zip(features, target)])
    nf_products = np.append(nfeatures[1:], 1)
    for i in range(len(nf_products)-2, -1, -1):
        nf_products[i] *= nf_products[i+1]
    C = (np.array(i) for i in itertools.product([0,1], repeat=len(nf_products)))
    lines = np.array([np.dot(nf_products, locs + next(C)) for i in range(2**len(nf_products))])
    performance_data = np.zeros((2**len(nf_products), 3))
    for _ in range(lines[0]):
        f.readline()
    for i, nlines in enumerate(np.insert(np.diff(lines), 0, 1)):
        for _ in range(nlines - 1):
            f.readline()
        performance_data[i, :] = np.array(f.readline().split()[5:]).astype('float')

weights = []
for feature, loc, target_coord in zip(features, locs, target):
    weights.append((feature[loc+1] - target_coord) / (feature[loc+1] - feature[loc]))
for weight in weights:
    lower_values, upper_values = np.split(performance_data, 2, axis=0)
    performance_data = weight * lower_values + (1-weight) * upper_values
return performance_data[0]



 # Validation: interpolate using scipy
from scipy.interpolate import interpn
import pandas as pd
permap = pd.read_table('permap.txt', skiprows=5, index_col=('Tin', 'RHin', 'Tout', 'mfr', 'f'))
Pel, Qcs, Qcl = permap['Pel'], permap['Qcs'], permap['Qcl']
dims = [len(feature) for feature in Pel.index.levels]
Pel_values = Pel.values.reshape(*dims)
Qcs_values = Qcs.values.reshape(*dims)
Qcl_values = Qcl.values.reshape(*dims)

print(interpn(tuple(features), Pel_values, np.array(target))[0],
      interpn(tuple(features), Qcs_values, np.array(target))[0],
      interpn(tuple(features), Qcl_values, np.array(target))[0])
