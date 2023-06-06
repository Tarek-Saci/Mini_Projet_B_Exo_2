import matplotlib.pyplot as plt
import numpy as np
import Exercice2bF as m
from importlib import reload
reload(m)
import time as time


#Choix des paramètres par l'utilisateur
params = m.get_params()
grid = m.create_grid(params)
dt=0.25*params['dx']**2/params['kappa']

duree=int(input(f'Entrer la durée d\'étude souhaitée (en s) sachant que le pas de temps pour les paramètres entrés est de {dt} : '))
if float.is_integer(duree/dt):
    nombre_increments=int(duree/dt)
else:
    nombre_increments=int(duree//dt +1)


#Affichage de la solution initiale
T = m.init_temp(grid, params)


#Déroulement de l'avancement temporel

m.avancement_tempo(nombre_increments)
