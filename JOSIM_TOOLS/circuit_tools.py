import os
import numpy as np
import time as tm
import multiprocessing as mp
import JOSIM_TOOLS.data_tools as data_tools

def parallelize(s_l_1,s_l_1_v,s_r_2,s_2_p,labels,resulution,end_time,start_time,time,q,c_p_d,p_p_d,d_p_d,target_frequency,Type_of_Simulation,start):

	print(f'{s_l_1_v}')
	point_of_fft=np.zeros((len(labels)))

	
	for s_l_2,s_l_2_v in zip(s_r_2,s_2_p):

		temp_cir_filename=f'JOSIM_TEMP/test_josim-{s_l_1%30}.js'
		data_filename=f'JOSIM_TEMP/test_josim-{s_l_1%30}.dat'

		simulation(temp_cir_filename,data_filename,s_l_1_v,s_l_2_v,labels,resulution,end_time,start_time,q,c_p_d)
		#+++++++++Time++++++++
		#print(f'after data process:{tm.perf_counter()-start}\n')
		#+++++++++Time++++++++


		trim_lin=process_data(data_filename,time,resulution)

		#+++++++++Time++++++++
		#print(f'after data process:{tm.perf_counter()-start}\n')
		#+++++++++Time++++++++

		#new_lin[s_l_2]=trim_lin
		if 'fft' in Type_of_Simulation:
			fft_result=data_tools.fft(trim_lin,labels,(time)/resulution,resulution,)
		
		if'fft_s'==Type_of_Simulation:
			point_of_fft=data_tools.point_sweep(trim_lin,time,resulution,labels,target_frequency)

	#+++++++++Time++++++++
	#print(f'after data process:{tm.perf_counter()-start}\n')
	#+++++++++Time++++++++	

	#point_of_fft=data_tools.mean_finder(trim_lin,(time)/resulution,resulution,labels)
	#data_tools.moving_ave(trim_lin,t,resulution,time,amp_2,amp_1)
	
	if Type_of_Simulation=='n':
		answer=trim_lin
		return answer

	elif Type_of_Simulation=='fft':
		answer=fft_result
		return answer

	elif Type_of_Simulation=='fft_s':
		answer=point_of_fft
		answer[0]=s_l_1_v
		return answer
	
	return 0
	


def simulation(temp_cir_filename,data_filename,s_l_1_v,s_l_2_v,labels,resulution,end_time,start_time,q,c_p_d):
	write_cir(temp_cir_filename,s_l_1_v,s_l_2_v,labels,resulution,end_time,start_time,q,c_p_d)
	os.system(f"./josim-cli {temp_cir_filename}>{data_filename}")


def process_data(data_filename,time,resulution):
	#Raad the results

	data_file = open(data_filename, "r")
	lines = data_file.readlines()
	data_file.close()

	#Deleting the extra word lines
	del lines[0:int(len(lines)-(time)/resulution+1)]		

	#Now all the results will be transferd to "data" array
	result=[]
	for string in lines:
		string=string.split()
		string=[float(i) for i in string]
		result.append(string)
	return result
	

def write_cir(file_name,s_l_1_v,s_l_2_v,labels,resulution,end_time,start_time,q,c_p_d):
	cir = open(file_name, 'w')
	#----------------------------------The Circuit
	
	
	IC=c_p_d.get("IC")
	RTYPE=c_p_d.get("RTYPE")
	R0=c_p_d.get("R0")
	c=c_p_d.get("c")
	fp=c_p_d.get("fp")
	fs=c_p_d.get("fs")
	RL=c_p_d.get("RL")



	cir.writelines([
			f'\n.model jj1 jj(IC={IC},RTYPE={RTYPE},R0={R0},c={c}p)',
			f'\n.include ../JOSIM_TOOLS/custom_elements.js',
			f'\nX_cir circulator 1 2 3',
			f'\nV_signal 0 4 sin(0 {10*s_l_2_v}u {fs}G 25p)',
			f'\nV_pump 4 1 sin(0 {s_l_1_v}u {fp}G)',
			f'\nX_JJ 80_jj 2 0',
			f'\nR_source_check 1 0 1000000',
			#f'\nL_JJ 2 0 1f',
			f'\nR_L 3 0 {RL}',
			#f'\nT_third 2 0 5 0 TD='+str(8.33333)+'p z0=50'
			#f'\nRthird 5 0 100000000'
			#f'\nT_fith 2 0 6 0 TD='+str(8.33333*3/5)+'p z0=50'
			#f'\nC_terminate 2 0 177f'
			#f'\nc_fil_pump 2 6 '+str(1000*q/(10*2*3.14159265))+'p '
			#f'\nl_fil_pump 2 6 '+str(1000/(10*2*3.14159265)/q)+'p '
			#f'\nc_fil_signal 6 7 '+str(1000*q/(11*2*3.14159265))+'p '
			#f'\nl_fil_signal 6 7 '+str(1000/(11*2*3.14159265)/q)+'p '
			#f'\nc_fil_idler 0 7 '+str(1000*q/(9*2*3.14159265))+'p '
			#f'\nl_fil_idler 0 7 '+str(1000/(9*2*3.14159265)/q)+'p '
			#f'\nc_fil_idler2 0 8 '+str(1000*q/(12*2*3.14159265))+'p '
			#f'\nl_fil_idler2 0 8 '+str(1000/(12*3.14159265)/q)+'p '
			#f'\nc_fil_idler3 0 6 '+str(1000*q/(30*2*3.14159265))+'p '
			#f'\nl_fil_idler3 6 2 '+str(1000/(30*2*3.14159265)/q)+'p '
	])

	for i in labels[1:]:
		cir.write('\n.PRINT DEVV '+i)
	
	cir.write('\n.Tran '+str(resulution)+'P '+str(end_time)+'P '+str(start_time)+'p')
	#--------------------------------------------
	cir.close()
	return 0

