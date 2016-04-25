#!/usr/bin/python

import os
import sys
import re
import commands
from rpmUtils.miscutils import splitFilename

from library import Environment, CommandLineUI

class CheckRPMNOTBuild(Environment):
    """docstring for CheckRPMNOTBuild"""
    def __init__(self):
        super(CheckRPMNOTBuild, self).__init__()
        self.all_pkg_arch_nofound = "all.pkg.%s.nofound" %(self.arch)
        self.pkg_not_build_srpm_file = "pkg_not_build_srpm_%s" %(self.arch)

        self.ui = CommandLineUI(echoResponses=False)
        
    def parse_srpm_package(self):
        print "### Generating the srpm package list ###"
        src_rpms = list()
        f = open(self.all_pkg_arch_nofound)
        pattern = re.compile("xxx (.*) xxx")
        for line in f.readlines():
            line = pattern.findall(line)[0]
            arch = line.split('.')[-1]
            package_name = line.split('.')[0]
            if arch == self.arch:
                for files in os.listdir(self.rh_cdrom_dir):
                    #(n, v, r, e, a) = splitFilename(os.path.join("/media/cdrom/Packages/", files))
                    (n, v, r, e, a) = splitFilename(files)
                    if a == self.arch and n == package_name:
                        command = "rpm -qpi %s 2>/dev/null" %(os.path.join(self.rh_cdrom_dir, files))
                        output = os.popen(command).read()
                        for line in output.split("\n"):
                            if line.split(" : ")[0].strip() == "Source RPM":
                                #srpmFile = os.path.join("/mnt/SRPMS", line.split(" : ")[1].strip())
                                srpmFile = line.split(" : ")[1].strip()
                                break
                        #print srpmFile
    
                        (rpmName, rpmVersion, rpmRealse, rpme, rpmArch) = splitFilename(srpmFile)
                        #print rpmName
                        for srpm in os.listdir(self.srpm_dir):
                            (n, v, r, e, a) = splitFilename(srpm)
                            if n == rpmName and srpmFile not in src_rpms:
                                src_rpms.append(srpmFile)
        f.close()
    
        print src_rpms
    
        f = file(self.pkg_not_build_srpm_file, "w+")
        for line in src_rpms:
            f.write(line+'\n')
        f.close()

    def generate_rpmlist(self, cdromDir):
        """docstring for generate_rpmlist"""
        COMMAND = "./gen-rpmlist.sh %s" %(cdromDir)
        #output = os.popen(command).read()
        print "### Generating rpm list ###"
        RES,OUTPUT = commands.getstatusoutput(COMMAND)
        rpmlist = "rpmlist.%s" % (self.arch)
        if RES == 0 and os.path.exists(rpmlist):
            return True 
        else:
            print "!!! Error generating the rpmlist files !!!"
            sys.exit(-1)
    
    def generate_pkglist(self):
        """docstring for generate_pkglist"""
        COMMAND = "./gen-pkglist.sh"
        print "### Generating pkg list ###"
        RES,OUTPUT = commands.getstatusoutput(COMMAND)
        if RES == 0 and os.path.exists(self.all_pkg_file):
            return True 
        else:
            print "!!! Error generating the pkg files !!!"
            sys.exit(-1)
    
    def run(self):
        answer = self.ui.promptConfirm(">>> Would you like to modify the path of Redhat CDROM(%s)?"\
                %(self.rh_cdrom_dir))
        if answer: 
            while True:
                res = self.ui.prompt("    >>> Please specify the path of Redhat CDROM: ")
                if os.path.exists(res):
                    self.rh_cdrom_dir = res
                    break
                else:
                    print "!!  %s does not exist, please input again !!" %(res)
        else:
            if not os.path.exists(self.rh_cdrom_dir):
                print "!! %s does not exist !!" %(self.rh_cdrom_dir)
                sys.exit(-1)
    
        print "### Starting. ####"
        if (self.generate_rpmlist(self.rh_cdrom_dir) == True):
            if (self.generate_pkglist() == True and os.path.exists(self.all_pkg_arch_nofound)):
                self.parse_srpm_package()
    
        print "### All Done. ####"

if __name__ == "__main__":
    CheckRPMNOTBuild().run()
