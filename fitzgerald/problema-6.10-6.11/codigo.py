####PROBLEMA 6.10 #########
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

polos = 4
vl = 460
vf = vl/np.sqrt(3)

f = 60

r1 = 0.103
r2 = 0.225

x1 = 1.10
x2 = 1.13

xm = np.complex(0, 59.4)

perdasAV = 265
perdasNucleo = 220

potenciaSaidaPlenaCarga = 25e3

def calcular_velocidade_sincrona(f, polos):

  return (120 * f) / polos

def calcular_velocidade_mecanica(ns, s):

  return (1 - s) * ns

def calcular_resistencia_nucleo(vf, perdasNucleo):

  return np.complex((vf**2) / (perdasNucleo/3), 0)

def calcular_impedancia_equivalente(r1, r2, x1, x2, rc, xm, s):

  z1 = np.complex(r1, x1)
  z2 = np.complex(r2/s, x2)
  zm = (rc * xm) / (rc + xm)

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

def calcular_potencia_saida(potenciaConvertida, perdasAV):

  return potenciaConvertida - perdasAV

def calcular_torque_carga(potenciaSaida, nm):

  return potenciaSaida / ((2*np.pi/60) * nm) 

def calcular_eficiencia(potenciaSaida, potenciaEntrada):

  return potenciaSaida / potenciaEntrada

def solucionar_fluxo_potencia_maquina(r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV):

    zeq = calcular_impedancia_equivalente(r1, r2, x1, x2, rc, xm, s)

    il = calcular_corrente_linha(vf, zeq)

    fp = calcular_fator_potencia(il)

    potenciaEntrada = calcular_potencia_entrada(vl, il, fp)

    perdasEstator = calcular_perdas_estator(il, r1)

    potenciaGAP = calcular_potencia_GAP(potenciaEntrada, perdasEstator, perdasNucleo)

    potenciaConvertida = calcular_potencia_convertida(potenciaGAP, s)

    potenciaSaida = calcular_potencia_saida(potenciaConvertida, perdasAV)

    nm = calcular_velocidade_mecanica(ns, s)

    torqueCarga = calcular_torque_carga(potenciaSaida, nm)

    eficiencia = calcular_eficiencia(potenciaSaida, potenciaEntrada)

    return nm, potenciaSaida, potenciaEntrada, fp, eficiencia, torqueCarga


def eficiencia_potenciaSaida(nm_0, nm_1, r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV):
  
  velocidades_mecanica = np.arange(nm_0, nm_1, -1)

  lista_eficiencia = []
  lista_potencia_saida = []
  for nm in velocidades_mecanica:

    s = (ns - nm) / ns

    _, potenciaSaida, _, _, eficiencia, _ = solucionar_fluxo_potencia_maquina(r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV)

    lista_eficiencia.append(eficiencia*100)

    lista_potencia_saida.append(potenciaSaida/1000)

  return lista_potencia_saida, lista_eficiencia

ns = calcular_velocidade_sincrona(f, polos)

rc = calcular_resistencia_nucleo(vf, perdasNucleo)

results = {}

for s in [0.01, 0.02, 0.03]:

    result = {}
    nm, potenciaSaida, potenciaEntrada, fp, eficiencia, torqueCarga = solucionar_fluxo_potencia_maquina(r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV)

    result["Velocidade Mecânica (rpm)"] = round(nm, 3)
    result["Torque Carga (N.m)"] = round(torqueCarga, 3)
    result["Potência Saída (kW)"] = round(potenciaSaida / 1000, 3)
    result["Potência Entrada (kW)"] = round(potenciaEntrada / 1000, 3)
    result["Fator de Potência"] = round(fp, 3)
    result["Eficiência (%)"] = round(eficiencia * 100, 3)

    results[s] = result

table_results = pd.DataFrame(data=results)
print(table_results)

####PROBLEMA 6.11 #########
escorregamentos = np.arange(1e-6, 1, 1e-6)

def busca_velocidade_mecanica_equivalente(escorregamentos, r1, r2, x1, x2, rc, xm, vf, ns, perdasNucleo, perdasAV, potenciaComparacao):

  nm_encontrado = 0
  for s in escorregamentos:

    nm, potenciaSaida, _ , _, _, _ = solucionar_fluxo_potencia_maquina(r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV)

    if (round(potenciaSaida, 0) == potenciaComparacao):
      nm_encontrado = nm
      break

  return nm_encontrado

#######Letra (A)##########
nm_plena_carga = busca_velocidade_mecanica_equivalente(escorregamentos, r1, r2, x1, x2, rc, xm, vf, ns, perdasNucleo, perdasAV, potenciaComparacao=potenciaSaidaPlenaCarga)

#######Letra (B)##########
nm_vazio = busca_velocidade_mecanica_equivalente(escorregamentos, r1, r2, x1, x2, rc, xm, vf, ns, perdasNucleo, perdasAV, potenciaComparacao=perdasAV)

print("Velocidade mecânica a plena carga: " + str(nm_plena_carga) + " (rpm)")
print("Velocidade mecânica a vazio: " + str(nm_vazio) + " (rpm)")

#######Letra (C)##########
lista_potencia_saida, lista_eficiencia = eficiencia_potenciaSaida(nm_vazio, nm_plena_carga, r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV)

plt.plot(lista_potencia_saida, lista_eficiencia)
plt.title("Eficiência x Potência Saída - Motor do problema 6.10")
plt.xlabel("Potência saída (kW)")
plt.ylabel("Eficiencia (%)")
plt.show()

#######Letra (D)##########
nm_5 = busca_velocidade_mecanica_equivalente(escorregamentos, r1, r2, x1, x2, rc, xm, vf, ns, perdasNucleo, perdasAV, potenciaComparacao=5000)
lista_potencia_saida, lista_eficiencia = eficiencia_potenciaSaida(nm_5, nm_plena_carga, r1, r2, x1, x2, rc, xm, s, vf, perdasNucleo, perdasAV)

plt.plot(lista_potencia_saida, lista_eficiencia)
plt.title("Eficiência x Potência Saída - Motor do problema 6.10")
plt.xlabel("Potência saída (kW)")
plt.ylabel("Eficiencia (%)")
plt.show()