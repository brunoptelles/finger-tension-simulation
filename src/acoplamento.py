import numpy as np
from src import physics

W = np.array([[1, 0.2, 0.1, 0.05],
              [0.25, 1, 0.35, 0.15],
              [0.1, 0.4, 1, 0.45],
              [0.05, 0.15, 0.35, 1]])


def ativacao_tensoes(ativacao):
    return W @ ativacao

#Vamos propor o modelo mais simples possivel, a pinca de um dedo:

def evolucao_pinca(F_alvo, dedo, ativacao_0, dt):

    T = ativacao_tensoes(ativacao_0)
    F = physics.calc_forca_dedo(T[dedo.num], dedo.rp, dedo.rs, dedo.l, dedo.teta, np.array([0, 1]))
    ativacao = ativacao_0
    it = 0
    
    while F_alvo > np.linalg.norm(F):
        d_ativacao = ativacao*(1 - np.linalg.norm(F)/F_alvo)
        ativacao = ativacao + d_ativacao*dt
        T = ativacao_tensoes(ativacao)
        F = physics.calc_forca_dedo(T[dedo.num], dedo.rp, dedo.rs, dedo.l, dedo.teta, np.array([0, 1]))
        it += 1
    
    return ativacao, T, F, it
