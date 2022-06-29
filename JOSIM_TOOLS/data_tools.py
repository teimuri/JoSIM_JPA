import numpy as np
import os
import matplotlib.pyplot as plt
from scipy import fftpack
#from scipy.fft import fft

#Ok #More improvment will be good
#This just plots the data for all the labels given
def plotter(data_list,labels,p_p_d,d_p_d):

    #font size
    plt.rcParams['font.size'] = '16'

    #Making sure data is a numpy array and not a list
    axises=np.array(data_list)
    
    if d_p_d.get("abs"):
        axises=abs(axises)

    if((len(axises[0])>2)&(p_p_d.get('seperat'))):
        figure, axis = plt.subplots(len(axises[0])-1)
        for i in range(1,len(axises[0])):
            axis[i-1].plot(axises[:,0],axises[:,i],linewidth='2')
            axis[i-1].set_title(labels[i])
    else:
        for i in range(1,len(axises[0])):
            plt.plot(axises[:,0],axises[:,i],label=labels[i],linewidth='2',color=p_p_d.get("color"))
            #plt.title(labels[1])

    plt.subplots_adjust(hspace=0.8)
    #plt.plot(p, x,'o',linewidth='0.5',markevery=8,label="ADS")
    plt.xlabel(p_p_d.get("x_axis"),fontsize=22)
    plt.ylabel(p_p_d.get("y_axis"),fontsize=22)
    
    return 0

#Ok
def fft(data_list,labels,time,resulution):
    plt.rcParams['font.size'] = '16'
    #time unit is 'p' so 'time_unit_factor' should be 10**(-12)
    time_unit_factor=10**(-12)

    axises=np.array(data_list)
    a=np.fft.rfft(axises,axis=0)/(len(axises)/2)
    a=abs(a)
    a[:,0]=np.array(list(range(int(time/2))))/((time*10**(-12))*resulution)
    return a

#Ok
def peak_finder(data_list,labels,start_time,end_time):
    data=np.array(data_list)
    peaks=np.amax(data,axis=0)
    print(peaks[1::])

def mean_finder(data_list,labels,start_time,end_time):
    data=np.array(data_list)
    means=np.mean(abs(data[10::]),axis=0)
    return means[1]

#Ok
def moving_ave(data_list,t,res,time,amp_2,amp_1):
    amp=abs(amp_2-amp_1)
    data=np.array(data_list)
    a=np.empty(int(time/t))
    b=np.empty(int(time/t))
    #print(np.ndarray.size(data))
    for i in range(int(time/t)):
        a[i]=np.mean(abs(data[i*int(t/res)+100:(i+1)*int(t/res)-100,2]))
        b[i]=i
    if(amp_2>amp_1):
        a=np.flip(a)

    figure, axis = plt.subplots(2)
    
    axis[0].plot(b*amp,a,linewidth='2')
    axis[0].set_title("IV Curve")

    axis[1].plot(b*amp,np.gradient(a)/(amp*10**(-6)),linewidth='2')
    axis[1].set_title("Deravitive of IV Curve")

    plt.subplots_adjust(hspace=0.8)

#OK
def pathmake(c_p_d,Type_of_Simulation,s_t_d):
    directory=f'JOSIM_PLOTS/{c_p_d}/{Type_of_Simulation}'
    if not os.path.exists(directory):
        os.makedirs(directory)




#Repair
def dif_fft(data_1,data_2,time,labels):
    axises_1=np.array(data_1)
    axises_2=np.array(data_2)

    plt.rcParams['font.size'] = '16'
    axises=axises_2-axises_1
    a=np.fft.rfft(axises,axis=0)/len(axises)
    print(len(a[:,0]))
    s=np.array(list(range(int(time/2))))/((time*10**(-12)))
    print(s)
    for i in range(1,len(axises[0])):
        plt.plot(s,abs(a[0:int(len(axises)),i]),label=labels[i])
    plt.legend(fontsize=18)
    plt.show()
    return 0

#Change name
def point_sweep(data_list,time,resulution,labels,freq):
    plt.rcParams['font.size'] = '16'
    axises=np.array(data_list)
    a=np.fft.rfft(axises,axis=0)/(len(axises)/2)
    s=np.array(list(range(int(time/2))))/((time*10**(-12))*resulution)
    return abs(a[int(time*10**(-12)*(freq*10**9))])

#Check
def fft_make_file(data_list,time,resulution,labels):


    plt.rcParams['font.size'] = '16'
    axises=np.array(data_list)
    a=np.fft.rfft(axises,axis=0)/(len(axises)/2)
    a[0:int(len(axises)),0]=np.array(list(range(int(time/2))))/((time*10**(-12))*resulution)
    new_file = open("test_josim_fft.dat", "w+")
    a=a.tolist()
    print(1)
    for i in a:
        print(a,file=new_file)
    new_file.close()
    return 0

def file_writer(filename,data):
    fin_result_file = open(filename, "w+")
    for i in data:
       print(i,file=fin_result_file)
    fin_result_file.close()