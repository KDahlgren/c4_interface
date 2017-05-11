#!/usr/bin/env python

import os, sys, time

# TODO: place magical installation code here

C4_FINDAPR_PATH_ORIG       = "./lib_orig/c4/cmake/FindApr.cmake"
C4_FINDAPR_PATH_CUSTOMMAIN = "./lib_customMain/c4/cmake/FindApr.cmake"
SETUP_DEBUG                = True
DEBUG                      = True

#################
#  GETAPR_LIST  #
#################
def getAPR_list() :
  cmd = 'find / -name "apr_file_io.h" | grep -v "Permission denied" > out.txt'
  print "Finding Apache Runtime library using command: " + cmd
  time.sleep(5) # message to user
  os.system( cmd )
  fo = open( "out.txt", "r" )

  pathList = []
  for path in fo :
    path = path.strip()
    path_split = path.split( "/" )
    path_split = path_split[:len(path_split)-1]
    path       = "/".join( path_split )
    pathList.append( path )

  os.system( 'rm out.txt' )

  return pathList


########################
#  DE DUPLICATE SETUP  #
########################
# this script modifies the contents of FindAPR.cmake in the c4 submodule
# prior to compilation.
# need to ensure only one SET command exists in FindAPR.cmake after discovering
# a valid apr library.
def deduplicateSetup( directory ) :
  # http://stackoverflow.com/questions/4710067/deleting-a-specific-line-in-a-file-python
  # protect against multiple runs of setup

  if directory == "customMain" :
    f = open( C4_FINDAPR_PATH_CUSTOMMAIN, "r+" )
  else :
    f = open( C4_FINDAPR_PATH_ORIG, "r+" )

  d = f.readlines()
  f.seek(0)
  for i in d:
    if not "set(APR_INCLUDES" in i :
      f.write(i)
  f.truncate()
  f.close()


#############
#  SET APR  #
#############
def setAPR( path, directory ) :
  # set one of the candidate APR paths
  newCmd = 'set(APR_INCLUDES "' + path + '")'

  # branch on directory type
  if directory == "customMain" :
    cmd = "(head -48 " + C4_FINDAPR_PATH_CUSTOMMAIN + "; " + "echo '" + newCmd + "'; " + "tail -n +49 " + C4_FINDAPR_PATH_CUSTOMMAIN + ")" + " > temp ; mv temp " + C4_FINDAPR_PATH_CUSTOMMAIN + ";"

  else :
    cmd = "(head -48 " + C4_FINDAPR_PATH_ORIG + "; " + "echo '" + newCmd + "'; " + "tail -n +49 " + C4_FINDAPR_PATH_ORIG + ")" + " > temp ; mv temp " + C4_FINDAPR_PATH_ORIG + ";"

  # execute cmd
  os.system( cmd )

  if directory == "customMain" :
    os.system( "make c4_customMain" )
  else :
    os.system( "make c4_orig" )


##########################
#  CHECK FOR MAKE ERROR  #
##########################
def checkForMakeError( path ) :
  flag = True
  if os.path.exists( os.path.dirname(os.path.abspath( __file__ )) + "/c4_out.txt" ) :
    fo = open( "./c4_out.txt", "r" )
    for line in fo :
      line = line.strip()
      if containsError( line ) :
        print "failed path apr = " + path
        flag = False
    fo.close()
    os.system( "rm ./c4_out.txt" ) # clean up
  return flag


####################
#  CONTAINS ERROR  #
####################
def containsError( line ) :
  if "error generated." in line :
    return True
  #elif "Error" in line :
  #  return True
  else :
    return False


######################
#  MAIN CUSTOM MAIN  #
######################
def main_customMain() :
  print "Running pyLDFI setup with args : \n" + str(sys.argv)

  # clean any existing libs
  os.system( "make clean" )

  # download submodules
  os.system( "make get-submodules" )
  # copy over template c4 main
  print "Copying template c4 main ..."
  os.system( "cp ./src/templateFiles/c4i_template.c ./lib/c4/src/c4i/c4i.c" )
  print "...done copying template c4 main."

  # ---------------------------------------------- #
  # run make for c4
  # find candidate apr locations
  apr_path_cands = getAPR_list()
  
  # set correct apr location
  flag    = True
  for path in apr_path_cands :
    try :
      deduplicateSetup( "customMain" )
    except IOError :
      setAPR( path, "customMain" )

    setAPR( path, "customMain" )

    try :
      flag = checkForMakeError( path )
    except IOError :
      print "./c4_out.txt does not exist"
  
    # found a valid apr library
    if flag :
      print ">>> C4 installed successfully <<<"
      print "... Done installing C4 Datalog evaluator"
      print "C4 install using APR path : " + path
      print "done installing c4."
    else :
      sys.exit( "failed to install C4. No fully functioning APR found." )
  # ---------------------------------------------- #


###############
#  MAIN ORIG  #
###############
def main_orig() :
  print "Running pyLDFI setup with args : \n" + str(sys.argv)

  # clean any existing libs
  os.system( "make clean" )

  # download submodules
  os.system( "make get-submodules" )

  # ---------------------------------------------- #
  # run make for c4
  # find candidate apr locations
  apr_path_cands = getAPR_list()
  
  # set correct apr location
  flag    = True
  for path in apr_path_cands :
    try :
      deduplicateSetup( "orig" )
    except IOError :
      setAPR( path, "orig" )

    setAPR( path, "orig" )

    try :
      flag = checkForMakeError( path )
    except IOError :
      print "./c4_out.txt does not exist"
  
    # found a valid apr library
    if flag :
      print ">>> C4 installed successfully <<<"
      print "... Done installing C4 Datalog evaluator"
      print "C4 install using APR path : " + path
      print "done installing c4."
    else :
      sys.exit( "failed to install C4. No fully functioning APR found." )
  # ---------------------------------------------- #


##############################
#  MAIN THREAD OF EXECUTION  #
##############################
if __name__ == "__main__" :

  main_customMain()
  main_orig()


#########
#  EOF  #
#########
