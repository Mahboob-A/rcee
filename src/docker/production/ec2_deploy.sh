#!/bin/bash 

set -o errexit 
set -o nounset 

# TODO  Saimun EC2 server has been used to deploy the project. 
#  Make sure the Environment variables are properly exported in the HOST Machine. 


# Export the variables in the host machine. 
if [[ -z "${ALGOCODE_AUTHRCEE_EC2_IP_ADDR}" ]]; then
    echo "EC2 Server IP Address for Auth and Code Manager Service is not defined."
    echo "Please export the EC2 server IP address in host machine and try again."
    exit 1
fi 

# upload from main branch (if .envs did not upload, exclude .envs from .gitignore for temporary before running the script)
# git archive --format tar --output ./production_project.tar main . 

# upload from currnet branch/directory (go to the branch form where the deployment should be uploaded.)
# tar --exclude='.git' --exclude='docker/production/ec2_deploy.sh' -cvf ./production_project.tar .
tar --exclude='.git' -cvf ./production_project.tar .


echo "Uploading the Project to the server ... " 

rsync -e "ssh -i ${ALGOCODE_AUTHRCEE_EC2_PEM}" ./production_project.tar ubuntu@"${ALGOCODE_AUTHRCEE_EC2_IP_ADDR}":/tmp/production_project.tar

echo "Upload complete ... "

echo "Building the docker compose  ... "

ssh -i "${ALGOCODE_AUTHRCEE_EC2_PEM}" -o StrictHostKeyChecking=no ubuntu@"${ALGOCODE_AUTHRCEE_EC2_IP_ADDR}" << 'ENDSSH'

    PROJECT_PATH=/home/ubuntu/algocode-rcee-service/rcee
    LOG_PATH=/home/ubuntu/algocode-rcee-service/logs
    WAIT_TIME=10

    echo "Creating directory for project and logs... "
    mkdir -p "$PROJECT_PATH"
    mkdir -p "$LOG_PATH"

    echo "Creating the log files ... "
    touch "$LOG_PATH"/general.log 
    touch "$LOG_PATH"/error.log 

    echo "Deleting the old project files ... "
    rm -rf "$PROJECT_PATH"/* 

    echo "Extracting the production_project.tar file in specified project directory ... "
    tar -xf /tmp/production_project.tar -C "$PROJECT_PATH"

    echo " Taking down running project docker containers ... "
    docker_compose_down_output=$(docker compose -p algocode_rcee_service -f "$PROJECT_PATH"/production.yml down)
    docker_compose_down_exit_code=$?
    
    if [[ $docker_compose_down_exit_code -ne 0 ]]; then 
        echo "Error: Taking down the running docker compose containers failed. (Exit code: $docker_compose_down_exit_code)"
        echo -e "\nError: Taking DOWN the running docker compose containers failed\nError Message: $docker_compose_down_output\nExit code: $docker_compose_down_exit_code\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/error.log
        exit $docker_compose_down_exit_code
    fi 

    echo "Waiting for \"$WAIT_TIME\" seconds before running the docker compose file ... "
    sleep "$WAIT_TIME"

    echo "Starting the docker compose file ... "
    docker_compose_up_output=$(sudo docker compose -p algocode_rcee_service -f $PROJECT_PATH/production.yml up --build -d --remove-orphans)
    docker_compose_up_exit_code=$?

    if [[ $docker_compose_up_exit_code -ne 0 ]]; then 
        echo "Error: Starting the docker compose containers failed. (Exit code: $docker_compose_up_exit_code)"
        echo -e "\nError: Starting the docker compose containers failed\nError Message: $docker_compose_up_output\nExit code: $docker_compose_up_exit_code\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/error.log
        exit $docker_compose_up_exit_code
    fi 

    echo -e "\nSuccess: New deployment is successful.\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/general.log

ENDSSH

echo "Build and Deploy of Algocode RCEE Service in the Server is Successful ... "
