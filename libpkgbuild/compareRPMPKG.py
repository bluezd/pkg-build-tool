#!/usr/bin/python

import os
from library import Environment, CommandLineUI
from rpmUtils.miscutils import splitFilename

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
        os.system("clear")
        if os.path.exists(self.all_pkg_file) and \
                os.path.exists(self.rpm_build_dir):
                    print "### Starting Verifying ###"
                    allPkgInISOOLD = list()
                    not_match_list = list()
                    f = open(self.all_pkg_file)
                    allPkgInISOOLD = [i.strip('\n') for i in f.readlines()]
                    f.close()
                    for line in allPkgInISOOLD:
                        if not os.path.exists(os.path.join(self.rpm_build_dir, line.strip())):
                            not_match_list.append(line.strip())

                    if len(not_match_list) > 0:
                        print "### FAIL: Following RPMs Do Not Exist In %s: ###" %(self.rpm_build_dir)
                        for i in not_match_list: print "### %s ###" %(i)

                        answer = self.ui.promptConfirm(">>> Would you like to re-generate %s ?"\
                                                    %(self.all_pkg_file))
                        if answer:
                            allPkgInISONew = list()
                            for j in os.listdir(self.rpm_build_dir):
                                (n, v, r, e, a) = splitFilename(j)
                                for k in not_match_list:
                                    (name, version, release, e, arch) = splitFilename(k)
                                    if (a == arch and n == name and
                                            ((v > version) or (v == version and r > release))):
                                            allPkgInISONew.append(j)
                                            break
                                else:
                                    if j in allPkgInISOOLD: allPkgInISONew.append(j)

                            f = open(os.path.join(os.path.dirname(self.all_pkg_file), "all.pkg.ppc64le.new"), "w+")
                            for line in allPkgInISONew:
                                f.write(line+'\n')
                            f.close()
                            print "### New all.pkg.ppc64le Has Been Generated (%s) ###" \
                                    %(os.path.join(os.path.dirname(self.all_pkg_file), "all.pkg.ppc64le.new"))
                    else:
                        print "### PASS: Each Pkg in %s Do Exist In %s ###" %(self.all_pkg_file, self.rpm_build_dir)
        else:
            print "!! Error: file does not exist !!"

if __name__ == "__main__":
    CompareRPMPKG().run()
