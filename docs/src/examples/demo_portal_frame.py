import openseespy.opensees as ops
# import opensees as ops  # local compilation
import opsvis as opsv

import matplotlib.pyplot as plt

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 3)

colL, girL = 4., 6.

Acol, Agir = 2.e-3, 6.e-3
IzCol, IzGir = 1.6e-5, 5.4e-5

E = 200.e9

Ep = {1: [E, Acol, IzCol],
      2: [E, Acol, IzCol],
      3: [E, Agir, IzGir]}

ops.node(1, 0., 0.)
ops.node(2, 0., colL)
ops.node(3, girL, 0.)
ops.node(4, girL, colL)

ops.fix(1, 1, 1, 1)
ops.fix(3, 1, 1, 0)

ops.geomTransf('Linear', 1)

# columns
ops.element('elasticBeamColumn', 1, 1, 2, Acol, E, IzCol, 1)
ops.element('elasticBeamColumn', 2, 3, 4, Acol, E, IzCol, 1)
# girder
ops.element('elasticBeamColumn', 3, 2, 4, Agir, E, IzGir, 1)

Px = 2.e+3
Wy = -10.e+3
Wx = 0.

Ew = {3: ['-beamUniform', Wy, Wx]}

ops.timeSeries('Constant', 1)
ops.pattern('Plain', 1, 1)
ops.load(2, Px, 0., 0.)

for etag in Ew:
    ops.eleLoad('-ele', etag, '-type', Ew[etag][0], Ew[etag][1],
                Ew[etag][2])

ops.constraints('Transformation')
ops.numberer('RCM')
ops.system('BandGeneral')
ops.test('NormDispIncr', 1.0e-6, 6, 2)
ops.algorithm('Linear')
ops.integrator('LoadControl', 1)
ops.analysis('Static')
ops.analyze(1)

ops.printModel()

# 1. plot model with tag lebels

opsv.plot_model()

# 2. plot supports and loads

plt.figure()
opsv.plot_supports_and_loads_2d()

# 3. plot deformed model

sfac = 80.

plt.figure()
# opsv.plot_defo(sfac)
opsv.plot_defo(sfac, fmt_interp='b.-')
opsv.plot_defo(sfac, 5, interpFlag=0, fmt_nodes='bo-')
opsv.plot_defo(sfac, 3, endDispFlag=0, fmt_interp='r.--')
opsv.plot_defo(sfac, 2, fmt_interp='g.-')

# 4. plot N, V, M forces diagrams

sfacN, sfacV, sfacM = 5.e-5, 5.e-5, 5.e-5

plt.figure()
minVal, maxVal = opsv.section_force_diagram_2d('N', sfacN)
plt.title(f'Axial forces, max = {maxVal:.2f}, min = {minVal:.2f}')

plt.figure()
minVal, maxVal = opsv.section_force_diagram_2d('T', sfacV)
plt.title(f'Shear forces, max = {maxVal:.2f}, min = {minVal:.2f}')

plt.figure()
minVal, maxVal = opsv.section_force_diagram_2d('M', sfacM)
plt.title(f'Bending moments, max = {maxVal:.2f}, min = {minVal:.2f}')

plt.show()

exit()
