# DockerFile is a template for creating a Docker image. This is where we describe everything we want to copy and install
# in the docker container e.g. python and packages, matlab runtime, and any other 3rd party software you need.

# We need to base our Docker image on an existing base image. Here I based it on latest ubuntu. All docker the community made can be 
# found on https://hub.docker.com. If you want to use some neuroimaging tools for instance, neurodebian image has some already installed.
# You can base your docker image on that.   
FROM ubuntu:latest

# This is not very important for Flyhweel purposes so you might as well delete it.
MAINTAINER YourName(yourEmail@gmail.com)

# Here we create a flywheel environment. Flywheel saves input and output into flywheel/v0. This is where the webpage looks for the input 
# and the output. You can keep these the same for all gears you make.
ENV FLYWHEEL /flywheel/v0/
RUN mkdir -p ${FLYWHEEL}

# Here we tell the DockerFile to copy "manifest.json" and "run" files to the Flyhweel directory when we make the Docker image. 
COPY manifest.json run ${FLYWHEEL}

# Giving execute privilage to the run script
RUN chmod +x /flywheel/v0/run

# Here we tell the DockerFile to copy the folder that contains our MATLAB compiled code from the current directory of your computer to /opt directory in the Docker image. 
# Do not forget where you copy stuff in the docker image because we will reference some of them in the run file the gear needs. 
COPY compiled_function/ /opt/compiled_function 

# Giving execute privilage to every file in compiled MATLAB directory
RUN chmod +x /opt/compiled_function/*  

# Here we tell DockerFile to update the packages and install some essential libraries as well as zip and unzip, python2, and wget.
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    zip \
    unzip \
    wget \
    python

# Download and install MATLAB Runtime with wget. The version here could be old. It has to match the matlab version you compiled your code with.
# So go to https://www.mathworks.com/products/compiler/matlab-runtime.html, and copy the link to the Linux zip file of the matching version and replace the one below.
RUN wget https://ssd.mathworks.com/supportfiles/downloads/R2020a/Release/5/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020a_Update_5_glnxa64.zip
RUN mkdir matlabins
RUN unzip MATLAB_Runtime_R2020a_Update_5_glnxa64.zip -d /matlabins/
RUN /matlabins/install -mode silent -agreeToLicense yes

# Here we set entrypoint to the DockerFile, so that when it is started, it will start the "run" script we copied automatically.
# Don't forget this. Otherwise, the gear doesn't start!!
ENTRYPOINT /flywheel/v0/run
