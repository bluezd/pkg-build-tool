#!/usr/bin/python

import os
import sys

from libpkgbuild.library import CommandLineUI
from libpkgbuild.checkDupRPM import CheckDupRpm 
from libpkgbuild.compareRPMRH import CompareRPMRH
from libpkgbuild.compareRPMPKG import CompareRPMPKG
from libpkgbuild.checkRPMNOTBuild import CheckRPMNOTBuild

def actionPrompt():
    """docstring for main"""
    #os.system("clear")
    print "################## The i-Soft OS Image Building Tool ##################"
    print "#    1. Generate the srpm list that need to build                     #"
    print "#    2. Check the RH CDROM to see which rpm has not been built yet    #"
    print "#    3. Check the all.pkg to see whether each item is correct         #"
    print "#    4. Check the duplicated rpms and remove the lower version        #"
    print "#                                                                     #"
    print "#    Press 'q' to quit this tool                                      #"
    print "#######################################################################"

def main():
    ui = CommandLineUI(echoResponses=False)
    os.system("clear")
    while True:
        actionPrompt()
        answer = ui.prompt("Ready to run this tool?", ["1", "2", "3", "4", "q"])
        os.system("clear")
        if answer == "1":
            CheckRPMNOTBuild().run()
        elif answer == "2":
            CompareRPMRH().run()
        elif answer == "3":
            CompareRPMPKG().run()
        elif answer == "4":
            CheckDupRpm().run()
        elif answer == "q":
            print "Exit this tool, bye."
            sys.exit(0)
        print

if __name__ == "__main__":
    main()
