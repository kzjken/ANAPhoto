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

def createPlot(srcFolder):
    srcPathIncExtName = srcFolder + "\\*." + "jpg"
    listAllEXIF = []

    for srcName in glob.glob(srcPathIncExtName):
        exifList = imgProcess.getExif(srcName)
        exifList.insert(0, os.path.basename(srcName))
        listAllEXIF.append(exifList)
    
    FocalLengthOrg = []
    FocalLength = []
    for item in listAllEXIF:
        FocalLengthOrg.append(item[4])
    CountNone = FocalLengthOrg.count("None")
    
    for item in FocalLengthOrg:
        if item != "None":
            FocalLength.append(float(item))

    ## Init Plot
    fig, axes = plt.subplots(3, figsize = (18,8))
    plt.subplots_adjust(bottom=0.06, top=0.94, left=0.06, right=0.88, hspace=0.35, wspace=0.35)

    ax = axes[0]
    ax1 = axes[1]
    ax2 = axes[2]

    ax.set_title('FocalLength')
    ax1.set_title('Aperture')
    ax2.set_title('ShutterSpd')

    ax.grid()
    ax1.grid()
    ax2.grid()

    lines = []
    lines1 = []
    lines2 = []

    # Plot1    
    List2DTemp = []
    for item in FocalLength:
        listTemp = []
        listTemp.append(item)
        listTemp.append(FocalLength.count(item))
        List2DTemp.append(listTemp)
    print(List2DTemp)
    List2DTemp =set(tuple(element) for element in List2DTemp)
    print(List2DTemp)
    List2DTemp = sorted(List2DTemp, key = lambda x: (x[0]))

    print(List2DTemp)

    x = []
    y = []

    for item in List2DTemp:
        x.append(item[0])
        y.append(item[1])

    x_pos = [i for i, _ in enumerate(x)]
    plt.bar(x_pos, y, color='blue')

    plt.xticks(x_pos, x)

    plt.show()

    # for i in range(0, lineNo + 1):
    #     x.clear()
    #     y.clear()    
    #     lineLabel = legendlabel[i]        
    #     for j in range(0, 200):
    #         x.append(float(xAxis[i * 200 + j]))            
    #         y.append(float(yAxis[i * 200 + j]))          
    #     if i == 0:       
    #         line, = ax.plot(x, y, lw = 1, linestyle = '--', label = lineLabel)
    #     else:
    #         line, = ax.plot(x, y, lw = 1, label = lineLabel)

    #     #line, = ax.plot(x, y, lw = 1, label = lineLabel)
    #     lines.append(line)
    # # Plot2
    # for i in range(0, lineNo + 1):
    #     x.clear()
    #     y.clear()    
    #     lineLabel = legendlabel[i]        
    #     for j in range(0, 200):
    #         x.append(float(xAxis[i * 200 + j]))            
    #         y.append(float(yAxisS[i * 200 + j]))  
    #     if i == 0:       
    #         line, = ax1.plot(x, y, lw = 1, linestyle = '--', label = lineLabel)
    #     else:
    #         line, = ax1.plot(x, y, lw = 1, label = lineLabel)

    #     #line, = ax.plot(x, y, lw = 1, label = lineLabel)
    #     lines1.append(line)
    # # Plot3
    # for i in range(0, lineNo + 1):
    #     x.clear()
    #     y.clear()    
    #     lineLabel = legendlabel[i]        
    #     for j in range(0, 200):
    #         x.append(float(xAxis2[i * 200 + j]))            
    #         y.append(float(yAxis2[i * 200 + j]))   
    #     if i == 0:       
    #         line, = ax2.plot(x, y, lw = 1, linestyle = '--', label = lineLabel)
    #     else:
    #         line, = ax2.plot(x, y, lw = 1, label = lineLabel)

    #     lines2.append(line)

    # # on_pick via legend
    # #leg = ax2.legend(fancybox=True, shadow=True, loc='upper right')
    # leg = ax1.legend(fancybox=True, shadow=True, bbox_to_anchor=(1,1), loc="upper left")
    
    # lined = {}  # Will map legend lines to original lines.
    # lined1 = {}  # Will map legend lines to original lines.
    # lined2 = {}  # Will map legend lines to original lines.

    # for legline, origline in zip(leg.get_lines(), lines):
    #     legline.set_picker(True)  # Enable picking on the legend line.
    #     lined[legline] = origline
    # for legline, origline in zip(leg.get_lines(), lines1):
    #     legline.set_picker(True)  # Enable picking on the legend line.
    #     lined1[legline] = origline
    # for legline, origline in zip(leg.get_lines(), lines2):
    #     legline.set_picker(True)  # Enable picking on the legend line.
    #     lined2[legline] = origline

    # def on_pick(event):
    #     # On the pick event, find the original line corresponding to the legend
    #     # proxy line, and toggle its visibility.
    #     legline = event.artist
    #     origline = lined[legline]
    #     origline1 = lined1[legline]
    #     origline2 = lined2[legline]
    #     visible = not origline.get_visible()
    #     origline.set_visible(visible)
    #     origline1.set_visible(visible)
    #     origline2.set_visible(visible)
    #     # Change the alpha on the line in the legend so we can see what lines
    #     # have been toggled.
    #     legline.set_alpha(1.0 if visible else 0.2)
    #     fig.canvas.draw()

    # fig.canvas.mpl_connect('pick_event', on_pick)
    # plt.show()

def createPlotTest(srcFolder):

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

        # # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        # labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
        # sizes = [15, 30, 45, 10]
        # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        # fig1, ax1 = plt.subplots()
        # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        #         shadow=True, startangle=90)
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # plt.show()

def analyse():
    log_text.configure(state = "normal")
    log_text.delete('1.0', END)   
    print("=======================================================================================")

    srcPath = srcPath_entry.get()
    if checkPath(srcPath):
        createPlotTest(srcPath)

    log_text.see(END)
    log_text.configure(state = "disable")

def thread_it(func, *args):		
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()

# plot_Button = ttk.Button(mainframe, text = "Analyse", command = analyse)
plot_Button = ttk.Button(mainframe, text = "Analyse", command = lambda:thread_it(analyse))
plot_Button.grid(row = 1, column = 2, sticky = (N, S), padx = 5, pady = 5, rowspan = 2)

#################################################################################################################################
# main
#################################################################################################################################
root.mainloop()

#pyinstaller --noconsole plotEXIF.py
