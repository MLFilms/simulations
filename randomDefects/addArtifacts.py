import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pprint as pp
import numpy as np
from PIL import Image, ImageDraw
import glob
import os
import random
from scipy.ndimage.filters import gaussian_filter
from skimage.transform import AffineTransform, warp

def randAdd(row):
    return row+random.randint(0,30)

def addScans(img):
    xDim,yDim,zDim = img.shape
    for i in range(0,xDim):
        img[i,:,:] = img[i,:,:]+random.randint(-30,30)
    for i in range(0,yDim):
        img[:,i,:] = img[:,i,:]+random.randint(-30,30)
    
    return img

def skewImage(image,shift):

    transform = AffineTransform(translation=shift)
    shifted = warp(image,transform, mode ='wrap', preserve_range =True)
    shifted = shifted.astype(image.dtype)
    return shifted

def standardize(image):
    image = image.astype(np.float64)
    imgMean = np.mean(image)
    imgSTD = np.std(image)
    image= (image - imgMean)/(6*imgSTD)
    image = image+0.5
    #image = image*255
    image = np.clip(image,0,1)
    return image


def standardizeRand(image):
    image = image.astype(np.float64)
    imgMean = np.mean(image)
    imgSTD = np.std(image)
    image= (image - imgMean)/(random.uniform(0.5,12)*imgSTD)
    image = image+random.uniform(0.3,0.7)
    #image = image*255
    image = np.clip(image,0,1)
    return image

def addCircle(image,xCoord,yCoord,radius):
    dims = image.shape
    xx,yy = np.mgrid[:dims[0],:dims[1]]

    radius = 10


    circle = radius>((xx - xCoord)**2+(yy-yCoord)**2)**(1/2)

    image[circle] = image[circle] + random.uniform(0.1,0.5)
    return image

def nRandCircles(image,n):
    dims = image.shape
    for i in range(0,n):
        image = addCircle(image,random.randint(0,dims[0]),random.randint(0,dims[1]),random.randint(5,20))
    return image


def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

def randomChanges(image,noiseImages,sigmaRange,skewRange):
    
    noiseImage = noiseImages[random.randint(0,len(noiseImages))-1]
    noiseImage = standardize(noiseImage)
    nDims = noiseImage.shape
    gDims = image.shape
    #changing noise pattern
    xSkew = random.randint(0,nDims[0])
    ySkew = random.randint(0,nDims[1])
    noiseImage = skewImage(noiseImage,(xSkew,ySkew))
    noiseImage = noiseImage[0:gDims[0],0:gDims[1],:]

    image = gaussian_filter(image,sigma=random.uniform(0,sigmaRange))
    image = image*random.uniform(0.4,1.6)
    noiseStrength = random.uniform(0.3,2.5)
    image = randomGrid(image)
    image = image+noiseImage*noiseStrength
    image = nRandCircles(image,3)
    return image

def randomGrid(image):
    dims = image.shape
    x = random.randint(0,dims[0])
    y = random.randint(0,dims[1])
    image[:x,:y] = image[:x,:y] +random.uniform(-0.5,0.5)
    image[x:,:y] = image[x:,:y] +random.uniform(-0.5,0.5)
    image[:x,y:] = image[:x,y:] +random.uniform(-0.5,0.5)
    image[:x,:y] = image[:x,:y] +random.uniform(-0.5,0.5)
    return image


def addArtifacts():
    targetDir = os.path.join(os.getcwd(),'accumulated')
    ext = 'jpg'
    outEXT = 'jpg'
    outDir = targetDir+"\\outMess\\"

    if not os.path.exists(outDir):
        os.makedirs(outDir)


    noiseImages = []
    for filename in glob.glob('noiseFiles\\*.jpg'):
        imgcv = cv2.imread(filename)
        noiseImages.append(imgcv)

    filePattern = 	targetDir+"\\*." + ext
    num = 1
    for filename in glob.glob(filePattern):

        num = num+1
        imgcv = cv2.imread(filename)

        sections = filename.split("\\")
        imName = sections[-1]
        

        prePost = imName.split(".")
        noEnd = prePost[0]


        imgMean = np.mean(imgcv)
        imgSTD = np.std(imgcv)


        image = standardizeRand(imgcv)
        noiseImage = standardizeRand(noiseImages[0])


        image = randomChanges(image,noiseImages,1.5,500)

        image = standardize(image)
        image = rgb2gray(image)

        image = np.clip(image,0,1)
        im = Image.fromarray(image*255)

        if im.mode != 'RGB':
            im = im.convert('RGB')

        im.save(outDir+noEnd+'.'+outEXT)


if __name__ == '__main__':
    addArtifacts()
