import subprocess
import os
import shutil 
import sys
import glob
import stat
import random
import imp

def simulate(targetLocation,k,beta,mu,N,endT,seed):
  simDir = os.path.join(os.getcwd(),'tmpFolder')
  targetLocation = os.path.join(os.getcwd(),targetLocation)

  setupEnvironment(simDir)
  try:
    performSimulation(simDir,k,beta,mu,N,endT,seed)
    moveFiles(simDir,targetLocation)
    cleanupDirectory(simDir)
  except:
    print(sys.exc_info()[0])
    cleanupDirectory(simDir)
  
def setupEnvironment(simDir):
  sourceDir = os.path.dirname(os.path.realpath(__file__))
  if os.path.exists(simDir):
    shutil.rmtree(simDir)
  
  os.mkdir(simDir)
  #shutil.copyfile(os.path.join(sourceDir,'fortran','LandauGin','defectT.o'), os.path.join(simDir,'defectT.o'))
  #subprocess.run(['gfortran','-O3','-o',os.path.join(sourceDir,'fortran','LandauGin','defect.o'),os.path.join(sourceDir,'fortran','LandauGin','lg.f90')])
  shutil.copyfile(os.path.join(sourceDir,'fortran','LandauGin','defect.o'), os.path.join(simDir,'defect.o'))
  shutil.copyfile(os.path.join(sourceDir,'fortran','LandauGin','imgGen.py'), os.path.join(simDir,'imgGen.py'))

def performSimulation(simDir,k,beta,mu,N,endT,seed):
  curDir = os.getcwd()
  os.chdir(simDir)

  #subprocess.run(['sudo','chmod','+x','tmpFolder/defect.o'])
  #subprocess.run(['chmod','+x','tmpFolder/defectT.o'])
  #print('here')
  os.chmod('defect.o',0o777)
  #subprocess.run(['chmod','+x','defect.o'])
  tmp = subprocess.run(['./defect.o',str(k),str(beta),str(mu),str(N),str(endT),str(seed)])

  #shutil.copyfile('imgGen.py',os.path.join(outDir,'imgGen.py'))
  sys.path.append(simDir)
  from imgGen import imgGenRand
  imgGenRand(50,50)

  #subprocess.run(['python','imgGen.py'])

  os.chdir(curDir)

def moveFiles(simDir,targetLocation):
  tmp = os.getcwd()
  os.chdir(simDir)
  if not os.path.exists(targetLocation):
    try:
      os.mkdir(targetLocation)
    except:
      print("Failed to generate target directory")
      return
  #subprocess.run(["mv *.dat "+targetLocation])
  #subprocess.run(["mv *.bmp "+targetLocation])
  for item in glob.glob('*.dat'):
    shutil.move(item,os.path.join(targetLocation,os.path.basename(item)))
  for item in glob.glob('*.bmp'):
    shutil.move(item,os.path.join(targetLocation,os.path.basename(item)))
  os.chdir(tmp)

def cleanupDirectory(simDir):
  return
  shutil.rmtree(simDir)

if __name__ == "__main__":
  simulate('dataFolder',1,10,0,200,300,random.randint(0,100000))
