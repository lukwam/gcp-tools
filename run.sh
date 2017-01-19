#!/bin/sh

DOCKER_SOCKET='/var/run/docker.sock'
SUDO=
TTY=

if [ "${TERM}" != "dumb" ]; then
        TTY='-it'
fi

if [ "$(uname -s)" != "Darwin" ]; then
    if [ ! -w "${DOCKER_SOCKET}" ]; then
        SUDO='sudo'
    fi
fi

$SUDO docker run $TTY --rm \
        -e GOOGLE_APPLICATION_CREDENTIALS=/root/.config/gcloud/application_default_credentials.json \
        -e PATH=/usr/src:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
        -v "$(pwd)":/usr/src \
        -v ~/.config:/root/.config \
        -v /etc/localtime:/etc/localtime:ro \
        -w /usr/src \
        lukwam/gcp-tools "$@"
