#!/usr/bin/python

import os
from library import Environment, CommandLineUI

class CompareRPMPKG(Environment):
    """docstring for CompareRPMPKG"""
    def __init__(self):
        super(CompareRPMPKG, self).__init__()
        self.ui = CommandLineUI(echoResponses=False)
        self.actions = (
            (">>> Would you like to modify the location of rpm build dir(%s)?" %(self.rpm_build_dir),
            "     >>> Please specifiy the new location of rpm build dir:",
            "self.rpm_build_dir"),
            (">>> Would you like to modify the location of %s?" %(self.all_pkg_file),
            "     >>> Please specifiy the new location of %s: " %(self.all_pkg_file),
            "self.all_pkg_file")
        ) 

    def run(self):
        #for key, value in self.actions.iteritems():
        for action in self.actions:
            answer = self.ui.promptConfirm(action[0])
            if answer:
                while True:
                    res = self.ui.prompt(action[1])
                    if os.path.exists(res):
                        if action[2] == "self.rpm_build_dir":
                            self.rpm_build_dir = res 
                        elif action[2] == "self.all_pkg_file":
                            self.all_pkg_file = res 
                        break
                    else:
                        print "!!  %s does not exist, please input again !!" %(res)

        if os.path.exists(self.all_pkg_file) and \
                os.path.exists(self.rpm_build_dir):
                    print "### Starting Verifying ###"
                    not_match = False
                    f = open(self.all_pkg_file)
                    for line in f:
                        if not os.path.exists(os.path.join(self.rpm_build_dir, line.strip())):
                            not_match = True
                            print "!! RPM: %s is not in %s !!" %(line.strip(), self.rpm_build_dir)
                    f.close()
                    print "### Done ###"
                    if not not_match:
                        print "### Each item in %s do exist in %s ###" %(self.all_pkg_file, self.rpm_build_dir)
        else:
            print "!! Error: file does not exist !!"

if __name__ == "__main__":
    CompareRPMPKG().run()
