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
        for files in os.listdir(self.rpm_build_dir):
            (n, v, r, e, a) = splitFilename(files)
            if n not in self.all_rpm_info.keys():
                self.all_rpm_info[n] = files
            else:
                (name, version, release, e, arch) = splitFilename(self.all_rpm_info[n])
                if ((v > version) or 
                        (v == version and r > release)):
                    self.dup_rpm_list.append(self.all_rpm_info[n])
                    self.all_rpm_info[n] = files
                else:
                    self.dup_rpm_list.append(files)

        if len(self.dup_rpm_list) > 0:
            print ">>> Find the duplicated RPMs(see file (%s)) ..." %(self.dup_rpm_list)
            f = open(self.rpm_dup_file, "w+")
            for line in self.dup_rpm_list:
                f.write(line+'\n')
            f.close()

            print ">>> Move the duplicated rpms ..."
            for rpms in self.dup_rpm_list:
                shutil.move(os.path.join(self.rpm_build_dir, rpms), self.backup_des_dir)
            print "*** All done ***"
        else:
            print "*** Do not find any duplicated RPMS ***"
        
        print ">>> checking again ..."
        self.get_all_build_rpm()

        for files in os.listdir(self.backup_des_dir):
            (n, v, r, e, a) = splitFilename(files)
            if n not in self.all_build_rpm:
                print "!! RPM: %s is not in %s" %(n, self.rpm_build_dir)

if __name__ == "__main__":
    CheckDupRpm().run()
