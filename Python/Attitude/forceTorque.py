import numpy as np
import qnv
import frames as fs

def gravityForceTorque(state):
	#gives force in ECIF and torque in body frame due to gravity


	v_L_b = 
	v_dL = v_L_b/nLg
	dL = np.linalg.norm(v_dL)
	dm = mu_m*dL
	v_F_i = np.zeros((3,1))
	v_T_b = np.zeros((3,1))
	q = state[7:10].copy()
	qi = qnv.quatInv(q);
	v_pos_sat_i = state[1:3].copy()
	v_pos_sat_b = qnv.quatRotate(q,v_pos_sat_i)

	if nLg>1 :
		for i in (1:nLg/2) :

			v_F_i, v_T_b = simpsonG(v_F_i,v_T_b,4,g_dFdT,dm,(2*i-1),v_dL,v_pos_sat_b,q)
			
		for i in (2:nLg/2) : 

			v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,2,g_dFdT,dm,(2*i-2)v_dL,v_pos_sat_b,q)
			
		for i = [1,nLg]:
			
			v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,1,g_dFdT,dm,i,v_dL,v_pos_sat_b,q) 

		v_F_i = v_F_i/3
		v_T_b = v_T_b/3

	else:
		v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,1,g_dFdT,dm,nLg/2,v_dL,v_pos_sat_b,q) 	

	return v_F_i, v_T_b

def g_da(p1,p2):
	#gives gravitational acceleration at position p1+p2
	da = -G*M*(p1+p2)/(np.linalg.norm(p1+p2)**3)
	return da

def g_dFdT(dm,v_pos_sat_b,v_pos_dL_b,q):
	#gives differential force in ECIF and differential torque in body frame due to gravity
	
	v_dF_b = dm*(g_da(v_pos_sat_b,v_pos_dL_b)
	v_dF_i = rotate(q,v_dF_b)
	v_dT_b = qnv.cross1(v_pos_dL_b,v_dF_b)
	return v_dF_i, v_dT_b


def magneticForceTorque(state,t):
	q = state[7:10].copy()
	qi = qnv.quatInv(q)
	v_pos_sat_i = state[1:3].copy()
	v_pos_sat_b = qnv.quatRotate(qi, v_pos_sat_i)
	v_v_sat_i = state[4:6].copy()
	v_L_b = 
	v_L_i = qnv.quatRotate(q,v_L_b)
	v_dL_i = v_L_i/nLb
	v_dL_cap_i = v_dL_i/np.linalg.norm(v_dL_i)
	dL = np.linalg.norm(v_dL_i)
	v_dL_b = v_L_b/nLb
	

	if nLb>1 :
		for i in (1:nLb/2):
			v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,4,m_dFdT,(2*i-1),v_pos_sat_b,v_dL_b,v_dL_cap_i,v_v_sat_i,q,t,dL) 
			
		for i in (2:nLb/2):
			v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,2,m_dFdT,(2*i-2),v_pos_sat_b,v_dL_b,v_dL_cap_i,v_v_sat_i,q,t,dL)
			
		for i = [1,nLg]:
			v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,1,m_dFdT,i,v_pos_sat_b,v_dL_b,v_dL_cap_i,v_v_sat_i,q,t,dL)

		v_F_i = v_F_i/3
		v_T_b = v_T_b/3

	else:
		v_F_i, v_T_b = simpsonG(v_F_i, v_T_b,1,m_dFdT,nLb/2,v_pos_sat_b,v_dL_b,v_dL_cap_i,v_v_sat_i,q,t,dL)

	return v_F_i, v_T_b


def m_dFdT(v_pos_dL_b,v_dL_cap_i,v_v_sat_i,q,t,dL):

		qi = qnv.quatInv(q)
		v_pos_dL_i = qnv.quatRotate(q,v_pos_dL_b)
		height = np.norm(v_pos_dL_i) - R
		v_pos_dL_e = fs.ecif2ecef(v_pos_dL_i,t)
		lat, lon = fs.latlon(v_pos_dL_e)
		v_B_n = igrf
		v_B_e = fs.ned2ecef(lat,lon)
		v_dL_cap_e = fs.ecif2ecef(v_dL_cap_i,t)
		v_v_sat_e = qnv.quatRotate(q,v_v_sat_i)
		e = np.dot(v_dL_cap_e, qnv.cross1(v_v_sat_e, v_B_e))
		i = e/mu_r
		v_dF_e = i*qnv.cross1(dL*v_dL_cap_e,v_B_e)
		v_dF_i = fs.ecec2ecif(v_dF_e, t)
		v_dF_b = qnv.quatRotate(v_dF_i, t)
		v_dL_cap_b = qnv.quatRotate(qi,v_dL_cap_i)
		v_dT_b = qnv.cross1(dL*v_dL_cap_b, v_dF_b)
		return v_dF_i, v_dT_b













