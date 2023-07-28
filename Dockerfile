FROM ubuntu:18.04

# Install dependencies
RUN apt -y update

# install python3, java, ant
RUN apt -y install python3 openjdk-8-jdk ant

COPY . /benchmarksql

# set workdir in /benchmarksql
WORKDIR /benchmarksql

# build benchmarksql
RUN ant
