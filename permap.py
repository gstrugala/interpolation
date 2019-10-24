import numpy as np
import pandas as pd

Tin = (21, 23)              # indoor temperature
RHin = (0.1, 0.5, 0.9)      # indoor relative humidity
Tout = (22, 30, 40)         # outdoor temperature
mfr = (0.1, 0.5, 0.9)       # mass flow rate
f = (0.1, 0.5, 0.9)         # compressor frequency
names = ['Tin', 'RHin', 'Tout', 'mfr', 'f']

lengths = lambda *args: [len(arg) for arg in args]
lentot = lambda *args: np.prod(lengths(*args))

Pel = np.random.uniform(0, 1.5, lentot(Tin, RHin, Tout, mfr, f))
Qcs = 1.5*Pel

idx = pd.MultiIndex.from_product([Tin, RHin, Tout, mfr, f], names=names)
permap = pd.DataFrame({'Pel':Pel, 'Qcs':Qcs, 'Qcl':np.zeros_like(Qcs)})
permap.index = idx
permap['Qcl'] = 0.8 * idx.get_level_values('RHin') * permap['Qcs']

permap.round(2).to_csv('permap.txt', sep='\t')

def prepend_line(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

for name, values in zip(reversed(names), reversed([Tin, RHin, Tout, mfr, f])):
    prepend_line('permap.txt', name + ' has {} values: {}'.format(len(values), values).replace('(', '').replace(')', ''))
