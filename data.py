import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.optimize import curve_fit

PIXELSIZE = 6.45 
FIGSIZE = (4,3)


    
# converts input string to normalized 2dim numpy float array
def conv_data(data):
    horizontal = data.split('\n')
    for i,e in enumerate(horizontal):
        horizontal[i] = e.split(' ')[:-1]
    return np.array(horizontal[:-1],dtype=float)

def normalize(data):
    result = np.empty((len(data),len(data[0])))
    maximum = 0
    for i in data:
        for j in i:
            if j > maximum:
                maximum = j
    for i,e in enumerate(data):
        for j,f in enumerate(e):
            result[i][j] = f/maximum
    return result

#top and bottom set the location on the
def data_img_printer(data,name,top,bottom,pos,scale):
    if not os.path.exists(os.getcwd() + 'img'):
        os.makedirs(os.getcwd() + 'img')
    fig, ax = plt.subplots(figsize=FIGSIZE)
    im = ax.imshow(normalize(data[name][top:bottom]), interpolation='nearest')
    ax.set_xticks(np.arange(len(data[name][0]))[::140] ,labels=axis(len(data[name][0]),pos,scale,True)[::140])
    ax.set_title(name)
    fig.tight_layout()
    fig.savefig('img/' + name + '_'+ str(top) + '_' + str(bottom) + '_raw.png')

def data_img_printer_full(data,name,pos,scale):
    if not os.path.exists(os.getcwd() + 'img'):
        os.makedirs(os.getcwd() + 'img')
    fig, ax = plt.subplots(figsize=FIGSIZE)
    im = ax.imshow(normalize(data[name]), interpolation='nearest')
    ax.set_xticks(np.arange(len(data[name][0]))[::140] ,labels = axis(len(data[name][0]),pos,scale,True)[::140])
    ax.set_title(name)
    fig.tight_layout()
    fig.savefig('img/' + name + '_full_raw.png')



       
#converts the data to a 1 dim line
def compress(data,name,top,bottom):
    result = np.zeros(len(data[name][0]))
    for i in data[name][top:bottom]:
        for j,e in enumerate(i):
            result[j] = e + result[j]
    return result

# scales a 1 Dim array by calculating the x average in iteratives steps and repositions the array to that average
def norm(array, cut):
    vals = np.sort(array)
    cut = int(len(array)*cut)
    average = np.average(vals[cut:-cut])
    for i,e in enumerate(array):
        array[i] = e - average
    return array
        
def histogram(data,name,top,bottom,pos,scale):
    if not os.path.exists(os.getcwd() + 'hist'):
        os.makedirs(os.getcwd() + 'hist')
    vals = norm(compress(data,name,top,bottom),0.1)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(axis(len(vals),pos,scale,False),vals)
    ax.set_title(name)
    fig.tight_layout()
    fig.savefig('hist/' + name + '_'+ str(top) + '_' + str(bottom) +'_hist.png')
    plt.close()
       
def axis(len, pos, scale, rounding):
    axis = np.zeros(len)
    begining = pos - round(len/2) * (scale * PIXELSIZE * 0.001)
    for i,_ in enumerate(axis):
        axis[i] = begining + (i) * (scale * PIXELSIZE * 0.001)
    if rounding:
        for i,e in enumerate(axis):
            axis[i] = round(e,0)
    return axis


def gauss(x, A, x0, sigma): 
    return A/(sigma*(np.sqrt(2*np.pi))) * (np.exp(-(x - x0) ** 2 / (2 * sigma ** 2)))

# Find Peaks peakhight: multiplyer of average to count as peak, peakrange: int of numbers arround a peak that is ignored from peak search, fitrange: int range where scipy tries to fit the gaussian
def peak_finder(data, name, top, bottom, pos, scale, plot, peakhight, peakrange, fitrange,helper):
    vals = norm(compress(data,name,top,bottom),0.1)
    average = np.average(vals)
    possible_peaks = []
    blocker = 0
    for i,e in enumerate(vals):
        if i < blocker:
            continue
        if e > (average * peakhight):
            check = False
            blocker = i + peakrange
            possible_peaks.append(i)
    result = []
    x = axis(len(vals),pos,scale,False)
    for i in possible_peaks:
        lower = i-fitrange
        upper = i+fitrange
        if lower< 0:
            lower = 0
        if upper > len(vals):
            upper = len(vals)
        y = vals[lower:upper]
        x0 = x[lower:upper]
        if helper:
            print(i)
            plt.plot(x0,y)
            plt.show()
        try:
            parameters, covariance = curve_fit(gauss, x0, y, p0=[np.max(x0),x[i], 30])
            if (parameters[1]>x0[-1] or parameters[1]<x0[0]):
                raise ValueError("Fit Value outside of bounds")
            result.append(parameters)
        except:
            print(name + ' Could not fit ' + str(x[i]))
    
    if plot:
        if not os.path.exists(os.getcwd() + '/peaks'):
            os.makedirs(os.getcwd() + '/peaks')
        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.plot(x,vals)   
        for i in result:
            ax.plot(x,gauss(x,i[0],i[1],i[2]),color= 'orange')
            ax.axvline(i[1],color='red')
        ax.set_title(name)
        fig.tight_layout()
        fig.savefig('peaks/' + name + '_'+ str(top) + '_' + str(bottom) +'_peaks.png')
        plt.close()
    return [result]

#loads data from the files and storres them in a np savefile
def data_save():
    data = {}
    for filename in os.listdir(os.getcwd() + '/data'):
        with open(os.path.join(os.getcwd() + '/data', filename), 'r') as f:
            print('Reading File ' + filename)
            data[filename] = conv_data(f.read())
    np.save('data',data,allow_pickle=True)
    
#loads from the np savefile
def data_load():
    return np.load(os.getcwd() + '/data.npy',allow_pickle=True).item()

