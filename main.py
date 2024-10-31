import numpy as np
import data

data.PIXELSIZE = 6.45

# Run Once to load all the files in /data into the data.npy file to increase loading speed on future runs
#data.data_save()

#Load data from File
d = data.data_load()

data.FIGSIZE = (4,3)
#The dictionary keys are the file names
for i in d.keys():
    #Print the full Image pos is the wavelengt of the center, scale the wavelength per detectorsize (grate specific) (nm/mm)
    #data.data_img_printer_full(d,i,pos=650,scale=4.321)
    
    #Cuts lines from the image top is the first line to print, bottom the last
    #data.data_img_printer(d,i,top=400,bottom=600,pos=650,scale=4.321)
    
    pass
    
    
data.FIGSIZE = (12,6)

#creates a baselinecorrected histogram of the selected area
data.histogram(d,'2_SplitSize040mm.asc',top=400,bottom=401,pos=650,scale=4.321)

for i,e in enumerate(d.keys()):
    #Searches for peaks in the histogram, plot plots the histogramm with the fittet gaussian curves, peakhigth is n * the standarddiviation and has to be surpassed to be classified as a peak, peak range defines a area after a peak in which no new peaks will be seachrched for, fitrange is the area befor and after a suspected peak that is used for the optimization function.
    match e[0]:
        case '1':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '2':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '3':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '4':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '5':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '6':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '7':
            pa = [400,401,650,4.321,True,1,5,30,True]
        case '8':
            pa = [400,401,650,4.321,True,1,5,30,False]
        case '9':
            pa = [400,401,650,4.321,True,1,5,30,False]

        
        
    data.peak_finder(d,e,top=pa[0],bottom=pa[1],pos=pa[2],scale=pa[3],plot=pa[4],peakhight=pa[5],peakrange=pa[6],fitrange=pa[7],helper=pa[8])
        
print(d.keys())

