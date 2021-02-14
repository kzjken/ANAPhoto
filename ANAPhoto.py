from os import path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import os
import glob
import imgProcess
import sys
import matplotlib.pyplot as plt
import threading

#################################################################################################################################
#------------------------------------------------------------- Globale ---------------------------------------------------------#
#################################################################################################################################
LIST_IMAGE = []

#################################################################################################################################
#------------------------------------------------------------- rp stdout--------------------------------------------------------#
#################################################################################################################################
class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        self.textbox.insert(END, text) # write text to textbox
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass

#################################################################################################################################
#------------------------------------------------------------- tkinter ---------------------------------------------------------#
#################################################################################################################################
root = Tk()
root.title("Image Analyzer [Z.Kang]")

mainframe = ttk.Frame(root, padding = "20 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)

#################################################################################################################################
# row 0 path
#################################################################################################################################
ttk.Label(mainframe, text = "Path:").grid(row = 0, column = 0, sticky = E, padx = 5, pady = 5)

srcPath = StringVar()
srcPath_entry = ttk.Entry(mainframe, width = 50, textvariable = srcPath)
srcPath_entry.grid(row = 0, column = 1, sticky = (W, E), padx = 5, pady = 5)

def selectSrcDir():  
    filepath = os.path.normpath(filedialog.askdirectory())
    srcPath.set(filepath)
ttk.Button(mainframe, text = "Select Folder", command = selectSrcDir).grid(row = 0, column = 2, sticky = W, padx = 5, pady = 5)

#################################################################################################################################
# row 1 - 20 log window
#################################################################################################################################
ttk.Label(mainframe, text = "Log:").grid(row = 1, column = 0, sticky = (N, E), padx = 5, pady = 5)

log_text = Text(mainframe, width = 150, height = 30, state = "disabled")
log_text.grid(row = 1, column = 1, sticky = (W, E), padx = 5, pady = 5, rowspan = 20)

logText_scrollbar = Scrollbar(mainframe, orient="vertical", command = log_text.yview)
logText_scrollbar.grid(row = 1, column = 1, sticky = (E, N, S), padx = 5, pady = 5, rowspan = 20)

log_text.configure(yscrollcommand = logText_scrollbar.set)

pl = PrintLogger(log_text) 
sys.stdout = pl             

#################################################################################################################################
# row 1 execute
#################################################################################################################################
def checkPath(srcFolder):
    print("Check Path:")
    if not os.path.exists(srcFolder):
        print("  Error：Invailed Path: " + srcFolder + ", please reselect!")
        print("=======================================================================================")
        return False
    else:   
        return True

def genPlot(srcFolder):
    srcPathIncExtName = srcFolder + "\\**\\*." + "jpg"    
    listImage = glob.glob(srcPathIncExtName, recursive = True)
    imageCount = len(listImage)
    if imageCount == 0:
        print("  Error：no images found in " + srcFolder + ", please reselect!")
        print("=======================================================================================")
    else:
        print("  " + str(imageCount) + " images found in " + srcFolder)
        print("=======================================================================================")

        listAllEXIF = []
        for index, srcName in enumerate(listImage):
            exifList = imgProcess.getExif(srcName)
            print(str(index + 1) + "." + os.path.basename(srcName) + ": " + str(exifList))
            log_text.see(END)
            exifList.insert(0, os.path.basename(srcName))
            listAllEXIF.append(exifList)
        
        focalLengthList = []
        focalLengthListCount = []
        for item in listAllEXIF:
            focalLengthList.append(item[4])
        noneFlCount = focalLengthList.count("None")
        focalLengthList = [float(x) for x in focalLengthList if x != "None"]

        List2DTemp = []
        for item in focalLengthList:
            listTemp = []
            listTemp.append(item)
            listTemp.append(focalLengthList.count(item))
            List2DTemp.append(listTemp)
        # print(List2DTemp)
        # print("=======================================================================================")

        List2DTemp =set(tuple(element) for element in List2DTemp)
        # print(List2DTemp)
        # print("=======================================================================================")

        List2DTemp = sorted(List2DTemp, key = lambda x: (x[0]))

        focalLengthList.clear()
        focalLengthListCount.clear()
        for item in List2DTemp:  
            focalLengthList.append(str(item[0]))
            focalLengthListCount.append(item[1])
        # focalLengthList.append("None")
        # focalLengthListCount.append(noneFlCount)
        print("=======================================================================================")
        sumImage = imageCount - noneFlCount
        for i in range(0, len(focalLengthList)):
            print(str(focalLengthList[i]) + ": " + str(focalLengthListCount[i]) + " ( " + str(round(focalLengthListCount[i] * 100 / sumImage, 2)) + "% )")
            log_text.see(END)


        label = []
        for index, item in enumerate(focalLengthList):
            label.append(item + "mm = " + str(focalLengthListCount[index]))

        fig1, ax1 = plt.subplots(figsize = (18,8))
        ax1.pie(focalLengthListCount, labels = label, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

def analyse():
    log_text.configure(state = "normal")
    log_text.delete('1.0', END)   
    print("=======================================================================================")

    srcPath = srcPath_entry.get()
    if checkPath(srcPath):
        genPlot(srcPath)

    log_text.see(END)
    log_text.configure(state = "disable")

def thread_it(func, *args):		
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

plot_Button = ttk.Button(mainframe, text = "Analyse", command = lambda:thread_it(analyse))
plot_Button.grid(row = 1, column = 2, sticky = (N, S), padx = 5, pady = 5, rowspan = 2)

#################################################################################################################################
# main
#################################################################################################################################
root.mainloop()

