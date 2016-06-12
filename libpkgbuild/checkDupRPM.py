#!/usr/bin/python

import os
import shutil
from library import Environment
from rpmUtils.miscutils import splitFilename

class CheckDupRpm(Environment):
    """docstring for CheckDupRpm"""
    def __init__(self):
        super(CheckDupRpm, self).__init__()
        self.all_rpm_info = dict()
        self.dup_rpm_list = list()

    def run(self):
        """docstring for run"""
        print "### Starting Verifying ###"
        for files in os.listdir(self.rpm_build_dir):
            (n, v, r, e, a) = splitFilename(files)
            if n not in self.all_rpm_info.keys():
                self.all_rpm_info[n] = files
            else:
                (name, version, release, e, arch) = splitFilename(self.all_rpm_info[n])
                if (a == arch and ((v > version) or
                        (v == version and r > release))):
                    self.dup_rpm_list.append(self.all_rpm_info[n])
                    self.all_rpm_info[n] = files
                else:
                    self.dup_rpm_list.append(files)

        if len(self.dup_rpm_list) > 0:
            print "### FAIL: Find Duplicated RPMs(see file (%s)) ..." %(self.dup_rpm_list)
            f = open(self.rpm_dup_file, "w+")
            for line in self.dup_rpm_list:
                f.write(line+'\n')
            f.close()

            while True:
                res = self.ui.prompt(">>> Please specify the locaiton of RPM remove target dir:")
                if os.path.exists(res):
                    self.backup_des_dir = res
                    break
                else:
                    print "!!  %s does not exist, please input again !!" %(res)

            print "### Moving Duplicated RPMs ###"
            for rpms in self.dup_rpm_list:
                shutil.move(os.path.join(self.rpm_build_dir, rpms), self.backup_des_dir)
            print "### Moving Complete ###"
        else:
            print "### PASS: Do Not Find Any Duplicated RPMs ###"
        
        self.get_all_build_rpm()
        for files in os.listdir(self.backup_des_dir):
            (n, v, r, e, a) = splitFilename(files)
            if n not in self.all_build_rpm:
                print "### WARN: %s Do Not Exist In %s" %(n, self.rpm_build_dir)

if __name__ == "__main__":
    CheckDupRpm().run()
