# DockerFile is a template for creating a Docker image. This is where we describe everything we want to copy and install
# in the docker container e.g. python and packages, matlab runtime, and any other 3rd party software you need.

# We need to base our Docker image on an existing base image. Here I used an image called neurodebian which is a linux xenial based
# image which have some neuroimaging tools already installed. If your gear will use matlab tools, I suggest going with ubuntu:latest.
# hub.docker.com is a good place to look for images which have specific softwares already installed  
FROM neurodebian:xenial

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

# Here we tell the DockerFile to copy the folder that contains our MATLAB code from the current directory of your computer to /opt directory in the Docker image. 
# Do not forget where you you copy stuff in the docker image because we will reference some of them in the run file the gear needs. 
COPY regressMotion/ /opt/regressMotion 

# Giving execute privilage to every file in compiled MATLAB directory
RUN chmod +x /opt/regressMotion/*  

# Here we tell DockerFile to update the packages and install some essential libraries as well as zip and unzip, and wget functions
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    zip \
    unzip \
    wget

# Here I am installing a specific python3 version I need which cannot be obtained with apt-get in the old version of docker image I am using. 
# You can skip this. The ubuntu base already has python.
RUN apt-get update \
    && apt-get install -y build-essential git libexpat1-dev libssl-dev zlib1g-dev software-properties-common\
    libncurses5-dev libbz2-dev liblzma-dev \
    libsqlite3-dev libffi-dev tcl-dev linux-headers-generic libgdbm-dev \
    libreadline-dev tk tk-dev openssl openssl-dev* wget curl
RUN wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz
RUN tar -xvf Python-3.7.8.tgz
RUN cd Python-3.7.8; ./configure --enable-shared; make; make test; make install
RUN cd /usr/local/lib/; cp libpython3.so /usr/lib64/; cp libpython3.so /usr/lib; cp libpython3.7m.so.1.0 /usr/lib64/; cp libpython3.7m.so.1.0 /usr/lib/; cd /usr/lib64; ln -s libpython3.7m.so.1.0 libpython3.7m.so; cd /usr/lib; ln -s libpython3.7m.so.1.0 libpython3.7m.so   

# Download and install MATLAB Runtime with wget. The version here could be old. It has to match the matlab version you compiled your code with.
# So go to https://www.mathworks.com/products/compiler/matlab-runtime.html, and copy the link to the Linux zip file of the matching version and replace the one below.

RUN wget https://ssd.mathworks.com/supportfiles/downloads/R2020a/Release/5/deployment_files/installer/complete/glnxa64/MATLAB_Runtime_R2020a_Update_5_glnxa64.zip
RUN mkdir matlabins
RUN unzip MATLAB_Runtime_R2020a_Update_5_glnxa64.zip -d /matlabins/
RUN /matlabins/install -mode silent -agreeToLicense yes

# Here we set entrypoint to the DockerFile, so that when it is started, it will start the "run" script we copied automatically.
# Don't forget this. Otherwise, the gear doesn't start!!
ENTRYPOINT /flywheel/v0/run