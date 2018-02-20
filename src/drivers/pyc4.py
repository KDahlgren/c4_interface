#!/usr/bin/env python

'''
driver.py
'''

# **************************************** #


#############
#  IMPORTS  #
#############
# standard python packages
import inspect, os, sqlite3, sys, time

# ------------------------------------------------------ #
# import sibling packages HERE!!!

if not os.path.abspath( __file__ + "/../.." ) in sys.path :
  sys.path.append( os.path.abspath( __file__ + "/../.." ) )

from wrapper import C4Wrapper

# **************************************** #


############
#  DRIVER  #
############
def driver() :

  pyc4( sys.argv )


##########
#  PYC4  #
##########
def pyc4( fileNameList ) :

  programFiles = fileNameList[1:-1]
  tableFile    = fileNameList[-1]

  print "[ Executing C4 wrapper ]"
  c4libpath = os.path.abspath( __file__ + "/../../../lib/c4/build/src/libc4/libc4.dylib" )
  w = C4Wrapper.C4Wrapper( ) # initializes c4 wrapper

  # /////////////////////////////////// #

  # collect programs
  progList = []
  for inFile in programFiles :
    rf = open( inFile, "r" )
    prog = []
    for line in rf :
      line = line.rstrip()
      prog.append( line )
    rf.close()
    progList.append( prog )

  # collect table list
  rf = open( tableFile, "r" )
  table_str1 = rf.readline()
  table_str1 = table_str1.rstrip()
  table_str1 = table_str1.split( "," )

  data = []
  data.extend( progList )
  data.append( table_str1 )

  #results_array = w.run( data )
  #results_array = w.run_pure( data )
  results_array = w.run_pure_iterative( data )

  print
  print "[ OUTPUTTING C4 EVALUATION RESULTS ]"
  for line in results_array :
    print line

  print
  print "PROGRAM ENDED SUCESSFULLY! =D"


#########################
#  THREAD OF EXECUTION  #
#########################
driver()


#########
#  EOF  #
#########
