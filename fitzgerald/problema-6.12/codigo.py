####PROBLEMA 6.12 #########
import numpy as np
import pandas as pd

polos = 4
vl = 4160
vf = vl/np.sqrt(3)

f = 60
nm = 1725

r1 = 0.521
r2 = 1.32

x1 = 4.98
x2 = 5.32

xm = 136

perdasRotacionais = 3500
perdasNucleo = 0

def calcular_velocidade_sincrona(f, polos):

  return (120 * f) / polos

def calcular_escorregamento(ns, nm):

  return (ns - nm) / ns

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

def calcular_potencia_saida(potenciaConvertida, perdasAV):

  return potenciaConvertida - perdasAV

def calcular_eficiencia(potenciaSaida, potenciaEntrada):

  return potenciaSaida / potenciaEntrada

result = {}

ns = calcular_velocidade_sincrona(f, polos)

s = calcular_escorregamento(ns, nm)

zeq = calcular_impedancia_equivalente(r1, r2, x1, x2, xm, s)

il = calcular_corrente_linha(vf, zeq)

fp = calcular_fator_potencia(il)

potenciaEntrada = calcular_potencia_entrada(vl, il, fp)

perdasEstator = calcular_perdas_estator(il, r1)

potenciaGAP = calcular_potencia_GAP(potenciaEntrada, perdasEstator, perdasNucleo)

potenciaConvertida = calcular_potencia_convertida(potenciaGAP, s)

potenciaSaida = calcular_potencia_saida(potenciaConvertida, perdasRotacionais)

eficiencia = calcular_eficiencia(potenciaSaida, potenciaEntrada)


result["Velocidade Mecânica (rpm)"] = round(nm, 3)
result["Potência Saída (kW)"] = round(potenciaSaida / 1000, 3)
result["Potência Entrada (kW)"] = round(potenciaEntrada / 1000, 3)
result["Fator de Potência"] = round(fp, 3)
result["Eficiência (%)"] = round(eficiencia * 100, 3)

table_results = pd.Series(data=result)
print(table_results)