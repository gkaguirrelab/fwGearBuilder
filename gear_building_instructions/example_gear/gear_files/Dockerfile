# DockerFile is a template for creating a Docker image. This is where we describe everything we want to copy and install
# in the docker container e.g. python and packages, matlab runtime, and any other 3rd party software you need.

# We need to base our Docker image on an existing base image. Here I based it on latest ubuntu. All docker the community made can be 
# found on https://hub.docker.com. If you want to use some neuroimaging tools for instance, neurodebian image has some already installed.
# You can base your docker image on that.   
FROM ubuntu:latest

# This is not important for Flyhweel purposes. Just a maintainer name if you want to store your docker image online on dockerhub.
MAINTAINER YourName(yourEmail@gmail.com)

# Here we create a flywheel environment. Flywheel saves input and output into flywheel/v0 in the docker container. This is where the webpage looks for the input 
# and saves the output. You can keep these the same for all gears you make.
ENV FLYWHEEL /flywheel/v0/
RUN mkdir -p ${FLYWHEEL}

# Here we tell the DockerFile to copy "manifest.json" and "run" files to the Flyhweel directory in the container when we make it. We haven't created these files yet in the instructions, but we will
COPY manifest.json run ${FLYWHEEL}

# Giving execute privilage to the run script
RUN chmod +x /flywheel/v0/run

# Here we tell the DockerFile to copy the folder that contains our MATLAB compiled code from the current directory of your computer to /opt directory in the Docker container. 
# We have already created this folder in the instructions. If you saved your compiled code to a folder which is not called compiled_function, change the name below.
COPY compiled_function/ /opt/compiled_function 

# Giving execute privilages to every file in compiled MATLAB directory. Change the name if you use a folder with different name.
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
# So go to https://www.mathworks.com/products/compiler/matlab-runtime.html, and copy the link to the Linux download file of your version and replace the one below.
RUN wget https://ssd.mathworks.com/supportfiles/downloads/R2020a/Release/5/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020a_Update_5_glnxa64.zip
RUN mkdir matlabins
RUN unzip MATLAB_Runtime_R2020a_Update_5_glnxa64.zip -d /matlabins/
RUN /matlabins/install -mode silent -agreeToLicense yes

# Here we set entrypoint to the DockerFile, so that when it is run, it will right away execute the "run" script that we will create.
# Don't forget this. Otherwise, the gear doesn't start!!
ENTRYPOINT /flywheel/v0/run
