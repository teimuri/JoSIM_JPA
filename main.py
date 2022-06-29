import root_function





#=============type of simulation==================
#type of simulation
# 'n' for normall
# 'fft' for fft
# 's' for sweep
# 'fft_s' for sweep on specefic frequency on fft

Type_of_Simulation='fft_s'

#=================================================

#=============Simulation mode==================
#Simulation mode
# 1 for normall plot
# 2 for absolut plot

Mode_of_Simulation=0

#=================================================



#==================PARAMETERS=====================
#c_p_d: Circuit parameters dictionary
c_p_d={"IC":f'{154}u',"RTYPE":f'{0}',"R0":f'{1.04}',"c":f'{0.1836/80}',"fp":f'{10}',"fs":f'{11}',"RL":f'{50}'}

#s_t_d: Simulation times dictionary.
s_t_d={"start_time":0,"end_time":20000,"resulution":1}

#s_p_d: Simulation parameters dictionary
s_p_d={"a":25,"s_r_1_d":5000,"s_r_1_u":6000,"s_r_2_d":0,"s_r_2_u":2}

#d_p_d: the way that data is processed. this dictionry is a set switches that can be used to have extra processes on result data. like taking the absolut value
d_p_d={"abs":0,"target_frequency":11}

#p_p_d: plot parameters dictionary
p_p_d={"x_axis":"a","y_axis":"b","fontsize":18,"seperat":1,"color":'#17e610'}

labels=['time','R_source_check','R_L']
#==================================================

root_function.root_func(Type_of_Simulation,Mode_of_Simulation,c_p_d,s_t_d,s_p_d,d_p_d,p_p_d,labels)