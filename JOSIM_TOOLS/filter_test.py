import os
import subprocess
import data_tools
import matplotlib.pyplot as plt
N=1		#number of sweep steps
M=19		#Maximum Number of elements or nodes needed in each step of sweep

#Unit of time is pico second
start_time=0
end_time=100000
resulution=1
labels=['time','V3','R_port_3']
#Level

for sweep_l_1 in range(1,2):
	new_linn=[[],[]]
	for sweep_l_2 in range(2):
		cir = open('test_josim.js', 'w')
		#----------------------------------The Circuit
		cir.writelines([
				'\nV3 		1 0 pulse(0m 1000 5P 1P 1P 1000p) '
				'\nR_port_3 3 0 50 '
				'\nc_fil 1 2 '+str(10000*sweep_l_2/(2*3.14)+0.000010)+'p '
				'\nl_fil 1 2 '+str(1*sweep_l_2/(2*3.14)+0.00001)+'p '
				'\nc_fil_2 3 2 '+str(9090.90*sweep_l_2/(2*3.14)+0.000010)+'p '
				'\nl_fil_2 3 2 '+str(0.909090*sweep_l_2/(2*3.14)+0.00001)+'p '
		])
		for i in labels[1:]:
			cir.write('\n.PRINT DEVV '+i)
		cir.write('\n.Tran '+str(resulution)+'P '+str(end_time)+'P '+str(start_time)+'p')
		#--------------------------------------------
		cir.close()

		os.system("./josim-cli test_josim.js>test_josim.dat") #Run josim and put the results in 'test_josim.dat'

		data_file = open("test_josim.dat", "r")
		lines = data_file.readlines()
		data_file.close()

		del lines[0:int(len(lines)-(end_time-start_time)/resulution+1)]	#Deleting the extra word lines	

		new_lines=[]
		for string in lines:
			string=string.split()
			string=[float(i) for i in string]
			new_lines.append(string)
		new_linn[sweep_l_2]=new_lines
	

	new_file = open("test_josim_trimmed.dat", "w+")
	for i in new_lines:
		print(i,file=new_file)
	new_file.close()


	data_tools.dif_fft(new_linn[0],new_linn[1],end_time-start_time,labels)
	#data_tools.peak_finder(new_lines,labels,start_time,end_time)
	#data_tools.plotter(new_lines,labels)
	#data_tools.fft(new_lines,(end_time-start_time)/resulution,resulution,labels)
	#data_tools.abs_plotter(new_lines,labels)
	print(sweep_l_2)
plt.show()