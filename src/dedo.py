import numpy as np

class Dedo():
    def __init__(self, rp, rs, l, teta, num, razao_elastica = 1):
        self.rp = rp
        self.rs = rs
        self.l = l
        self.teta = np.deg2rad(teta)
        self.num = num
        self.razao_elastica = razao_elastica
        