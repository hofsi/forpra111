import numpy as np
import matplotlib.pyplot as plt
import os
import data
from matplotlib import colormaps



def task1(x,vals,result):
    if not os.path.exists(os.getcwd() + '/final'):
        os.makedirs(os.getcwd() + '/final')
    fig, ax = plt.subplots(figsize=data.FIGSIZE)
    ax.plot(x,vals/1000)   
    for j,i in enumerate(result):
        ax.plot(x,data.gauss(x,i[0],i[1],i[2])/1000,color= 'orange', linestyle='--')
        ax.axvline(i[1],color=colormaps['viridis'](75*j),linestyle='--', label='x = '+str(round(i[1],2)))
    fig.tight_layout()
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Counts (K)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.xlim(360,370)
    fig.savefig('final/1_plot.png')
    plt.close()

def task2(x,vals,result):
    if not os.path.exists(os.getcwd() + '/final'):
        os.makedirs(os.getcwd() + '/final')
    fig, ax = plt.subplots(2, 2, figsize=data.FIGSIZE)
    title = ['0.05mm','0.09mm','0.15mm','0.20mm']
    for j,e in enumerate([ax[0,0],ax[0,1],ax[1,0],ax[1,1]]):
        e.plot(x,vals[j]/1000)   
        #for i in result[j][0]:
        #    e.plot(x,data.gauss(x,i[0],i[1],i[2])/1000,color= 'orange', linestyle='--')
        #    e.axvline(i[1],color='red',linestyle='--', label='x = '+str(round(i[1],2)))
        
        e.set_xlabel("Wavelength (nm)")
        e.set_ylabel("Counts (K)")
        e.grid(True)
        e.set_title( 'Slit width ' + title[j])
        e.set_xlim(361,368) 
    fig.tight_layout()
    plt.tight_layout()
    fig.savefig('final/2_plot.png')
    plt.close()

def task3(x,vals,result):
    pixel = [398, 1191]
    pdiff = pixel[1] - pixel[0]
    chip = 6.54
    cdiff = pdiff * chip
    wave = [467.82,479.99]
    wdiff = wave[1] - wave[0]
    print('cdiff')
    print(cdiff)
    print('wdiff')
    print(wdiff)
    print('nm/um:')
    print(wdiff/cdiff)
    
    if not os.path.exists(os.getcwd() + '/final'):
        os.makedirs(os.getcwd() + '/final')
    fig, ax = plt.subplots(figsize=data.FIGSIZE)
    ax.plot(x,vals/1000)
    reference = [467.82,479.99]
    for i,e in enumerate(result):
        ax.plot(x,data.gauss(x,e[0],e[1],e[2])/1000,color= 'orange', linestyle='--')
        ax.axvline(e[1],color=colormaps['viridis'](100*i),linestyle='--', label='x(peak) = '+str(round(e[1],2)))
        ax.axvline(reference[i],color=colormaps['viridis'](100*i+100),linestyle='--', label='x(ref)     = '+str(reference[i]))
    fig.tight_layout()
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Counts (K)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.xlim(466,481)
    fig.savefig('final/3_plot.png')
    plt.close()
 
def task4(x,vals):     
    if not os.path.exists(os.getcwd() + '/final'):
        os.makedirs(os.getcwd() + '/final')
    fig, ax = plt.subplots(1, 3, figsize=data.FIGSIZE)
    title = ['1800/mm','600/mm','300/mm']
    for j,e in enumerate([ax[0],ax[1],ax[2]]):
        e.plot(x[j],vals[j]/1000)   
        
        e.set_xlabel("Wavelength (nm)")
        e.set_ylabel("Counts (K)")
        e.grid(True)
        e.set_title( 'Slit width ' + title[j])
        #e.set_xlim(361,368)
        e.set_ylim(-50,)
    fig.tight_layout()
    plt.tight_layout()
    fig.savefig('final/4_plot.png')
    plt.close()  

def task5(x,vals):
    if not os.path.exists(os.getcwd() + '/final'):
        os.makedirs(os.getcwd() + '/final')
    fig, ax = plt.subplots(2, 2, figsize=data.FIGSIZE)
    title = ['2mm','4mm','6mm','8mm']
    for j,e in enumerate([ax[0,0],ax[0,1],ax[1,0],ax[1,1]]):
        e.plot(x,vals[j]/1000)   
        
        e.set_xlabel("Wavelength (nm)")
        e.set_ylabel("Counts (K)")
        e.grid(True)
        e.set_title( 'Apperature width ' + title[j])
        e.set_xlim(707,711) 
    fig.tight_layout()
    plt.tight_layout()
    fig.savefig('final/5_plot.png')
    plt.close()
    
data.PIXELSIZE = 6.45
data.DEBUG = True
# Run Once to load all the files in /data into the data.npy file to increase loading speed on future runs
#data.data_save()

#Load data from File
d = data.data_load()

data.FIGSIZE = (8,6)
#The dictionary keys are the file names
for i in d.keys():
    #Print the full Image pos is the wavelengt of the center, scale the wavelength per detectorsize (grate specific) (nm/mm)
    #data.data_img_printer_full(d,i,pos=365,scale=4.321)
    
    #Cuts lines from the image top is the first line to print, bottom the last
    #data.data_img_printer(d,i,top=400,bottom=600,pos=650,scale=4.321)
    pass
 
    
data.FIGSIZE = (12,6)

#creates a baselinecorrected histogram of the selected area
#data.histogram(d,'2_SplitSize040mm.asc',top=400,bottom=401,pos=650,scale=4.321)

result_2 = []
vals_2 = []
vals_4 = []
x_4 = []
i_4 = 0
list_4 = [data.grating['1800'],data.grating['600'],data.grating['300']]
x_5 = []
vals_5 =[]
for i,e in enumerate(d.keys()):
    #Searches for peaks in the histogram, plot plots the histogramm with the fittet gaussian curves, peakhigth is n * the standarddiviation and has to be surpassed to be classified as a peak, peak range defines a area after a peak in which no new peaks will be seachrched for, fitrange is the area befor and after a suspected peak that is used for the optimization function.
    match e[0]:
        case '1':
            pa = [700,900,365,data.grating['1200'],True,1,5,0,False]
        case '2':
            pa = [700,900,365,data.grating['1200'],True,1,5,0,False]
        case '3':
            pa = [700,900,472,data.grating['1200'],True,1,5,0,False]
        case '4':
            pa = [700,900,472,data.grating['1200'],True,1,0.2,0,False]
        case '5':
            pa = [700,900,709,data.grating['1800'],True,1,5,0,False]
        case '6':
            pa = [700,900,365,data.grating['600'],True,1,5,0,False]
        case '7':
            pa = [700,900,740,data.grating['600'],True,1,5,0,False]
        case '8':
            pa = [700,900,727,data.grating['1200'],True,1,5,0,False]
        case '9':
            pa = [700,900,365,data.grating['1200'],True,1,5,0,False]


    #data.data_img_printer(d,e,top=0,bottom=2000,pos=pa[2],scale=pa[3])
    #print(data.peak_finder(d,e,top=pa[0],bottom=pa[1],pos=pa[2],scale=pa[3],plot=pa[4],peakhight=pa[5],peakrange=pa[6],fitrange=pa[7],helper=pa[8],plotter=None))
    
    #Task 1
    if e[0] == '1' and False:
        print(data.peak_finder(d,e,top=pa[0],bottom=pa[1],pos=pa[2],scale=pa[3],plot=pa[4],peakhight=pa[5],peakrange=pa[6],fitrange=pa[7],helper=pa[8],plotter=task1))
    #Task 2
    if e[0] == '2' and False:
        result_2.append(data.peak_finder(d,e,top=pa[0],bottom=pa[1],pos=pa[2],scale=pa[3],plot=pa[4],peakhight=pa[5],peakrange=pa[6],fitrange=pa[7],helper=pa[8],plotter=None))
        vals_2.append(data.compress(d,e,top=pa[0],bottom=pa[1]))
        x_2 = data.axis(len(vals_2[0]),pa[2],pa[3],False)
    #Task 3
    if e[0] == '3' and False:
        print(data.peak_finder(d,e,top=pa[0],bottom=pa[1],pos=pa[2],scale=pa[3],plot=pa[4],peakhight=pa[5],peakrange=pa[6],fitrange=pa[7],helper=pa[8],plotter=task3))
        
    #Task 4
    if e[0] == '4' and False:
        print(e)
        vals_4.append(data.compress(d,e,top=pa[0],bottom=pa[1]))
        x_4.append(data.axis(len(vals_4[-1]),pa[2],list_4[i_4],False))
        i_4 +=1
    #Task 5
    if e[0] == '5' and True:
        print(e)
        vals_5.append(data.compress(d,e,top=pa[0],bottom=pa[1]))
        x_5 = data.axis(len(vals_5[0]),pa[2],pa[3],False)
    
#task2(x_2,vals_2,result_2)
task5(x_5,vals_5[1:])
data.FIGSIZE = (12,4)
#task4(x_4,vals_4)

