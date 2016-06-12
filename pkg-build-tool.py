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
    print "################## The i-Soft OS Image Building Tool ##################"
    print "#    1. Generating SRPM Package List                                  #"
    print "#    2. Checking RPMs Has Not Been Built(Compared with RH CDROM)      #"
    print "#    3. Removing Duplicated Lower Version RPMs                        #"
    print '#    4. Checking/Generating "all.pkg.$arch" File                      #'
    print "#                                                                     #"
    print "#    Press 'q' to quit this tool                                      #"
    print "#######################################################################"

def quit():
    """docstring for quit"""
    print "Quit ... bye."
    sys.exit(0)

def main():
    ui = CommandLineUI(echoResponses=False)
    actions = {
            "1" : "CheckRPMNOTBuild().run()",
            "2" : "CompareRPMRH().run()",
            "3" : "CheckDupRpm().run()",
            "4" : "CompareRPMPKG().run()",
            "q" : "quit()"}

    os.system("clear")
    while True:
        actionPrompt()
        answer = ui.prompt("Ready to run this tool?", ["1", "2", "3", "4", "q"])
        os.system("clear")
        eval(actions[answer])
        print

if __name__ == "__main__":
    main()
