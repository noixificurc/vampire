#!/bin/python

from numpy import ( abs, 
                    allclose, 
                    arctan2, 
                    array, 
                    concatenate,
                    cos, 
                    eye, 
                    floor, 
                    ndarray, 
                    outer, 
                    pi, 
                    round,
                    sin,
                    trunc )
from numpy.linalg import inv, norm
from itertools import permutations, product
from re import match



#-----------------
#
# configuration
#
#-----------------
p2ucf = './ucf/mn3sn.ucf'  # path to unit cell file
th    = 1e-10  # relative threshold



#-----------------
#
# Mn3Sn
#
#-----------------
# basis change
#-----------------
# fractional and laboratory coordinates
frac2lab = array([ [1,        0, 0],
                   [0, 3 ** 0.5, 0],
                   [0,        0, 1] ])  # fractional to laboratory
lab2frac = inv(frac2lab)  # proportional to fractional
# reciprocal lattice vector and laboratory coordinates
lat2lab = array([ [ 1, 0.5, 0],
                  [ 0, 0.5, 0],
                  [ 0,   0, 1] ])  # lattice to laboratory
lab2lat = inv(lat2lab)  # laboratory to lattice



#-----------------
# origins
#-----------------
origin_ucf  = array([0,0,0])                         # origin of unit cell file
origin_conv = origin_ucf + array([-0.25, -1/12, 0])  # conventional unit cell
origin_btm  = -origin_conv                           # center of bottom layer
origin_top  = origin_btm + array([0,0,0.5])          # center of bottom layer
origin_inv  = origin_btm + array([0,0,0.25])         # center symmetric unit cell



#-----------------
# symmetry transformation
#-----------------
class symmetry():
  '''
  Handle symmetries.
  '''
  hsb       = None  # high symmetry point
  mtrx_lab  = None  # symmetry transformation matrix in laboratory basis
  mtrx_frac = None  # symmetry transformation matrix in fractional basis

  def __init__(self, hsp:ndarray, mtrx_lab:ndarray):
    '''
    Constructor.
    :param hsp:      high symmetry point
    :param mtrx_lab: symmetry transformation matrix
    '''
    self.hsp       = array(hsp)
    self.mtrx_lab  = array(mtrx_lab)
    self.mtrx_frac = lab2frac @ self.mtrx_lab @ frac2lab

identity  = eye(3)                                # identity
inversion = -identity                             # inversion
phi       = 2 * pi / 3                            # 3-fold rotation angle
c3z       = array([ [cos(phi), -sin(phi), 0],
                    [sin(phi),  cos(phi), 0],
                    [       0,         0, 1] ])   # 3-fold rotation
sigmaz    = eye(3) - 2 * outer([0,0,1], [0,0,1])  # z-reflection
sigmax    = eye(3) - 2 * outer([1,0,0], [1,0,0])  # z-reflection
# symmetry generator
gen1 = array([ symmetry(origin_btm, identity),
               symmetry(origin_btm, sigmaz),
               symmetry(origin_btm, sigmax),
               symmetry(origin_btm, c3z) ])
gen2 = array([ symmetry(origin_top, identity),
               symmetry(origin_top, sigmaz),
               symmetry(origin_top, sigmax),
               symmetry(origin_top, c3z) ])
gen3 = array([ symmetry(origin_inv, identity),
               symmetry(origin_inv, inversion),
               symmetry(origin_inv, sigmax),
               symmetry(origin_inv, c3z) ])
gen4 = array([ symmetry(origin_ucf, identity),
               symmetry(origin_ucf, inversion) ])

def group_generator(gen:ndarray):
  '''
  Generate a closed symmetry group of symmetry group.
  :param generator: set of symmetries 
  :return: symmetry group
  '''
  # start with identity and add invers transformations
  group = [symmetry(gen[0].hsp, identity)]  # group
  gen   = list(gen) + [symmetry(g.hsp, inv(g.mtrx_lab)) for g in gen]
  def ck_group(A:ndarray):
    '''
    Compare a symmetry transformation with elements in group.
    :param A: transformation to compare
    :return:  True if A is in group, False if not
    '''
    return any(allclose(A, B.mtrx_lab, atol=th) for B in group)
  i = 0  # loop counter
  while i < len(group):
    for s in gen:
      n = group[i].mtrx_lab @ s.mtrx_lab  # generated transformation
      if not ck_group(n):
        group.append(symmetry(s.hsp, n))
    i += 1
  return array(group)

perm = permutations([ group_generator(gen1),
                      group_generator(gen2),
                      group_generator(gen3) ])
sym = concatenate([list(product(*p)) for p in perm])



#-----------------
#
# data handler
#
#-----------------
class site():
  '''
  Handle lattice sites.
  '''
  sid      = None  # lattice site ID
  crd_frac = None  # fractional laboratory coordinates

  def __init__(self, sid:int, crd_frac:ndarray):
    '''
    Constructor.
    :param sid:      lattice site ID
    :param crd_frac: fractional lattice coordinates
    '''
    self.sid      = int(sid)
    self.crd_frac = array(crd_frac, dtype=float)


class tensor():
  '''
  Handle exchange interaction parameter.
  '''
  iid          = None  # interaction ID
  sid          = None  # lattice site ID's
  crd_uc_trgt  = None  # fractional coordinates of target unit cell
  mtrx         = None  # exchange matrix
  site         = None  # interacting lattice sites
  crd_frac     = None  # fractional coordinates of virtual lattice sites
  crd_frac_uc  = None  # fractional unit cell coordinates
  crd_frac_prj = None  # fractional coordinates projected into center asymmetric unit cell
  dist_frac    = None  # fractional interaction distance
  sym          = None  # invers symmetry transformation relative to reference interaction
  revers       = None  # direction of interaction relative to reference interaction

  def __init__( self, 
                iid:int, 
                sid:int, 
                crd_uc_trgt:ndarray, 
                mtrx:ndarray ):
    '''
    Constructor.
    :param iid:         interaction ID
    :param sid:         lattice site ID's
    :param crd_uc_trgt: coordinates of target unit cell
    :param mtrx:        exchange matrix
    '''
    self.iid         = int(iid)
    self.sid         = array(sid, dtype=int)
    self.crd_uc_trgt = array(crd_uc_trgt, dtype=int)
    self.mtrx        = array(mtrx, dtype=float).reshape(3,3)

  def addSite(self, nsite:site):
    '''
    Add a new lattice site.
    :param nsite: new site
    '''
    for j,i in enumerate(self.sid):
      if i == nsite.sid:
        if not isinstance(self.site, ndarray):
          self.site = array([None,None])
        self.site[j] = nsite
    
  def locate(self):
    '''
    Handle interaction location.
    '''
    if not isinstance(self.site, ndarray) or self.site.size != 2:
      raise ValueError('No site available!')
    # coordinates of virtual lattice sites
    self.crd_frac = array([ self.site[0].crd_frac, 
                            self.site[1].crd_frac + self.crd_uc_trgt ])
    # project into center symmetric unit cell 
    # laboratory coordinates in conventional unit cell
    crd_lab = (self.crd_frac - origin_conv) @ lab2lat.transpose()
    self.crd_frac_uc = floor(round(crd_lab, 10)) @ lat2lab.transpose()
    self.crd_frac_prj = self.crd_frac - self.crd_frac_uc[0]
    # fractional interaction distance
    self.dist_frac = self.crd_frac[1] - self.crd_frac[0]

  def transform(self):
    '''
    Symmetry transform exchange matrix.
    '''
    if not isinstance(self.revers, bool):
      raise ValueError('No exchange direction available!.')
    elif not isinstance(self.sym, ndarray):
      raise ValueError('No transformation available!.')
    # transformed exchange matrix
    matrix_sym = self.mtrx
    for s in self.sym:
      matrix_sym = inv(s.mtrx_lab) @ matrix_sym @ s.mtrx_lab
    if self.revers:
      return matrix_sym.transpose()
    else:
      return matrix_sym



#-----------------
#
# process data
#
#-----------------
# read file
#-----------------
ucf = []  # unit cell file content
with open(p2ucf, 'r') as f:
    for l in f.readlines():
      if l.strip()[0] != '#':
        ucf.append(l.strip())
ucf = array(ucf)



#-----------------
# organize data
#-----------------
# line numbers
idx_sec_atom    = None  # start of atom section
idx_sec_intrctn = None  # start of interaction section
# determine line numbers
for i,l in enumerate(ucf):
  if l == '12 3':
    idx_sec_atom = i
  elif match(r"^\d+\s+tensorial$", l.strip()):
    idx_sec_intrctn =i
# content of atom section
sec_atom = array([ a.split() for a in ucf[idx_sec_atom + 1:idx_sec_intrctn] ])
# lattice sites
lattice = array([ site(s[0], s[1:4]) for s in sec_atom ])
# content of interaction section
sec_intrctn = array([ i.split() for i in ucf[idx_sec_intrctn + 1:] ])
# exchange interactions
exchange = array([ tensor(i[0], i[1:3], i[3:6], i[6:15]) for i  in sec_intrctn])



#-----------------
# locate exchange interactions
#-----------------
for e in exchange:
  [e.addSite(s) for s in lattice]
  e.locate()



#-----------------
# spacial transformation
#-----------------
# compare transformed coordinates with reference interaction
ref = exchange[0]  # reference interaction
exch_radius = ((frac2lab @ (ref.dist_frac)) ** 2).sum()  # exchange radius
for s in sym:
  crd_frac_prj = ref.crd_frac_prj
  for k in s:
    crd_frac_prj = (crd_frac_prj - k.hsp) @ k.mtrx_frac.transpose() + k.hsp
  for e in exchange:
    if isinstance(e.sym, ndarray):
      continue
    for i,c in enumerate([crd_frac_prj, crd_frac_prj[::-1]]):
      dif_frac_prj = (e.crd_frac_prj - c) @ frac2lab.transpose()
      if all(abs(dif_frac_prj.flatten()) < th * exch_radius):
        e.sym = s
        e.revers = (i == True)
        break

# check spacial symmetry
for e in exchange:
  if not isinstance(e.sym, ndarray):
    raise ValueError(f'No spacial symmetry found for {e.iid}!')


#-----------------
# exchange transformation
#-----------------
# check if spacial symmetry matches exchange transformation
for e in exchange:
  exch_mag = abs(ref.mtrx).max()  # magnitude of exchange
  dif_matrix = abs(ref.mtrx - e.transform())
  if any(dif_matrix.flatten() > th * exch_mag):
    text = f'No exchange transformation found for {e.iid}!\n' \
           + 'Transformation matrices are:\n'
    for s in e.sym:
      text = text + ' '.join(f'{j:> 8.2e}' for j in s.mtrx_lab.flatten()) + '.\n'
    text = text + f'Inversion: {e.revers}.'
    raise ValueError(text)
