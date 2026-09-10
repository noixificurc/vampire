#!/bin/python

from numpy import array, cos, eye, outer, pi, sin, sqrt
from numpy.linalg import norm


#------------------------------
# parameter
#------------------------------
v0008 = [ 0.000000e+00, -2.691513e+01,  2.382135e+01]
v0014 = [ 2.330919e+01, -1.345756e+01, -2.382135e+01]
v0208 = [-2.330919e+01, -1.345756e+01, -2.382135e+01]
v0209 = [-2.330919e+01,  1.345756e+01,  2.382135e+01]
v0902 = [ 2.330919e+01, -1.345756e+01, -2.382135e+01]
v0114 = [ 2.330919e+01,  1.345756e+01,  2.382135e+01]

v     = v0008
alpha = 0
n     = [0,0,1]

print(norm(v0008), array(v0008)/norm(v0008))


#------------------------------
# helper functions
#------------------------------
def vec2mat(v):
  v = array(v)
  vx, vy, vz = v
  return array([
    [0,   -vz,  vy],
    [vz,   0,  -vx],
    [-vy, vx,   0]
  ])


def rotz(alpha):
  rad = alpha * pi / 180
  c = cos(rad)
  s = sin(rad)
  return array([
    [c, -s, 0],
    [s,  c, 0],
    [0,  0, 1]
  ])


def rotate(S, alpha):
  R = rotz(alpha)
  print(R)
  return R @ S @ R.T


def mirror(S, n):
  if norm(n):
    n = array(n) / norm(n)
  M = eye(3) - 2 * outer(n, n)
  print(M)
  return M @ S @ M.T


def mat2vec(S):
  return array([
    S[2, 1], # vx
    S[0, 2], # vy
    S[1, 0]  # vz
  ])


#------------------------------
# run
#------------------------------
V = vec2mat(v)
V = rotate(V, alpha)
V = mirror(V, n)
vp = mat2vec(V)


#------------------------------
# output
#------------------------------
print('input:  ', " ".join(f"{i:> 8.4f}" for i in v))
print('output: ', " ".join(f"{i:> 8.4f}" for i in vp))
