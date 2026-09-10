#!/bin/python 

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from numpy import linspace

#-------------
# site
#-------------
# sites of shifted kagome lattices in rectangular unit cell
atoms=[ (  0, 0 ,0.000000, 0.000000, 0.000000 ),
        (  1, 1 ,0.500000, 0.000000, 0.000000 ),
        (  2, 2 ,0.250000, 0.250000, 0.000000 ),
        (  3, 3 ,0.750000, 0.250000, 0.000000 ),
        (  4, 1 ,0.000000, 0.500000, 0.000000 ),
        (  5, 0 ,0.500000, 0.500000, 0.000000 ),
        (  6, 3 ,0.250000, 0.750000, 0.000000 ),
        (  7, 2 ,0.750000, 0.750000, 0.000000 ),
        (  8, 1 ,0.000000, 0.166667, 0.500000 ),
        (  9, 0 ,0.500000, 0.166667, 0.500000 ),
        ( 10, 3 ,0.250000, 0.416667, 0.500000 ),
        ( 11, 2 ,0.750000, 0.416667, 0.500000 ),
        ( 12, 0 ,0.000000, 0.666667, 0.500000 ),
        ( 13, 1 ,0.500000, 0.666667, 0.500000 ),
        ( 14, 2 ,0.250000, 0.916667, 0.500000 ),
        ( 15, 3 ,0.750000, 0.916667, 0.500000 ) ]


#-------------
# plot
#-------------
fig = figure(figsize=(7,6))
fig.add_subplot(111)
ax = fig.axes[0]

for i,m,x,y,z in atoms:
    if m == 3:
      c = 'tab:green'
    else:
      if z == 0:
        c = 'tab:blue'
      else:
        c = 'tab:red'

    ax.scatter(x,y,s=120, c=c)
    ax.text( x+0.02, y+0.02, str(i), fontsize=10)

ax.set_xlim(-0.1,1.1)
ax.set_ylim(-0.05,1.05)
ax.set_yticks(linspace(0,1,13))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Unit cell sites (blue: z=0, red: z=0.5)')
ax.set_aspect(3**(1/2))
ax.grid(True)

p2out='./main.pdf'
plt.savefig(p2out, bbox_inches='tight')
