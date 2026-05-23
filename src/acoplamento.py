import numpy as np
from src import physics
from src import ativacao

W = np.array([[1, 0.2, 0.1, 0.05],
              [0.25, 1, 0.35, 0.15],
              [0.1, 0.4, 1, 0.45],
              [0.05, 0.15, 0.35, 1]])


def ativacao_tensoes(ativacao):
    return W @ ativacao

#Vamos propor o modelo mais simples possivel, a pinca de um dedo: nesse caso
#o estado de tensoes da ativacao eh igual ao estado de tensoes se eu apenas aplicasse a forca

def evo_pinca(F_alvo, dedo, ativacao_0, dt = 1):

    T = ativacao_tensoes(ativacao_0)
    F = physics.calc_forca_dedo(T[dedo.num], dedo.rp, dedo.rs, dedo.l, dedo.teta, np.array([0, 1]))
    ativacao = ativacao_0
    it = 0
    
    while F_alvo > np.linalg.norm(F):
        
        ativacao = ativacao.simples(ativacao, F_alvo, F, dt)
        T = ativacao_tensoes(ativacao)
        F = physics.calc_forca_dedo(T[dedo.num], dedo.rp, dedo.rs, dedo.l, dedo.teta, np.array([0, 1]))
        it += 1
    
    return ativacao, T, F, it

#Agora, a pinca com dois dedos: eh necessario M = 0, a evolucao agora eh necessaria para 
#encontrar o estado real de tensoes

#COLOCAR A RESPOSTA DAS FORCAS NUM VETOR 3, PARA EVENTUALMENTE MANDAR P SISTEMA INERCIAL

def evo_pinca_2(F_alvo, F_alvo_dir, mao, dedos, ativacao_0, dt = 1):
    #dedos = tupla com os dedos envolvidos na pinca
    #F_alvo_dir = np.array(4, 2) codificando a direcao das resultantes em cada dedo

    T = ativacao_tensoes(ativacao_0)
    F = np.zeros([4, 3])

    for i in dedos:
        F[i] = physics.calc_forca_dedo(T[i], mao.dedo[i].rp, mao.dedo[i].rs, mao.dedo[i].l, mao.dedo[i].teta, F_alvo_dir[i])
    
    F = mao.rot_dedo_para_mao(F)

    ativacao = ativacao_0
    it = 0

    while F_alvo > np.linalg.norm(F):
        
        ativacao = ativacao.simples(ativacao, F_alvo, F, dt)

        T = ativacao_tensoes(ativacao)

        for i in dedos:
            F[i] = physics.calc_forca_dedo(T[i], mao.dedo[i].rp, mao.dedo[i].rs, mao.dedo[i].l, mao.dedo[i].teta, F_alvo_dir[i])
            R = physics.calc_resultante(F, F_alvo)
        it += 1
    
    return ativacao, T, F, it
