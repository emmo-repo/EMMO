from continuumio/miniconda3
#from ubuntu:latest

RUN apt update && apt install -y texlive-latex-extra pandoc gcc
RUN conda install -c conda-forge graphviz
RUN pip install Cython
RUN pip install pydot 
RUN pip install ase
RUN pip install Owlready2==0.10

ENV PYTHONPATH "/emmo/python:${PYTHONPATH}"




### docker run -it -v c:/:/emmo emmo

