#!/usr/bin/env python

import os
import tarfile
import argparse

#Setup agument parser
parser = argparse.ArgumentParser()
parser.add_argument("texname", help="Name of the tex file")
parser.add_argument("-t", "--tarname", help="Name of the tar file")
parser.add_argument("-f", "--format", help="Preferred Format of figures to package (default eps)")
args = parser.parse_args()
texname = args.texname

#Get location of tex file
texdir = os.path.dirname(os.path.realpath(texname))+"/"

#Create tarball
if args.tarname:
    tarname = args.tarname
else:
    tarname = texname.split('/')[-1]+'_packaged.tar'
figtar = tarfile.open(tarname, mode='w')

#Parse latex file and add files
with open(texname,'r') as f:
    for line in f:

        #Skip Commented figures
        if line[0] == "%":
            continue

        #Add all figures to tarball
        if "\includegraphics" in line:
            filename = line.split("{")[1]
            filename = filename.replace("./","").replace("}","").replace("\n","")
            #If preferred format specified
            if args.format:
                fileformat = args.format
                filename = filename + "." + fileformat
                if os.path.isfile(texdir+filename):
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    figtar.add(texdir+filename, arcname=filename)
                else:
                    print(filename + " not found, skipping ")

            #Otherwise use existing file with preference for eps
            else:
                if os.path.isfile(texdir+filename + ".eps"):
                    filename += ".eps"
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    print(texdir+filename)
                    figtar.add(texdir+filename, arcname=filename)
                elif os.path.isfile(texdir+filename + ".pdf"):
                    filename += ".pdf"
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    figtar.add(texdir+filename, arcname=filename)
                else:
                    print(texdir+filename + " not found as an eps of pdf, skipping ")

        #Add bibtex files to tarball
        if "\bibliography" in line:
            filename = line.split("{")[1]
            filename = filename.replace("./","").replace("}","").replace("\n","") + ".bib"
            print("adding " + filename + " to " + figtar.name.split('/')[-1])
            figtar.add(texdir+filename, arcname='./')

print("adding " + texname.split('/')[-1] + " to " + figtar.name.split('/')[-1])
figtar.add(texname, arcname=texname.split('/')[-1])
figtar.close
