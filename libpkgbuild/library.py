#!/usr/bin/python

import string, os, sys, copy, re
import readline, getpass
from rpmUtils.miscutils import splitFilename

class Environment(object):
    def __init__(self):
        self.arch = os.uname()[-1]
        self.rpm_build_dir = "/project/results/RPMS/"
        self.rh_cdrom_dir = "/media/cdrom/"
        self.srpm_dir = "/mnt/SRPMS/"
        self.rpm_dup_file = "duplicated_rpm_list"
        self.backup_des_dir = "/home/mockbuild/dzhu-backup/duplicated_packages"
        self.all_pkg_file = "all.pkg.%s" %(self.arch)

    def get_all_build_rpm(self):
        """docstring for get_all_rpm_info"""
        self.all_build_rpm = list()
        for files in os.listdir(self.rpm_build_dir):
            (n, v, r, e, a) = splitFilename(files)
            self.all_build_rpm.append(n)

    def run(self):
        """docstring for run"""
        pass

class CommandLineUI(object):
    def __init__(self, echoResponses=True):
        self.echo = echoResponses
        
    # utilities
    def printPipe(self, pipe):
        while 1:
            line = pipe.readline()
            if line:
                print line
            else:
                return pipe.close()
            

    def prompt(self, question, answers=None):
        while True:
            sys.stdout.write(question)
            if answers:
                sys.stdout.write(" (")
                sys.stdout.write("|".join(answers))
                sys.stdout.write(") ")
            sys.stdout.flush()
            response = sys.stdin.readline()
            if response.strip() and self.echo:
                sys.stdout.write("response: %s" % response)

            # if there were answers supplied, don't allow a blank response
            if not answers or response.strip():
                return response.strip()

            sys.stdout.write("!! Please enter a response !!\n")

    def promptInteger(self, question, answers=None):
        while True:
            sys.stdout.write(question)
            if answers:
                sys.stdout.write(" (")
                sys.stdout.write("|".join(answers))
                sys.stdout.write(") ")
            sys.stdout.flush()
            response = sys.stdin.readline()
            try:
                value =  string.atoi(response.strip())
                if self.echo:
                    sys.stdout.write("response: %u\n" % value)
                return value
            except ValueError:
                sys.stdout.write("Please enter an integer.\n")
    
    def promptConfirm(self, question):
        YES = "y"
        SAMEASYES = ["y", "yes", "ya", "yup", "affirmative", "roger", "go", 
                     "engage", "whatever", "way", "si", "oui", "ja", "1", "true"]
        NO = "n"
        SAMEASNO = ["n", "no", "na", "nada" "negative", "negatory", "stop", 
                    "never", "nooooo!", "no way", "non", "nein", "nicht", "0", "false"]
        while True:
            answer = self.prompt(question, (YES, NO))
            if answer.lower() in SAMEASYES:
                return True
            if answer.lower() in SAMEASNO:
                return False
            # otherwise 
            sys.stdout.write("Please answer %s or %s.\n" %(YES, NO))
    
    def promptContinue(self, message):
        return self.promptConfirm(question=("%s - continue? " % message))
            
            
    def promptEdit(self, label, value, answers=None):
        if not value:
            value = ""
        if answers:
            label += " ("
            label += "|".join(answers)
            label += ") "
        while True:
            readline.set_startup_hook(lambda: readline.insert_text(value))
            try:
                answer = raw_input(label).strip()
                if not answers or answer in answers:
                    return answer
                # otherwise
                print "Please enter one of the following: %s" % " | ".join(answers)
            finally:
                readline.set_startup_hook()
            
    def promptPassword(self, message):
        return getpass.getpass(message)
