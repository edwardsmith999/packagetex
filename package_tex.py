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
texdir = os.path.dirname(os.path.realpath(texname))

#Create tarball
if args.tarname:
    tarname = args.tarname
else:
    tarname = texname+'_packaged.tar'
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
                if os.path.isfile(filename):
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    figtar.add(filename)
                else:
                    print(filename + " not found, skipping ")

            #Otherwise use existing file with preference for eps
            else:
                if os.path.isfile(filename + ".eps"):
                    filename += ".eps"
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    figtar.add(filename)
                elif os.path.isfile(filename + ".pdf"):
                    filename += ".pdf"
                    print("adding " + filename + " to " + figtar.name.split('/')[-1])
                    figtar.add(filename)
                else:
                    print(filename + " not found as an eps of pdf, skipping ")

        #Add bibtex files to tarball
        if "\bibliography" in line:
            filename = line.split("{")[1]
            filename = filename.replace("./","").replace("}","").replace("\n","") + ".bib"
            print("adding " + filename + " to " + figtar.name.split('/')[-1])
            figtar.add(filename)

print("adding " + texname + " to " + figtar.name.split('/')[-1])
figtar.add(texname)
figtar.close
