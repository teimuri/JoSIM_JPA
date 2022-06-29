#Explnations:
#"s" in variables stand for 'sweep'
#"r" stands for 'range'
#"p" stands for 'point'
#"h" stands for hold
#"d" stands for 'data' or 'dictionary'
#"v" for 'value'
#"l" for 'level'
#"trim" for trimmed
#"lin" for line
#"fin" for final

import os
import sys
import time as tm
import numpy as np
import subprocess
import JOSIM_TOOLS.data_tools as data_tools
import JOSIM_TOOLS.circuit_tools as circuit_tools
import matplotlib.pyplot as plt
import multiprocessing as mp






def root_func(Type_of_Simulation,Mode_of_Simulation,c_p_d,s_t_d,s_p_d,d_p_d,p_p_d,labels):
	pool = mp.Pool(mp.cpu_count())
	
	



	#+++++++++Time++++++++
	start=tm.perf_counter()
	#+++++++++Time++++++++

	#  ███    ███  █████  ██ ███    ██      ██████  ██████  ██████  ███████ 
	#  ████  ████ ██   ██ ██ ████   ██     ██      ██    ██ ██   ██ ██      
	#  ██ ████ ██ ███████ ██ ██ ██  ██     ██      ██    ██ ██   ██ █████   
	#  ██  ██  ██ ██   ██ ██ ██  ██ ██     ██      ██    ██ ██   ██ ██      
	#  ██      ██ ██   ██ ██ ██   ████      ██████  ██████  ██████  ███████ 
	#                                                                       
	#                                                                       

	N=1		#number of sweep steps
	M=1		#Maximum Number of elements or nodes needed in each step of sweep
	q=100
	#Unit of time is pico second

	results = []

	start_time=s_t_d.get("start_time")
	end_time=s_t_d.get("end_time")
	resulution=s_t_d.get("resulution")
	time=end_time-start_time




	#Levels
	a=s_p_d.get("a")
	s_r_1_d=s_p_d.get("s_r_1_d")
	s_r_1_u=s_p_d.get("s_r_1_u")
	s_r_2_d=s_p_d.get("s_r_2_d")
	s_r_2_u=s_p_d.get("s_r_2_u")

	if(Type_of_Simulation=="fft_s"):
		s_r_1=range(int(s_r_1_d/a),int(s_r_1_u/a))
	else:
		a=1
		s_r_1=range(int(s_r_1_d/a),int(s_r_1_d/a+1))
	s_r_2=range(s_r_2_d,s_r_2_u)
	s_1_p=np.array(list(s_r_1))
	s_2_p=np.array(list(s_r_2))

	s_1_p=s_1_p*a
	s_2_p=s_2_p

	s_1_d_store=np.empty(0)
	s_2_d_store=np.empty(0)

	target_frequency=d_p_d.get("target_frequency")



	


	#==================ERROR CHECKING==================

	#if(Type_of_Simulation!='fft_s'):
	#	if((s_r_2_d!=1)|(s_r_2_u!=2)):
	#		sys.exit("s_r_2_d and s_r_2_u should be equal for this simulation")
	#==================================================

	#open the result file for writing
	fin_result_file = open(f'test_josim_trimmed.dat', "w+")
	print(f'#Type_of_Simulation:{Type_of_Simulation}\n#d_p_d:{d_p_d}\n#c_p_d:{c_p_d}\n#s_t_d:{s_t_d}\n#s_p_d:{s_p_d}',file=fin_result_file)

	for s_l_1,s_l_1_v in zip(s_r_1,s_1_p):
		pool.apply_async(circuit_tools.parallelize, args=(s_l_1,s_l_1_v,s_r_2,s_2_p,labels,resulution,end_time,start_time,time,q,c_p_d,p_p_d,d_p_d,target_frequency,Type_of_Simulation,start), callback=results.append)
	
	pool.close()
	pool.join()
	fin_result_file.close()
	if(Type_of_Simulation=='n'):
		data_tools.plotter(results[0],labels,p_p_d,d_p_d)
		with open('test_josim_trimmed.dat' , 'wb') as f:
			np.savetxt(f, results[0], delimiter=' ', newline='\n', header='', footer='', comments='# ')
		#print(*results[0],file=fin_result_file,sep="\n")

	elif(Type_of_Simulation=='fft'):
		data_tools.plotter(results[0],labels,p_p_d,d_p_d)
		with open('test_josim_trimmed.dat' , 'wb') as f:
			np.savetxt(f, results[0], delimiter=' ', newline='\n', header='', footer='', comments='# ')
		#print(*results[0],file=fin_result_file,sep="\n")

	elif(Type_of_Simulation=='fft_s'):
		results=np.array(results)
		s_1_d_store=results.reshape(len(s_r_1),len(labels))
		s_1_d_store=s_1_d_store[s_1_d_store[:,0].argsort()]
		with open('test_josim_trimmed.dat' , 'wb') as f:
			np.savetxt(f, s_1_d_store, delimiter=' ', newline='\n', header='', footer='', comments='# ')
		#' '.join(map(str, s_1_d_store))
		#print(*s_1_d_store,file=fin_result_file,sep="\n")

		data_tools.plotter(s_1_d_store,labels,p_p_d,d_p_d)
	
	data_tools.pathmake(c_p_d,Type_of_Simulation,s_t_d)
	plt.savefig(f'JOSIM_PLOTS/{c_p_d}/{Type_of_Simulation}/{s_t_d}--{s_r_1_d}--{s_r_1_u}.svg',transparent=True)

	#+++++++++Time++++++++
	end=tm.perf_counter()
	print(end-start)
	#+++++++++Time++++++++

	plt.show()


	#===========In Development Tools============
		#data_tools.fft_make_file(trim_lin,(time)/resulution,resulution,labels)
		#data_tools.dif_fft(new_lin[0],new_lin[1],time,labels)
		#data_tools.peak_finder(trim_lin,labels,start_time,end_time)
	#===========================================

	#  ███████ ███    ██ ██████  
	#  ██      ████   ██ ██   ██ 
	#  █████   ██ ██  ██ ██   ██ 
	#  ██      ██  ██ ██ ██   ██ 
	#  ███████ ██   ████ ██████  