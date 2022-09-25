import pandas as pd
from math import log
from random import random
import numpy as np

INF = 999999
NUMBER_OF_SERVERS = 10

def getArrivalTime(_lambda_max, s):
  t = s
  while(1):
    u = random()
    t = t - ((1/_lambda_max) * log(u))
    u = random()

    if (u <= (_lambda_max)): 
      return t

def getExecutionTime(_lambda):
  b = 1/_lambda
  exec_time = np.random.exponential(b)
  return exec_time

# Simulacion
# 2400 solicitudes por minuto -> 40 por segundo

# Variables iniciales
Tp = 0                              # Tiempo luego de cerrar el server
T = 3600                            # Tiempo de cierre del server
_lambda_max = 40 * T                # Solicitudes 
_lambda_exp = 10                    # Solicitudes que puede atender por segundo
t = 0                               # Tiempo actual en segundos
Na = 0                              # Numero de llegadas al tiempo t
Nd = 0                              # Numero de salidas al tiempo t             
ta = getArrivalTime(_lambda_max, t) # Tiempo de llegada de un evento
td = 999999                         # Tiempo de salida de un evento
n = 0                               # Cantidad de solicitudes en el sistema

# SYSTEM STATUS INIT
iddle_times = []
SS = []
for _ in range(NUMBER_OF_SERVERS):
  SS.append(INF)
  iddle_times.append(0)

## Variables para las metricas
arrival_time = []
in_line_time = []
departure_time = []

# Se inicia la simulacion
while (1):
  ss_min = min(SS)
  ss_min_index = SS.index(ss_min)

  # [99999, 99999, 99999]

  # -> Solicitud entrante y no es tiempo de cierre
  # if ((ta <= td) and (ta <= T)):
  if ((ta <= ss_min) and (ta <= T)):

    # Check para ver si el servidor estaba desocupado
    if (ss_min == INF): iddle_times[ss_min_index] += ta - t

    t = ta
    Na += 1
    n += 1
    ta = getArrivalTime(_lambda_max, t)

    # Se atiende directamente la solicitud
    if (n <= NUMBER_OF_SERVERS):
      in_line_time.append(0)
      td = t + getExecutionTime(_lambda_max)
      SS[ss_min_index] = td

    # Guardamos tiempo de llegada
    arrival_time.append(t)

  # -> Solicitud de salida y no es tiempo de cierre
  elif ((ss_min < ta) and (ss_min <= T)):
    t = ss_min
    n -= 1
    Nd += 1


    # Ya no quedan mas solicitudes en el sistema
    if (SS.count(INF) >= n):
      SS[ss_min_index] = INF
    else:
      waited_time = t - arrival_time[Nd]
      in_line_time.append(waited_time) 
      td = t + getExecutionTime(_lambda_max)
      SS[ss_min_index] = td
    
    # Guardamos metricas
    departure_time.append(t)

  # -> El evento ocurre luego de cerrar el server, pero sigue atendiendo
  elif ((min(ta, ss_min) > T) and (n > 0)):
    t = ss_min
    n -= 1
    Nd += 1

    # Si aun no se terminan las solicitudes
    if (n > 0):
      waited_time = t - arrival_time[Nd]
      in_line_time.append(waited_time) 
      td = t + getExecutionTime(_lambda_max) 
      SS[ss_min_index] = td

    # Guardamos metricas
    departure_time.append(t)

  # -> El evento ocurre luego de cerrar el server, ya no atiende
  else:
    Tp = max(t - T, 0)

