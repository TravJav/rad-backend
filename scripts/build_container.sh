#!/bin/bash


# Build backend container
DOCKER_BUILDKIT=1 docker build -t api-radpair -f ./Dockerfile .

# Check if the Docker build was successful, and the image is available
if docker image inspect api-radpair &> /dev/null; then
    echo "Docker build successful. Image api-radpair:latest is available."
else
    echo "Docker build failed or image not found. Check the build logs for details."
    exit 1
fi
