# packagetex

This scripts address the annoying case of sending a latex file to a collaborator, only to find out that you have missed an essential file.

The repo contains a simple python script which parses the latex file, determines all included figures and packages them together with the latex file into a tarball ready to send to a collaborator. 


> usage: package_tex.py [-h] [-t TARNAME] [-f FORMAT] texname

> positional arguments:
>   texname               Name of the tex file

> optional arguments:
>   -h, --help            show this help message and exit
>   -t TARNAME, --tarname TARNAME
>                         Name of the tar file
>   -f FORMAT, --format FORMAT
>                         Preferred Format of figures to package (default eps)
