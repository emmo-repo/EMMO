from continuumio/miniconda3

RUN apt update && apt install -y graphviz pandoc gcc
RUN pip install Cython
RUN pip install pydot 
RUN pip install ase
RUN pip install Owlready2==0.10

ENV PYTHONPATH "/emmo/python:${PYTHONPATH}"




### docker run -it -v c:/:/emmo emmo

