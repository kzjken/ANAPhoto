import os
import time
from PIL import Image

#####################################################################################
# getExif via PIL
#####################################################################################
def getExif(imageName):
    listExif = []
    image = Image.open(imageName)
    dictExif = image.getexif()  
    #print(dictExif)  
    DateTimeOriginal = str(dictExif.get(36867))
    CameraModel = str(dictExif.get(272))
    Aperture = str(dictExif.get(33437))
    FocalLength = str(dictExif.get(41989))
    ShutterSpd = str(dictExif.get(33434))

    listExif.append(DateTimeOriginal)
    listExif.append(CameraModel)
    listExif.append(Aperture)
    listExif.append(FocalLength)
    listExif.append(ShutterSpd)
    image.close()
    
    return listExif

#####################################################################################
# rename file according shot time and device
#####################################################################################
def renameAccExif(imageName, listEXIF):
    DateTimeOriginal = listEXIF[0]
    CameraModel = listEXIF[1]

    # new filename part 1: time    
    filenameRaw = ""
    if DateTimeOriginal != "None":
        filenameRaw = DateTimeOriginal
    else:
        fileModTime = time.localtime(os.stat(imageName).st_mtime)
        filenameRaw = time.strftime("%Y%m%d_%H%M%S", fileModTime)

    #print(filenameRaw)    

    filenameRaw = filenameRaw.replace(':','')
    filenameRaw = filenameRaw.replace(' ','_')

    # new filename part 2: device part
    if CameraModel != "None":
        filenameRaw = filenameRaw + "_" + CameraModel
    filenameRaw = filenameRaw.replace(' ','')
    
    filename, file_extension = os.path.splitext(imageName)
    filenameRaw += file_extension
    
    return filenameRaw

#####################################################################################
# rename and compressed image
#####################################################################################
def renAndcompImg(src, dest, quality):
    img = Image.open(src)
    if 'exif' in img.info.keys():
        exif_dict = img.info["exif"]
        img.save(dest, quality = quality, optimize = True, exif = exif_dict)
    else:
        img.save(dest, quality = quality, optimize = True)