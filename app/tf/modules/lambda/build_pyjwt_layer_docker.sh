#!/bin/bash
set -e

OUTPUT_ZIP="$1"
TEMP_DIR=$(mktemp -d)

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker not running, skipping layer build"
    exit 0
fi

# Use Docker to build layer with Linux binaries
docker run --rm \
    -v "$TEMP_DIR":/var/task \
    public.ecr.aws/lambda/python:3.11 \
    pip install PyJWT requests google-auth google-auth-oauthlib -t /var/task/python/ --upgrade

cd $TEMP_DIR
zip -r "$OUTPUT_ZIP" python -q
rm -rf $TEMP_DIR

echo "Layer built with Docker"
