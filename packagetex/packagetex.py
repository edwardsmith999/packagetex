#!/usr/bin/env python
import os
import tarfile
import argparse

class packagetex:

    def __init__(self, texpath, tarname=None, figformat=None):

        self.texpath = texpath
        #Check file exists and if tex file
        if os.path.isfile(texpath):
            #Check extension
            assert texpath.find(".tex") == True
        else:
            print("Tex file " + texpath + " does not exist or is not found")
            raise IOError

        self.texname = texpath.split('/')[-1]
        self.tarname = tarname
        self.figformat = figformat

        if self.tarname==None:
            self.tarname = "./" + self.texname+'_packaged.tar'

    def get_figurename(self, line):
        return (line.split("{")[1]
                .replace("./","")
                .replace("}","")
                .replace("\n",""))

    #Function to print filename and tarname
    def printadd(self, name):
        print("adding " + name + " to " + self.tarname.split('/')[-1])

    def pack(self):

        #Get location of tex file
        texdir = os.path.dirname(os.path.realpath(self.texpath))+"/"

        #Create tarball
        figtar = tarfile.open(self.tarname, mode='w')

        #Parse latex file and add files
        with open(self.texpath,'r') as f:
            for line in f:

                #Skip Commented figures
                if line[0] == "%":
                    continue

                #Add all figures to tarball
                if "\includegraphics" in line:
                    filename = self.get_figurename(line)
                    #If preferred format specified
                    if self.figformat:
                        figformat = self.figformat
                        filename = filename + "." + figformat
                        if os.path.isfile(texdir+filename):
                            self.printadd(filename)
                            figtar.add(texdir+filename, arcname=filename)
                        else:
                            print(filename + " not found, skipping ")

                    #Otherwise use existing file with preference for eps
                    else:
                        if os.path.isfile(texdir+filename + ".eps"):
                            filename += ".eps"
                            self.printadd(filename)
                            #print(texdir+filename)
                            figtar.add(texdir+filename, arcname=filename)
                        elif os.path.isfile(texdir+filename + ".pdf"):
                            filename += ".pdf"
                            self.printadd(filename)
                            figtar.add(texdir+filename, arcname=filename)
                        else:
                            print(texdir+filename + " not found as an eps of pdf, skipping ")

                #Add bibtex files to tarball
                if "\bibliography" in line:
                    filename = self.get_figurename(line)  + ".bib"
                    self.printadd(filename)
                    figtar.add(texdir+filename, arcname='./')

        #Add tex file itself
        self.printadd(self.texname)
        figtar.add(self.texpath, arcname=self.texname)

        #Close tarball
        figtar.close()


def executepackagetex():

    #Setup agument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("texpath", help="Name of the tex file with path")
    parser.add_argument("-t", "--tarname", help="Name of the tar file")
    parser.add_argument("-f", "--format", help="Preferred Format of figures to package (default eps)")
    args = parser.parse_args()

    #Create packagetex object
    pt = packagetex(args.texpath, args.tarname, args.format)
    pt.pack() 

if __name__ == "__main__":

    executepackagetex()

