###################6.18##############
import numpy as np
import matplotlib.pyplot as plt

polos = 4
vl = 460
vf = vl/np.sqrt(3)

f = 60

r1 = 0.15
r2 = 0.154

x1 = 0.852
x2 = 1.066

xm = 20

perdasAV = 400
perdasNucleo = 400
perdasDiversas = 150

def calcular_velocidade_sincrona(f, polos):

  return (120 * f) / polos

def calcular_velocidade_mecanica(ns, s):

  return (1 - s) * ns

def calcular_impedancia_equivalente(r1, r2, x1, x2, xm, s):

  z1 = np.complex(r1, x1)
  z2 = np.complex(r2/s, x2)
  zm = np.complex(0, xm)

  return z1 + ((zm * z2) / (zm + z2))

def calcular_corrente_linha(vf, zeq):

  return vf / zeq

def calcular_fator_potencia(il):

  return np.cos(np.angle(il))

def calcular_potencia_entrada(vl, il, fp):

  return np.sqrt(3) * vl * np.abs(il)*fp

def calcular_perdas_estator(il, r1):

  return 3 * (np.abs(il)**2) * r1

def calcular_potencia_GAP(potenciaEntrada, perdasEstator, perdasNucleo):

  return potenciaEntrada - perdasEstator - perdasNucleo

def calcular_potencia_convertida(potenciaGAP, s):

  return (1 - s) * potenciaGAP

def calcular_potencia_saida(potenciaConvertida, perdasMecanicas):

  return potenciaConvertida - perdasMecanicas

def calcular_torque_induzido(potenciaConvertida, nm):

  return potenciaConvertida / ((2*np.pi/60) * nm) 

def calcular_eficiencia(potenciaSaida, potenciaEntrada):

  return potenciaSaida / potenciaEntrada

def solucionar_fluxo_potencia_maquina(ns, r1, r2, x1, x2, xm, s, vf, vl, perdasNucleo, perdasAV, perdasDiversas):

    zeq = calcular_impedancia_equivalente(r1, r2, x1, x2, xm, s)

    il = calcular_corrente_linha(vf, zeq)

    fp = calcular_fator_potencia(il)

    potenciaEntrada = calcular_potencia_entrada(vl, il, fp)

    perdasEstator = calcular_perdas_estator(il, r1)

    potenciaGAP = calcular_potencia_GAP(potenciaEntrada, perdasEstator, perdasNucleo)

    potenciaConvertida = calcular_potencia_convertida(potenciaGAP, s)

    potenciaSaida = calcular_potencia_saida(potenciaConvertida, perdasMecanicas=perdasAV + perdasDiversas)
    
    nm = calcular_velocidade_mecanica(ns, s)

    torqueInduzido = calcular_torque_induzido(potenciaConvertida, nm)

    eficiencia = calcular_eficiencia(potenciaSaida, potenciaEntrada)

    return nm, potenciaSaida, potenciaConvertida, eficiencia, torqueInduzido


ns =  calcular_velocidade_sincrona(f, polos)

escorregamentos = np.arange(1e-3, 0.1, 1e-4)

lista_nm = []
lista_torque = []
lista_potencia_saida = []
lista_potencia_convertida = []
lista_eficiencia = []
for s in escorregamentos:

  nm, potenciaSaida, potenciaConvertida, eficiencia, torque = solucionar_fluxo_potencia_maquina(ns, r1, r2, x1, x2, xm, s, vf, vl,perdasNucleo, perdasAV, perdasDiversas)

  lista_nm.append(nm)
  lista_torque.append(torque)
  lista_potencia_saida.append(potenciaSaida/1000)
  lista_potencia_convertida.append(potenciaConvertida/1000)
  lista_eficiencia.append(eficiencia*100)

plt.plot(lista_nm, lista_torque)
plt.title("Curva Torque x Velocidade - Motor do problema 6.15")
plt.xlabel("nm (rpm)")
plt.ylabel("Torque Induzido (N.m)")
plt.show()

plt.plot(lista_nm, lista_potencia_saida)
plt.title("Curva Potência Saída x Velocidade - Motor do problema 6.15")
plt.xlabel("nm (rpm)")
plt.ylabel("Potência Saída (kW)")
plt.show()

plt.plot(lista_nm, lista_potencia_convertida)
plt.title("Curva Potência Convertida x Velocidade - Motor do problema 6.15")
plt.xlabel("nm (rpm)")
plt.ylabel("Potência Convertida (kW)")
plt.show()

plt.plot(lista_nm, lista_eficiencia)
plt.title("Curva Eficiência x Velocidade - Motor do problema 6.15")
plt.xlabel("nm (rpm)")
plt.ylabel("Eficiencia (%)")
plt.show()