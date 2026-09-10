#!/bin/python 

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from numpy import linspace

#-------------
# site
#-------------
# sites of shifted kagome lattices in rectangular unit cell
atoms=[ (  0, 0, 0.0,  0.0,                0.0 ),
        (  1, 1, 0.5,  0.0,                0.0 ),
        (  2, 2, 0.25, 0.25,               0.0 ),
        (  3, 0, 0.5,  0.5,                0.0 ),
        (  4, 1, 0.0,  0.5,                0.0 ),
        (  5, 2, 0.75, 0.75,               0.0 ),
        (  6, 0, 0.5,  0.1666666666666667, 0.5 ),
        (  7, 1, 0.0,  0.1666666666666667, 0.5 ),
        (  8, 2, 0.25, 0.9166666666666667, 0.5 ),
        (  9, 0, 0.0,  0.6666666666666667, 0.5 ),
        ( 10, 1, 0.5,  0.6666666666666667, 0.5 ),
        ( 11, 2, 0.75, 0.4166666666666667, 0.5 ) ]


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
