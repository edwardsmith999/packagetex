import os
import tarfile

texname = 'MOP_13_es.tex'
figtar = tarfile.open(texname+'_figures.tar', mode='w')
with open(texname,'r') as f:
    for line in f:

        #Skip Comments
        if line[0] == "%":
            continue

        if "\includegraphics" in line:
            filename = line.split("{")[1]
            filename = filename.replace("./","").replace("}","").replace("\n","") + ".pdf"
            print("adding " + filename + " to " + figtar.name.split('/')[-1])
            figtar.add(filename)

print("adding " + texname + " to " + figtar.name.split('/')[-1])
figtar.add(texname)
figtar.close
