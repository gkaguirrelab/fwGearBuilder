FROM ubuntu:bionic-20200112 as builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
                    software-properties-common \
                    build-essential \
                    apt-transport-https \
                    ca-certificates \
                    gnupg \
                    software-properties-common \
                    wget \
                    ninja-build \
                    git \
                    python \
                    zlib1g-dev

RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null \
    | apt-key add - \
  && apt-add-repository -y 'deb https://apt.kitware.com/ubuntu/ bionic main' \
  && apt-get update \
  && apt-get -y install cmake=3.18.3-0kitware1 cmake-data=3.18.3-0kitware1 

ADD . /tmp/ants/source
RUN mkdir -p /tmp/ants/build \
    && cd /tmp/ants/build \
    && mkdir -p /opt/ants \
    && git config --global url."https://".insteadOf git:// \
    && cmake \
      -GNinja \
      -DBUILD_TESTING=OFF \
      -DBUILD_SHARED_LIBS=ON \
      -DCMAKE_INSTALL_PREFIX=/opt/ants \
      /tmp/ants/source \
    && cmake --build . --parallel \
    && cd ANTS-build \
    && cmake --install .

FROM ubuntu:bionic-20200112
COPY --from=builder /opt/ants /opt/ants

ENV ANTSPATH="/opt/ants/bin" \
    PATH="/opt/ants/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/ants/lib:$LD_LIBRARY_PATH"
RUN apt-get update \
    && apt install -y --no-install-recommends zlib1g-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get upgrade -y
RUN apt-get update -y
RUN apt-get install python3 -y

# copy new ants template script to the bin 
COPY antsMultivariateTemplateConstruction2.sh /opt/ants/bin/antsMultivariateTemplateConstruction2.sh

#Initialize flywheel v0 and move the required files into the container 
ENV FLYWHEEL /flywheel/v0/
RUN mkdir -p ${FLYWHEEL}
COPY manifest.json run ${FLYWHEEL}
RUN chmod +x /flywheel/v0/run

# Set the entrypoint  
ENTRYPOINT /flywheel/v0/run
