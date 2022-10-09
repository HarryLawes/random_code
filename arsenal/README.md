# Arsenal Data Science Sandbox

This repository contains a simplified sample of our data in CSV format covering 3 recent Premier League matches and a Docker image built on https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook. 

## Prerequisites
- [Git LFS](https://git-lfs.github.com/) to reduce the Git overhead for large files, e.g. tracking data

If you wish to use the Docker container (optional):
    - [Docker](https://docs.docker.com/) with at least 4GB of memory allocated
    - `make` (_Windows users, we recommend using Docker with [Windows Subsystem for Linux](https://docs.docker.com/desktop/windows/wsl/)_)

## Getting Started Locally
1. `pip install -r requirements.txt`
2. `jupyter lab`
3. Browse to one of the local URLs printed to the terminal using your preferred web browser
4. Start exploring the data using JupyterLab

## Getting Started using Docker
1. Clone this repository to your local machine
2. Open a shell and change directories to the repo root
3. `make run`
4. Browse to one of the URLs printed to the terminal using your preferred web browser
5. Start exploring the data using JupyterLab
