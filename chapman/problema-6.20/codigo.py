###################6.20##############
import numpy as np
import matplotlib.pyplot as plt

v_phase = 208/np.sqrt(3)
polos = 6
f = 60

ns = 120*f/polos

wsync = ns * (2*np.pi)/60

r1 = 0.1054
r2 = 0.0707

x1 = 0.211
x2 = 0.317

xm = 4.789

def calcular_torque(vth, r2, rth, s, wsin, xth, x2):

  return (3 * (vth ** 2) * r2/s) / (wsin * ((rth + r2/s)**2 + (xth + x2)**2))


def calcular_zth(r1, x1, xm):

  rth = r1 * ((xm / (x1 + xm))**2)
  xth = x1

  return np.complex(rth, xth)


def calcular_vth(r1, x1, xm, v_phase):

  return v_phase * (xm / np.sqrt(r1**2 + (x1 + xm)**2))


def calculate_n_mecanina(s, ns):

  return (1-s) * ns

escorregamentos = np.arange(0.0001, 1, 0.001, dtype=None)

lista_torque = []
lista_nm = []
lista_potencia_saida = []

for s in escorregamentos:

  zth = calcular_zth(r1, x1, xm)

  vth = calcular_vth(r1, x1, xm, v_phase)

  torque = calcular_torque(vth, r2, np.real(zth), s, wsync, np.imag(zth), x2)

  nm = calculate_n_mecanina(s, ns)

  potencia_saida = torque * nm * (2*np.pi/60)

  lista_torque.append(torque)
  lista_potencia_saida.append(potencia_saida)
  lista_nm.append(nm)

plt.plot(lista_nm, lista_torque)
plt.title("Curva Torque x Velocidade - Problema 6.20")
plt.xlabel("nm (rpm)")
plt.ylabel("Torque Induzido (N.m)")
plt.show()