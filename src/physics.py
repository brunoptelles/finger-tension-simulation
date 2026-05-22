import numpy as np


def calc_tensao_dedo(F, rp, rs, l, teta_graus, razao_elastica = 1):
    #l = [l1, l2, l3]  rs = [rs1, rs2, 0]   rp = [rp1, rp2, rp3]   teta = [teta1, teta2, teta3]
    #F = [Fx,Fy]    razao_elastica = kp/ks 
    delta = 1
    teta = np.deg2rad(teta_graus)

    d_Fp = np.sum(rp*delta)
    d_Fs = np.sum(rs*delta)

    d_y = np.array([0, np.dot(l, np.cos(teta))*delta])
    d_x = np.array([-np.dot(l,np.sin(teta))*delta, 0])

    Fs = (np.dot(F,d_x) + np.dot(F,d_y))/(razao_elastica*d_Fp**2/d_Fs + d_Fs)
    Fp = razao_elastica*Fs*d_Fp/d_Fs

    return np.array([Fp, Fs])


def calc_forca_dedo(T, rp, rs, l, teta_graus, dir, razao_elastica = 1):
    #l = [l1, l2, l3]  rs = [rs1, rs2, 0]   rp = [rp1, rp2, rp3]   teta = [teta1, teta2, teta3]
    #F = [Fx,Fy]    razao_elastica = kp/ks   dir = [x, y] - restricao de direcao da forca resultante
    delta = 0.0001
    teta = np.deg2rad(teta_graus)
    dir_norm = dir/np.linalg.norm(dir)
    angulo_F_Fx = np.arccos(dir_norm[0])

    d_Fp = np.sum(rp*delta)
    d_Fs = np.sum(rs*delta)

    d_y = np.array([0, np.dot(l, np.cos(teta))*delta])
    d_x = np.array([-np.dot(l,np.sin(teta))*delta, 0])
    

    Fs = T/(razao_elastica*d_Fp/d_Fs + 1)
    Fp = razao_elastica*Fs*d_Fp/d_Fs

    #F = (Fp*d_Fp + Fs*d_Fs)/(np.cos(angulo_F_Fx)*d_x + np.sin(angulo_F_Fx)*d_y)
    F = (Fp*d_Fp + Fs*d_Fs)/(dir_norm[0]*d_x[0] + dir_norm[1]*d_y[1])

    return dir_norm * F
