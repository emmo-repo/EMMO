Creating a docker image
=======================

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
