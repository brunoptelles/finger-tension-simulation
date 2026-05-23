import numpy as np

def simples(ativacao, F_alvo, F, dt = 1):

    d_ativacao = ativacao*(1 - np.linalg.norm(F)/F_alvo)
    ativacao = ativacao + d_ativacao*dt

    return ativacao