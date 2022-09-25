import pandas as pd
from math import log
from random import random

INF = 999999

def getArrivalTime(_lambda_max, s):
  t = s
  while(1):
    u = random()
    t = t - ((1/_lambda_max) * log(u))
    u = random()

    if (u <= (_lambda_max)): 
      return t

def getExecutionTime(_lambda_max, s):
  print('wuuu')
  return 0

# Simulacion
# 2400 solicitudes por minuto -> 40 por segundo

# Variables iniciales
T = 3600                            # Tiempo de cierre del server
_lambda_max = 40 * T                # Solicitudes 
t = 0                               # Tiempo actual en segundos
Na = 0                              # Numero de llegadas al tiempo t
Nd = 0                              # Numero de salidas al tiempo t             
ta = getArrivalTime(_lambda_max, t) # Tiempo de llegada de un evento
td = 999999                         # Tiempo de salida de un evento
n = 0                               # Cantidad de solicitudes en el sistema

## Variables para las metricas
iddle_time = 0
arrival_time = []
in_line_time = []
departure_time = []

# Se inicia la simulacion
while (1):

  # -> Solicitud entrante y no es tiempo de cierre
  if ((ta <= td) and (ta <= T)):

    # Check para ver si el servidor estaba desocupado
    if (td == INF): iddle_time += ta - t

    t = ta
    Na += 1
    n += 1
    ta = getArrivalTime(_lambda_max, t)

    # Se atiende directamente la solicitud
    if (n == 1):
      in_line_time.append(0) 
      td = t + getExecutionTime(_lambda_max, t)

    # Guardamos tiempo de llegada
    arrival_time.append(t)

  # -> Solicitud de salida y no es tiempo de cierre
  elif ((td < ta) and (td <= T)):
    t = td
    n -= 1
    Nd += 1

    # Ya no quedan mas solicitudes en el sistema
    if (n == 0):
      td = INF
    else:
      waited_time = t - arrival_time[Nd]
      in_line_time.append(waited_time) 
      td = t + getExecutionTime(_lambda_max, t) 
    
    # Guardamos metricas
    departure_time.append(t)

  # -> El evento ocurre luego de cerrar el server, pero sigue atendiendo
  elif ((min(ta, td) > T) and (n > 0)):
    t = td
    n -= 1
    Nd += 1

    # Si aun no se terminan las solicitudes
    if (n > 0):
      waited_time = t - arrival_time[Nd]
      in_line_time.append(waited_time) 
      td = t + getExecutionTime(_lambda_max, t) 

    # Guardamos metricas
    departure_time.append(t)

  # -> El evento ocurre luego de cerrar el server, ya no atiende
  else:
    Tp = max(t - T, 0)

