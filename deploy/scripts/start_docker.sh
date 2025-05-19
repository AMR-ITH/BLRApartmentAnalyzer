#!/bin/bash
# Log everything to start_docker.log
exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging in to ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 038950678452.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling the Docker image..."
docker pull 038950678452.dkr.ecr.ap-south-1.amazonaws.com/apartment:latest

CONTAINER_NAME="ml-project-bangalore-flats"

echo "Checking for existing container..."

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing container..."
    docker stop $CONTAINER_NAME
fi

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Removing existing container..."
    docker rm $CONTAINER_NAME
fi

echo "Starting new container..."
docker run -d -p 80:8000 --name $CONTAINER_NAME -e DAGSHUB_USER_TOKEN=417106249b48809359d7f319b24f814e569b0769 038950678452.dkr.ecr.ap-south-1.amazonaws.com/apartment

echo "Container started successfully!"
