#!/usr/bin/env python

import os, sys

##########
#  MAIN  #
##########
def main() :
  print "Running PyC4 setup with args : \n" + str(sys.argv)

  # clean any existing libs
  os.system( "make clean" )

  # run
  os.system( "make" ) 


##############################
#  MAIN THREAD OF EXECUTION  #
##############################
if __name__ == "__main__" :
  main()


#########
#  EOF  #
#########
