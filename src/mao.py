import numpy as np

class Mao():
    def __init__(self, dedo_0, dedo_1, dedo_2, dedo_3, teta_0, teta_1, teta_2, teta_3):
        #0, 1, 2, 3 - Indicador, Meio, Anelar, Min

        self.dedo = [dedo_0, dedo_1, dedo_2, dedo_3]
        self.teta = np.deg2rad([teta_0, teta_1, teta_2, teta_3])

    def geometria(self, r0, r1, r2, r3, f0, f1, f2):
        #avaliando a mao direita, vista de cima, eixo x - seguindo a ordem dos dedos, eixo y - p onde o dedo aponta, eixo z - p cima da mao
        #ri = raio de cada dedo
        #fi = folga entre os dedos
        #self.dbi = distancia da base de cada dedo ate o "centro" 
        #self.dpi = distancia da ponta de  cada dedo ate o "centro"
        #self.dpbi = distancia da ponta de cada dedo ate a base

        self.db0 = np.array([r0 + f0 + 2*r1 + f1/2, 0, 0])
        self.db1 = np.array([r1 + f1/2, 0, 0])
        self.db2 = np.array([-(f1/2 + r2), 0, 0])
        self.db3 = np.array([-(f1/2 + 2*r2 + f2 + r3), 0, 0])

        l_dpb = []

        for dedo, teta in zip(self.dedo, self.teta):

            dist = np.array([0, np.sum(dedo.l*np.cos(dedo.teta)), np.sum(dedo.l*np.sen(dedo.teta))])

            rot = np.array([np.cos(teta), -np.sen(teta), 0,
                            np.sen(teta), np.cos(teta), 0,
                            0,            0,            1])

            l_dpb.append(rot @ dist)
        
        self.dpb0 = l_dpb[0]
        self.dpb1 = l_dpb[1]
        self.dpb2 = l_dpb[2]
        self.dpb3 = l_dpb[3]

        self.dp0 = self.dpb0 + self.db0
        self.dp1 = self.dpb1 + self.db1
        self.dp2 = self.dpb2 + self.db2
        self.dp3 = self.dpb3 + self.db3

    def rot_dedo_para_mao(self, F):

        F_rot = np.zero(4, 3)

        for dedo, teta in zip(self.dedo, self.teta):

            rot = np.array([np.cos(teta), -np.sen(teta), 0,
                            np.sen(teta), np.cos(teta), 0,
                            0,            0,            1])
            
            F_rot[dedo, :] = rot @ F

        return F_rot
