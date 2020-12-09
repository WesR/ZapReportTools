FROM debian:stable-slim

RUN apt update 
RUN apt --yes --force-yes install \
    texlive-base \
    texlive-extra-utils \
    python3
RUN apt clean -y