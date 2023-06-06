import numpy as np
import matplotlib.pyplot as plt


#########Définition des paramètres###############################
def get_params():
    params = {}
    params['L'] = input('Largeur de la plaque')
    params['nx'] = int(input('Nombre de segments selon x'))
    params['H'] = input('Longueur de la plaque')
    params['ny'] = int(input('Nombre de segments selon y'))
    params['kappa'] = 98.8e-6
    params['dx'] = params['L'] / (params['nx'])
    params['dy'] = params['H'] / (params['ny'])
    params['xc'] = input('Abscisse du point chaud')
    params['yc'] = input('Ordonnée du point chaud')
    params['A'] = input('Amplitude de la surchauffe')
    params['sigma'] = input('Paramètre sigma de la surchauffe')
    params['T0'] = input('Température ambiante')

    return params


##########Génération de la grille de calcul############################
def create_grid(p):
    L = p['L']
    H = p['H']
    nx = p['nx']
    ny = p['ny']

    x = np.linspace(0, L, nx + 1)
    y = np.linspace(0, H, ny + 1)
    X, Y = np.meshgrid(x, y)
    grid = {}
    grid['X'] = X
    grid['Y'] = Y

    return grid


############"Génération de la solution initiale###########################
def init_temp(grid, par):
    T = par['A'] * np.exp(-((grid['X'] - par['xc']) ** 2 + (grid['Y'] - par['yc']) ** 2) / (2 * par['sigma'])) + par[
        'T0']
    T[0] = T[-1] = par['T0']
    T[:, 0] = T[:, -1] = par['T0']
    return T


###############Calcul RHS avec des boucles###############################
#Cette fonction ne sera pas utilisée par la suite
def calcul_RHS_boucles(T, param):
    RHS = np.zeros([param['ny'], param['nx']])
    for i in range(1, param['ny'] - 1):
        for j in range(1, param['nx'] - 1):
            RHS[i, j] = param['kappa'] * ((T[i + 1, j] - 2 * T[i, j] + T[i - 1, j]) / (param['dy']) ** 2 + (
                        T[i, j + 1] - 2 * T[i, j] + T[i, j - 1]) / (param['dx']) ** 2)
    return RHS


##############Calcul RHS vectoriel#####################
def calcul_RHS_vector(T, param):
    T_dx = np.roll(T, -1, axis=1)

    T_mdx = np.roll(T, 1, axis=1)
    T_dy = np.roll(T, -1, axis=0)
    T_mdy = np.roll(T, 1, axis=0)
    RHS = param['kappa'] * ((T_dy - 2 * T + T_mdy) / (param['dy']) ** 2 + (
            T_dx - 2 * T + T_mdx) / (param['dx']) ** 2)
    RHS[0] = RHS[-1] = 0
    RHS[:, 0] = RHS[:, -1] = 0

    return RHS


###########Affichage des résultats########################
def visu_unique(grid, T):
    plt.contourf(grid['X'], grid['Y'], T)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.colorbar()
    plt.show()


params = get_params()
grid = create_grid(params)

T = init_temp(grid, params)

def avancement_tempo(nb_increments):
    params = get_params()
    grid = create_grid(params)
    T = init_temp(grid, params)
    print('tempe',type(T))
    dt = 0.25 * params['dx'] ** 2 / params['kappa']
    Temperatures = []
    Temperatures.append(T)
    print('temp',Temperatures)

    residus = np.array([0])
    maximum = np.array([np.max(T)])
    minimum = np.array([np.min(T)])
    mean = np.array([np.mean(T)])
    L2 = np.array([0])
    Linf = np.array([0])

    for i in range(nb_increments):
        RHS = calcul_RHS_vector(T, params)
        res = (T + dt * RHS - T) / (T + dt * RHS)
        residus = np.append(residus, res)
        Linf = np.append(Linf, np.max(np.absolute(res)))
        L2 = np.append(L2, np.mean(np.square(res)))
        T = T + dt * RHS
        minimum = np.append(minimum, np.min(T))
        maximum = np.append(maximum, np.max(T))
        mean = np.append(mean, np.mean(T))
        Temperatures.append(T)

    x = np.linspace(1, nb_increments + 1, nb_increments + 1)

    # Affichage du max et du min
    plt.subplot(2, 2, 1)
    plt.plot(x, maximum)
    plt.plot(x, minimum)
    plt.xlabel('Nombre d\'incréments')
    plt.ylabel('Température')
    plt.title('Evolution des températures minimale et maximale')

    # Affichage de la moyenne
    plt.subplot(2, 2, 2)
    plt.plot(x, mean)
    plt.xlabel('Nombre d\'incréments')
    plt.ylabel('Température')
    plt.title('Evolution de la température moyenne')
    # Affichage du L2
    plt.subplot(2, 2, 3)
    plt.plot(x, L2)
    plt.xlabel('Nombre d\'incréments')
    plt.ylabel('Norme L2 du résidus')

    # Affichage du Linfini
    plt.subplot(2, 2, 4)
    plt.plot(x, Linf)
    plt.xlabel('Nombre d\'incréments')
    plt.ylabel('Norme Linf du résidus')
    plt.show()

    nombre_subplots = nb_increments

    # Calculer le nombre de lignes et de colonnes nécessaires pour la grille de subplots
    nombre_lignes = int(nombre_subplots ** 0.5)
    nombre_colonnes = int((nombre_subplots + nombre_lignes - 1) / nombre_lignes)

    # Créer la grille de subplots
    fig, axes = plt.subplots(nombre_lignes, nombre_colonnes)

    # Parcourir les subplots et les personnaliser
    for i, ax in enumerate(axes.flat):
        if i<nombre_subplots :
            trace = ax.contourf(grid['X'], grid['Y'], Temperatures[i])
            fig.colorbar(trace)

    # Suppression des subplots inutilisés
    if nombre_subplots < len(axes.flat):
        for j in range(nombre_subplots, len(axes.flat)):
            fig.delaxes(axes.flatten()[j])

    # Ajuster les espaces entre les subplots
    fig.tight_layout()
    plt.show()
