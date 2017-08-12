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

  programFile = sys.argv[1]
  tableFile   = sys.argv[2]

  print "[ Executing C4 wrapper ]"
  c4libpath = os.path.abspath( __file__ + "/../../../lib/c4/build/src/libc4/libc4.dylib" )
  w = C4Wrapper.C4Wrapper( c4libpath ) # initializes c4 wrapper

  # /////////////////////////////////// #
  rf = open( programFile, "r" )
  prog1 = []
  for line in rf :
    line = line.rstrip()
    prog1.append( line )
  rf.close()

  rf = open( tableFile, "r" )
  table_str1 = rf.readline()
  table_str1 = table_str1.rstrip()
  table_str1 = table_str1.split( "," )

  results_array = w.run( [ prog1, table_str1 ] )

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
