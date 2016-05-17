#!/bin/bash

#Generación de PDF compilando el archivo LaTeX con pdflatex
cd tex
pdflatex -synctex=1 -interaction=nonstopmode -output-directory=../ hearcloud.tex
pdflatex -synctex=1 -interaction=nonstopmode -output-directory=../ hearcloud.tex
cd ..
rm {*.aux,*.lof,*.log,*.lol,*.lot,*.out,*.synctex.gz,*toc}
