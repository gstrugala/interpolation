from math import floor
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
    for _ in range(5):
        features.append([num(v) for v in f.readline().split(' : ')[1].split(', ')])
    f.readline()
    nfeatures = [int(float(n)) for n in f.readline().split()]
    locs = [find(feature, value) for feature, value in zip(features, target)]
    print(features)
    print(nfeatures)
    print(locs)
