#!/usr/bin/env python

import os
import tarfile
import argparse

def get_figurename(line):
    return (line.split("{")[1]
            .replace("./","")
            .replace("}","")
            .replace("\n",""))

#Setup agument parser
parser = argparse.ArgumentParser()
parser.add_argument("texname", help="Name of the tex file")
parser.add_argument("-t", "--tarname", help="Name of the tar file")
parser.add_argument("-f", "--format", help="Preferred Format of figures to package (default eps)")
args = parser.parse_args()

#Get tex file and path to tex file
texpath = args.texname
texname = texpath.split('/')[-1]

#Get location of tex file
texdir = os.path.dirname(os.path.realpath(texpath))+"/"

#Create tarball
if args.tarname:
    tarname = args.tarname
else:
    tarname = texname+'_packaged.tar'
figtar = tarfile.open(tarname, mode='w')

#Function to print filename and tarname
def printadd(name):
    print("adding " + name + " to " + figtar.name.split('/')[-1])

#Parse latex file and add files
with open(texpath,'r') as f:
    for line in f:

        #Skip Commented figures
        if line[0] == "%":
            continue

        #Add all figures to tarball
        if "\includegraphics" in line:
            filename = get_figurename(line)
            #If preferred format specified
            if args.format:
                fileformat = args.format
                filename = filename + "." + fileformat
                if os.path.isfile(texdir+filename):
                    printadd(filename)
                    figtar.add(texdir+filename, arcname=filename)
                else:
                    print(filename + " not found, skipping ")

            #Otherwise use existing file with preference for eps
            else:
                if os.path.isfile(texdir+filename + ".eps"):
                    filename += ".eps"
                    printadd(filename)
                    print(texdir+filename)
                    figtar.add(texdir+filename, arcname=filename)
                elif os.path.isfile(texdir+filename + ".pdf"):
                    filename += ".pdf"
                    printadd(filename)
                    figtar.add(texdir+filename, arcname=filename)
                else:
                    print(texdir+filename + " not found as an eps of pdf, skipping ")

        #Add bibtex files to tarball
        if "\bibliography" in line:
            filename = get_figurename(line)  + ".bib"
            printadd(filename)
            figtar.add(texdir+filename, arcname='./')

printadd(texname)
figtar.add(texpath, arcname=texname)
figtar.close
