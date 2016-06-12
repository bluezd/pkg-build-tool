#!/usr/bin/python

import os
from rpmUtils.miscutils import splitFilename
from library import Environment, CommandLineUI

class CompareRPMRH(Environment):
    """docstring for CompareRPMRH"""
    def __init__(self):
        super(CompareRPMRH, self).__init__()
        self.ui = CommandLineUI(echoResponses=False)
        self.actions = (
            (">>> Would you like to modify the location of isoft rpm build dir(%s)?" %(self.rpm_build_dir),
            "     >>> Please specifiy the new location of rpm build dir: ",
            "self.rpm_build_dir"),
            (">>> Would you like to modify the location of RH CDROM dir(%s)?" %(self.rh_cdrom_dir),
            "     >>> Please specifiy the new location of RH CDROM dir: ",
            "self.rh_cdrom_dir")
        )

    def run(self):
        """docstring for run"""
        for action in self.actions:
            answer = self.ui.promptConfirm(action[0])
            if answer:
                while True:
                    res = self.ui.prompt(action[1])
                    if os.path.exists(res):
                        if action[2] == "self.rpm_build_dir":
                            self.rpm_build_dir = res 
                        elif action[2] == "self.rh_cdrom_dir":
                            self.rh_cdrom_dir = res 
                        break
                    else:
                        print "!!  %s does not exist, please input again !!" %(res)

        os.system("clear")
        if os.path.exists(self.rh_cdrom_dir) and \
                os.path.exists(self.rpm_build_dir):
                    print "### Starting Verifying ###"
                    isoft_build_rpm_list = list()
                    not_build = False
                    for files in os.listdir(self.rpm_build_dir):
                        (n, v, r, e, a) = splitFilename(files)
                        if a == self.arch and n not in isoft_build_rpm_list:
                            isoft_build_rpm_list.append(n)

                    for files in os.listdir(self.rh_cdrom_dir):
                        (n, v, r, e, a) = splitFilename(files)
                        if a == self.arch and n not in isoft_build_rpm_list:
                            not_build = True
                            print "### FAIL: %s Has Not Been Built ###" %(files)

                    if not not_build:
                        print "### PASS: All Arch Related RPMs Have Been Built ###"
        else:
            print "!! Error: file does not exist !!" 

if __name__ == "__main__":
    CompareRPMRH().run()
