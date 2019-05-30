European Materials and Modelling Ontology (EMMO)
================================================
EMMO is a multidisciplinary effort to develop a standard
representational framework (the ontology) based on current materials
modelling knowledge, including physical sciences, analytical
philosophy and information and communication technologies.  This
multidisciplinarity is illustrated by the figure on the title page.
It provides the connection between the physical world, materials
characterisation world and materials modelling world.

EMMO is released under a [Creative Commons license](emmo/LICENSE.md).
The accompinied Python API is released under the [BSD
license](python/LICENSE.txt).


Content of this repository
--------------------------
  * emmo: OWL sources for the ontology
  * python: Python API for working with EMMO


Creating a docker image
-----------------------

File->preferences->Render->Render by annotation property

# Instructions for Dockerenvironment, note that docker must be running
# Instructions given for Powershell in Windows10

Preparations in Windows10, Powershell
run "Set-NetConnectionProfile -interfacealias "vEthernet (DockerNAT)" -NetworkCategory Private"
Allow for external mounting of C:/ in Docker (as administrator)
	Docker (rightclick in system tray)->Settings->Shared Drives->tick of C->Apply

To create image (Windows10 and Linux):
docker build -t emmo .

To run image:
docker run --rm -it -v ${PWD}:/emmo emmo (Windows10, Powershell)
docker run --rm -it -v $(pwd):/emmo emmo (linux)
