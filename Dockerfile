FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/wf-base:fbe8-main

RUN apt-get update -y &&\
    apt-get install -y wget libncurses5 &&\
    apt-get install gzip


ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 


RUN conda config --add channels bioconda
RUN conda config --add channels conda-forge


RUN conda install -c bioconda fastp transrate jellyfish
#RUN conda install -c bioconda fastp transrate trinotate transdecoder blast hmmer jellyfish
RUN conda install -c conda-forge sqlite
#RUN conda install trinity 

RUN curl -L -O https://github.com/trinityrnaseq/trinityrnaseq/releases/download/Trinity-v2.14.0/trinityrnaseq-v2.14.0.FULL.tar.gz &&\
	#gunzip trinityrnaseq-v2.14.0.FULL.tar.gz &&\
	tar -zxvf trinityrnaseq-v2.14.0.FULL.tar.gz &&\
	#make install
	mv trinityrnaseq-v2.14.0 Trinity


#
# STOP HERE:
# The following lines are needed to ensure your build environment works
# correctly with latch.

COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN  sed -i 's/latch/wf/g' flytekit.config
RUN python3 -m pip install --upgrade latch
WORKDIR /root
