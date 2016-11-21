gcp-tools
=========

Python tools for working with Google Cloud Platform

# Installation #

Requires Docker. If not already installed, install here:

https://docs.docker.com/engine/installation/

Verify Docker is running and that you can connect:

`docker ps`

Requires Google Cloud SDK. If not already installed, install here:

https://cloud.google.com/sdk/

Make sure your gcloud client is up-to-date (precede with "sudo" if you are not logged in as root.):

`gcloud components update`

Authenticate using application-default credentials:

`gcloud auth application-default login`

If you are running gcloud on a different host than where your browser is running, do this instead:

`gcloud auth application-default login --no-launch-browser`

and follow the directions to authorize access to your account.

Clone this repo:

`git clone http://github.com/lukwam/gcp-tools`

Build a the docker image from the Dockerfile.

`cd gcp-tools`

`./build.sh`

When the container is done building, you can try running it with:

`./run.sh create_projects.py my-project-name-01`

replacing "my-project-name-01" with the name of the project you'd like to create.

# Scripts #

## create_projects.py ##

Creates GCP projects.

## report.py ##

Displays information about your GCP resources:
* Number of organizations
* Number of billing accounts
* Number of projects
