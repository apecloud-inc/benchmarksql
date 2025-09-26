FROM ubuntu:18.04

# Install dependencies
RUN apt-get update

RUN apt-get install -y python3 openjdk-8-jdk ant

COPY . /benchmarksql

# set workdir in /benchmarksql
WORKDIR /benchmarksql

# build benchmarksql
RUN ant

RUN apt-get clean && rm -rf /var/lib/apt/lists/*
